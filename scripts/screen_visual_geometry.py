#!/usr/bin/env python3
"""Conservative bounds screening; not a native parser or engineering acceptance."""
import argparse
import json
import math
from pathlib import Path


def box(value):
    if (not isinstance(value, list) or len(value) != 4
            or any(type(v) not in (int, float) or not math.isfinite(v) for v in value)
            or value[2] <= value[0] or value[3] <= value[1]):
        raise ValueError('Expected finite nonempty [xmin,ymin,xmax,ymax]')
    return value


def gap(a, b):
    return math.hypot(max(a[0]-b[2], b[0]-a[2], 0), max(a[1]-b[3], b[1]-a[3], 0))


def intersects(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def screen(data):
    if not isinstance(data, dict) or type(data.get('schema')) is not int or data['schema'] != 1:
        raise ValueError('Expected schema 1')
    kind = data.get('kind')
    if kind not in ('pcb', 'schematic') or data.get('unit') != ('mm' if kind == 'pcb' else 'sheet'):
        raise ValueError('Invalid kind or unit')
    for key in ('baseline_id', 'source'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError('Missing ' + key)
    if data.get('coverage') not in ('complete', 'partial'):
        raise ValueError('Explicit coverage required')
    missing = data.get('missing')
    if not isinstance(missing, list) or any(not isinstance(x, str) or not x.strip() for x in missing):
        raise ValueError('Explicit missing-geometry list required')
    objects = data.get('objects')
    if not isinstance(objects, list) or not objects:
        raise ValueError('Nonempty object list required')
    ids = set()
    for obj in objects:
        if not isinstance(obj, dict): raise ValueError('Invalid object')
        ident = obj.get('id')
        if not isinstance(ident, str) or not ident.strip() or ident in ids:
            raise ValueError('Missing or duplicate object ID')
        ids.add(ident)
        box(obj.get('bbox'))
        if not isinstance(obj.get('kind'), str) or not obj['kind'].strip():
            raise ValueError('Object kind required')
        if kind == 'pcb':
            if obj['kind'] not in ('pad', 'silk', 'mask'):
                raise ValueError('PCB object kind must be pad, silk or mask')
            layers = obj.get('layers')
            if not isinstance(layers, list) or not layers or any(not isinstance(x, str) or not x.strip() for x in layers):
                raise ValueError('Explicit occupied layer names required')
    suspects = []
    if kind == 'schematic':
        usable = box(data.get('usable'))
        if not isinstance(data.get('reserved'), list): raise ValueError('Reserved bounds list required')
        reserved = [box(x) for x in data['reserved']]
        for obj in objects:
            b = obj['bbox']
            if b[0] < usable[0] or b[1] < usable[1] or b[2] > usable[2] or b[3] > usable[3]:
                suspects.append({'id': obj['id'], 'reason': 'outside-usable-page'})
            for i, r in enumerate(reserved):
                if intersects(b, r): suspects.append({'id': obj['id'], 'reason': 'reserved-area', 'area': i})
    else:
        present = {o['kind'] for o in objects}
        for category in sorted({'pad', 'silk', 'mask'} - present):
            missing = missing + ['absent-category:' + category]
        limits = data.get('limits')
        required = {'pad-pad', 'silk-silk', 'mask-silk'}
        if not isinstance(limits, dict) or set(limits) != required:
            raise ValueError('All three spacing limits required')
        if any(type(v) not in (int, float) or not math.isfinite(v) or v <= 0 for v in limits.values()):
            raise ValueError('Spacing limits must be finite and strictly positive')
        for i, a in enumerate(objects):
            for b in objects[i+1:]:
                rule = '-'.join(sorted([a['kind'], b['kind']]))
                layers = sorted(set(a['layers']) & set(b['layers']))
                if rule not in limits or not layers: continue
                distance = gap(a['bbox'], b['bbox'])
                if distance < limits[rule]:
                    suspects.append({'ids': [a['id'], b['id']], 'rule': rule, 'layers': layers,
                                     'aabb_gap_mm': distance, 'required_mm': limits[rule]})
    return {'scope': 'conservative-transformed-bounds-only', 'baseline_id': data['baseline_id'],
            'source': data['source'], 'suspects': suspects, 'missing_geometry': missing,
            'screen_clear': not suspects and not missing and data['coverage'] == 'complete',
            'engineering_acceptance': 'NOT_ASSESSED',
            'limitations': 'Coverage is caller-declared. AABBs can over-report rotated/irregular shapes. Text readability, exact contours, net correctness and block separators need independent review.'}


def unique(pairs):
    out = {}
    for key, value in pairs:
        if key in out: raise ValueError('Duplicate JSON key: ' + key)
        out[key] = value
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('snapshot', type=Path)
    args = p.parse_args()
    try:
        result = screen(json.loads(args.snapshot.read_text(encoding='utf-8-sig'), object_pairs_hook=unique))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        p.exit(2, f'ERROR: {exc}\n')
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    return int(not result['screen_clear'])


if __name__ == '__main__':
    raise SystemExit(main())
