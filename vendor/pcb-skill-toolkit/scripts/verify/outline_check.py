# -*- coding: utf-8 -*-
"""Check one simple board outline and copper/drill edge clearance in millimetres.

The cut follows the stroke CENTRE: reported centreline dimensions are the board
dimensions, with no subtraction of pen width. Unordered/reversed strokes are
reconnected by their actual endpoints (1e-6 mm tolerance). Open, branched,
self-intersecting, overlapping, multiple-ring and region/flash outlines are rejected;
there is no bounding-box acceptance fallback. Internal cutouts are unsupported.

Copper polygon EDGES and entire drill slot centrelines are checked, including
intersections with concave board boundaries. Circular flashes, round strokes and
drill/slot radii are measured analytically against the parsed outline. Other
curved apertures and Gerber arcs use the shared reader's polygon approximation:
arc chord target is 0.02 mm (720-segment cap can exceed it), other curve errors
depend on aperture size/tessellation. Results near those errors need independent
verification; these are not exact curved-geometry manufacturing certificates.
Negative margins indicate outside geometry; their depth is sampled, not an exact
maximum penetration. Positive polygon/segment margins use all edge pairs.

Omitted copper/drill inputs are explicitly NOT CHECKED; an explicitly supplied
empty file fails coverage. A zero exit only accepts the supplied, supported scope.

USAGE: outline_check.py OUTLINE.GKO [--size W,H] [--edge 0.30]
           [--copper L1.GTL ...] [--drills D.DRL ...] [--tol 0.0005] [--json out.json]
       outline_check.py --selftest
"""
from __future__ import print_function

import argparse
import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, os.pardir, "placement"))
import geom2d as G
import gerber as GB
import clearance as CL

JOIN_TOL = 1e-6
EPS = 1e-9
APPROXIMATION = ("Gerber arcs are chord-flattened (0.02 mm target, 720 segment cap); "
                 "rounded non-circular flash outlines are tessellated. Curve error "
                 "depends on geometry; independently verify near-threshold results.")


def _finite(values, label):
    if any(not math.isfinite(v) for v in values):
        raise ValueError("%s must contain finite numbers" % label)


def _edges(poly):
    return list(zip(poly, poly[1:] + poly[:1]))


def _simple_polygon(poly, label):
    if len(poly) > 1 and math.dist(poly[0], poly[-1]) <= EPS:
        poly = poly[:-1]
    if len(poly) < 3:
        raise ValueError("%s has fewer than three vertices" % label)
    _finite([v for p in poly for v in p], label)
    edges = _edges(poly)
    for i, (a, b) in enumerate(edges):
        if math.dist(a, b) <= EPS:
            raise ValueError("%s contains a zero-length edge" % label)
        for j in range(i + 1, len(edges)):
            c, d = edges[j]
            adjacent = j == i + 1 or (i == 0 and j == len(edges) - 1)
            if adjacent:
                # Adjacent edges may share their endpoint, but may not backtrack.
                shared, u, v = (b, a, d) if j == i + 1 else (a, b, c)
                if (G.dist_point_segment(*u, *shared, *v) <= EPS or
                        G.dist_point_segment(*v, *shared, *u) <= EPS):
                    raise ValueError("%s has overlapping/backtracking edges" % label)
            elif G.dist_segment_segment(a, b, c, d) <= EPS:
                raise ValueError("%s self-intersects, touches or overlaps" % label)
    if G.poly_area(poly) <= EPS * EPS:
        raise ValueError("%s has zero area" % label)
    return poly


def outline_of(layer):
    """Return (ordered points, closed, pens, bbox); reject unsupported topology."""
    if layer.regions or layer.flashes:
        raise ValueError("outline regions/flashes unsupported; need one stroked ring")
    if not layer.segs:
        raise ValueError("no geometry on the outline layer")
    nodes, links, adjacency = [], [], []

    def node(point):
        _finite(point, "outline endpoint")
        matches = [i for i, p in enumerate(nodes) if math.dist(p, point) <= JOIN_TOL]
        if len(matches) > 1:
            raise ValueError("ambiguous outline endpoint matching")
        if matches:
            return matches[0]
        nodes.append(point)
        adjacency.append([])
        return len(nodes) - 1

    pens = []
    for s in layer.segs:
        _finite([s.ap.w, s.ap.h, s.ap.r, s.ap.dia], "outline pen")
        if min(s.ap.w, s.ap.h, s.ap.r, s.ap.dia) < 0:
            raise ValueError("outline pen must be nonnegative")
        pens.append(round(s.ap.dia, 6))
        a, b = node((s.x1, s.y1)), node((s.x2, s.y2))
        if a == b:
            raise ValueError("zero-length outline segment")
        k = len(links)
        links.append((a, b))
        adjacency[a].append(k)
        adjacency[b].append(k)
    if any(len(a) != 2 for a in adjacency):
        raise ValueError("outline is open or branched: every endpoint must have degree 2")
    used, ordered, current = set(), [], 0
    while True:
        ordered.append(nodes[current])
        candidates = [k for k in adjacency[current] if k not in used]
        if not candidates:
            break
        k = candidates[0]
        used.add(k)
        a, b = links[k]
        current = b if a == current else a
        if current == 0:
            break
    if len(used) != len(links):
        raise ValueError("multiple outline rings/internal cutouts unsupported")
    poly = _simple_polygon(ordered, "outline")
    return poly + poly[:1], True, sorted(set(pens)), G.bbox_of(poly)


def margin_to_outline(x, y, poly, bbox=None, use_poly=True):
    """Signed point distance; bounding-box acceptance is deliberately unsupported."""
    if not use_poly:
        raise ValueError("a validated outline polygon is required; no bbox fallback")
    d = min(G.dist_point_segment(x, y, *a, *b) for a, b in _edges(poly))
    if d <= EPS:
        return 0.0
    return d if G.point_in_poly(x, y, poly) else -d


def _segment_margin(a, b, board):
    """Whole-segment clearance, splitting at every boundary intersection."""
    boundary = _edges(board)
    minimum = min(G.dist_segment_segment(a, b, c, d) for c, d in boundary)
    dx, dy = b[0] - a[0], b[1] - a[1]
    length2 = dx * dx + dy * dy
    cuts = [0.0, 1.0]
    for c, d in boundary:
        ex, ey = d[0] - c[0], d[1] - c[1]
        den = dx * ey - dy * ex
        if abs(den) > 1e-15:
            t = ((c[0] - a[0]) * ey - (c[1] - a[1]) * ex) / den
            u = ((c[0] - a[0]) * dy - (c[1] - a[1]) * dx) / den
            if -EPS <= t <= 1 + EPS and -EPS <= u <= 1 + EPS:
                cuts.append(max(0.0, min(1.0, t)))
        elif length2 > 0:
            for p in (c, d):
                if G.dist_point_segment(*p, *a, *b) <= EPS:
                    cuts.append(max(0.0, min(1.0,
                        ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / length2)))
    cuts = sorted(set(cuts))
    samples = cuts + [(s + t) / 2 for s, t in zip(cuts, cuts[1:])]
    signed = min(margin_to_outline(a[0] + t * dx, a[1] + t * dy, board)
                 for t in samples)
    return signed if signed < -EPS else minimum


def _polygon_margin(poly, board):
    poly = _simple_polygon(list(poly), "copper polygon")
    return min(_segment_margin(a, b, board) for a, b in _edges(poly))


def _validate_aperture(ap):
    _finite([ap.w, ap.h, ap.r], "aperture dimensions")
    if ap.kind != "POLY" and (ap.w <= 0 or ap.h <= 0):
        raise ValueError("copper aperture dimensions must be positive")
    if ap.r < 0:
        raise ValueError("aperture rounding must be nonnegative")


def _copper_margins(layer, board):
    for f in layer.flashes:
        _finite([f.x, f.y], "flash coordinates")
        _validate_aperture(f.ap)
        if f.ap.kind == "C":
            m = margin_to_outline(f.x, f.y, board) - f.ap.w / 2
        elif f.ap.kind == "O":
            r = min(f.ap.w, f.ap.h) / 2
            dx, dy = f.ap.w / 2 - r, f.ap.h / 2 - r
            m = _segment_margin((f.x - dx, f.y - dy), (f.x + dx, f.y + dy), board) - r
        else:
            m = _polygon_margin(CL._flash_poly(f), board)
        yield m, "FLASH %s @(%.3f,%.3f)" % (f.ap, f.x, f.y)
    for s in layer.segs:
        _finite([s.x1, s.y1, s.x2, s.y2], "stroke coordinates")
        _validate_aperture(s.ap)
        if s.ap.kind != "C":
            raise ValueError("non-circular stroked copper aperture unsupported")
        m = _segment_margin((s.x1, s.y1), (s.x2, s.y2), board) - s.ap.dia / 2
        yield m, "STROKE (%.3f,%.3f)-(%.3f,%.3f)" % (s.x1, s.y1, s.x2, s.y2)
    for i, poly in enumerate(layer.regions):
        yield _polygon_margin(poly, board), "REGION #%d" % i


def _read(path):
    with open(path, encoding="utf-8", errors="strict") as fh:
        return fh.read()


def run(outline_path, size=None, edge=0.30, copper=(), drills=(), tol=5e-4, top=10,
        out=None):
    _finite([edge, tol], "edge and tolerance")
    if edge < 0 or tol <= 0:
        raise ValueError("edge must be nonnegative and tolerance must be positive")
    if size is not None:
        if len(size) != 2:
            raise ValueError("size must contain exactly width,height")
        _finite(size, "size")
        if min(size) <= 0:
            raise ValueError("size dimensions must be positive")
    lay = GB.parse_gerber(_read(outline_path), outline_path)
    pts, closed, pens, bb = outline_of(lay)
    board = pts[:-1]
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    fail = 0
    print("BOARD OUTLINE   %s" % os.path.basename(outline_path))
    print("path closes        : %s (one simple ring)" % closed)
    print("pen diameter(s)    : %s mm" % pens)
    print("SIZE (centreline)  : %.4f x %.4f mm" % (w, h))
    print("  Finished dimensions follow the stroke CENTRE; do not subtract pen width.")
    print("edge test uses     : complete edges against the validated outline polygon")
    print("approximation      : %s" % APPROXIMATION)
    if size is not None:
        good = abs(w - size[0]) <= tol and abs(h - size[1]) <= tol
        print("required           : %.4f x %.4f mm -> %s" % (*size, "PASS" if good else "FAIL"))
        fail += not good

    coverage, worst_cu, worst_dr = {"copper": [], "drills": []}, [], []
    for kind, paths in (("copper", copper), ("drills", drills)):
        if not paths:
            print("%s: NOT CHECKED (no files supplied)" % kind.upper())
        for path in paths:
            if kind == "copper":
                layer = GB.parse_gerber(_read(path), path)
                rows = [(m, os.path.basename(path), desc)
                        for m, desc in _copper_margins(layer, board)]
                worst_cu.extend(rows)
            else:
                _tools, hits, _plated = GB.parse_excellon(_read(path), path)
                rows = []
                for hit in hits:
                    _finite([hit.x, hit.y, hit.x2, hit.y2, hit.dia], "drill geometry")
                    if hit.dia <= 0:
                        raise ValueError("drill diameter must be positive (tool must be defined)")
                    m = _segment_margin((hit.x, hit.y), (hit.x2, hit.y2), board) - hit.dia / 2
                    rows.append((m, os.path.basename(path), "DRILL/SLOT d=%.4f" % hit.dia))
                worst_dr.extend(rows)
            state = "checked" if rows else "not_checked_empty"
            coverage[kind].append({"file": str(path), "status": state, "features": len(rows)})
            if not rows:
                print("%s: NOT CHECKED (empty file: %s)" % (kind.upper(), path))
                fail += 1

    counts = {}
    for kind, rows in (("copper", worst_cu), ("drill", worst_dr)):
        rows.sort(key=lambda x: x[0])
        bad = sum(m < edge - EPS for m, _f, _d in rows)
        outside = sum(m < -EPS for m, _f, _d in rows)
        counts[kind] = (bad, outside)
        if rows:
            print("%s: %d features; %d outside; %d below %.4f mm -> %s" %
                  (kind.upper(), len(rows), outside, bad, edge, "FAIL" if bad else "PASS"))
            for m, f, d in rows[:top]:
                print("  %.6f mm  %s  %s" % (m, f, d))
            fail += bool(bad)
    res = {"size": [w, h], "closed": closed, "pens": pens,
           "copper_outside": counts["copper"][1], "drill_outside": counts["drill"][1],
           "copper_margin_violations": counts["copper"][0],
           "drill_margin_violations": counts["drill"][0],
           "min_copper_margin": worst_cu[0][0] if worst_cu else None,
           "min_drill_margin": worst_dr[0][0] if worst_dr else None,
           "coverage": coverage,
           "copper_status": "not_supplied" if not copper else
               ("incomplete" if any(x["status"] != "checked" for x in coverage["copper"]) else "checked"),
           "drill_status": "not_supplied" if not drills else
               ("incomplete" if any(x["status"] != "checked" for x in coverage["drills"]) else "checked"),
           "approximation": APPROXIMATION, "failed_gates": int(fail)}
    print("failed gates: %d (supplied supported scope only)" % fail)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=2, allow_nan=False)
    return int(fail)


def _selftest():
    import tempfile
    with tempfile.TemporaryDirectory(prefix="outline-selftest-") as tmp:
        op = os.path.join(tmp, "board.GKO")
        text = ("%FSLAX26Y26*%\n%MOMM*%\n%ADD10C,0.2*%\nD10*\n"
                "X0Y0D02*\nX20000000Y0D01*\nX20000000Y10000000D01*\n"
                "X0Y10000000D01*\nX0Y0D01*\nM02*\n")
        with open(op, "w", encoding="utf-8") as fh:
            fh.write(text)
        assert run(op, size=(20, 10)) == 0
        pts, _closed, _pens, _bb = outline_of(GB.parse_gerber(text))
        assert abs(margin_to_outline(20.3, 9, pts) + 0.3) < EPS
    print("outline_check selftest: PASS")
    return 0


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outline", nargs="?")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--size")
    parser.add_argument("--edge", type=float, default=0.30)
    parser.add_argument("--tol", type=float, default=5e-4)
    parser.add_argument("--copper", nargs="+", default=[])
    parser.add_argument("--drills", nargs="+", default=[])
    parser.add_argument("--json")
    opts = parser.parse_args(argv[1:])
    if opts.selftest:
        return _selftest()
    if not opts.outline:
        parser.error("an outline file is required")
    try:
        size = tuple(float(v) for v in opts.size.split(",")) if opts.size is not None else None
        return int(bool(run(opts.outline, size=size, edge=opts.edge, tol=opts.tol,
                            copper=opts.copper, drills=opts.drills, out=opts.json)))
    except (ValueError, OSError, OverflowError) as error:
        print("NOT CHECKED / INPUT ERROR: %s" % error, file=sys.stderr)
        if opts.json:
            with open(opts.json, "w", encoding="utf-8") as fh:
                json.dump({"status": "not_checked", "error": str(error),
                           "failed_gates": 1}, fh, indent=2, allow_nan=False)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
