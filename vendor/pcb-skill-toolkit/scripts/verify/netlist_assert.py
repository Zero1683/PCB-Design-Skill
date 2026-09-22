# -*- coding: utf-8 -*-
"""Run explicit connectivity assertions against the board: must-connect,
must-not-connect, must-be-open.

WHAT THIS MEASURES
    PHYSICAL connectivity, from geometry, ignoring net names entirely.  Every piece of
    copper on the board -- pads, tracks, vias -- is grouped by whether outlines actually
    touch on a shared layer.  The assertions are then evaluated against those groups:

      must_connect      every member of the group lands in the SAME copper group
      must_not_connect  no two members share a copper group
      must_be_open      the member's group contains nothing but itself

    A member is either a pad reference "U1.7" or a net name "GND" (which expands to
    every pad the netlist gives that net).

    Names are used only to FIND the copper; the verdict comes from geometry.  That is
    the point: a short is two pieces of copper touching, whatever the netlist calls
    them, and an EDA's own net-based check cannot see a short it has already absorbed
    into its net model.

WHAT THIS CANNOT SEE
    * Pour copper, unless you declare it.  A net closed by a plane or a pour will read
      as many groups here.  Pass `--plane-nets GND,AGND`: any group that carries a via
      or a through-hole pad is then treated as reaching the plane.  That is a MODEL, not
      a measurement -- the measurement is the Gerber (verify/clearance.py, which reports
      copper claimed by two nets).
    * Resistance.  Two pads joined by a 0.1 mm 40 mm trace "connect" here.
    * Components.  A must-connect through a series resistor is NOT connected copper and
      correctly fails; assert the two halves separately.
    * Anything about intent.  You write the assertions; this only checks them.

WHY BOTH DIRECTIONS MATTER
    A board that passes must-connect and has never been asked a must-not-connect
    question has not been checked for shorts at all.  Write the negative assertions --
    supply rails against each other and against ground, a differential pair's two
    halves, anything switched -- and write must-be-open for every test point and unused
    pin you expect to float.

HOW IT WAS VALIDATED
    The connectivity core is the same union-find that decided acceptance on a released
    board.  `--selftest` runs assertions of all three kinds against a synthetic board
    with a deliberate short and a deliberate open.

USAGE
    python3 netlist_assert.py board.json assertions.json [--plane-nets "GND"]
                              [--json out.json]
    python3 netlist_assert.py --selftest

ASSERTIONS FILE
    {
      "must_connect":     [["U1.1", "C1.2"], ["U1.20", "U1.21", "L1.1"]],
      "must_not_connect": [["VBUS", "GND"], ["U1.5", "U1.6"]],
      "must_be_open":     ["TP1.1", "U1.44"]
    }
    Those references are an EXAMPLE shape, not a suggested set -- every board's
    assertions are its own.
"""
from __future__ import print_function

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, os.pardir, "placement"))
import geom2d as G                                                    # noqa: E402
import boardmodel as BM                                               # noqa: E402


class Obj(object):
    __slots__ = ("pts", "r", "layers", "kind", "ref", "bb", "net")

    def __init__(self, pts, r, layers, kind, ref, net=""):
        self.pts, self.r, self.kind, self.ref = pts, r, kind, ref
        self.layers = tuple(layers)
        self.net = net
        bb = G.bbox_of(pts)
        self.bb = (bb[0] - r, bb[1] - r, bb[2] + r, bb[3] + r)


def copper_objects(board):
    cu = tuple(board.layers["copper"])
    out = []
    for t in board.tracks:
        out.append(Obj([(t["x1"], t["y1"]), (t["x2"], t["y2"])], t["w"] / 2.0,
                       (t["layer"],), "track", None))
    for v in board.vias:
        out.append(Obj([(v["x"], v["y"])],
                       float(v.get("pad") or board.rules["via_pad"]) / 2.0,
                       board.via_layers(v), "via", None, v.get("net", "")))
    for rec in board.all_pads():
        layer_groups = [rec["layers"]] if rec.get("layer_bridge") else [(layer,) for layer in rec["layers"]]
        for layers in layer_groups:
            out.append(Obj(rec["poly"], 0.0, layers, "pad",
                           "%s.%s" % (rec["des"], rec["num"]), rec["net"]))
    return out


def groups(board, plane_nets=(), tol=1e-6):
    """Union-find over ALL copper, net-blind.  -> (objs, group_id_per_obj)."""
    plane_nets = set(plane_nets)
    objs = copper_objects(board)
    par = list(range(len(objs)))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            par[ra] = rb

    CELL = 2.0
    buckets = {}
    for k, o in enumerate(objs):
        for gx in range(int(o.bb[0] // CELL), int(o.bb[2] // CELL) + 1):
            for gy in range(int(o.bb[1] // CELL), int(o.bb[3] // CELL) + 1):
                buckets.setdefault((gx, gy), []).append(k)
    seen = set()
    for lst in buckets.values():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                i, j = sorted((lst[a], lst[b]))
                if (i, j) in seen:
                    continue
                seen.add((i, j))
                A, B = objs[i], objs[j]
                if not (set(A.layers) & set(B.layers)):
                    continue
                if not G.boxes_overlap(A.bb, B.bb):
                    continue
                if G.poly_distance(A.pts, B.pts) - A.r - B.r <= tol:
                    union(i, j)

    if plane_nets:
        # Declared plane nets: a group that reaches more than one layer (it holds a via
        # or a through-hole pad) is treated as touching that net's plane.  This is a
        # MODEL of copper this geometry cannot see, and it is applied per declared net
        # so that two different plane nets are never merged with each other.
        anchors = {}
        for k, o in enumerate(objs):
            if o.kind not in ("pad", "via"):
                continue
            net = o.net
            if net not in plane_nets:
                continue
            if len(o.layers) < 2 or not set(o.layers) & set(board.layers.get("solid_planes", [])):
                continue                    # single-layer: no way down to the plane
            if net in anchors:
                union(k, anchors[net])
            else:
                anchors[net] = k

    gid = [find(i) for i in range(len(objs))]
    return objs, gid


def resolve(board, ref):
    """A pad reference 'U1.7' or a net name -> [pad refs]."""
    if "." in ref:
        return [ref]
    pads = [("%s.%s" % (d, p)) for d, p in board.nets.get(ref, [])]
    if pads:
        return pads
    pads = ["%s.%s" % (r["des"], r["num"]) for r in board.all_pads()
            if r["net"] == ref]
    return pads


def evaluate(board, assertions, plane_nets=()):
    allowed = {"must_connect", "must_not_connect", "must_be_open"}
    if not isinstance(assertions, dict) or not assertions or set(assertions) - allowed:
        raise ValueError("Expected a nonempty assertion object with known rule names")
    total = 0
    for kind, items in assertions.items():
        if not isinstance(items, list):
            raise ValueError("%s must be a list" % kind)
        total += len(items)
        for item in items:
            refs = [item] if kind == "must_be_open" else item
            if not isinstance(refs, list) or not refs:
                raise ValueError("Each rule needs references")
            if any(not isinstance(r, str) or not r.strip() or r != r.strip() for r in refs):
                raise ValueError("References must be nonempty strings without outer whitespace")
            if kind != "must_be_open" and (len(refs) < 2 or len(set(refs)) != len(refs)):
                raise ValueError("Connection rules need at least two distinct references")
    if not total:
        raise ValueError("An empty assertion set cannot establish connectivity")
    if plane_nets and not board.layers.get("solid_planes"):
        raise ValueError("Plane net assumptions require declared solid plane layers")
    if any(not resolve(board, n) for n in plane_nets):
        raise ValueError("Declared plane net does not resolve to any pad")
    objs, gid = groups(board, plane_nets)
    by_ref = {}
    for i, o in enumerate(objs):
        if o.ref:
            by_ref.setdefault(o.ref, []).append(i)
    results = []

    def gof(ref):
        return {gid[i] for i in by_ref.get(ref, [])}

    def unresolved(members):
        return [m for m in members if not resolve(board, m)
                or any(r not in by_ref for r in resolve(board, m))]

    for grp in assertions.get("must_connect", []):
        missing_members = unresolved(grp)
        if missing_members:
            results.append(("must_connect", grp, False, "missing references: %s" % missing_members))
            continue
        refs = []
        for m in grp:
            refs += resolve(board, m)
        missing = [r for r in refs if r not in by_ref]
        gs = {r: gof(r) for r in refs if r in by_ref}
        distinct = set().union(*gs.values()) if gs else set()
        okk = (not missing) and len(distinct) <= 1 and bool(gs)
        results.append(("must_connect", grp, okk,
                        "missing pads %s" % missing if missing else
                        ("%d distinct copper groups: %s"
                         % (len(distinct),
                            {r: sorted(g) for r, g in list(gs.items())[:8]}) if not okk
                         else "all %d pad(s) on one piece of copper" % len(gs))))

    for grp in assertions.get("must_not_connect", []):
        missing_members = unresolved(grp)
        if missing_members:
            results.append(("must_not_connect", grp, False, "missing references: %s" % missing_members))
            continue
        refs = []
        for m in grp:
            refs.append((m, resolve(board, m)))
        pairs_bad = []
        for a in range(len(refs)):
            for b in range(a + 1, len(refs)):
                ga = set().union(*(gof(r) for r in refs[a][1]))
                gb = set().union(*(gof(r) for r in refs[b][1]))
                shared = ga & gb
                if shared:
                    pairs_bad.append((refs[a][0], refs[b][0], sorted(shared)[:3]))
        okk = not pairs_bad
        results.append(("must_not_connect", grp, okk,
                        "no shared copper" if okk else
                        "SHARED COPPER: %s" % pairs_bad))

    for m in assertions.get("must_be_open", []):
        if unresolved([m]):
            results.append(("must_be_open", m, False, "missing reference: %s" % m))
            continue
        refs = resolve(board, m)
        bad = []
        for r in refs:
            indices = by_ref.get(r, [])
            if not indices:
                bad.append((r, "no such pad"))
                continue
            copper_groups = {gid[i] for i in indices}
            others = [objs[k] for k in range(len(objs))
                      if gid[k] in copper_groups and objs[k].ref != r]
            if others:
                bad.append((r, "touches %d other object(s): %s"
                            % (len(others), [o.ref or o.kind for o in others[:5]])))
        results.append(("must_be_open", m, not bad,
                        "floats" if not bad else str(bad)))
    return results


def run(board, assertions, plane_nets=(), out=None):
    res = evaluate(board, assertions, plane_nets)
    print("=" * 74)
    print("NETLIST ASSERTIONS   %s" % board.source)
    print("=" * 74)
    print("connectivity is measured from GEOMETRY; net names only locate the copper.")
    if plane_nets:
        print("plane nets declared: %s  (their groups are MODELLED, not measured)"
              % list(plane_nets))
    print()
    fails = 0
    for kind, subject, okk, detail in res:
        if not okk:
            fails += 1
        print("%-18s %-46s %s" % (kind,
                                  str(subject)[:46],
                                  "PASS" if okk else "FAIL"))
        if not okk:
            print("      %s" % detail)
    print()
    print("assertions: %d   failed: %d" % (len(res), fails))
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump([{"kind": k, "subject": s, "pass": bool(o), "detail": d}
                       for k, s, o, d in res], fh, indent=1)
        print("wrote %s" % out)
    return fails


def _selftest():
    ok = True
    print("netlist_assert selftest")
    doc = BM.synthetic_board()
    # give R1.1 and C2.1 a real track so they physically connect
    doc["tracks"] = [{"net": "OUT", "layer": 1, "x1": 22.75, "y1": 10.0,
                      "x2": 22.0, "y2": 10.75, "w": 0.2}]
    b = BM.Board(doc)

    res = evaluate(b, {"must_connect": [["R1.2", "C2.1"]]})
    good = res[0][2]
    print("  must_connect on two pads a track joins        : %s (%s)"
          % ("OK" if good else "FAIL", res[0][3]))
    ok = ok and bool(good)

    res = evaluate(b, {"must_connect": [["J1.1", "MOD1.2"]]})
    good = not res[0][2]
    print("  must_connect on two UNROUTED pads fails       : %s" % ("OK" if good else "FAIL"))
    ok = ok and bool(good)

    # a deliberate short: drop a fat track across two different-net pads
    doc2 = BM.synthetic_board()
    doc2["tracks"] = [{"net": "OOPS", "layer": 1, "x1": 3.0, "y1": 25.0,
                       "x2": 7.0, "y2": 25.0, "w": 1.0}]
    b2 = BM.Board(doc2)
    res = evaluate(b2, {"must_not_connect": [["J1.1", "J1.2"]]})
    good = not res[0][2]
    print("  must_not_connect catches a shorting track     : %s (%s)"
          % ("OK" if good else "FAIL", res[0][3][:56]))
    ok = ok and bool(good)

    res = evaluate(b, {"must_be_open": ["J1.1"]})
    good = res[0][2]
    print("  must_be_open on a truly floating pad          : %s" % ("OK" if good else "FAIL"))
    ok = ok and bool(good)

    res = evaluate(b2, {"must_be_open": ["J1.1"]})
    good = not res[0][2]
    print("  must_be_open fails once something touches it  : %s" % ("OK" if good else "FAIL"))
    ok = ok and bool(good)

    res = evaluate(b, {"must_connect": [["NOSUCH.1", "R1.2"]]})
    good = not res[0][2] and "missing" in res[0][3]
    print("  a reference that does not exist FAILS loudly  : %s" % ("OK" if good else "FAIL"))
    ok = ok and bool(good)

    print("netlist_assert selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 3:
        print(__doc__)
        return 2
    board = BM.load(argv[1])
    with open(argv[2], encoding="utf-8") as fh:
        assertions = json.load(fh, object_pairs_hook=BM.unique_json_object)
    pn = []
    if "--plane-nets" in argv:
        pn = [s.strip() for s in argv[argv.index("--plane-nets") + 1].split(",") if s.strip()]
    out = argv[argv.index("--json") + 1] if "--json" in argv else None
    return 1 if run(board, assertions, plane_nets=pn, out=out) else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except (ValueError, OSError, KeyError, IndexError) as error:
        print("INPUT ERROR: %s" % error, file=sys.stderr)
        sys.exit(2)
