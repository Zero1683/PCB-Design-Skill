# -*- coding: utf-8 -*-
"""Placement gate: is this placement ROUTABLE?  Free-span and via-lane statistics.

WHAT THIS MEASURES
    A collision-free placement is not the acceptance criterion.  The reference project
    produced one that could not be routed, and the number that explained why was not a
    clearance -- it was the width of the corridors BETWEEN the courtyards.  This script
    measures those corridors against the board's own rules:

    1. FREE SPANS.  Scanning every `--step` mm across the board in both axes, the gaps
       between courtyards are collected.  A span is "via-capable" when it is at least
         via_pad + 2 * clearance
       wide -- computed from `rules`, never a hard-coded 0.70 mm.  Two boards with the
       same layout and different rules have different answers, and the whole point of
       the measurement is to notice that.
    2. TRACK LANES.  How many tracks of `--track-width` fit side by side in each span:
         lanes = floor((span - clearance) / (track_width + clearance))
       This is the number that explains a stalled autoroute.  On the reference board a
       0.55 mm channel held exactly ONE 0.254 mm track; dropping the signal width to
       0.10 mm made the same channel hold TWO, and the route completed.
    3. ESCAPE.  Every part needs at least one side offering a via-capable corridor, or
       its pads cannot get to another layer.  Parts with no such side are listed.

WHAT THIS CANNOT SEE
    * Anything about layers.  A span blocked on the top side may be wide open on an
      inner layer; this is a plan-view courtyard measurement and nothing else.  It tells
      you where a router will struggle, not that a route is impossible.
    * Copper that already exists.  Tracks, pours and vias are ignored -- this is a
      PLACEMENT tool, run before routing.  For the routed board use verify/clearance.py.
    * Diagonal corridors.  Spans are sampled along X and Y only.  A 45-degree channel is
      invisible to it and will be under-reported.
    * Board cutouts.  Like courtyard_check, the outline is used as a bounding box, so a
      span that runs through a milled slot is counted as free when it is not.

HOW IT WAS VALIDATED
    Ported from the placement checker of a released board, where the reported via-capable
    fraction and the "no escape side" list were the numbers that drove the placement
    revision that finally routed.  `--selftest` runs a synthetic two-part board whose
    corridor width is known analytically.

USAGE
    python3 channels.py board.json [--step 0.25] [--track-width 0.10] [--json out.json]
    python3 channels.py --selftest
"""
from __future__ import print_function

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boardmodel as BM                                               # noqa: E402


def via_lane_width(rules):
    """Copper-to-copper width a via needs: its pad plus a clearance on each side."""
    return rules["via_pad"] + 2.0 * rules["clearance"]


def lanes_in(span, track_width, clearance):
    """How many parallel tracks of `track_width` fit in a `span` mm corridor."""
    if span <= clearance:
        return 0
    return int(math.floor((span - clearance) / (track_width + clearance)))


def scan_axis(board, axis, step):
    """Free spans across the board.

    axis='x': spans run along X, sampled at every `step` of Y.  Returns
    [(width, sample_coord, from, to)].
    """
    x0, y0, x1, y1 = board.outline_bbox()
    boxes = [p.court for p in board.parts.values()]
    spans = []
    lo, hi = (y0, y1) if axis == "x" else (x0, x1)
    start, end = (x0, x1) if axis == "x" else (y0, y1)
    n = int((hi - lo) / step)
    for i in range(n + 1):
        v = lo + i * step
        blocked = []
        for b in boxes:
            if axis == "x":
                if b[1] <= v <= b[3]:
                    blocked.append((b[0], b[2]))
            else:
                if b[0] <= v <= b[2]:
                    blocked.append((b[1], b[3]))
        blocked.sort()
        cur = start
        for a, z in blocked:
            if a > cur:
                spans.append((a - cur, v, cur, a))
            cur = max(cur, z)
        if end > cur:
            spans.append((end - cur, v, cur, end))
    return spans


def escape_sides(board, probe=3.0):
    """{des: {'left': mm, 'right': mm, 'below': mm, 'above': mm}} of clear space."""
    x0, y0, x1, y1 = board.outline_bbox()
    items = [(d, p.court) for d, p in board.parts.items()]
    out = {}
    for d, b in items:
        room = {}
        for k in ("left", "right", "below", "above"):
            if k == "left":
                win = (b[0] - probe, b[1], b[0], b[3])
            elif k == "right":
                win = (b[2], b[1], b[2] + probe, b[3])
            elif k == "below":
                win = (b[0], b[1] - probe, b[2], b[1])
            else:
                win = (b[0], b[3], b[2], b[3] + probe)
            free = probe
            for e, ob in items:
                if e == d:
                    continue
                if not (ob[2] <= win[0] or ob[0] >= win[2] or
                        ob[3] <= win[1] or ob[1] >= win[3]):
                    if k == "left":
                        free = min(free, b[0] - ob[2])
                    elif k == "right":
                        free = min(free, ob[0] - b[2])
                    elif k == "below":
                        free = min(free, b[1] - ob[3])
                    else:
                        free = min(free, ob[1] - b[3])
            edge = {"left": b[0] - x0, "right": x1 - b[2],
                    "below": b[1] - y0, "above": y1 - b[3]}[k]
            room[k] = round(min(free, max(edge, 0.0)), 4)
        out[d] = room
    return out


def run(board, step=0.25, track_width=None, out=None, top=5):
    R = board.rules
    need = via_lane_width(R)
    tw = R["clearance"] if track_width is None else track_width
    res = {"via_lane_width": need, "clearance": R["clearance"],
           "via_pad": R["via_pad"], "track_width": tw, "step": step}

    print("=" * 74)
    print("ROUTING CHANNELS   (measured against THIS board's rules, not a constant)")
    print("=" * 74)
    print("clearance rule         : %.4f mm" % R["clearance"])
    print("via pad                : %.4f mm" % R["via_pad"])
    print("=> a via needs         : %.4f mm of clear corridor" % need)
    print("track width assumed    : %.4f mm" % tw)
    print()

    for axis, label in (("x", "horizontal corridors (sampling every %.2f mm of y)" % step),
                        ("y", "vertical corridors (sampling every %.2f mm of x)" % step)):
        sp = scan_axis(board, axis, step)
        wide = [s for s in sp if s[0] >= need]
        pct = 100.0 * len(wide) / max(len(sp), 1)
        # lanes are bucketed 0..7 plus ">=8": beyond that the corridor is open board
        # and the exact count is noise, not information.
        lane_hist = {}
        for w, _v, _a, _b in sp:
            k = lanes_in(w, tw, R["clearance"])
            key = k if k < 8 else ">=8"
            lane_hist[key] = lane_hist.get(key, 0) + 1
        print("  %s" % label)
        print("    free spans sampled    : %d" % len(sp))
        print("    via-capable (>= %.3f) : %d (%.0f %%)" % (need, len(wide), pct))
        print("    dead ends (< %.3f mm) : %d" % (need, len(sp) - len(wide)))
        ordered = [(k, lane_hist[k]) for k in range(8) if k in lane_hist]
        if ">=8" in lane_hist:
            ordered.append((">=8", lane_hist[">=8"]))
        print("    track lanes per span  : %s"
              % ", ".join("%s:%d" % kv for kv in ordered))
        widest = sorted(sp, key=lambda s: -s[0])[:top]
        print("    widest %d              : %s" % (top,
              [(round(w, 3), "%s=%.2f" % ("y" if axis == "x" else "x", v))
               for w, v, _a, _b in widest]))
        res[axis] = {"spans": len(sp), "via_capable": len(wide),
                     "via_capable_pct": round(pct, 2), "lane_histogram": lane_hist,
                     "widest": round(widest[0][0], 4) if widest else None}
        print()

    print("=" * 74)
    print("ESCAPE   (every part needs one side offering %.3f mm)" % need)
    print("=" * 74)
    room = escape_sides(board)
    stuck = sorted((d, r) for d, r in room.items() if max(r.values()) < need)
    print("parts with NO via-capable side: %d" % len(stuck))
    for d, r in stuck[:20]:
        print("   %-10s %s" % (d, r))
    res["no_escape"] = [d for d, _r in stuck]

    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("wrote %s" % out)
    return len(stuck)


def _selftest():
    ok = True
    print("channels selftest")
    doc = BM.synthetic_board()
    # two 1.6 x 0.8 courtyards with a corridor of exactly 1.0 mm between them
    doc["components"] = [
        {"des": "A", "footprint": "R0603", "x": 5.0, "y": 15.0, "angle": 0},
        {"des": "B", "footprint": "R0603", "x": 5.0 + 1.1 + 1.0 + 1.1, "y": 15.0,
         "angle": 0},
    ]
    doc["pad_nets"] = {}
    doc["nets"] = {}
    doc["vias"] = []
    doc["tracks"] = []
    b = BM.Board(doc)
    need = via_lane_width(b.rules)
    good = abs(need - (0.50 + 2 * 0.102)) < 1e-9
    print("  via lane width from rules                     : %.4f mm  %s"
          % (need, "OK" if good else "FAIL"))
    ok &= good

    sp = scan_axis(b, "x", 0.25)
    mid = [s for s in sp if abs(s[1] - 15.0) < 1e-9]
    inner = [s for s in mid if s[2] > 6.0 and s[3] < 8.5]
    good = inner and abs(inner[0][0] - 1.0) < 1e-6
    print("  corridor between two parts                    : %.4f mm  %s"
          % (inner[0][0] if inner else float("nan"), "OK" if good else "FAIL"))
    ok &= bool(good)

    # 1.0 mm span, 0.102 clearance, 0.10 track -> floor((1.0-0.102)/0.202) = 4 lanes
    n = lanes_in(1.0, 0.10, 0.102)
    good = n == 4
    print("  lanes of 0.10 mm track in 1.0 mm              : %d  %s"
          % (n, "OK" if good else "FAIL (want 4)"))
    ok &= good
    # the reference project's own case: 0.55 mm channel
    n1 = lanes_in(0.55, 0.254, 0.102)
    n2 = lanes_in(0.55, 0.10, 0.102)
    good = n1 == 1 and n2 == 2
    print("  0.55 mm channel: 0.254 mm track -> %d lane(s), 0.10 mm -> %d  %s"
          % (n1, n2, "OK - reproduces the measured case" if good else "FAIL"))
    ok &= good

    room = escape_sides(b)
    good = max(room["A"].values()) >= need
    print("  A has a via-capable escape side               : %s" % ("OK" if good else "FAIL"))
    ok &= good
    print("channels selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 2:
        print(__doc__)
        return 2
    step = float(argv[argv.index("--step") + 1]) if "--step" in argv else 0.25
    twv = (float(argv[argv.index("--track-width") + 1])
           if "--track-width" in argv else None)
    out = argv[argv.index("--json") + 1] if "--json" in argv else None
    board = BM.load(argv[1])
    return 1 if run(board, step=step, track_width=twv, out=out) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
