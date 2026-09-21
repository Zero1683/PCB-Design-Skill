# -*- coding: utf-8 -*-
"""Placement gate: no part may lie under, or inside, any other part's body.

WHAT THIS MEASURES
    Exact polygon-to-polygon clearance between the BODY of every component and the body
    of every other component, in board millimetres.  0.000 means the two bodies overlap,
    i.e. one part is under (or inside) the other.  A "body" is the footprint's assembly
    outline where it has one, else its silkscreen, else its pad bounding box -- what
    physically occupies the space, as distinct from the courtyard, which is the union
    that includes the pads.

WHAT THIS CANNOT SEE
    * Height.  Two bodies that overlap in plan may be perfectly fine if one is a 0.1 mm
      pad-level marking and the other is 5 mm up -- and two bodies that clear in plan can
      still collide if one overhangs its own outline.  A footprint's courtyard IS NOT THE
      PART: on the reference board a barrel jack's layer-48 courtyard stopped at x 38.350
      while its moulded body reached x 41.400, a 3.05 mm overhang in which three passives
      were legally placed.  The gate that sees THAT is verify/mesh3d.py, working on the
      real 3D export.  Run both.
    * Concave bodies.  The EasyEDA adapter reduces a multi-primitive assembly outline to
      its bounding box (see import_easyeda._ring).  For containment that is conservative
      -- it can report a false overlap, never a false clearance -- but an L-shaped part
      will report gaps that are pessimistic.
    * Intentional stacking.  A part legitimately mounted on top of another (a shield, a
      socketed module) reports 0.000 here and always will.  Put it in --allow.

FAULT FIXED HERE (fault 3 of 4 -- "a placement gate that only tested large module bodies")
    The original gate collected "module bodies" as those with area >= 20 mm2 and tested
    other parts only against those.  A 0603 was therefore legally placed UNDERNEATH a
    3.5 x 2.8 mm tantalum, whose body is 9.8 mm2: the tantalum is not a module, so
    nothing was looking.  This version has NO size filter.  Every part is tested against
    every other part, which on a 180-part board is 16 110 pairs and still runs in
    seconds because of the bounding-box pre-filter.  `--min-area` exists ONLY to
    reproduce the old, broken behaviour for comparison, and says so when used.

    The measurement itself also depends on fault 2's fix: an edge-to-edge distance
    function cannot see a small part lying wholly inside a big one, which is precisely
    the case this gate exists to catch.  geom2d.poly_distance tests containment first.

HOW IT WAS VALIDATED
    Ported from the gate that found a real FATAL on the reference board -- an 0805
    capacitor lying entirely inside a cantilevered module's body, nearest-pad-to-body
    distance 0.000 mm, which would have prevented the module's 11 solder joints from
    forming -- and which read 0 violations over 1611 pairs once the board was fixed.
    `--selftest` runs the synthetic board, where C1 is under a module and C2 is under a
    9-mm2-class part that the old size filter would have skipped.

USAGE
    python3 body_clearance.py board.json [--near 3.0] [--top 20] [--json out.json]
                              [--allow "U1:SHIELD1,J2:J3"] [--min-area 0]
    python3 body_clearance.py --selftest
"""
from __future__ import print_function

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom2d as G                                                    # noqa: E402
import boardmodel as BM                                               # noqa: E402


def parse_allow(spec):
    """"A:B,C:D" -> {frozenset({'A','B'}), frozenset({'C','D'})}"""
    out = set()
    for item in (spec or "").split(","):
        item = item.strip()
        if not item:
            continue
        if ":" not in item:
            raise SystemExit("--allow entries look like DES1:DES2, got %r" % item)
        a, b = item.split(":", 1)
        out.add(frozenset((a.strip(), b.strip())))
    return out


def measure(board, near=3.0, min_area=0.0, allow=()):
    """[(gap, desA, desB)] for every pair whose bodies come within `near` mm.

    `near` only limits which pairs are MEASURED, not which are reported as violations:
    a pair further apart than `near` cannot overlap, so skipping it is exact, not a
    heuristic.  Raise it only if you also want the near-miss ranking to go further out.
    """
    bodies = board.bodies(min_area=min_area)
    boxes = {d: G.bbox_of(poly) for d, poly, _a in bodies}
    rows, viol = [], []
    for i in range(len(bodies)):
        d1, p1, _a1 = bodies[i]
        for j in range(i + 1, len(bodies)):
            d2, p2, _a2 = bodies[j]
            if frozenset((d1, d2)) in allow:
                continue
            if not G.boxes_overlap(boxes[d1], boxes[d2], near):
                continue
            g = G.poly_distance(p1, p2)
            rows.append((g, d1, d2))
            if g <= 0.0:
                viol.append((g, d1, d2))
    rows.sort(key=lambda t: t[0])
    viol.sort(key=lambda t: t[0])
    return rows, viol, len(bodies)


def run(board, near=3.0, top=20, min_area=0.0, allow=(), out=None):
    rows, viol, nbodies = measure(board, near=near, min_area=min_area, allow=allow)
    print("=" * 74)
    print("BODY-TO-BODY CLEARANCE   (every part against every part, no size filter)")
    print("=" * 74)
    if min_area > 0.0:
        print("!! --min-area %.1f mm2 is set.  This REPRODUCES THE ORIGINAL FAULT: parts"
              % min_area)
        print("!! smaller than that are not treated as bodies, which is how a 0603 was")
        print("!! legally placed under a 9.8 mm2 tantalum.  Use it only for comparison.")
    print("bodies considered      : %d" % nbodies)
    print("pairs measured (<= %.1f mm apart): %d" % (near, len(rows)))
    print("body sources           : %s"
          % BM._count([p.court_source for p in board.parts.values()]))
    print()
    print("tightest %d pairs:" % top)
    for g, d1, d2 in rows[:top]:
        flag = "   ** ONE PART IS UNDER THE OTHER **" if g <= 0.0 else ""
        print("   %8.3f mm  %-10s %-10s%s" % (g, d1, d2, flag))
    print()
    print("VIOLATIONS (overlapping bodies): %d" % len(viol))
    for g, d1, d2 in viol:
        a = board.parts[d1]
        c = board.parts[d2]
        aa = G.poly_area(a.body)
        cc = G.poly_area(c.body)
        under = d1 if aa < cc else d2
        over = d2 if aa < cc else d1
        print("   %-10s (%.2f mm2) is under %-10s (%.2f mm2)"
              % (under, min(aa, cc), over, max(aa, cc)))
    res = {"bodies": nbodies, "pairs": len(rows), "violations": len(viol),
           "tightest": [[round(g, 4), a, c] for g, a, c in rows[:top]],
           "overlaps": [[a, c] for _g, a, c in viol]}
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("wrote %s" % out)
    return len(viol)


def _selftest():
    b = BM.Board(BM.synthetic_board())
    ok = True
    print("body_clearance selftest (synthetic board)")
    rows, viol, n = measure(b)
    pairs = {frozenset(v[1:]) for v in viol}
    good = frozenset(("MOD1", "C1")) in pairs
    print("  C1 under the 36 mm2 module found              : %s" % ("OK" if good else "FAIL"))
    ok &= good
    good = frozenset(("R1", "C2")) in pairs
    print("  C2 under the 1.28 mm2 R1 found (fault 3)      : %s" % ("OK" if good else "FAIL"))
    ok &= good

    # reproduce the fault: with the old >= 20 mm2 filter, R1/C2 disappears
    _r, viol20, _n = measure(b, min_area=20.0)
    pairs20 = {frozenset(v[1:]) for v in viol20}
    good = frozenset(("R1", "C2")) not in pairs20 and frozenset(("MOD1", "C1")) not in pairs20
    print("  ...and the old >= 20 mm2 filter misses BOTH   : %s (%d violations vs %d)"
          % ("OK - the fault reproduces" if good else "FAIL", len(viol20), len(viol)))
    ok &= good

    allow = parse_allow("MOD1:C1")
    _r, viol_a, _n = measure(b, allow=allow)
    good = frozenset(("MOD1", "C1")) not in {frozenset(v[1:]) for v in viol_a}
    print("  --allow suppresses a declared stack           : %s" % ("OK" if good else "FAIL"))
    ok &= good
    print("body_clearance selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 2:
        print(__doc__)
        return 2

    def opt(name, default, cast=float):
        return cast(argv[argv.index(name) + 1]) if name in argv else default

    board = BM.load(argv[1])
    n = run(board,
            near=opt("--near", 3.0),
            top=opt("--top", 20, int),
            min_area=opt("--min-area", 0.0),
            allow=parse_allow(argv[argv.index("--allow") + 1] if "--allow" in argv else ""),
            out=argv[argv.index("--json") + 1] if "--json" in argv else None)
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
