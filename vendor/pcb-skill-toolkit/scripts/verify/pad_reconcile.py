# -*- coding: utf-8 -*-
"""Reconcile the PCB's pad-to-net map, pad by pad, against the schematic netlist.

WHAT THIS MEASURES
    Four differences between what the BOARD holds and what the SCHEMATIC says:
      1. pads whose net on the PCB differs from the schematic's;
      2. pads carrying a net the schematic does not assign to them;
      3. schematic pins for which the placed footprint has no such pad;
      4. the symmetric difference of the two NET SETS.
    Plus a per-component summary so a single mis-rotated or mis-mapped part shows up as
    a block of differences rather than a scatter.

WHY IT IS NOT ENOUGH TO ASK THE EDA
    An EDA's own "netlist error" / "import changes" comparison is the same code path
    that built the board.  On the reference project that call returned success and did
    nothing.  A comparison is only evidence when the two sides came from different code:
    here one side is the PCB document's own PAD_NET records and the other is a netlist
    exported from the schematic.

    The pad-number trap this exists for: a pad is bound to its net by the footprint
    ELEMENT id, not by the pad NUMBER.  They coincide for most parts and do NOT for a
    connector whose several shell legs all carry pad number "1" -- keying by number put
    a ground net on the wrong pin, and nothing complained.  The board JSON produced by
    placement/import_easyeda.py carries BOTH keys ("DES.NUM" and "DES#ELEM") so this
    script can report where they disagree.

WHAT THIS CANNOT SEE
    * Whether the SCHEMATIC is right.  Both sides can agree and both be wrong.
    * Physical connectivity.  Two pads on the same net may not be routed; that is
      routing/route_accept.py.  Two pads on different nets may be shorted; that is
      verify/netlist_assert.py and verify/clearance.py.
    * A footprint whose pad numbering does not match its symbol's pin numbering.  Both
      sides use the same names, so a consistent mis-mapping is invisible here -- the
      thing that catches it is the pad-by-pad geometric check against the EDA's own
      reported pad coordinates, which is a different measurement (and worth doing: on
      the reference project it is what settled the rotation convention).

HOW IT WAS VALIDATED
    On a released board it reported 0 differing pads over 574 pad-net records and an
    empty net-set difference, and it is the check that found a connector's shell pads
    bound to the wrong pin on an earlier revision.  `--selftest` runs a synthetic board
    with each of the four difference kinds present.

USAGE
    python3 pad_reconcile.py board.json [--netlist netlist.json] [--json out.json]
                             [--top 20]
    python3 pad_reconcile.py --selftest

    `netlist.json` is {"NETNAME": [["U1","7"], ["C3","1"]], ...}.  If the board JSON
    already carries a "nets" section, --netlist overrides it.
"""
from __future__ import print_function

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, os.pardir, "placement"))
import boardmodel as BM                                               # noqa: E402


def reconcile(board, netlist=None):
    nets = netlist if netlist is not None else board.nets
    if not nets:
        raise SystemExit(
            "no schematic netlist.  This script exists to compare TWO sources; with\n"
            "only one it has nothing to say.  Export the netlist and pass --netlist.")

    if not isinstance(nets, dict):
        raise BM.BoardError("schematic netlist must be an object")
    want = {}                       # logical schematic pins: DES.NUM -> net
    for net, members in nets.items():
        if not isinstance(net, str) or not net.strip() or not isinstance(members, list):
            raise BM.BoardError("invalid schematic net or member list: %r" % (net,))
        for member in members:
            if (not isinstance(member, (list, tuple)) or len(member) != 2
                    or any(not isinstance(v, (str, int)) or isinstance(v, bool)
                           or not str(v).strip() for v in member)):
                raise BM.BoardError("invalid schematic pin member: %r" % (member,))
            des, pad = member
            key = "%s.%s" % (des, pad)
            if key in want and want[key] != net:
                raise BM.BoardError("schematic pin %s belongs to conflicting nets %s and %s"
                                    % (key, want[key], net))
            want[key] = net

    # Keep every physical land. DES.NUM is only a grouping key, never an
    # overwrite destination for observations from different physical pads.
    groups, physical = {}, {}
    for rec in board.all_pads():
        key = "%s.%s" % (rec["des"], rec["num"])
        groups.setdefault(key, []).append(rec)
    differ, extra, missing = [], [], []
    for key, records in sorted(groups.items()):
        for rec in records:
            identity = ("%s#%s" % (rec["des"], rec["elem"])
                        if rec.get("elem") is not None else key)
            if identity in physical:
                raise BM.BoardError("duplicate physical pad identity: %s" % identity)
            physical[identity] = rec["net"]
            # Keep historical single-pad diagnostic labels, disambiguate repeats.
            label = identity if len(records) > 1 else key
            if key in want and rec["net"] != want[key]:
                differ.append((label, want[key], rec["net"]))
            elif key not in want and rec["net"]:
                extra.append((label, rec["net"]))
    for key, net in sorted(want.items()):
        if key not in groups:
            missing.append((key, net))

    multi = {k: len(v) for k, v in groups.items() if len(v) > 1}
    # The compatibility summary is scalar only where every land agrees;
    # conflicting observations are retained as a list, never last-write-wins.
    have = {}
    for key, records in groups.items():
        observed = sorted({rec["net"] for rec in records})
        have[key] = observed[0] if len(observed) == 1 else observed
    nets_pcb = {n for n in physical.values() if n}
    nets_sch = set(nets)
    return {"want": want, "have": have, "physical_have": physical,
            "differ": differ, "extra": extra, "missing": missing,
            "multi_land_pads": multi, "nets_pcb": nets_pcb, "nets_sch": nets_sch,
            "net_diff": sorted(nets_pcb ^ nets_sch)}


def run(board, netlist=None, top=20, out=None):
    r = reconcile(board, netlist)
    print("=" * 74)
    print("PAD-BY-PAD RECONCILIATION   %s" % board.source)
    print("=" * 74)
    print("components on the PCB      : %d" % len(board.parts))
    print("pad records on the PCB     : %d" % sum(len(p.pads) for p in board.parts.values()))
    print("distinct pads (DES.NUM)    : %d" % len(r["have"]))
    print("schematic pin->net pairs   : %d" % len(r["want"]))
    if r["multi_land_pads"]:
        print("pads with SEVERAL lands    : %d %s"
              % (len(r["multi_land_pads"]),
                 sorted(r["multi_land_pads"])[:6]))
        print("   (every physical land was checked using its element identity)")
    print()
    print("pads whose net DIFFERS                     : %d" % len(r["differ"]))
    for k, wnt, hv in r["differ"][:top]:
        print("     %-12s schematic %-16s pcb %s" % (k, wnt, hv or "(none)"))
    print("pads with a net the schematic does not give: %d" % len(r["extra"]))
    for k, hv in r["extra"][:top]:
        print("     %-12s pcb %s" % (k, hv))
    print("schematic pins with no such footprint pad  : %d" % len(r["missing"]))
    for k, wnt in r["missing"][:top]:
        print("     %-12s schematic %s" % (k, wnt))
    print()
    print("distinct nets: pcb %d   schematic %d" % (len(r["nets_pcb"]), len(r["nets_sch"])))
    print("net-set difference (%d): %s" % (len(r["net_diff"]), r["net_diff"][:20]))

    per = {}
    for k, _w, _h in r["differ"]:
        des = k.split("#")[0].split(".")[0]
        per[des] = per.get(des, 0) + 1
    if per:
        print()
        print("differences by component (a block here is usually ONE bad mapping):")
        for des, n in sorted(per.items(), key=lambda kv: -kv[1])[:top]:
            print("     %-10s %d" % (des, n))

    fails = len(r["differ"]) + len(r["extra"]) + len(r["missing"]) + len(r["net_diff"])
    print()
    print("total differences: %d" % fails)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump({"differ": r["differ"], "extra": r["extra"],
                       "missing": r["missing"], "net_diff": r["net_diff"],
                       "multi_land_pads": r["multi_land_pads"],
                       "physical_have": r["physical_have"]}, fh, indent=1)
        print("wrote %s" % out)
    return fails


def _selftest():
    ok = True
    print("pad_reconcile selftest")
    doc = BM.synthetic_board()
    # introduce each of the four difference kinds
    doc["pad_nets"]["R1.2"] = "WRONG"          # 1. differs
    doc["pad_nets"]["J1.2"] = "STRAY"          # 2. a net the schematic does not give
    doc["nets"]["GND"].append(["MOD1", "99"])  # 3. a pin with no such pad
    b = BM.Board(doc)
    r = reconcile(b)

    good = ("R1.2", "OUT", "WRONG") in r["differ"]
    print("  a pad whose net differs is found              : %s" % ("OK" if good else "FAIL"))
    ok = ok and good
    good = ("J1.2", "STRAY") in r["extra"] or ("J1.2", "GND", "STRAY") in r["differ"]
    print("  a stray net on a pad is found                 : %s" % ("OK" if good else "FAIL"))
    ok = ok and good
    good = ("MOD1.99", "GND") in r["missing"]
    print("  a schematic pin with no pad is found          : %s" % ("OK" if good else "FAIL"))
    ok = ok and good
    good = "WRONG" in r["net_diff"] and "STRAY" in r["net_diff"]
    print("  the net-set difference lists both new names   : %s (%s)"
          % ("OK" if good else "FAIL", r["net_diff"]))
    ok = ok and good

    clean = BM.Board(BM.synthetic_board())
    r2 = reconcile(clean)
    good = not (r2["differ"] or r2["extra"] or r2["missing"] or r2["net_diff"])
    print("  a consistent board reconciles with 0 diffs    : %s" % ("OK" if good else "FAIL"))
    ok = ok and good

    try:
        d3 = BM.synthetic_board()
        d3["nets"] = {}
        reconcile(BM.Board(d3))
        good = False
    except SystemExit:
        good = True
    print("  refuses to run with only ONE source           : %s" % ("OK" if good else "FAIL"))
    ok = ok and good

    print("pad_reconcile selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 2:
        print(__doc__)
        return 2
    board = BM.load(argv[1])
    netlist = None
    if "--netlist" in argv:
        with open(argv[argv.index("--netlist") + 1], encoding="utf-8") as fh:
            netlist = json.load(fh, object_pairs_hook=BM.unique_json_object)
    top = int(argv[argv.index("--top") + 1]) if "--top" in argv else 20
    out = argv[argv.index("--json") + 1] if "--json" in argv else None
    return 1 if run(board, netlist=netlist, top=top, out=out) else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except (BM.BoardError, ValueError, OSError) as exc:
        print("INPUT ERROR: %s" % exc, file=sys.stderr)
        sys.exit(2)
