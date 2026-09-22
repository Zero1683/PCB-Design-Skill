# -*- coding: utf-8 -*-
"""Solder-mask coverage of identified copper pad flashes, using actual geometry.

The union of mask flashes and simple linear regions is compared with each pad.
PASS means full area coverage; it does not certify mask dams, paste or assembly.
Partial openings can be intentional solder-mask-defined pads: they are NOT_CHECKED
unless --allow-partial-openings explicitly declares that policy for this layer.
--tol is retained only for concentric expansion reporting; it never enlarges mask.
Untagged exports need --assume-all-pads. Unsupported geometry is NOT_CHECKED.
Only literal exposed outline macros are supported, including macros named
RoundRect. Parameterized/compound RoundRect exports require another capable
checker; their geometry is never inferred from the macro name or ADD parameters.

No external geometry dependency is required. Circle/line boundary intersections
partition the plane into vertical strips with invariant boundary ordering. Interval
union/subtraction in each strip therefore checks area coverage without sampling a
grid or approximating curved outlines. Numerical resolution is 1e-10 mm; geometric
features below that resolution are outside this check's scope.

USAGE: mask_check.py COPPER.GTL MASK.GTS [--tol 0.02] [--assume-all-pads]
           [--allow-partial-openings] [--json out.json] [--top 10]
       mask_check.py --selftest
"""
from __future__ import print_function

import argparse
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerber as GB

EPS = 1e-10


def _cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _line_hits(a, b, c, d):
    u, v, w = _sub(b, a), _sub(d, c), _sub(c, a)
    den = _cross(u, v)
    if abs(den) < EPS * EPS:
        return []  # collinear endpoints are already strip boundaries
    t, s = _cross(w, v) / den, _cross(w, u) / den
    if -EPS <= t <= 1 + EPS and -EPS <= s <= 1 + EPS:
        return [(a[0] + t * u[0], a[1] + t * u[1])]
    return []


def _on_segment(p, a, b):
    v, w = _sub(b, a), _sub(p, a)
    return (abs(_cross(v, w)) <= EPS * max(1, math.hypot(*v)) and
            min(a[0], b[0]) - EPS <= p[0] <= max(a[0], b[0]) + EPS and
            min(a[1], b[1]) - EPS <= p[1] <= max(a[1], b[1]) + EPS)


def _polygon(points):
    pts = [tuple(p) for p in points]
    if pts and pts[0] == pts[-1]:
        pts.pop()
    if len(pts) < 3 or any(len(p) != 2 or not all(math.isfinite(v) for v in p) for p in pts):
        raise ValueError('Invalid or nonfinite polygon')
    if len(set(pts)) != len(pts):
        raise ValueError('Repeated polygon vertex / compound contour unsupported')
    edges = list(zip(pts, pts[1:] + pts[:1]))
    for i, (a, b) in enumerate(edges):
        if math.dist(a, b) <= EPS:
            raise ValueError('Degenerate polygon edge')
        incoming, outgoing = _sub(a, pts[i-1]), _sub(b, a)
        if (abs(_cross(incoming, outgoing)) <= EPS * EPS and
                incoming[0]*outgoing[0]+incoming[1]*outgoing[1] < 0):
            raise ValueError('Backtracking polygon edge unsupported')
        for j in range(i + 1, len(edges)):
            if j == i + 1 or (i == 0 and j == len(edges) - 1):
                continue
            c, d = edges[j]
            if (_line_hits(a, b, c, d) or _on_segment(a, c, d) or
                    _on_segment(b, c, d) or _on_segment(c, a, b) or _on_segment(d, a, b)):
                raise ValueError('Self-intersecting / compound polygon unsupported')
    origin = pts[0]
    area = sum(_cross(_sub(a, origin), _sub(b, origin)) for a, b in edges)
    if abs(area) <= EPS * EPS:
        raise ValueError('Zero-area polygon')
    return ('P', pts)


def _disk(x, y, r):
    if not all(math.isfinite(v) for v in (x, y, r)) or r <= EPS:
        raise ValueError('Invalid circle')
    return ('C', (x, y, r))


def _rect(x, y, w, h):
    return _polygon([(x-w/2, y-h/2), (x+w/2, y-h/2),
                     (x+w/2, y+h/2), (x-w/2, y+h/2)])


def _flash(f):
    a, x, y = f.ap, f.x, f.y
    if not all(math.isfinite(v) for v in (x, y, a.w, a.h)) or min(a.w, a.h) <= EPS:
        raise ValueError('Nonpositive/nonfinite flash dimensions')
    if a.kind == 'C':
        return [_disk(x, y, a.w / 2)]
    if a.kind == 'R':
        return [_rect(x, y, a.w, a.h)]
    if a.kind == 'POLY':
        return [_polygon([(x+px, y+py) for px, py in a.verts])]
    if a.kind not in ('O', 'RR'):
        raise ValueError('Unsupported aperture %s' % a.kind)
    r = min(a.w, a.h)/2 if a.kind == 'O' else a.r/2
    if not math.isfinite(r) or r < 0 or r > min(a.w, a.h)/2:
        raise ValueError('Invalid rounded aperture radius')
    if r <= EPS:
        return [_rect(x, y, a.w, a.h)]
    dx, dy = a.w/2-r, a.h/2-r
    pieces = []
    if a.w-2*r > EPS:
        pieces.append(_rect(x, y, a.w-2*r, a.h))
    if a.h-2*r > EPS:
        pieces.append(_rect(x, y, a.w, a.h-2*r))
    pieces.extend(_disk(x+sx*dx, y+sy*dy, r) for sx, sy in set(
        (sx, sy) for sx in (-1, 1) for sy in (-1, 1)))
    return pieces


def _bbox(s):
    if s[0] == 'C':
        x, y, r = s[1]
        return x-r, y-r, x+r, y+r
    return (min(p[0] for p in s[1]), min(p[1] for p in s[1]),
            max(p[0] for p in s[1]), max(p[1] for p in s[1]))


def _boundaries(s):
    if s[0] == 'C':
        return [s]
    p = s[1]
    return [('L', (a, b)) for a, b in zip(p, p[1:] + p[:1])]


def _hits(a, b):
    if a[0] == b[0] == 'L':
        return _line_hits(*a[1], *b[1])
    if a[0] == 'L':
        a, b = b, a
    x, y, r = a[1]
    if b[0] == 'L':
        p, q = b[1]
        u, v = _sub(q, p), _sub(p, (x, y))
        aa = u[0]**2 + u[1]**2
        bb, cc = 2*(u[0]*v[0]+u[1]*v[1]), v[0]**2+v[1]**2-r*r
        disc = bb*bb-4*aa*cc
        if disc < 0:
            return []
        roots = [(-bb + sign*math.sqrt(disc))/(2*aa) for sign in (-1, 1)]
        return [(p[0]+t*u[0], p[1]+t*u[1]) for t in roots if 0 <= t <= 1]
    xx, yy, rr = b[1]
    dx, dy = xx-x, yy-y
    d = math.hypot(dx, dy)
    if d == 0 or d > r+rr or d < abs(r-rr):
        return []
    along = (r*r-rr*rr+d*d)/(2*d)
    h = math.sqrt(max(0, r*r-along*along))
    return [(x+along*dx/d+sign*h*dy/d, y+along*dy/d-sign*h*dx/d) for sign in (-1, 1)]


def _merge(intervals):
    out = []
    for lo, hi in sorted(intervals):
        if hi-lo <= EPS:
            continue
        if out and lo <= out[-1][1]+EPS:
            out[-1] = (out[-1][0], max(out[-1][1], hi))
        else:
            out.append((lo, hi))
    return out


def _slice(shapes, x):
    result = []
    for kind, data in shapes:
        if kind == 'C':
            cx, cy, r = data
            v = r*r-(x-cx)**2
            if v > 0:
                h = math.sqrt(v)
                result.append((cy-h, cy+h))
        else:
            ys = []
            for a, b in zip(data, data[1:] + data[:1]):
                if min(a[0], b[0]) < x < max(a[0], b[0]):
                    ys.append(a[1]+(x-a[0])*(b[1]-a[1])/(b[0]-a[0]))
            ys.sort()
            if len(ys) % 2:
                raise ValueError('Unstable polygon slice')
            result.extend(zip(ys[::2], ys[1::2]))
    return _merge(result)


def _classify(pad, mask):
    """Return full/partial/none by interval arrangements of exact boundaries."""
    boxes = [_bbox(p) for p in pad]
    xmin, ymin = min(b[0] for b in boxes), min(b[1] for b in boxes)
    xmax, ymax = max(b[2] for b in boxes), max(b[3] for b in boxes)
    masks = []
    for s in mask:
        a, b, c, d = _bbox(s)
        if a <= xmax and c >= xmin and b <= ymax and d >= ymin:
            masks.append(s)
    if not masks:
        return 'none'
    boundaries, xs = [], {xmin, xmax}
    for s in pad + masks:
        boundaries.extend(_boundaries(s))
        if s[0] == 'C':
            x, _, r = s[1]
            xs.update((x-r, x+r))
        else:
            xs.update(p[0] for p in s[1])
    for i, a in enumerate(boundaries):
        for b in boundaries[i+1:]:
            xs.update(p[0] for p in _hits(a, b))
    xs = sorted(x for x in xs if xmin <= x <= xmax)
    overlap = uncovered = False
    for left, right in zip(xs, xs[1:]):
        if right-left <= EPS:
            continue
        x = (left+right)/2
        mi = _slice(masks, x)
        for lo, hi in _slice(pad, x):
            cursor = lo
            for a, b in mi:
                if min(hi, b)-max(lo, a) > EPS:
                    overlap = True
                if b <= cursor:
                    continue
                if a > cursor+EPS:
                    break
                cursor = max(cursor, b)
                if cursor >= hi-EPS:
                    break
            if cursor < hi-EPS:
                uncovered = True
        if overlap and uncovered:
            return 'partial'
    return 'partial' if overlap and uncovered else 'full' if overlap else 'none'


def _audit_text(text, copper=False):
    """Reject information the shared lightweight parser would otherwise discard."""
    tokens = list(GB._TOKEN.finditer(text))
    end = 0
    region, contours, interpolation, section = False, 0, 1, ''
    formats = units = draws = 0
    ended = False
    for token in tokens:
        if text[end:token.start()].strip():
            raise ValueError('Unparsed Gerber text')
        end = token.end()
        raw = token.group(0).strip()
        if ended:
            raise ValueError('Data after M02 is unsupported')
        if raw.startswith('%'):
            body = raw[1:-1].strip()
            if body.startswith('AM'):
                continue  # macro validation is performed by the parser
            for stmt in (s.strip() for s in body.split('*') if s.strip()):
                formats += bool(GB._FS.fullmatch(stmt))
                units += stmt == 'MOMM'
            continue  # parameter validation is performed by the parser
        cmd = raw[:-1].strip()
        if cmd.startswith('G04'):
            tag = GB._SECTION.match(cmd)
            if tag:
                section = tag.group(1) if tag.group(2) == 'Start' else ''
            continue
        if cmd == 'G36':
            if region:
                raise ValueError('Nested region unsupported')
            if copper and section != 'Copper':
                raise ValueError('Copper region pad identity is unavailable; pad-flash scope incomplete')
            region, contours, draws = True, 0, 0
            continue
        if cmd == 'G37':
            if not region or contours != 1 or draws < 2:
                raise ValueError('Empty or compound/hole region unsupported')
            region = False
            continue
        if cmd == 'M02':
            if region:
                raise ValueError('Unterminated region')
            ended = True
            continue
        if cmd in ('G74', 'G75') or GB._APSEL.fullmatch(cmd):
            continue
        mode = re.match(r'^G0?([123])(?=[XYIJD]|$)', cmd)
        if mode:
            interpolation = int(mode.group(1))
            cmd = cmd[mode.end():]
        if not cmd:
            continue
        if not re.fullmatch(r'(?:[XYIJ]-?\d+)*D0?[123]', cmd):
            raise ValueError('Unsupported or malformed Gerber command %r' % cmd)
        op = int(GB._DCODE.search(cmd).group(1))
        if region:
            if op == 2:
                contours += 1
                if contours > 1:
                    raise ValueError('Compound/hole regions unsupported; contours cannot be unioned')
            elif op != 1 or interpolation != 1:
                raise ValueError('Only simple linear region contours are supported')
            else:
                draws += 1
        elif op == 1 and (not copper or section in ('', 'Pad', 'Via')):
            raise ValueError('Stroked mask openings or unidentified/pad copper strokes unsupported')
    if text[end:].strip() or region or not ended:
        raise ValueError('Unterminated Gerber input')
    if formats != 1 or units != 1:
        raise ValueError('Exactly one explicit supported format and millimetre unit declaration required')


def _parse_verified(text, name):
    """Use actual AM semantics even when a macro has the special name RoundRect.

    The shared reader has a legacy name-based RoundRect shortcut. Macro names do
    not define geometry. Rename that macro locally so the ordinary, strict macro
    parser handles its real outline, rejecting compound/parameterized primitives.
    An undefined RoundRect is rejected rather than inferred from ADD dimensions.
    """
    tokens = list(GB._TOKEN.finditer(text))
    macros, used = {}, False
    for token in tokens:
        raw = token.group(0).strip()
        if not raw.startswith('%'):
            continue
        body = raw[1:-1].strip()
        if body.startswith('AM'):
            parts = body.split('*')
            macros[parts[0][2:].strip()] = [p.strip() for p in parts[1:] if p.strip()]
            continue
        for stmt in (s.strip() for s in body.split('*') if s.strip()):
            add = GB._ADD.fullmatch(stmt)
            used = used or bool(add and add.group(2) == 'RoundRect')
    if not used:
        return GB.parse_gerber(text, name)
    if 'RoundRect' not in macros:
        raise ValueError('Undefined RoundRect macro: aperture dimensions cannot establish its geometry')
    try:
        GB._macro_outline(macros['RoundRect'])  # actual primitive, not its name
    except ValueError as error:
        raise ValueError('RoundRect macro geometry is unsupported: %s; '
                         'parameterized/compound RoundRect requires an independent capable checker'
                         % error) from error
    alias = 'MaskVerifiedRoundRect'
    while alias in macros:
        alias += '_'
    pieces, end = [], 0
    for token in tokens:
        pieces.append(text[end:token.start()])
        end = token.end()
        raw = token.group(0).strip()
        if raw.startswith('%'):
            body = raw[1:-1].strip()
            if body.startswith('AM'):
                macro_name, rest = body.split('*', 1)
                if macro_name[2:].strip() == 'RoundRect':
                    raw = '%AM' + alias + '*' + rest + '%'
            else:
                statements = body.split('*')
                for i, stmt in enumerate(statements):
                    add = GB._ADD.fullmatch(stmt.strip())
                    if add and add.group(2) == 'RoundRect':
                        statements[i] = ('ADD' + add.group(1) + alias +
                            (',' + add.group(3) if add.group(3) is not None else ''))
                raw = '%' + '*'.join(statements) + '%'
        pieces.append(raw)
    pieces.append(text[end:])
    return GB.parse_gerber(''.join(pieces), name)


def match(copper, mask, tol=0.02, assume_all_pads=False, allow_partial_openings=False):
    if not math.isfinite(tol) or tol < 0:
        raise ValueError('--tol must be finite and nonnegative')
    tagged = any(f.section for f in copper.flashes + copper.segs)
    pads = [f for f in copper.flashes if assume_all_pads or f.section == 'Pad']
    vias = [f for f in copper.flashes if not assume_all_pads and f.section == 'Via']
    if not assume_all_pads and any(not f.section for f in copper.flashes):
        raise ValueError('Untagged copper flashes require --assume-all-pads; identity not checked')
    if not pads:
        raise ValueError('No pad flashes in checked scope')
    if mask.segs:
        raise ValueError('Stroked mask openings unsupported')
    shapes = [s for f in mask.flashes for s in _flash(f)]
    shapes.extend(_polygon(p) for p in mask.regions)
    opened, covered, partial, exp = [], [], [], {}
    for p in pads:
        state = _classify(_flash(p), shapes)
        if state == 'none':
            covered.append(p)
        elif state == 'partial':
            partial.append(p)
        else:
            opened.append((p, None))
            # Expansion only has a scalar meaning for one concentric same-kind flash.
            matches = [m for m in mask.flashes if m.ap.kind == p.ap.kind and
                       math.hypot(m.x-p.x, m.y-p.y) <= min(tol, EPS) and
                       _classify(_flash(p), _flash(m)) == 'full']
            if len(matches) == 1 and matches[0].ap.kind in ('C', 'R', 'O', 'RR'):
                m = matches[0]
                ex, ey = (m.ap.w-p.ap.w)/2, (m.ap.h-p.ap.h)/2
                key = round(ex, 4) if abs(ex-ey) <= EPS else 'anisotropic'
            else:
                key = 'geometry-union/offset'
            exp[key] = exp.get(key, 0)+1
    via_open, via_partial, via_tented = [], [], []
    for v in vias:
        state = _classify(_flash(v), shapes)
        (via_open if state == 'full' else via_partial if state == 'partial' else via_tented).append(v)
    state = ('FAIL' if covered else 'NOT_CHECKED' if partial and not allow_partial_openings else 'PASS')
    return dict(tagged=tagged, pads=pads, vias=vias, opened=opened, covered=covered,
                partial=partial, expansion=exp, via_open=via_open, via_partial=via_partial,
                via_tented=via_tented, state=state)


def run(copper_path, mask_path, tol=0.02, assume_all_pads=False, top=10, out=None,
        allow_partial_openings=False):
    result = {'state': 'NOT_CHECKED', 'coverage': {'scope': 'copper pad flashes on one supplied side',
              'pads': None, 'checked': 0, 'via_identity': 'unavailable'},
              'policy': 'positive-area opening' if allow_partial_openings else 'full pad coverage',
              'numerical_resolution_mm': EPS}
    try:
        if not math.isfinite(tol) or tol < 0 or top < 0:
            raise ValueError('--tol must be finite/nonnegative and --top nonnegative')
        with open(copper_path, encoding='utf-8') as fh:
            cu_text = fh.read()
        with open(mask_path, encoding='utf-8') as fh:
            mk_text = fh.read()
        _audit_text(cu_text, copper=True)
        _audit_text(mk_text)
        cu, mk = _parse_verified(cu_text, copper_path), _parse_verified(mk_text, mask_path)
        r = match(cu, mk, tol, assume_all_pads, allow_partial_openings)
        result.update(state=r['state'], pads=len(r['pads']), opened=len(r['opened']),
                      partial=len(r['partial']), covered=len(r['covered']), tagged=r['tagged'],
                      vias=len(r['vias']) if not assume_all_pads else None,
                      vias_open=len(r['via_open']) if not assume_all_pads else None,
                      vias_partial=len(r['via_partial']) if not assume_all_pads else None,
                      expansion={str(k): v for k, v in r['expansion'].items()})
        result['coverage'].update(pads=len(r['pads']), checked=len(r['pads']),
                                 excluded_nonpad_flashes=len(cu.flashes)-len(r['pads'])-len(r['vias']),
                                 excluded_copper_regions=len(cu.regions),
                                 excluded_nonpad_strokes=len(cu.segs),
                                 via_identity='unavailable (all flashes assumed pads)' if assume_all_pads else 'G04 sections')
        if r['partial'] and not allow_partial_openings:
            result['reason'] = 'Partial openings need a declared SMD-pad policy (--allow-partial-openings)'
        if r['covered']:
            result['reason'] = '%d pad(s) have no positive-area mask opening' % len(r['covered'])
        print('pads: %d; full: %d; partial: %d; no opening: %d' %
              (len(r['pads']), len(r['opened']), len(r['partial']), len(r['covered'])))
        for label in ('covered', 'partial'):
            for p in r[label][:top]:
                print('  %s pad %s at (%.6f, %.6f)' % (label, p.ap, p.x, p.y))
        print('vias full / partial / tented: %s' % ('unavailable' if assume_all_pads else
              '%d / %d / %d' % (len(r['via_open']), len(r['via_partial']), len(r['via_tented']))))
        print('mask expansion per side: %s' % result['expansion'])
    except (ValueError, OSError, OverflowError) as error:
        result['reason'] = str(error)
    print('verdict: %s%s' % (result['state'], ' - '+result['reason'] if result.get('reason') else ''))
    print('scope: %s; checked: %s; policy: %s' %
          (result['coverage']['scope'], result['coverage']['checked'], result['policy']))
    if out:
        with open(out, 'w', encoding='utf-8') as fh:
            json.dump(result, fh, indent=2, allow_nan=False)
            fh.write('\n')
    return 0 if result['state'] == 'PASS' else 1 if result['state'] == 'FAIL' else 2


def _selftest():
    cases = [
        ([_disk(8, 8, .25)], [_polygon([(0, 0), (10, 0), (0, 10)])], 'none'),
        ([_disk(2, 2, .25)], [_disk(2.1, 2, 1)], 'full'),
        ([_disk(0, 0, 1)], [_disk(0, 0, .5)], 'partial'),
        ([_rect(0, 0, 2, 2)], [_rect(-.5, 0, 1, 2), _rect(.5, 0, 1, 2)], 'full'),
        ([_disk(0, 0, 1)], [_disk(2, 0, 1)], 'none'),
    ]
    ok = all(_classify(p, m) == expected for p, m, expected in cases)
    print('mask_check selftest: %s (%d cases)' % ('PASS' if ok else 'FAIL', len(cases)))
    return 0 if ok else 1


def main(argv):
    if argv[1:] == ['--selftest']:
        return _selftest()
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('copper')
    parser.add_argument('mask')
    parser.add_argument('--tol', type=float, default=.02)
    parser.add_argument('--top', type=int, default=10)
    parser.add_argument('--json')
    parser.add_argument('--assume-all-pads', action='store_true')
    parser.add_argument('--allow-partial-openings', action='store_true')
    for flag in ('--tol', '--top', '--json', '--assume-all-pads', '--allow-partial-openings'):
        if sum(a.split('=', 1)[0] == flag for a in argv[1:]) > 1:
            parser.error('Duplicate option %s' % flag)
    args = parser.parse_args(argv[1:])
    return run(args.copper, args.mask, args.tol, args.assume_all_pads,
               args.top, args.json, args.allow_partial_openings)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
