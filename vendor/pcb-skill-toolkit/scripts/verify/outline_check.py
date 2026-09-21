# -*- coding: utf-8 -*-
"""Board outline: size, closure, and anything that sticks out of it.

WHAT THIS MEASURES
    From the outline Gerber alone:
      * the extent and the size, against `--size W,H` if you give one;
      * whether the outline path CLOSES (an open outline is a milling instruction the
        fabricator has to guess at);
      * the pen width it is drawn with, which is where the real edge sits: the cut
        follows the CENTRE of the stroke, so a 0.2 mm pen means the finished board is
        the reported extent minus one pen width.
    Then, given copper and drill files:
      * every copper primitive whose outline reaches OUTSIDE the board, or comes closer
        to it than `--edge`;
      * every drilled feature whose edge does the same.

WHAT THIS CANNOT SEE
    * A non-rectangular board, properly.  Copper-outside is tested against the outline
      POLYGON where the outline is a single closed path, and against its bounding box
      otherwise -- the report says which was used.  A board with internal cutouts or
      milled slots needs those treated as keep-outs and this does not do that; check
      them by eye on the render.
    * V-scoring, tab-routing and panel rails.  A board that will be scored has copper
      restrictions this knows nothing about.
    * Whether the size is the size you ordered.  It measures; you compare.

HOW IT WAS VALIDATED
    On a released board this read 41.400 x 100.000 mm to within 0.0005 mm, matched the
    design model's outline, and reported the closest drill edge and copper edge that the
    fabrication review used.  `--selftest` runs synthetic geometry with a known answer.

USAGE
    python3 outline_check.py OUTLINE.GKO [--size 41.4,100.0] [--edge 0.30]
                             [--copper L1.GTL L4.GBL ...] [--drills D.DRL ...]
                             [--tol 0.0005] [--json out.json]
    python3 outline_check.py --selftest
"""
from __future__ import print_function

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, os.pardir, "placement"))
import geom2d as G                                                    # noqa: E402
import gerber as GB                                                   # noqa: E402
import clearance as CL                                                # noqa: E402


def outline_of(layer):
    """-> (points, closed, pens, bbox).  Points follow the stroke order."""
    pts = []
    for s in layer.segs:
        if not pts:
            pts.append((s.x1, s.y1))
        pts.append((s.x2, s.y2))
    for r in layer.regions:
        pts.extend(r)
    if not pts:
        raise SystemExit("no geometry on the outline layer")
    closed = (abs(pts[0][0] - pts[-1][0]) < 1e-6 and abs(pts[0][1] - pts[-1][1]) < 1e-6)
    pens = sorted({round(s.ap.dia, 6) for s in layer.segs})
    return pts, closed, pens, G.bbox_of(pts)


def margin_to_outline(x, y, poly, bbox, use_poly):
    """Distance from a point to the board edge; negative when outside."""
    if use_poly:
        d = min(G.dist_point_segment(x, y, poly[i][0], poly[i][1],
                                     poly[(i + 1) % len(poly)][0],
                                     poly[(i + 1) % len(poly)][1])
                for i in range(len(poly)))
        return d if G.point_in_poly(x, y, poly) else -d
    inside = (bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3])
    d = min(abs(x - bbox[0]), abs(x - bbox[2]), abs(y - bbox[1]), abs(y - bbox[3]))
    return d if inside else -d


def run(outline_path, size=None, edge=0.30, copper=(), drills=(), tol=5e-4, top=10,
        out=None):
    lay = GB.parse_gerber(open(outline_path, encoding="utf-8",
                               errors="replace").read(), outline_path)
    pts, closed, pens, bb = outline_of(lay)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    fail = 0

    print("=" * 74)
    print("BOARD OUTLINE   %s" % os.path.basename(outline_path))
    print("=" * 74)
    print("segments           : %d   regions %d" % (len(lay.segs), len(lay.regions)))
    print("pen diameter(s)    : %s mm" % pens)
    print("path closes        : %s" % closed)
    if not closed:
        print("   ** an open outline is a milling path the fabricator has to guess at **")
        fail += 1
    print("extent             : X %.6f .. %.6f    Y %.6f .. %.6f"
          % (bb[0], bb[2], bb[1], bb[3]))
    print("SIZE (stroke path) : %.4f x %.4f mm" % (w, h))
    if pens:
        print("   the cut follows the stroke CENTRE, so the finished board is about")
        print("   %.4f x %.4f mm with a %.4f mm pen." % (w - pens[-1], h - pens[-1], pens[-1]))
    if size:
        okw = abs(w - size[0]) < tol
        okh = abs(h - size[1]) < tol
        print("required           : %.4f x %.4f mm  -> %s"
              % (size[0], size[1], "PASS" if (okw and okh) else "FAIL"))
        if not (okw and okh):
            fail += 1

    use_poly = closed and len(pts) >= 4 and not lay.regions
    print("edge test uses     : %s"
          % ("the outline polygon" if use_poly else
             "the outline BOUNDING BOX (a cutout or an open path would be missed)"))

    worst_cu, outside_cu = [], []
    for path in copper:
        cl = GB.parse_gerber(open(path, encoding="utf-8", errors="replace").read(), path)
        for centre, poly, desc in CL.primitives(cl):
            for (px, py) in poly:
                m = margin_to_outline(px, py, pts, bb, use_poly)
                worst_cu.append((m, os.path.basename(path), desc))
                if m < 0:
                    outside_cu.append((m, os.path.basename(path), desc))
                    break
    worst_cu.sort(key=lambda t: t[0])
    if copper:
        print()
        print("COPPER vs the outline   (need >= %.4f mm)" % edge)
        print("  copper primitives reaching OUTSIDE the board: %d" % len(outside_cu))
        for m, f, d in outside_cu[:top]:
            print("     %8.4f  %-28s %s" % (m, f, d[:60]))
        print("  closest %d copper points:" % top)
        seen = set()
        shown = 0
        for m, f, d in worst_cu:
            if d in seen:
                continue
            seen.add(d)
            print("     %8.4f  %-28s %s" % (m, f, d[:60]))
            shown += 1
            if shown >= top:
                break
        bad = [x for x in worst_cu if x[0] < edge - 1e-9]
        print("  copper inside the %.3f mm edge margin: %d point(s)" % (edge, len(bad)))
        if outside_cu:
            fail += 1

    worst_dr = []
    for path in drills:
        _t, hits, _p = GB.parse_excellon(open(path, encoding="utf-8",
                                              errors="replace").read(), path)
        for hgb in hits:
            r = hgb.dia / 2.0
            for (px, py) in ((hgb.x, hgb.y), (hgb.x2, hgb.y2)):
                m = margin_to_outline(px, py, pts, bb, use_poly) - r
                worst_dr.append((m, os.path.basename(path), hgb.dia, px, py))
    worst_dr.sort(key=lambda t: t[0])
    if drills:
        print()
        print("DRILLS vs the outline   (need >= %.4f mm)" % edge)
        print("  closest drill edge : %.4f mm  (d=%.3f at %.3f, %.3f in %s)"
              % (worst_dr[0][0], worst_dr[0][2], worst_dr[0][3], worst_dr[0][4],
                 worst_dr[0][1]))
        bad = [x for x in worst_dr if x[0] < edge - 1e-9]
        outd = [x for x in worst_dr if x[0] < 0]
        print("  drills outside the board          : %d" % len(outd))
        print("  drills inside the %.3f mm margin  : %d" % (edge, len(bad)))
        if outd:
            fail += 1

    res = {"size": [w, h], "closed": closed, "pens": pens,
           "copper_outside": len(outside_cu),
           "min_copper_margin": worst_cu[0][0] if worst_cu else None,
           "min_drill_margin": worst_dr[0][0] if worst_dr else None,
           "failed_gates": fail}
    print()
    print("failed gates: %d" % fail)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("wrote %s" % out)
    return fail


_OUTLINE = """G04 outline*
%FSLAX26Y26*%
%MOMM*%
%ADD10C,0.200000*%
D10*
X0Y0D02*
X20000000Y0D01*
X20000000Y10000000D01*
X0Y10000000D01*
X0Y0D01*
M02*
"""

_COPPER = """G04 copper*
%FSLAX26Y26*%
%MOMM*%
%ADD10C,0.200000*%
%ADD11R,1.000000X1.000000*%
G04 Track Start*
D10*
X1000000Y1000000D02*
X19000000Y1000000D01*
G04 Track End*
G04 Pad Start*
D11*
X19800000Y9000000D03*
G04 Pad End*
M02*
"""


def _selftest():
    import tempfile
    ok = True
    print("outline_check selftest")
    tmp = tempfile.mkdtemp(prefix="pcbkit-")
    op = os.path.join(tmp, "o.GKO")
    cp = os.path.join(tmp, "c.GTL")
    open(op, "w").write(_OUTLINE)
    open(cp, "w").write(_COPPER)

    lay = GB.parse_gerber(_OUTLINE, "o")
    pts, closed, pens, bb = outline_of(lay)
    good = closed and abs(bb[2] - bb[0] - 20.0) < 1e-9 and abs(bb[3] - bb[1] - 10.0) < 1e-9
    print("  20 x 10 closed outline read                   : %s" % ("OK" if good else "FAIL"))
    ok = ok and good
    good = pens == [0.2]
    print("  pen diameter %s mm                          : %s"
          % (pens, "OK" if good else "FAIL"))
    ok = ok and good

    # the 1 mm pad centred at x=19.8 reaches x=20.3, i.e. 0.3 mm OUTSIDE
    m = margin_to_outline(20.3, 9.0, pts, bb, True)
    good = m < 0 and abs(m + 0.3) < 1e-9
    print("  a pad overhanging the edge reads %.4f mm     : %s"
          % (m, "OK - negative means outside" if good else "FAIL"))
    ok = ok and good

    n = run(op, size=(20.0, 10.0), edge=0.30, copper=[cp], tol=1e-4, top=3)
    good = n >= 1
    print("  run() fails the board (copper outside)        : %s (%d failed gates)"
          % ("OK" if good else "FAIL", n))
    ok = ok and good

    print("outline_check selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def _list_after(argv, flag):
    if flag not in argv:
        return []
    out = []
    for a in argv[argv.index(flag) + 1:]:
        if a.startswith("--"):
            break
        out.append(a)
    return out


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 2:
        print(__doc__)
        return 2
    size = None
    if "--size" in argv:
        size = tuple(float(v) for v in argv[argv.index("--size") + 1].split(","))
    edge = float(argv[argv.index("--edge") + 1]) if "--edge" in argv else 0.30
    tol = float(argv[argv.index("--tol") + 1]) if "--tol" in argv else 5e-4
    out = argv[argv.index("--json") + 1] if "--json" in argv else None
    n = run(argv[1], size=size, edge=edge, copper=_list_after(argv, "--copper"),
            drills=_list_after(argv, "--drills"), tol=tol, out=out)
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
