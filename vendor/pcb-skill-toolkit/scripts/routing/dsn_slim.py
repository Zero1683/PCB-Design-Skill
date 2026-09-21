# -*- coding: utf-8 -*-
"""Cut a Specctra DSN down to what the autorouter should actually be asked to do.

WHAT THIS DOES
    Two edits, both of which exist because of measured failures, not tidiness:

    1. WIRING -- keep only the copper worth protecting.
       Feeding a router every existing trace as protected wiring OVERFLOWS ITS STACK.
       Measured: 3326 protected traces crashed FreeRouting inside `PolylineTrace.combine`,
       which recurses once per trace in a connected chain.  `-Xss512m` only moved the
       crash from 3 seconds to 11 minutes.  The fix is not more stack, it is FEWER
       PROTECTED TRACES: keep the copper that is finished, verified and expensive to
       redo (matched pairs, tuned stubs), rip the rest and let the router lay it again.

    2. NETWORK -- drop nets the router must not be given.
       * POURED NETS.  A ground that is a solid plane plus pours is not a routing
         problem.  Asking a router to lay traces for it wastes channel width on copper
         the pour would have made anyway.
       * NETS THE ROUTER CANNOT PHYSICALLY DO.  Measured on one board: after five passes
         and 39 minutes the router had laid ZERO segments of nine power rails -- every
         rail's island count still equalled its pad count -- while burning 105 s per
         connection gained, because 0.50 mm of track plus two 0.102 mm clearances needs
         0.704 mm and the placement's channels were 0.55 mm.  Route those by hand or by
         a dedicated pass, and take them out of the router's search space.

WHAT THIS CANNOT SEE
    * Whether dropping a net was correct.  A dropped net is NOT routed.  Something else
      must close it, and route_accept.py must be told to expect it (`--expect-open`), or
      you will ship an open circuit that every gate called a pass.
    * Whether the kept wiring is actually good.  "Protected" means "do not touch", not
      "verified".  Verify before you protect.
    * Whether the stack will now survive.  The kept-count assertion (`--min-kept` /
      `--max-kept`) is a guard against a filter that silently matched nothing or
      everything; it is not a prediction about the router.

HOW IT WAS VALIDATED
    Ported from the slimmer of a released board, where it took a crashing 3326-wire DSN
    down to 51 wires plus 7 vias and the run completed.  `--selftest` slims a synthetic
    DSN and checks the counts and the dropped-net assertion.

USAGE
    python3 dsn_slim.py in.dsn out.dsn --keep "MIPI_D0P,MIPI_D0N,RST"
                        [--drop "GND,AGND"] [--drop-file nets.txt]
                        [--min-kept 1] [--max-kept 100000]
    python3 dsn_slim.py --selftest
"""
from __future__ import print_function

import re
import sys

WIRE_RE = re.compile(r"    \((?:wire|via)\b.*?\n    \)\n", re.S)
NET_IN_ENTRY_RE = re.compile(r"\(net ([^)]*)\)")
NET_BLOCK_RE = re.compile(r"    \(net (\S+)\n(?:.*?\n)*?    \)\n")


def slim(text, keep=(), drop=(), min_kept=0, max_kept=None, verbose=True):
    keep = set(keep)
    drop = set(drop)
    report = {}

    head, sep, wiring = text.partition("  (wiring\n")
    if not sep:
        raise SystemExit("no (wiring section in this DSN -- is it really a Specctra DSN?")

    body = wiring.rstrip()
    if not body.endswith(")"):
        raise SystemExit("unexpected tail after the wiring section")
    body = body[:body.rindex(")")]          # drop the file's closing paren
    inner = body.rstrip()
    if not inner.endswith(")"):
        raise SystemExit("unexpected tail inside the wiring section")
    inner = inner[:inner.rindex(")")]       # drop the wiring section's closing paren

    entries = WIRE_RE.findall(inner)
    kept = []
    for e in entries:
        m = NET_IN_ENTRY_RE.search(e)
        if m and m.group(1).strip().strip("'\"") in keep:
            kept.append(e)
    nwire = sum(1 for e in kept if e.lstrip().startswith("(wire"))
    nvia = len(kept) - nwire
    report["wiring_in"] = len(entries)
    report["wiring_kept"] = len(kept)
    report["wires"] = nwire
    report["vias"] = nvia
    if len(kept) < min_kept or (max_kept is not None and len(kept) > max_kept):
        raise SystemExit(
            "kept %d wiring entries, expected %s..%s.\n"
            "A keep-list that matched nothing looks exactly like a board with no copper;\n"
            "that is why this is fatal." % (len(kept), min_kept, max_kept))

    dropped = []
    if drop:
        if "  (network" not in head:
            raise SystemExit("no (network section found to drop nets from")
        ns = head.index("  (network")
        ne = head.index("  (wiring") if "  (wiring" in head else len(head)
        block = head[ns:ne]

        def cut(m):
            if m.group(1).strip("'\"") in drop:
                dropped.append(m.group(1).strip("'\""))
                return ""
            return m.group(0)

        newblock, scanned = NET_BLOCK_RE.subn(cut, block)
        head = head[:ns] + newblock + head[ne:]
        report["nets_scanned"] = scanned
        missing = drop - set(dropped)
        if missing:
            raise SystemExit(
                "asked to drop %s but %s was not found in the network section.\n"
                "Either the name is misspelled or the exporter quotes it differently --\n"
                "carrying on would leave the router routing a net you meant to remove."
                % (sorted(drop), sorted(missing)))
    report["dropped"] = sorted(dropped)

    out = head + "  (wiring\n" + "".join(kept) + "  )\n)\n"
    if verbose:
        print("wiring entries : %d -> %d kept (%d wire, %d via)"
              % (len(entries), len(kept), nwire, nvia))
        print("nets dropped   : %s" % (report["dropped"] or "none"))
        if drop:
            print("               (a dropped net is NOT routed -- something else must "
                  "close it)")
    return out, report


_MINI = """(pcb b.dsn
  (network
    (net GND
      (pins U1-1 U2-1)
    )
    (net SIG
      (pins U1-2 U2-2)
    )
    (net KEEPME
      (pins U1-3 U2-3)
    )
  )
  (wiring
    (wire(path TopLayer 3.94 100 100 200 200 )
      (net KEEPME)
      (type protect)
    )
    (wire(path TopLayer 3.94 300 300 400 400 )
      (net SIG)
      (type protect)
    )
    (wire(path TopLayer 3.94 500 500 600 600 )
      (net GND)
      (type protect)
    )
    (via via0 700 700
      (net KEEPME)
      (type protect)
    )
  )
)
"""


def _selftest():
    ok = True
    print("dsn_slim selftest")
    out, rep = slim(_MINI, keep=["KEEPME"], drop=["GND"], verbose=False)
    good = rep["wiring_kept"] == 2 and rep["wires"] == 1 and rep["vias"] == 1
    print("  kept only the protected net (1 wire + 1 via)  : %s (%d of %d)"
          % ("OK" if good else "FAIL", rep["wiring_kept"], rep["wiring_in"]))
    ok &= good
    good = rep["dropped"] == ["GND"] and "(net GND\n" not in out
    print("  poured net removed from the network           : %s" % ("OK" if good else "FAIL"))
    ok &= good
    good = "(net SIG\n" in out
    print("  other nets left in the network                : %s" % ("OK" if good else "FAIL"))
    ok &= good
    good = out.rstrip().endswith(")") and out.count("(wiring") == 1
    print("  output still closes its parens                : %s" % ("OK" if good else "FAIL"))
    ok &= good

    try:
        slim(_MINI, keep=["NOSUCHNET"], min_kept=1, verbose=False)
        good = False
    except SystemExit:
        good = True
    print("  empty keep-list is fatal, not silent          : %s" % ("OK" if good else "FAIL"))
    ok &= good

    try:
        slim(_MINI, keep=["KEEPME"], drop=["NOSUCHNET"], verbose=False)
        good = False
    except SystemExit:
        good = True
    print("  drop of a missing net is fatal                : %s" % ("OK" if good else "FAIL"))
    ok &= good
    print("dsn_slim selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def _names(argv, flag):
    if flag not in argv:
        return []
    return [s.strip() for s in argv[argv.index(flag) + 1].split(",") if s.strip()]


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 3:
        print(__doc__)
        return 2
    keep = _names(argv, "--keep")
    drop = _names(argv, "--drop")
    if "--drop-file" in argv:
        with open(argv[argv.index("--drop-file") + 1], encoding="utf-8") as fh:
            drop += [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
    mink = int(argv[argv.index("--min-kept") + 1]) if "--min-kept" in argv else 0
    maxk = int(argv[argv.index("--max-kept") + 1]) if "--max-kept" in argv else None
    with open(argv[1], encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    out, _rep = slim(text, keep=keep, drop=drop, min_kept=mink, max_kept=maxk)
    with open(argv[2], "w", encoding="utf-8") as fh:
        fh.write(out)
    print("wrote %s" % argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
