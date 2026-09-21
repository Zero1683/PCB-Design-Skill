# -*- coding: utf-8 -*-
"""Solder-mask opening coverage: does every pad that must be soldered have one?

WHAT THIS MEASURES
    For one side of the board, from the copper Gerber and the solder-mask Gerber:
      * every copper PAD flash, and whether a mask flash or mask region opens over it;
      * the mask EXPANSION per side, as a histogram, so an odd pad stands out;
      * every copper VIA flash and whether it has an opening -- zero openings means the
        vias are tented, which is usually what a design intends and always worth
        stating out loud rather than assuming.

    Pads and vias are told apart by the exporter's G04 section tags.  Where the exporter
    does not tag its objects, `--assume-all-pads` treats every flash as a pad and the
    via line is reported as unavailable rather than as zero.

WHAT THIS CANNOT SEE
    * Whether an opening is BIG ENOUGH for assembly.  It reports the expansion; the
      stencil and the assembler's process window decide.
    * Mask slivers between openings.  Two openings that nearly merge leave a mask web
      too thin to survive; that needs a raster of the mask layer against the
      fabricator's minimum dam, which this does not do.
    * Pads drawn as REGIONS rather than flashes.  A region-drawn pad has no flash to
      match and is invisible here; the counts printed let you notice that
      (copper flashes far fewer than the board model's pad count).
    * Paste.  A mask opening is not a paste aperture; check the paste layer separately.

MATCHING RULE, AND ITS LIMIT
    A mask flash matches a pad when their centres agree to within `--tol` (default
    0.02 mm).  That is exact for the usual case, where the exporter emits the mask
    aperture concentric with the pad.  It will MISS a mask opening that is deliberately
    offset, and it will mis-pair two pads closer together than the tolerance.  Both are
    reported as "no opening", which is the safe direction to be wrong in.

HOW IT WAS VALIDATED
    On a released board this reproduced the fabrication review's numbers exactly: every
    pad on both sides had an opening, all vias were tented, and the expansion histogram
    was a single value plus the known exceptions.  `--selftest` runs synthetic layers
    including a pad deliberately left covered.

USAGE
    python3 mask_check.py COPPER.GTL MASK.GTS [--tol 0.02] [--assume-all-pads]
                          [--json out.json] [--top 10]
    python3 mask_check.py --selftest
"""
from __future__ import print_function

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerber as GB                                                   # noqa: E402


def _key(x, y, q=0.001):
    return (round(x / q), round(y / q))


def match(copper, mask, tol=0.02, assume_all_pads=False):
    tagged = any(f.section for f in copper.flashes)
    pads = [f for f in copper.flashes
            if (assume_all_pads or not tagged or f.section == "Pad")]
    vias = [f for f in copper.flashes if tagged and f.section == "Via"]

    # bucket the mask flashes so matching is not O(pads x mask)
    buckets = {}
    q = max(tol * 2.0, 0.001)
    for f in mask.flashes:
        buckets.setdefault((int(f.x / q), int(f.y / q)), []).append(f)

    def find(x, y):
        best = None
        for gx in (int(x / q) - 1, int(x / q), int(x / q) + 1):
            for gy in (int(y / q) - 1, int(y / q), int(y / q) + 1):
                for f in buckets.get((gx, gy), ()):
                    if abs(f.x - x) <= tol and abs(f.y - y) <= tol:
                        d = abs(f.x - x) + abs(f.y - y)
                        if best is None or d < best[0]:
                            best = (d, f)
        return best[1] if best else None

    regions = [(min(p[0] for p in r), min(p[1] for p in r),
                max(p[0] for p in r), max(p[1] for p in r)) for r in mask.regions]

    def in_region(x, y):
        for x0, y0, x1, y1 in regions:
            if x0 - 1e-6 <= x <= x1 + 1e-6 and y0 - 1e-6 <= y <= y1 + 1e-6:
                return True
        return False

    opened, covered, exp = [], [], {}
    for p in pads:
        m = find(p.x, p.y)
        if m is not None:
            opened.append((p, m))
            e = round((max(m.ap.w, m.ap.h) - max(p.ap.w, p.ap.h)) / 2.0, 4)
            exp[e] = exp.get(e, 0) + 1
        elif in_region(p.x, p.y):
            opened.append((p, None))
            exp["region"] = exp.get("region", 0) + 1
        else:
            covered.append(p)
    via_open = [v for v in vias if find(v.x, v.y) is not None]
    return {"tagged": tagged, "pads": pads, "vias": vias, "opened": opened,
            "covered": covered, "expansion": exp, "via_open": via_open}


def run(copper_path, mask_path, tol=0.02, assume_all_pads=False, top=10, out=None):
    cu = GB.parse_gerber(open(copper_path, encoding="utf-8",
                              errors="replace").read(), copper_path)
    mk = GB.parse_gerber(open(mask_path, encoding="utf-8",
                              errors="replace").read(), mask_path)
    r = match(cu, mk, tol=tol, assume_all_pads=assume_all_pads)

    print("=" * 74)
    print("SOLDER-MASK COVERAGE   %s  vs  %s"
          % (os.path.basename(copper_path), os.path.basename(mask_path)))
    print("=" * 74)
    if not r["tagged"]:
        print("NOTE: this copper layer carries no G04 section tags, so pads and vias")
        print("      cannot be told apart.  Every flash is treated as a pad and the")
        print("      via line below is UNAVAILABLE, not zero.")
    print("copper pad flashes     : %d" % len(r["pads"]))
    print("copper via flashes     : %s"
          % (len(r["vias"]) if r["tagged"] else "unavailable (untagged export)"))
    print("mask flashes / regions : %d / %d" % (len(mk.flashes), len(mk.regions)))
    print("pads WITH an opening   : %d" % len(r["opened"]))
    print("pads WITHOUT           : %d" % len(r["covered"]))
    for p in r["covered"][:top]:
        print("     covered pad %s at (%.3f, %.3f)" % (p.ap, p.x, p.y))
    print("mask expansion per side: %s"
          % {k: v for k, v in sorted(r["expansion"].items(), key=lambda kv: -kv[1])})
    if r["tagged"]:
        print("vias with an opening   : %d   (0 = fully tented, usually intended)"
              % len(r["via_open"]))
    res = {"pads": len(r["pads"]), "opened": len(r["opened"]),
           "covered": len(r["covered"]),
           "vias": len(r["vias"]) if r["tagged"] else None,
           "vias_open": len(r["via_open"]) if r["tagged"] else None,
           "expansion": {str(k): v for k, v in r["expansion"].items()},
           "tagged": r["tagged"]}
    print()
    print("verdict: %s" % ("PASS" if not r["covered"] else
                           "FAIL - %d pad(s) have no mask opening" % len(r["covered"])))
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("wrote %s" % out)
    return len(r["covered"])


_CU = """G04 copper*
%FSLAX26Y26*%
%MOMM*%
%ADD11R,1.000000X0.600000*%
%ADD12C,0.500000*%
G04 Pad Start*
D11*
X2000000Y2000000D03*
X4000000Y2000000D03*
X6000000Y2000000D03*
G04 Pad End*
G04 Via Start*
D12*
X8000000Y2000000D03*
G04 Via End*
M02*
"""

_MK = """G04 mask*
%FSLAX26Y26*%
%MOMM*%
%ADD11R,1.100000X0.700000*%
G04 Pad Start*
D11*
X2000000Y2000000D03*
X4000000Y2000000D03*
G04 Pad End*
M02*
"""


def _selftest():
    ok = True
    print("mask_check selftest")
    cu = GB.parse_gerber(_CU, "cu")
    mk = GB.parse_gerber(_MK, "mk")
    r = match(cu, mk)
    good = len(r["pads"]) == 3 and len(r["vias"]) == 1
    print("  pads and vias separated by section tag        : %d / %d  %s"
          % (len(r["pads"]), len(r["vias"]), "OK" if good else "FAIL"))
    ok = ok and good
    good = len(r["opened"]) == 2 and len(r["covered"]) == 1
    print("  the third pad is correctly reported COVERED   : %s" % ("OK" if good else "FAIL"))
    ok = ok and good
    good = r["expansion"].get(0.05) == 2
    print("  expansion 0.05 mm per side on both openings   : %s (%s)"
          % ("OK" if good else "FAIL", r["expansion"]))
    ok = ok and good
    good = len(r["via_open"]) == 0
    print("  the via is tented (0 openings)                : %s" % ("OK" if good else "FAIL"))
    ok = ok and good
    r2 = match(cu, mk, assume_all_pads=True)
    good = len(r2["pads"]) == 4
    print("  --assume-all-pads treats every flash as a pad : %d  %s"
          % (len(r2["pads"]), "OK" if good else "FAIL"))
    ok = ok and good
    print("mask_check selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 3:
        print(__doc__)
        return 2
    tol = float(argv[argv.index("--tol") + 1]) if "--tol" in argv else 0.02
    out = argv[argv.index("--json") + 1] if "--json" in argv else None
    top = int(argv[argv.index("--top") + 1]) if "--top" in argv else 10
    n = run(argv[1], argv[2], tol=tol,
            assume_all_pads=("--assume-all-pads" in argv), top=top, out=out)
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
