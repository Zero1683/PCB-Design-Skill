#!/usr/bin/env python3
"""Compare normalized records, review revisions, and screen body envelopes."""
import argparse
import json
import math
from report_provenance import read_source
from pathlib import Path


def load_snapshot(data):
    if (not isinstance(data, dict) or type(data.get('schema')) is not int
            or data['schema'] != 1 or data.get('kind') not in {'schematic', 'pcb', 'bom'}):
        raise ValueError('Expected normalized schema=1, kind=schematic|pcb|bom')
    for key in ('baseline_id', 'source', 'coverage'):
        if not isinstance(data.get(key), str) or not data[key].strip(): raise ValueError(f'Missing {key}')
    if data['coverage'] != 'complete': raise ValueError('Partial exports cannot establish whole-design consistency')
    parts = data.get('components')
    if not isinstance(parts, list) or not parts: raise ValueError('Empty or absent component export')
    found = {}
    for part in parts:
        if not isinstance(part, dict): raise ValueError('Component entries must be objects')
        ref = part.get('ref')
        if not isinstance(ref, str) or not ref.strip() or ref in found: raise ValueError('Missing/duplicate reference designator')
        for key in ('part', 'value', 'footprint'):
            if not isinstance(part.get(key), str): raise ValueError(f'{ref}: {key} must be explicit text')
        for key in ('fitted', 'in_bom'):
            if type(part.get(key)) is not bool: raise ValueError(f'{ref}: {key} must be a boolean')
        if data['kind'] != 'bom':
            pins = part.get('pins')
            if not isinstance(pins, dict) or not pins: raise ValueError(f'{ref}: explicit pin mapping required')
            if any(not isinstance(k, str) or not k.strip() or
                   (v is not None and (not isinstance(v, str) or not v.strip())) for k, v in pins.items()):
                raise ValueError(f'{ref}: use explicit null for documented no-connect pins')
        found[ref] = part
    return found


def differences(left, right, a, b, filter_bom=True):
    is_bom = 'bom' in (left['kind'], right['kind'])
    if is_bom and filter_bom:
        a = {k:v for k,v in a.items() if v['in_bom']}
        b = {k:v for k,v in b.items() if v['in_bom']}
    changes = []
    for ref in sorted(set(a) | set(b)):
        if ref not in a or ref not in b:
            changes.append({'ref': ref, 'only_in': 'right' if ref not in a else 'left'}); continue
        for key in ('part', 'value', 'footprint', 'fitted', 'in_bom') + (() if is_bom else ('pins',)):
            if a[ref][key] != b[ref][key]:
                changes.append({'ref':ref, 'field':key, 'left':a[ref][key], 'right':b[ref][key]})
    return changes


def compare(left, right):
    a, b = load_snapshot(left), load_snapshot(right)
    if left['baseline_id'] != right['baseline_id']:
        raise ValueError('Cross-document comparison requires the same baseline')
    changes = differences(left, right, a, b)
    return {'scope':'normalized-record-comparison', 'baseline_id':left['baseline_id'],
            'sources':[left['source'],right['source']], 'differences':changes,
            'records_match':not changes, 'physical_connectivity':'NOT_ASSESSED'}


def revision_diff(before, after):
    a, b = load_snapshot(before), load_snapshot(after)
    if before['kind'] != after['kind']:
        raise ValueError('Revision diff requires the same document kind')
    if before['baseline_id'] == after['baseline_id']:
        raise ValueError('Revision diff requires distinct baseline IDs; use compare for one baseline')
    changes = differences(before, after, a, b, filter_bom=False)
    return {'scope':'normalized-component-and-pin-revision-diff',
            'baselines':[before['baseline_id'],after['baseline_id']],
            'sources':[before['source'],after['source']], 'differences':changes,
            'records_match':not changes,
            'geometry_routing_and_rule_changes':'NOT_ASSESSED',
            'electrical_correctness':'NOT_ASSESSED'}


def geometry(data, clearance):
    parts = load_snapshot(data)
    if data['kind'] != 'pcb' or not math.isfinite(clearance) or clearance < 0:
        raise ValueError('Geometry needs a PCB snapshot and nonnegative clearance in mm')
    boxes, missing, pairs = [], [], []
    for ref, part in parts.items():
        if not part['fitted']: continue
        box = part.get('body_aabb_mm')
        if box is None or not part.get('geometry_source'):
            missing.append(ref); continue
        if part.get('side') not in {'top','bottom'} or len(box) != 4 or any(type(v) not in (int,float) or not math.isfinite(v) for v in box) or box[2] <= box[0] or box[3] <= box[1]:
            raise ValueError(f'{ref}: invalid board-coordinate body AABB or side')
        boxes.append((ref,part['side'],box))
    for i,(ref,side,a) in enumerate(boxes):
        for other,other_side,b in boxes[i+1:]:
            if side != other_side: continue
            dx=max(b[0]-a[2],a[0]-b[2],0);dy=max(b[1]-a[3],a[1]-b[3],0)
            overlap=a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]
            gap=math.hypot(dx,dy)
            if overlap or gap < clearance:
                pairs.append({'refs':[ref,other],'aabb_overlap':overlap,'aabb_gap_mm':gap})
    if not boxes and not missing: raise ValueError('No fitted components to screen')
    return {'scope':'conservative-body-envelope-screen-only','baseline_id':data['baseline_id'],
            'suspect_pairs':pairs,'missing_geometry':missing,'checked_components':len(boxes),
            'geometry_acceptance':'NOT_ASSESSED',
            'limitations':'Board-coordinate transformed AABBs may over-report rotated bodies. No pad/copper, outline, mating-space, height or opposite-side validation.'}


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result: raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=unique_keys)


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='mode',required=True)
    c=sub.add_parser('compare');c.add_argument('left',type=Path);c.add_argument('right',type=Path)
    d=sub.add_parser('diff');d.add_argument('before',type=Path);d.add_argument('after',type=Path)
    g=sub.add_parser('geometry');g.add_argument('pcb',type=Path);g.add_argument('--clearance-mm',type=float,required=True)
    args=p.parse_args()
    try:
        if args.mode in ('compare', 'diff'):
            left, lp = read_source(args.left if args.mode == 'compare' else args.before, 'left')
            right, rp = read_source(args.right if args.mode == 'compare' else args.after, 'right')
            result = compare(left, right) if args.mode == 'compare' else revision_diff(left, right)
            result['source_inputs'] = [lp, rp]
        else:
            data, source = read_source(args.pcb, 'snapshot')
            result=geometry(data,args.clearance_mm)
            result['source_inputs'] = [source]
    except (OSError,ValueError,KeyError,TypeError) as exc:p.exit(2,f'ERROR: {exc}\n')
    print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    return int(not result['records_match']) if args.mode in {'compare','diff'} else int(bool(result['suspect_pairs'] or result['missing_geometry']))


if __name__=='__main__':raise SystemExit(main())
