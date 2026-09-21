# -*- coding: utf-8 -*-
"""Acceptance check for a routed board.  Progress metric: ISLANDS MERGED.

RUN THIS ON THE FILE THE EDA HANDS BACK, never on the file you pushed.
A tool reporting success is not evidence.  Every number below is measured off the
document the EDA actually holds after the import.

WHAT THIS MEASURES
    1. ISLANDS.  For each net, its copper objects -- pads, track segments, vias -- are
       grouped by whether their true outlines TOUCH on a shared layer.  A fully routed
       net is one island.  The headline numbers are:
           islands  = sum over nets of that net's island count
           merges   = sum over nets of (islands - 1)   <-- the work still to do
       MERGES OUTSTANDING is the progress metric, not "percent routed" and not "unrouted
       connections".  It is monotone, it is comparable between runs, and it goes to zero
       exactly when the board is connected.  With `--baseline` the delta against a
       previous board state is printed, which is how two candidate routes get compared
       on the same ruler.
    2. PROTECTED NETS.  Nets you told the router not to touch must still be one island.
       A router that "improved" a tuned differential pair has broken it.
    3. SOLID PLANES UNCUT.  Zero routed segments on any declared plane layer.
    4. DIFFERENT-NET CLEARANCE at the board's own rule, exact, outline to outline.
    5. EXPECTED-OPEN NETS.  Nets deliberately withheld from the router (poured nets,
       hand-routed rails) are reported separately instead of counting as failures --
       but they are LISTED every time, so "we meant to do that" stays a decision
       somebody made rather than a silence.

WHAT THIS CANNOT SEE
    * POUR COPPER.  This walks pads, tracks and vias only.  A net that is closed by a
      pour will keep reporting islands here forever, and that is the WRONG RULER for it.
      Declare such nets with `--plane-nets`: each island holding a via or a through-hole
      pad is then treated as reaching the plane.  For the real answer on a poured net,
      measure the manufactured artwork -- verify/clearance.py and the Gerber raster.
    * The schematic.  A net that is one island can still be the WRONG net.  That is
      verify/pad_reconcile.py and verify/netlist_assert.py.
    * Manufacturing.  Copper this says is fine can still be un-fabricable; the Gerber
      is the artefact that gets built, and verify/ measures that.
    * Anything about the router's internal state.  If a run stalls, that is
      route_supervise.py.

HOW IT WAS VALIDATED
    Ported from the acceptance checker of a released 4-layer board, where the
    islands-merged number is what selected between competing autorouter sessions and
    where the plane-uncut and protected-net gates each caught a real regression.
    `--selftest` runs a synthetic board with a deliberately split net.

USAGE
    python3 route_accept.py board.json [--baseline old.json]
                            [--protected "MIPI_D0P,MIPI_D0N"]
                            [--plane-nets "GND,AGND"]
                            [--expect-open "VBUS"]
                            [--clearance 0.102] [--top 12] [--json out.json]
    python3 route_accept.py --selftest
"""
from __future__ import print_function

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_PLACEMENT = os.path.join(_HERE, os.pardir, "placement")
if not os.path.isdir(_PLACEMENT):
    raise SystemExit("routing/ expects its sibling placement/ directory (for the board "
                     "model and geometry).  Keep scripts/ together, or set PYTHONPATH.")
sys.path.insert(0, _PLACEMENT)
import geom2d as G                                                    # noqa: E402
import boardmodel as BM                                               # noqa: E402


class Node(object):
    __slots__ = ("pts", "r", "layers", "kind", "label", "bb")

    def __init__(self, pts, r, layers, kind, label):
        self.pts, self.r, self.kind, self.label = pts, r, kind, label
        self.layers = tuple(layers)
        bb = G.bbox_of(pts)
        self.bb = (bb[0] - r, bb[1] - r, bb[2] + r, bb[3] + r)


def net_nodes(board, net):
    out = []
    for t in board.tracks:
        if t.get("net") == net:
            out.append(Node([(t["x1"], t["y1"]), (t["x2"], t["y2"])],
                            t["w"] / 2.0, (t["layer"],), "track", "T"))
    cu = tuple(board.layers["copper"])
    for v in board.vias:
        if v.get("net") == net:
            out.append(Node([(v["x"], v["y"])],
                            float(v.get("pad") or board.rules["via_pad"]) / 2.0,
                            cu, "via", "V"))
    for rec in board.all_pads():
        if rec["net"] == net:
            out.append(Node(rec["poly"], 0.0, rec["layers"], "pad",
                            "%s.%s" % (rec["des"], rec["num"])))
    return out


def islands_of(board, net, plane=False, tol=1e-6):
    """-> list of islands, each a list of Nodes."""
    ns = net_nodes(board, net)
    par = list(range(len(ns)))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    def union(a, c):
        ra, rc = find(a), find(c)
        if ra != rc:
            par[ra] = rc

    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            A, B = ns[i], ns[j]
            if not (set(A.layers) & set(B.layers)):
                continue
            if not G.boxes_overlap(A.bb, B.bb):
                continue
            if G.poly_distance(A.pts, B.pts) - A.r - B.r <= tol:
                union(i, j)
    if plane:
        # A declared plane net is closed by copper this model cannot see.  Any island
        # that carries a via or a through-hole pad reaches the plane, so they are all
        # the same island.  Islands with NEITHER are still reported separately -- those
        # are the ones that genuinely have no way down.
        anchor = None
        cu = set(board.layers["copper"])
        for i, nd in enumerate(ns):
            if nd.kind == "via" or len(set(nd.layers) & cu) > 1:
                if anchor is None:
                    anchor = i
                else:
                    union(i, anchor)
    groups = {}
    for i in range(len(ns)):
        groups.setdefault(find(i), []).append(ns[i])
    return list(groups.values())


def connectivity(board, plane_nets=()):
    """{net: (islands, pads, has_track)} over every net that owns copper."""
    plane_nets = set(plane_nets)
    nets = {r["net"] for r in board.all_pads() if r["net"]}
    nets |= {t.get("net") for t in board.tracks if t.get("net")}
    nets |= {v.get("net") for v in board.vias if v.get("net")}
    out = {}
    for net in sorted(nets):
        g = islands_of(board, net, plane=(net in plane_nets))
        npads = sum(1 for x in g for n in x if n.kind == "pad")
        ntr = sum(1 for x in g for n in x if n.kind == "track")
        out[net] = (len(g), npads, ntr)
    return out


def clearance_violations(board, limit=None, report=12):
    """Exact different-net clearance over pads, tracks and vias.  Pours excluded --
    see the module docstring and verify/clearance.py."""
    limit = board.rules["clearance"] if limit is None else limit
    objs = []
    cu = tuple(board.layers["copper"])
    for t in board.tracks:
        objs.append((Node([(t["x1"], t["y1"]), (t["x2"], t["y2"])], t["w"] / 2.0,
                          (t["layer"],), "track", "T:%s" % t.get("net", "")),
                     t.get("net", "")))
    for v in board.vias:
        objs.append((Node([(v["x"], v["y"])],
                          float(v.get("pad") or board.rules["via_pad"]) / 2.0, cu,
                          "via", "V:%s" % v.get("net", "")), v.get("net", "")))
    for rec in board.all_pads():
        objs.append((Node(rec["poly"], 0.0, rec["layers"], "pad",
                          "P:%s.%s" % (rec["des"], rec["num"])), rec["net"]))
    CELL = 2.0
    buckets = {}
    for k, (o, _n) in enumerate(objs):
        for gx in range(int((o.bb[0] - limit) // CELL), int((o.bb[2] + limit) // CELL) + 1):
            for gy in range(int((o.bb[1] - limit) // CELL), int((o.bb[3] + limit) // CELL) + 1):
                buckets.setdefault((gx, gy), []).append(k)
    seen = set()
    worst, viol = [], []
    for lst in buckets.values():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                i, j = sorted((lst[a], lst[b]))
                if (i, j) in seen:
                    continue
                seen.add((i, j))
                A, na = objs[i]
                B, nb = objs[j]
                if na and na == nb:
                    continue
                if not (set(A.layers) & set(B.layers)):
                    continue
                if not G.boxes_overlap(A.bb, B.bb, limit):
                    continue
                d = G.poly_distance(A.pts, B.pts) - A.r - B.r
                row = (d, A.label, B.label, tuple(sorted(set(A.layers) & set(B.layers))))
                worst.append(row)
                if d < limit - 1e-9:
                    viol.append(row)
    worst.sort(key=lambda t: t[0])
    viol.sort(key=lambda t: t[0])
    return viol, worst[:report], len(seen)


def run(board, baseline=None, protected=(), plane_nets=(), expect_open=(),
        limit=None, top=12, out=None):
    fail = 0
    rep = connectivity(board, plane_nets)
    expect_open = set(expect_open)
    split = {n: v for n, v in rep.items() if v[0] > 1 and n not in expect_open}
    islands = sum(v[0] for v in rep.values())
    merges = sum(v[0] - 1 for n, v in rep.items() if n not in expect_open)

    print("=" * 74)
    print("ROUTE ACCEPTANCE   %s" % board.source)
    print("=" * 74)
    print("tracks %-6d vias %-5d netted pads %-5d components %-4d"
          % (len(board.tracks), len(board.vias),
             sum(1 for r in board.all_pads() if r["net"]), len(board.parts)))
    print("nets with copper %-5d  fully connected %-5d  split %-5d"
          % (len(rep), len(rep) - len(split) - len(expect_open & set(rep)), len(split)))
    print("ISLANDS %-6d  MERGES OUTSTANDING %-6d   <-- the progress metric"
          % (islands, merges))

    if baseline is not None:
        brep = connectivity(baseline, plane_nets)
        bm = sum(v[0] - 1 for n, v in brep.items() if n not in expect_open)
        bc = len(brep) - len([1 for n, v in brep.items()
                              if v[0] > 1 and n not in expect_open]) - len(expect_open & set(brep))
        cc = len(rep) - len(split) - len(expect_open & set(rep))
        print("baseline %s -> connected %d, merges %d" % (baseline.source, bc, bm))
        print("DELTA    connected %+d   merges %+d   (negative merges = progress)"
              % (cc - bc, merges - bm))

    print("-" * 74)
    bad = [n for n in protected if rep.get(n, (99, 0, 0))[0] != 1]
    print("GATE protected nets still one island        : %s"
          % ("PASS (%d nets)" % len(protected) if not bad else "FAIL %s" % bad))
    fail += 1 if bad else 0

    planes = [l for l in board.layers.get("solid_planes", [])]
    on_plane = [t for t in board.tracks if t.get("layer") in planes]
    print("GATE solid planes uncut %-19s: %s"
          % (str(planes), "PASS" if not on_plane else
             "FAIL (%d routed segments on a plane)" % len(on_plane)))
    fail += 1 if on_plane else 0

    lim = board.rules["clearance"] if limit is None else limit
    viol, worst, npairs = clearance_violations(board, lim, report=top)
    print("GATE different-net clearance >= %.4f mm   : %s (%d pairs examined)"
          % (lim, "PASS" if not viol else "FAIL (%d violations)" % len(viol), npairs))
    for v in viol[:top]:
        print("        %8.4f  %-24s %-24s layers %s" % v)
    fail += 1 if viol else 0
    if worst:
        print("     tightest legal pairs:")
        for v in worst[:min(top, 5)]:
            print("        %8.4f  %-24s %-24s layers %s" % v)

    print("GATE merges outstanding == 0                : %s"
          % ("PASS" if merges == 0 else "FAIL (%d)" % merges))
    fail += 1 if merges else 0

    if expect_open:
        print("-" * 74)
        print("DECLARED OPEN (not counted as failures -- somebody chose this):")
        for n in sorted(expect_open):
            v = rep.get(n)
            print("   %-18s %s" % (n, "islands=%d pads=%d" % (v[0], v[1]) if v
                                   else "not present on the board"))

    if split:
        print("-" * 74)
        print("worst remaining nets:")
        for n, v in sorted(split.items(), key=lambda kv: -kv[1][0])[:top]:
            print("   SPLIT %-18s islands=%-4d pads=%-4d tracks=%d" % (n, v[0], v[1], v[2]))

    print("-" * 74)
    print("failed gates: %d" % fail)
    res = {"islands": islands, "merges": merges, "nets": len(rep),
           "split": {n: v[0] for n, v in split.items()},
           "clearance_violations": len(viol), "plane_segments": len(on_plane),
           "protected_broken": bad, "failed_gates": fail}
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("wrote %s" % out)
    return fail


def _selftest():
    ok = True
    print("route_accept selftest")
    doc = BM.synthetic_board()
    # VCC: pads at MOD1.2 (x 13.2), C1.2 (x 10.75), R1.1 (x 21.25), J1.1 (x 3.73)
    # the stock track runs 10 -> 22 at y = 14, touching nothing: 4 islands, 3 merges
    b = BM.Board(doc)
    rep = connectivity(b)
    good = rep["VCC"][0] == 5
    print("  unrouted VCC is %d islands                     : %s"
          % (rep["VCC"][0], "OK" if good else "FAIL (want 5)"))
    ok &= good

    # now join MOD1.2 to C1.2 with a real track and watch merges drop by one
    doc2 = BM.synthetic_board()
    doc2["tracks"] = [{"net": "VCC", "layer": 1, "x1": 13.2, "y1": 10.0,
                       "x2": 10.75, "y2": 10.0, "w": 0.2}]
    b2 = BM.Board(doc2)
    r2 = connectivity(b2)
    good = r2["VCC"][0] == rep["VCC"][0] - 2
    print("  one real track merges two pad islands         : %d -> %d  %s"
          % (rep["VCC"][0], r2["VCC"][0], "OK" if good else "FAIL"))
    ok &= good

    # plane semantics: GND has a via, so with --plane-nets it collapses
    gnd_plain = len(islands_of(b, "GND"))
    gnd_plane = len(islands_of(b, "GND", plane=True))
    good = gnd_plane < gnd_plain
    print("  --plane-nets collapses via-bearing islands    : %d -> %d  %s"
          % (gnd_plain, gnd_plane, "OK" if good else "FAIL"))
    ok &= good

    # plane gate: a segment on a declared plane layer must fail
    doc3 = BM.synthetic_board()
    doc3["tracks"].append({"net": "VCC", "layer": 15, "x1": 1.0, "y1": 1.0,
                           "x2": 2.0, "y2": 1.0, "w": 0.2})
    b3 = BM.Board(doc3)
    on_plane = [t for t in b3.tracks if t["layer"] in b3.layers["solid_planes"]]
    good = len(on_plane) == 1
    print("  a segment on the solid plane is detected      : %s" % ("OK" if good else "FAIL"))
    ok &= good

    # clearance: two different-net pads under the rule
    doc4 = BM.synthetic_board()
    doc4["components"] = [
        {"des": "A", "footprint": "R0603", "x": 5.0, "y": 5.0, "angle": 0},
        {"des": "B", "footprint": "R0603", "x": 5.0 + 1.1 + 0.05 + 1.1, "y": 5.0,
         "angle": 0}]
    doc4["pad_nets"] = {"A.2": "N1", "B.1": "N2"}
    doc4["tracks"] = []
    doc4["vias"] = []
    b4 = BM.Board(doc4)
    viol, _w, _n = clearance_violations(b4, 0.102)
    good = len(viol) == 1 and abs(viol[0][0] - 0.05) < 1e-6
    print("  0.05 mm different-net pad gap flagged at 0.102: %s (%d, %.4f mm)"
          % ("OK" if good else "FAIL", len(viol), viol[0][0] if viol else float("nan")))
    ok &= good
    print("route_accept selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def _names(argv, flag):
    if flag not in argv:
        return []
    return [s.strip() for s in argv[argv.index(flag) + 1].split(",") if s.strip()]


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 2:
        print(__doc__)
        return 2
    board = BM.load(argv[1])
    base = BM.load(argv[argv.index("--baseline") + 1]) if "--baseline" in argv else None
    lim = float(argv[argv.index("--clearance") + 1]) if "--clearance" in argv else None
    top = int(argv[argv.index("--top") + 1]) if "--top" in argv else 12
    out = argv[argv.index("--json") + 1] if "--json" in argv else None
    n = run(board, baseline=base, protected=_names(argv, "--protected"),
            plane_nets=_names(argv, "--plane-nets"),
            expect_open=_names(argv, "--expect-open"),
            limit=lim, top=top, out=out)
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
