#!/usr/bin/env python3
"""Reconcile observed PCB models; query and diff bounded views without losing raw data."""
import argparse
import copy
from collections import Counter
from pathlib import Path
import sys

import audit_design
import workflow_io as io


def build(snapshot, board, binding):
    parts=audit_design.load_snapshot(snapshot)
    if snapshot['kind']!='pcb': raise ValueError('Use an observed PCB snapshot, not schematic intent or BOM')
    if type(binding.get('schema')) is not int or binding['schema']!=1 or binding.get('role')!='observed': raise ValueError('Expected observed binding schema 1')
    identity={k:io.text(binding.get(k),k) for k in ('project_id','document_id','baseline_id')}
    if snapshot['baseline_id']!=identity['baseline_id']: raise ValueError('Baseline mismatch')
    if board.get('units')!='mm' or type(board.get('schema')) is not int or board['schema']!=1: raise ValueError('Expected toolkit schema 1 in mm')
    coverage=board.get('import_coverage',{})
    count=len(board.get('components',[]))
    if (any(type(coverage.get(k)) is not int for k in ('pcb_documents','source_components','imported_components','missing_footprints'))
        or coverage.get('pcb_documents')!=1 or coverage.get('source_components')!=count
        or coverage.get('imported_components')!=count or coverage.get('missing_footprints')!=0):
        raise ValueError('Missing or inconsistent native import coverage')
    if binding.get('snapshot_digest')!=io.digest(snapshot) or binding.get('board_digest')!=io.digest(board):
        raise ValueError('Binding hashes do not match inputs')
    io.text(binding.get('readback_evidence'),'readback_evidence')
    # Preserve NC explicitly. The native importer may omit unassigned PAD_NET records.
    nc=binding.get('unconnected_pins',[])
    if not isinstance(nc,list) or any(not isinstance(v,list) or len(v)!=2 or
        any(not isinstance(s,str) or not s for s in v) for v in nc): raise ValueError('Invalid unconnected_pins')
    ncset={tuple(v) for v in nc}
    if len(ncset)!=len(nc): raise ValueError('Duplicate unconnected pin declaration')
    used_nc=set(); components={}; ids=set(); footprints=board['footprints']; netmap=board['pad_nets']
    known_netkeys=set();mapping=binding.get('footprint_map',{})
    if set(mapping)!=set(parts): raise ValueError('Provide an explicit per-reference footprint mapping')
    for component in board['components']:
        ref=io.text(component.get('des'),'designator')
        if ref in components or ref not in parts: raise ValueError('Duplicate or unexpected component: '+ref)
        native=io.text(component.get('native_id'),'native component ID; re-export with current importer')
        if native in ids: raise ValueError('Duplicate native component ID')
        ids.add(native); part=parts[ref]; fpid=component['footprint']
        if mapping[ref]!={'snapshot':part['footprint'],'toolkit':fpid}: raise ValueError('Footprint mapping mismatch: '+ref)
        if fpid not in footprints: raise ValueError('Missing footprint: '+ref)
        for key in ('x','y','angle'): io.finite(component.get(key),key)
        if component.get('side') not in ('top','bottom'): raise ValueError('Explicit component side required')
        pins={}; pad_ids=set()
        repeated=Counter(pad.get('num') for pad in footprints[fpid].get('pads',[]))
        for pad in footprints[fpid].get('pads',[]):
            pin=io.text(pad.get('num'),'physical pad number')
            elem=io.text(pad.get('elem'),'physical pad element ID')
            if elem in pad_ids: raise ValueError('Duplicate physical pad element')
            pad_ids.add(elem)
            bynum=ref+'.'+pin; byelem=ref+'#'+elem
            known_netkeys.update((bynum,byelem))
            if repeated[pin]>1 and byelem not in netmap:
                raise ValueError('Repeated-number pad requires its own element net: '+byelem)
            observed=[netmap[k] for k in (bynum,byelem) if k in netmap]
            if any(v is not None and (not isinstance(v,str) or not v.strip()) for v in observed):
                raise ValueError('Invalid net value; unassigned pins require explicit NC declaration')
            if len(set(observed))>1: raise ValueError('Number/element net mismatch: '+ref+'.'+pin)
            if observed: net=observed[0]
            elif (ref,pin) in ncset: net=None
            else: raise ValueError('Missing pad net is unknown, not NC: '+ref+'.'+pin)
            if (ref,pin) in ncset:
                used_nc.add((ref,pin))
                if net is not None: raise ValueError('Declared NC is connected')
            if pin in pins and pins[pin]!=net: raise ValueError('Repeated pad number has conflicting nets')
            pins[pin]=net
        if not pins or pins!=part['pins']: raise ValueError('Actual pin-net mismatch: '+ref)
        components[ref]={'native_id':native,'record':copy.deepcopy(part),
                         'placement':copy.deepcopy(component),'physical_pad_count':len(pad_ids)}
    if set(components)!=set(parts) or used_nc!=ncset: raise ValueError('Incomplete component or NC coverage')
    if set(netmap)-known_netkeys:raise ValueError('Pad-net entries reference missing physical pads')
    # The auxiliary schematic netlist is retained, not substituted for actual PAD_NET.
    result={'schema':1,'kind':'reconciled-pcb','role':'observed',**identity,
            'binding':copy.deepcopy(binding),'normalized':copy.deepcopy(snapshot),
            'board':copy.deepcopy(board),'components':components,
            'coverage':{'component_pin_reconciliation':'MATCH','geometry':'UPSTREAM_SUPPORTED_RECORDS_ONLY',
                        'native_restore':'NOT_SUPPORTED','electrical_acceptance':'NOT_ASSESSED'}}
    result['digest']=io.digest(result)
    return result


def validate(data):
    if not isinstance(data,dict) or data.get('kind')!='reconciled-pcb': raise ValueError('Expected reconciled PCB')
    clean={k:v for k,v in data.items() if k!='digest'}
    if data.get('digest')!=io.digest(clean): raise ValueError('Reconciled data changed without rebuilding')
    expected=build(data['normalized'],data['board'],data['binding'])
    if expected!=data: raise ValueError('Reconciliation provenance or index mismatch')
    return data


def summary(data):
    return {k:data[k] for k in ('project_id','document_id','baseline_id','digest','coverage')} | {
        'counts':{'components':len(data['components']),
                  **{k:len(data['board'].get(k,[])) for k in ('tracks','vias','pours','footprints')}}}


def query(data, section='components', ref=None, net=None, offset=0, limit=25):
    if type(offset) is not int or offset<0 or type(limit) is not int or not 1<=limit<=100:
        raise ValueError('offset >= 0; limit must be 1..100')
    if section not in ('components','tracks','vias','pours','footprints','rules','layers','outline'):
        raise ValueError('Unknown query section')
    if ref is not None and section!='components': raise ValueError('Reference filter applies to components')
    if net is not None and section not in ('components','tracks','vias','pours'): raise ValueError('No net filter for this section')
    source=data['components'] if section=='components' else data['board'].get(section,[])
    entries=[{'id':k,'data':v} for k,v in sorted(source.items())] if isinstance(source,dict) else [{'id':str(i),'data':v} for i,v in enumerate(source)]
    if ref is not None: entries=[v for v in entries if v['id']==ref]
    if net is not None:
        entries=[v for v in entries if (net in v['data']['record']['pins'].values() if section=='components' else v['data'].get('net')==net)]
    # Only explicit queries return detailed geometry/attributes. Never delete them from disk.
    return {'digest':data['digest'],'baseline_id':data['baseline_id'],'section':section,
            'total':len(entries),'offset':offset,'items':entries[offset:offset+limit],
            'next_offset':offset+limit if offset+limit<len(entries) else None}


def delta(before, after, offset=0, limit=25):
    if any(before[k]!=after[k] for k in ('project_id','document_id')): raise ValueError('Cross-project/document diff is invalid')
    if type(offset) is not int or offset<0 or type(limit) is not int or not 1<=limit<=100: raise ValueError('Invalid pagination')
    changes=[]
    for ref in sorted(set(before['components'])|set(after['components'])):
        a=before['components'].get(ref);b=after['components'].get(ref)
        if a!=b: changes.append({'section':'components','id':ref,'change':'added' if a is None else 'removed' if b is None else 'modified'})
    for key in sorted(set(before['board'])|set(after['board'])):
        if key=='components': continue
        if before['board'].get(key)!=after['board'].get(key):
            changes.append({'section':key,'change':'modified','before_digest':io.digest(before['board'].get(key)),
                            'after_digest':io.digest(after['board'].get(key))})
    return {'before':before['digest'],'after':after['digest'],
            'baselines':[before['baseline_id'],after['baseline_id']],
            'binding_changed':before['binding']!=after['binding'],'total':len(changes),
            'changes':changes[offset:offset+limit], 'next_offset':offset+limit if offset+limit<len(changes) else None,
            'scope':'component-records-and-preserved-board-sections; not native geometry acceptance'}


def bounded_output(result, max_bytes=16384, items_key=None, offset=0):
    """Limit complete UTF-8 JSON + newline; oversized records become explicit digest handles."""
    if type(max_bytes) is not int or not 1024 <= max_bytes <= 1048576:
        raise ValueError('max-bytes must be 1024..1048576')
    def size(v): return len(io.encoded(v)) + 1
    if items_key is None:
        if size(result) > max_bytes: raise ValueError('Metadata exceeds output budget; use an offline export')
        return result
    page=copy.deepcopy({k:v for k,v in result.items() if k!=items_key})
    page[items_key]=[]
    page['budget']={'max_bytes':max_bytes,'oversized_records':0,'size_unit':'UTF-8 bytes including newline'}
    page['next_offset']=offset if offset < page['total'] else None
    if size(page)>max_bytes: raise ValueError('Page metadata exceeds output budget; use an offline export')
    consumed=0
    for record in result[items_key]:
        candidate=copy.deepcopy(page);candidate[items_key].append(record)
        candidate['next_offset']=offset+consumed+1 if offset+consumed+1<page['total'] else None
        if size(candidate)>max_bytes:
            if consumed: break
            handle={'oversized':True,'record_offset':offset,'record_digest':io.digest(record),
                    'record_bytes':len(io.encoded(record)),
                    'retrieve':'export full board/normalized data to a local file; inspect this record offline'}
            candidate[items_key]=[handle];candidate['budget']['oversized_records']=1
            if size(candidate)>max_bytes: raise ValueError('Output budget cannot hold record handle')
        page=candidate;consumed+=1
    return page


def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='action',required=True)
    b=sub.add_parser('build');b.add_argument('--snapshot',type=Path,required=True);b.add_argument('--board',type=Path,required=True)
    b.add_argument('--binding',type=Path,required=True);b.add_argument('--output',type=Path,required=True)
    h=sub.add_parser('hash');h.add_argument('input',type=Path)
    for command in ('summary','query','diff','export'):
        q=sub.add_parser(command);q.add_argument('input',type=Path)
        if command in ('summary','query','diff'):q.add_argument('--max-bytes',type=int,default=16384)
        if command=='diff':q.add_argument('after',type=Path)
        if command in ('query','diff'):
            q.add_argument('--offset',type=int,default=0);q.add_argument('--limit',type=int,default=25)
        if command=='query':
            q.add_argument('--section',default='components');q.add_argument('--ref');q.add_argument('--net')
        if command=='export':q.add_argument('--format',choices=('normalized','board'),required=True);q.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    try:
        if args.action=='hash':result={'digest':io.digest(io.read(args.input))}
        elif args.action=='build':
            result=build(io.read(args.snapshot),io.read(args.board),io.read(args.binding));io.save(args.output,result,exclusive=True)
            result=summary(result)|{'file':str(args.output.resolve())}
        else:
            data=validate(io.read(args.input))
            if args.action=='summary':result=summary(data)
            elif args.action=='query':result=query(data,args.section,args.ref,args.net,args.offset,args.limit)
            elif args.action=='diff':result=delta(data,validate(io.read(args.after)),args.offset,args.limit)
            else:
                io.save(args.output,data[args.format],exclusive=True);result={'file':str(args.output.resolve()),'format':args.format}
        if args.action in ('summary','query','diff'):
            result=bounded_output(result,args.max_bytes,{'query':'items','diff':'changes'}.get(args.action),getattr(args,'offset',0))
        sys.stdout.buffer.write(io.encoded(result)+b'\n')
    except (ValueError,KeyError,TypeError,OSError) as error: p.exit(2,'ERROR: '+str(error)+'\n')


if __name__=='__main__':main()
