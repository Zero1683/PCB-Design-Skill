# -*- coding: utf-8 -*-
"""Drill census straight from the Excellon files, per file and de-duplicated.

WHAT THIS MEASURES
    How many holes the fabricator will actually drill, and of what sizes.  Per FILE
    first, then the UNION of distinct features across files, then the subset relations
    between files.

THE TRAP THIS EXISTS FOR
    One drill file can be a STRICT SUBSET of another.  On the reference board
    `Drill_PTH_Through_Via.DRL` (517 hits) is entirely contained in
    `Drill_PTH_Through.DRL` (526 hits): the via file is a convenience listing, not an
    additional set of holes.  SUMMING THE FILES DOUBLE-COUNTS -- it gave 1057 where the
    truth was 540, which is the difference between "comfortably inside the fabricator's
    free-drill allowance" and "over it".  This script therefore:
      * reports each file separately,
      * proves or disproves the subset relation for every ordered pair,
      * reports the union of distinct features as THE number.
    A G85 line carries two coordinates and is ONE drilled feature (a routed slot), not
    two holes.

WHAT THIS CANNOT SEE
    * Whether a hole is in the right place.  Cross-check the count against an
      independent board model -- placement/boardmodel.py's `all_holes()` gives one, and
      two artefacts produced by different code paths agreeing is the actual evidence.
    * Plating, beyond the TYPE=PLATED header comment.  If your exporter omits it, this
      says `plated=False` and you must decide from the file name yourself -- the script
      will not infer it, because a file name is not a measurement.
    * Fabricator-specific rules: minimum drill, aspect ratio, drill-to-copper.  Those
      need the copper layers as well; see clearance.py and the hole-to-hole gate in
      placement/courtyard_check.py.
    * Backdrilling, blind and buried vias.  Everything here is treated as through.

HOW IT WAS VALIDATED
    On a released board it reproduced the census that two independent design models
    agreed on, and its subset proof is what corrected a drill count that had been
    reported nearly twice too high.  `--selftest` runs synthetic files including a
    deliberate subset pair.

USAGE
    python3 drill_census.py FILE.DRL [FILE.DRL ...] [--budget 621] [--json out.json]
    python3 drill_census.py --selftest
"""
from __future__ import print_function

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerber as GB                                                   # noqa: E402


def census(paths, tol=4):
    files = []
    for p in paths:
        text = open(p, encoding="utf-8", errors="replace").read()
        tools, hits, plated = GB.parse_excellon(text, p)
        files.append({"path": p, "name": os.path.basename(p), "tools": tools,
                      "hits": hits, "plated": plated,
                      "keys": set(h.key(tol) for h in hits)})
    return files


def subset_matrix(files, tol=4):
    """[(a_index, b_index, is_subset, shared)] for every ordered pair."""
    out = []
    for i, a in enumerate(files):
        for j, b in enumerate(files):
            if i == j:
                continue
            shared = len(a["keys"] & b["keys"])
            out.append((i, j, a["keys"] <= b["keys"] and bool(a["keys"]), shared))
    return out


def run(paths, budget=None, out=None):
    files = census(paths)
    print("=" * 74)
    print("DRILL CENSUS")
    print("=" * 74)
    for f in files:
        hits = f["hits"]
        slots = [h for h in hits if h.is_slot]
        sizes = {}
        for h in hits:
            k = "%.3f%s" % (h.dia, "S" if h.is_slot else "")
            sizes[k] = sizes.get(k, 0) + 1
        print("%-34s tools %2d  features %4d  (round %4d, slots %2d)  plated=%s"
              % (f["name"], len(f["tools"]), len(hits), len(hits) - len(slots),
                 len(slots), f["plated"]))
        print("    sizes: %s" % "  ".join("%s x%d" % kv for kv in sorted(sizes.items())))
        print("    distinct features in this file: %d%s"
              % (len(f["keys"]),
                 "" if len(f["keys"]) == len(hits)
                 else "   <-- %d duplicate coordinate(s) WITHIN the file"
                      % (len(hits) - len(f["keys"]))))

    print()
    print("SUBSET RELATIONS  (this is the number that gets double-counted)")
    any_subset = False
    for i, j, is_sub, shared in subset_matrix(files):
        if shared == 0:
            continue
        a, b = files[i], files[j]
        mark = "  <-- STRICT SUBSET: do NOT add these two files together" if is_sub else ""
        any_subset = any_subset or is_sub
        print("   %-30s shares %4d of its %4d features with %-30s%s"
              % (a["name"], shared, len(a["keys"]), b["name"], mark))
    if not any_subset:
        print("   no file is a subset of another; the files are disjoint sets of holes")

    union = set()
    for f in files:
        union |= f["keys"]
    naive = sum(len(f["hits"]) for f in files)
    print()
    print("naive sum of every line in every file : %d" % naive)
    print("DISTINCT DRILLED FEATURES (the union) : %d" % len(union))
    if naive != len(union):
        print("   the difference of %d is what a naive sum would over-report"
              % (naive - len(union)))
    plated = set()
    unplated = set()
    for f in files:
        (plated if f["plated"] else unplated).add(id(f))
    pl = set()
    for f in files:
        if f["plated"]:
            pl |= f["keys"]
    print("   of which plated: %d   non-plated: %d" % (len(pl), len(union - pl)))
    if budget:
        print()
        print("budget %d  ->  %s (%d %s)"
              % (budget, "WITHIN" if len(union) <= budget else "OVER",
                 abs(budget - len(union)),
                 "to spare" if len(union) <= budget else "over"))
    res = {"files": [{"name": f["name"], "hits": len(f["hits"]),
                      "distinct": len(f["keys"]), "plated": f["plated"]}
                     for f in files],
           "naive_sum": naive, "distinct_total": len(union),
           "plated": len(pl), "unplated": len(union - pl),
           "budget": budget,
           "over_budget": (budget is not None and len(union) > budget)}
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("wrote %s" % out)
    return 1 if (budget is not None and len(union) > budget) else 0


_A = """M48
;TYPE=PLATED
METRIC,LZ
T1C0.300
T2C0.900
%
T1
X1.000Y1.000
X2.000Y1.000
X3.000Y1.000
T2
X5.000Y5.000
M30
"""
# a strict subset of _A: the same three 0.300 holes and nothing else
_B = """M48
;TYPE=PLATED
METRIC,LZ
T1C0.300
%
T1
X1.000Y1.000
X2.000Y1.000
X3.000Y1.000
M30
"""
_C = """M48
METRIC,LZ
T1C1.000
%
T1
X9.000Y9.000
X10.000Y9.000G85X12.000Y9.000
M30
"""


def _selftest():
    import tempfile
    ok = True
    print("drill_census selftest")
    tmp = tempfile.mkdtemp(prefix="pcbkit-")
    pa = os.path.join(tmp, "PTH.DRL")
    pb = os.path.join(tmp, "PTH_Via.DRL")
    pc = os.path.join(tmp, "NPTH.DRL")
    open(pa, "w").write(_A)
    open(pb, "w").write(_B)
    open(pc, "w").write(_C)

    files = census([pa, pb, pc])
    good = [len(f["hits"]) for f in files] == [4, 3, 2]
    print("  per-file counts 4 / 3 / 2                     : %s" % ("OK" if good else "FAIL"))
    ok = ok and good

    rel = subset_matrix(files)
    is_sub = [(i, j) for i, j, sub, sh in rel if sub]
    good = (1, 0) in is_sub and (0, 1) not in is_sub
    print("  via file proved a STRICT SUBSET of the PTH file: %s" % ("OK" if good else "FAIL"))
    ok = ok and good

    union = set()
    for f in files:
        union |= f["keys"]
    good = len(union) == 6
    print("  naive sum 9, distinct union %d                 : %s"
          % (len(union), "OK - the subset is not counted twice" if good else "FAIL"))
    ok = ok and good

    slots = [h for f in files for h in f["hits"] if h.is_slot]
    good = len(slots) == 1
    print("  a G85 line is ONE feature, not two            : %s" % ("OK" if good else "FAIL"))
    ok = ok and good

    good = files[0]["plated"] and not files[2]["plated"]
    print("  plated flag read from the header comment      : %s" % ("OK" if good else "FAIL"))
    ok = ok and good

    print("drill_census selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    paths = [a for a in argv[1:] if not a.startswith("--")
             and argv[argv.index(a) - 1] not in ("--budget", "--json")]
    if not paths:
        print(__doc__)
        return 2
    budget = int(argv[argv.index("--budget") + 1]) if "--budget" in argv else None
    out = argv[argv.index("--json") + 1] if "--json" in argv else None
    return run(paths, budget=budget, out=out)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
