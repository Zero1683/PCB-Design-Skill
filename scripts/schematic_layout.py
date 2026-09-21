"""Plan rigid G2-A blocks from measured geometry; compare native readbacks. Python 3.10+."""
import argparse
import copy
from pathlib import Path
import workflow_io as io


def rect(value):
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError('Rectangle must be [xmin,ymin,xmax,ymax]')
    for n in value: io.finite(n, 'rectangle')
    if value[2] <= value[0] or value[3] <= value[1]:
        raise ValueError('Rectangle must have positive extent')
    return value


def overlap(a, b, gap=0):
    return a[0] < b[2]+gap and b[0] < a[2]+gap and a[1] < b[3]+gap and b[1] < a[3]+gap


def shift(box, dx, dy):
    return [box[0]+dx, box[1]+dy, box[2]+dx, box[3]+dy]


def source_check(source):
    if type(source.get('schema')) is not int or source['schema'] != 1:
        raise ValueError('Unsupported schema')
    if source.get('phase') != 'G2-A' or source.get('role') != 'observed':
        raise ValueError('Only observed unwired G2-A scopes are supported')
    if source.get('units') != 'raw-0.01inch' or source.get('axis') != 'y-up':
        raise ValueError('Explicit EasyEDA schematic units and y-up axis required')
    if source.get('complete_scope') is not True:
        raise ValueError('Complete scoped inventory required')
    for key in ('project_id', 'document_id', 'baseline_id', 'scope_id'):
        io.text(source.get(key), key)
    for key in ('wire_count', 'bus_count'):
        if type(source.get(key)) is not int or source[key] != 0:
            raise ValueError('Scope must have zero wires and buses')
    objects = source.get('objects')
    if not isinstance(objects, list) or not objects:
        raise ValueError('Measured objects required')
    result = {}
    for obj in objects:
        if set(obj) != {'id','bbox','anchor','facts'}:
            raise ValueError('Object properties outside id/bbox/anchor must be captured inside facts')
        identity = io.text(obj.get('id'), 'stable ID')
        if identity in result: raise ValueError('Duplicate stable ID')
        rect(obj['bbox'])
        if not isinstance(obj.get('anchor'), list) or len(obj['anchor']) != 2:
            raise ValueError('Measured placement anchor required')
        for n in obj['anchor']: io.finite(n, 'anchor')
        facts = obj.get('facts')
        if not isinstance(facts, dict) or not facts:
            raise ValueError('Identity, orientation and pin facts required')
        for key in ('designator', 'device_id', 'footprint_id'): io.text(facts.get(key), key)
        io.finite(facts.get('rotation'), 'rotation')
        if not isinstance(facts.get('pins'), dict) or not facts['pins']:
            raise ValueError('Full pin map including explicit null NC required')
        result[identity] = obj
    return result


def plan(source, spec):
    objects = source_check(source)
    if spec.get('format') not in ('free-layout', 'framed-layout'):
        raise ValueError('Select one of the two schematic formats')
    bounds = rect(spec['usable_rect'])
    gap, pad, title_height = [io.finite(spec[k], k) for k in ('gap', 'padding', 'title_height')]
    if min(gap, pad, title_height) <= 0: raise ValueError('Positive spacing required')
    obstacles = [rect(r) for r in spec.get('obstacles', [])]
    groups = spec.get('blocks')
    if not isinstance(groups, list) or not groups: raise ValueError('Ordered blocks required')
    used, block_ids, frames, moves = set(), set(), [], []
    x, top, row_bottom = bounds[0], bounds[3], bounds[3]
    row_has_items = False
    for group in groups:
        bid = io.text(group.get('id'), 'block ID'); title = io.text(group.get('title'), 'title')
        if bid in block_ids: raise ValueError('Duplicate block ID')
        block_ids.add(bid)
        width = io.finite(group['measured_title_width'], 'measured title width')
        if width <= 0: raise ValueError('Positive measured title width required')
        members = group['members']
        if not isinstance(members, list) or not members: raise ValueError('Block members required')
        local = []
        for mid in members:
            if mid not in objects or mid in used: raise ValueError('Missing or multiply owned object')
            used.add(mid); local.append(objects[mid])
        for i, obj in enumerate(local):
            if any(overlap(obj['bbox'], other['bbox'], pad) for other in local[:i]):
                raise ValueError('Local measured envelopes collide: '+bid+'; fix local block before packing')
        union = [min(o['bbox'][0] for o in local), min(o['bbox'][1] for o in local),
                 max(o['bbox'][2] for o in local), max(o['bbox'][3] for o in local)]
        w = max(union[2]-union[0], width)+2*pad
        h = union[3]-union[1]+3*pad+title_height
        if w > bounds[2]-bounds[0]: raise ValueError('Block wider than usable sheet: '+bid)
        # Bounded shelf packing, preserving functional order and rigid local geometry.
        for attempt in range(2*len(obstacles)+3):
            if x+w > bounds[2]:
                x, top = bounds[0], row_bottom-gap
                row_has_items = False
            box = [x, top-h, x+w, top]
            if box[1] < bounds[1]: raise ValueError('NO_FIT: enlarge/split sheet or change local layout')
            hits = [r for r in obstacles if overlap(box, r, gap)]
            if not hits: break
            lower_top = min(r[1]-gap for r in hits)
            if not row_has_items and 0 < top-lower_top < h:
                top = lower_top
                continue
            x = max(r[2] for r in hits)+gap
        else: raise ValueError('NO_FIT: bounded obstacle search exhausted')
        dx, dy = x+pad-union[0], top-title_height-2*pad-union[3]
        frames.append({'id':bid, 'title':title, 'bbox':box,
                       'title_bbox':[x+pad, top-pad-title_height, x+pad+width, top-pad]})
        for obj in local:
            target = copy.deepcopy(obj)
            target['bbox'] = shift(obj['bbox'], dx, dy)
            target['anchor'] = [obj['anchor'][0]+dx, obj['anchor'][1]+dy]
            moves.append({'id':obj['id'], 'from':obj['anchor'], 'to':target['anchor'], 'expected':target})
        row_bottom = min(row_bottom, box[1]); x += w+gap
        row_has_items = True
    if used != set(objects): raise ValueError('Unassigned objects in scope')
    result = {'schema':1, 'kind':'schematic-placement-plan', 'source':source, 'spec':spec,
              'source_digest':io.digest(source), 'moves':moves, 'frames':frames,
              'status':'PLANNED_NOT_APPLIED', 'scope':'rigid unwired block packing only'}
    result['digest'] = io.digest(result)
    return result


def validate_plan(value):
    rebuilt = plan(value['source'], value['spec'])
    if rebuilt != value: raise ValueError('Plan changed or incompatible planner version')


def verify(value, observed, tolerance=0.01):
    validate_plan(value); source_check(observed)
    io.finite(tolerance, 'tolerance')
    if tolerance < 0 or tolerance > min(value['spec']['padding'], value['spec']['gap'])/4:
        raise ValueError('Tolerance exceeds spacing margin')
    phase = observed.get('capture_stage')
    if phase not in ('after-apply', 'after-reload'): raise ValueError('Explicit capture stage required')
    source = value['source']; failures = []
    for key in ('project_id','document_id','baseline_id','scope_id','units','axis'):
        if observed.get(key) != source.get(key): failures.append(key)
    expected = copy.deepcopy(source)
    expected['objects'] = [move['expected'] for move in value['moves']]
    def check_items(wanted, actual, label, fields):
        if not isinstance(actual, list): failures.append(label+':missing'); return
        ids = [o.get('id') for o in actual]
        if len(set(ids)) != len(ids) or set(ids) != {o['id'] for o in wanted}:
            failures.append(label+':inventory'); return
        index = {o['id']:o for o in actual}
        for item in wanted:
            got = index[item['id']]
            for key in fields:
                a,b = item.get(key),got.get(key)
                if key in ('bbox','anchor','title_bbox'):
                    if not isinstance(b,list) or len(a)!=len(b): failures.append(label+':'+item['id']+':'+key); continue
                    for v in b: io.finite(v, key)
                    if any(abs(u-v)>tolerance for u,v in zip(a,b)):failures.append(label+':'+item['id']+':'+key)
                elif a!=b: failures.append(label+':'+item['id']+':'+key)
    check_items(expected['objects'], observed['objects'], 'objects', ('bbox','anchor','facts'))
    check_items(value['frames'], observed.get('frames'), 'frames', ('bbox','title','title_bbox'))
    if not failures:
        bounds=value['spec']['usable_rect'];gap=value['spec']['gap'];pad=value['spec']['padding']
        frames=observed['frames'];index={o['id']:o for o in observed['objects']}
        groups={g['id']:g['members'] for g in value['spec']['blocks']}
        def inside(a,b,margin=0):
            return a[0]>=b[0]+margin and a[1]>=b[1]+margin and a[2]<=b[2]-margin and a[3]<=b[3]-margin
        for i,f in enumerate(frames):
            box=rect(f['bbox']);title=rect(f['title_bbox'])
            if not inside(box,bounds):failures.append('actual-frame-out-of-bounds:'+f['id'])
            if not inside(title,box,pad):failures.append('actual-title-margin:'+f['id'])
            if any(overlap(box,g['bbox'],gap) for g in frames[:i]):failures.append('actual-frame-gap:'+f['id'])
            if any(overlap(box,r,gap) for r in value['spec'].get('obstacles',[])):failures.append('actual-obstacle-gap:'+f['id'])
            local=[index[mid]['bbox'] for mid in groups[f['id']]]
            for j,b in enumerate(local):
                if not inside(b,box,pad) or overlap(b,title,pad):failures.append('actual-content-margin:'+f['id'])
                if any(overlap(b,c,pad) for c in local[:j]):failures.append('actual-content-gap:'+f['id'])
    return {'status':'MISMATCH' if failures else 'MATCH', 'capture_stage':phase,
            'plan_digest':value['digest'], 'observed_digest':io.digest(observed), 'failures':failures,
            'scope':'declared scoped geometry and identity/pin facts; native save and electrical acceptance not established'}


def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='action',required=True)
    a=sub.add_parser('plan');a.add_argument('--source',required=True);a.add_argument('--spec',required=True);a.add_argument('--output',required=True)
    a=sub.add_parser('verify');a.add_argument('--plan',required=True);a.add_argument('--observed',required=True);a.add_argument('--tolerance',type=float,default=0.01)
    a=sub.add_parser('preflight');a.add_argument('--plan',required=True);a.add_argument('--source',required=True)
    args=p.parse_args()
    try:
        if args.action=='plan':
            result=plan(io.read(args.source),io.read(args.spec));io.save(Path(args.output),result,exclusive=True)
            print(io.encoded({'status':result['status'],'digest':result['digest'],'objects':len(result['moves'])}).decode())
        elif args.action=='preflight':
            value=io.read(args.plan);validate_plan(value)
            fresh=io.read(args.source);source_check(fresh)
            if io.digest(fresh)!=value['source_digest']:raise ValueError('STALE: readback differs from planning source')
            print('{"status":"SOURCE_MATCH_NOT_APPLIED"}')
        else:
            result=verify(io.read(args.plan),io.read(args.observed),args.tolerance)
            print(io.encoded(result).decode())
            if result['status']!='MATCH':return 1
    except (ValueError,KeyError,TypeError,OSError) as e:p.exit(2,'ERROR: '+str(e)+'\n')
    return 0


if __name__=='__main__':raise SystemExit(main())
