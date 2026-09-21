# -*- coding: utf-8 -*-
"""Placement gate: courtyard separation, pad-to-outline, and hole-to-hole.

WHAT THIS MEASURES
    1. COURTYARD SEPARATION.  Edge-to-edge gap between every pair of placed courtyards,
       where a courtyard is union(assembly outline, real pad boxes, hole boxes) -- see
       boardmodel.  Reported as a histogram plus the tightest pairs, and failed when a
       pair is closer than `rules.min_courtyard_gap` (0 = must not overlap).
    2. PAD AND DRILL TO BOARD OUTLINE.  Closest approach of every pad polygon and every
       drilled feature to the outline bounding box, against `rules.pad_to_outline` and
       `rules.edge_clearance`.
    3. HOLE-TO-HOLE, NET-BLIND.  Edge-to-edge distance between every pair of drilled
       features -- pad holes, NPTH, and VIAS -- against `rules.hole_to_hole`.

    Numbers first, verdict second.  A collision-free placement is not by itself an
    acceptance criterion: the reference project produced one that could not be routed.
    Read the histogram, not just the PASS line.

WHAT THIS CANNOT SEE
    * Height.  Two courtyards can be 2 mm apart and still collide in 3D if one part
      overhangs (verify/mesh3d.py) or if one sits over the other (body_clearance.py).
    * Copper.  Tracks and pours are not placement objects; use verify/clearance.py.
    * A non-rectangular board.  The outline test uses the outline's BOUNDING BOX, so a
      board with a cutout or a rounded corner is checked against a box that is larger
      than the real board -- optimistic exactly where a routed corner is tightest.
      This is the one place in the toolkit where a limitation is optimistic rather than
      conservative; treat a marginal edge result as unproven and measure it in the EDA.
    * Whether the courtyard the library drew is the courtyard the assembler needs.
      IPC courtyard excess is a library decision this tool inherits.

FAULT ENCODED HERE (part of fault 3's family)
    The copper clearance sweep deliberately skips SAME-NET pairs, which is correct for
    copper and WRONG for holes: the mechanical rule applies to any two holes whatever
    their net.  On the reference board three vias the router stacked on one node (two
    0.02 mm apart, two coincident) passed the same-net-skipping sweep and then failed
    the EDA's real DRC.  `hole_to_hole` below never looks at a net.

HOW IT WAS VALIDATED
    The hole-to-hole gate is a port of the checker that reproduced an EDA DRC's three
    findings exactly, and read 0 on the release baseline.  `--selftest` runs the
    synthetic board from boardmodel, which carries a deliberate 0.05 mm same-net via
    pair that this gate must catch.

USAGE
    python3 courtyard_check.py board.json [--json out.json] [--top N]
    python3 courtyard_check.py --selftest
"""
from __future__ import print_function

import itertools
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom2d as G                                                    # noqa: E402
import boardmodel as BM                                               # noqa: E402


def courtyard_pairs(board):
    """[(gap_mm, desA, desB)] for every pair, closest first."""
    items = sorted((d, p.court) for d, p in board.parts.items())
    out = []
    for i in range(len(items)):
        d1, b1 = items[i]
        for j in range(i + 1, len(items)):
            d2, b2 = items[j]
            out.append((G.rect_gap(b1, b2), d1, d2))
    out.sort(key=lambda t: t[0])
    return out


def pad_to_outline(board):
    """[(margin_mm, des, pad)] -- smallest distance from a pad edge to the outline box."""
    x0, y0, x1, y1 = board.outline_bbox()
    out = []
    for rec in board.all_pads():
        b = rec["bbox"]
        m = min(b[0] - x0, b[1] - y0, x1 - b[2], y1 - b[3])
        out.append((m, rec["des"], rec["num"]))
    out.sort(key=lambda t: t[0])
    return out


def hole_to_outline(board):
    x0, y0, x1, y1 = board.outline_bbox()
    out = []
    for h in board.all_holes():
        r = h["d"] / 2.0 + h["slot_len"] / 2.0
        m = min(h["x"] - r - x0, h["y"] - r - y0, x1 - (h["x"] + r), y1 - (h["y"] + r))
        out.append((m, h["des"] or h["kind"], h["num"]))
    out.sort(key=lambda t: t[0])
    return out


def hole_to_hole(board, rule=None):
    """Net-blind hole-to-hole violations, closest first.

    A slot is modelled as a capsule: the distance is measured between the two hole
    outlines, so a 1.7 mm slot is not treated as a 1.7 mm round hole.
    """
    rule = board.rules["hole_to_hole"] if rule is None else rule
    holes = list(board.all_holes())
    bad = []
    for a, c in itertools.combinations(holes, 2):
        d = _hole_gap(a, c)
        if d < rule - 1e-9:
            bad.append((d, a, c))
    bad.sort(key=lambda t: t[0])
    return bad, len(holes)


def _hole_gap(a, c):
    if a["slot_len"] <= 0.0 and c["slot_len"] <= 0.0:
        return math.hypot(a["x"] - c["x"], a["y"] - c["y"]) - a["d"] / 2.0 - c["d"] / 2.0
    pa = _hole_core(a)
    pc = _hole_core(c)
    return G.poly_distance(pa, pc) - a["d"] / 2.0 - c["d"] / 2.0


def _hole_core(h):
    """The slot's centre segment; a round hole is a degenerate one-point core."""
    L = h["slot_len"]
    if L <= 0.0:
        return [(h["x"], h["y"])]
    return [(h["x"] - L / 2.0, h["y"]), (h["x"] + L / 2.0, h["y"])]


# --------------------------------------------------------------------------- report

def run(board, top=10, out=None):
    failures = 0
    R = board.rules
    res = {}

    print("=" * 74)
    print("COURTYARD SEPARATION   (courtyard = union of outline, pads and holes)")
    print("=" * 74)
    pairs = courtyard_pairs(board)
    overlaps = [p for p in pairs if p[0] < 0]
    hist = {}
    bands = [(-1e9, 0.0, "<0 OVERLAP"), (0.0, 0.30, "0.00-0.30"),
             (0.30, 0.50, "0.30-0.50"), (0.50, 0.70, "0.50-0.70"),
             (0.70, 1.00, "0.70-1.00"), (1.00, 2.00, "1.00-2.00"),
             (2.00, 1e9, ">2.00")]
    for g, _a, _b in pairs:
        for lo, hi, name in bands:
            if lo <= g < hi:
                hist[name] = hist.get(name, 0) + 1
                break
    print("component pairs        : %d" % len(pairs))
    print("courtyard OVERLAPS     : %d" % len(overlaps))
    for _lo, _hi, name in bands:
        print("  gap %-14s %6d" % (name, hist.get(name, 0)))
    print("tightest %d pairs:" % top)
    for g, d1, d2 in pairs[:top]:
        print("   %8.3f mm  %-10s %-10s" % (g, d1, d2))
    lim = R["min_courtyard_gap"]
    bad = [p for p in pairs if p[0] < lim - 1e-9]
    print("pairs closer than the %.3f mm minimum: %d" % (lim, len(bad)))
    if bad:
        failures += 1
    res["courtyard"] = {"pairs": len(pairs), "overlaps": len(overlaps),
                        "histogram": hist, "min_gap": pairs[0][0] if pairs else None,
                        "violations": len(bad)}

    print()
    print("=" * 74)
    print("PAD / DRILL TO BOARD OUTLINE")
    print("=" * 74)
    ob = board.outline_bbox()
    print("outline bbox           : %.3f %.3f %.3f %.3f  (%.3f x %.3f mm)"
          % (ob[0], ob[1], ob[2], ob[3], ob[2] - ob[0], ob[3] - ob[1]))
    pm = pad_to_outline(board)
    print("closest %d pads (need >= %.3f mm):" % (top, R["pad_to_outline"]))
    for m, des, num in pm[:top]:
        print("   %8.3f mm  %-10s pad %s" % (m, des, num))
    badp = [x for x in pm if x[0] < R["pad_to_outline"] - 1e-9]
    print("pads inside the margin : %d" % len(badp))
    if badp:
        failures += 1
    hm = hole_to_outline(board)
    if hm:
        print("closest drill          : %.3f mm (%s), need >= %.3f mm"
              % (hm[0][0], hm[0][1], R["edge_clearance"]))
        badh = [x for x in hm if x[0] < R["edge_clearance"] - 1e-9]
        print("drills inside the margin: %d" % len(badh))
        if badh:
            failures += 1
    else:
        badh = []
    res["outline"] = {"bbox": ob, "min_pad_margin": pm[0][0] if pm else None,
                      "pad_violations": len(badp),
                      "min_drill_margin": hm[0][0] if hm else None,
                      "drill_violations": len(badh)}

    print()
    print("=" * 74)
    print("HOLE TO HOLE  (NET-BLIND -- same net counts, see the module docstring)")
    print("=" * 74)
    viol, nholes = hole_to_hole(board)
    print("drilled features       : %d" % nholes)
    print("rule                   : %.4f mm between ANY two hole edges" % R["hole_to_hole"])
    print("violations             : %d" % len(viol))
    for d, a, c in viol[:top]:
        print("   %8.4f mm  %-4s %-10s (%s) at (%.3f, %.3f)  ~  %-4s %-10s (%s) at (%.3f, %.3f)"
              % (d, a["kind"], a["des"] or "-", a["net"] or "-", a["x"], a["y"],
                 c["kind"], c["des"] or "-", c["net"] or "-", c["x"], c["y"]))
    if viol:
        failures += 1
    res["hole_to_hole"] = {"holes": nholes, "rule": R["hole_to_hole"],
                           "violations": len(viol),
                           "worst": round(viol[0][0], 5) if viol else None}

    print()
    print("failed gate groups: %d" % failures)
    res["failed_groups"] = failures
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("wrote %s" % out)
    return failures


def _selftest():
    b = BM.Board(BM.synthetic_board())
    print("courtyard_check selftest (synthetic board)")
    ok = True
    pairs = courtyard_pairs(b)
    ov = [p for p in pairs if p[0] < 0]
    good = any(set(p[1:]) == {"MOD1", "C1"} for p in ov)
    print("  MOD1/C1 courtyard overlap detected            : %s" % ("OK" if good else "FAIL"))
    ok &= good
    viol, n = hole_to_hole(b)
    good = len(viol) == 1 and abs(viol[0][0] - (0.05 - 0.3)) < 1e-9
    print("  same-net via pair 0.05 mm apart flagged       : %s (%d of %d holes, gap %.4f)"
          % ("OK" if good else "FAIL", len(viol), n, viol[0][0] if viol else float("nan")))
    ok &= good
    # and it must NOT be caught by a net-aware sweep -- prove the fault is real
    same_net = viol and viol[0][1]["net"] == viol[0][2]["net"]
    print("  ...and both holes are on the SAME net         : %s"
          % ("OK - a net-aware sweep would miss it" if same_net else "FAIL"))
    ok &= bool(same_net)
    pm = pad_to_outline(b)
    print("  closest pad to outline                        : %.3f mm (%s pad %s)"
          % (pm[0][0], pm[0][1], pm[0][2]))
    print("courtyard_check selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 2:
        print(__doc__)
        return 2
    out = None
    top = 10
    if "--json" in argv:
        out = argv[argv.index("--json") + 1]
    if "--top" in argv:
        top = int(argv[argv.index("--top") + 1])
    board = BM.load(argv[1])
    return 1 if run(board, top=top, out=out) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
