# -*- coding: utf-8 -*-
"""Rewrite an EDA-exported Specctra DSN so an autorouter routes the board you designed.

WHAT THIS DOES
    Patches an existing .dsn in place-of-export.  It does not generate a DSN from
    scratch -- the EDA's own exporter knows the pad stacks and the netlist, and
    re-deriving those is exactly the kind of second source that should be CHECKED, not
    trusted.  Four edits, each one paid for on a real board:

    1. SOLID INNER PLANES BECOME `(type power)`.
       EasyEDA exports a solid GND plane as `(type signal)`.  A router given that will
       cut the reference plane to pieces, and every impedance-controlled pair on the
       board loses its reference.  `(type power)` layers are not routed on.
       If the assertion that the layer block was found fails, STOP -- the export format
       changed and every other edit below is now suspect.

    2. PER-NET WIDTHS.
       Every class is exported with one default width.  Widths that are set by PHYSICS
       (impedance, IPC-2221 current) rather than by routing convenience must be pinned
       per class, or dropping the default silently halves them.

    3. CLASS MEMBERS ARE EMITTED BARE.
       This is the expensive one.  EasyEDA writes `(class X 'X' ...)` -- the net name
       SINGLE-QUOTED.  FreeRouting then binds the class to nothing, and every net comes
       back at the structure default width.  A 40-minute run was lost to this before it
       was noticed, with a nominally-90-ohm USB pair routed at ~120 ohm.  The rewritten
       class emits the member bare: `(class X X ...)`.

    4. OPTIONAL BOARD-EDGE KEEPOUT RING.
       A router honours only the CLASS clearance from the DSN boundary, not the board's
       own edge rule.  Measured: with a 0.115 mm class clearance it placed a via 0.2036
       mm from the outline against a 0.29972 mm edge rule.  Insetting the boundary
       polygon instead makes FreeRouting fail on load ("Polyline: must contain at least
       2 different points", then an NPE), so the cure is a keepout RING on every copper
       layer.  ring + clearance is the real edge margin you get.

WHAT THIS CANNOT SEE
    * Whether the router obeyed any of it.  The DSN is a request.  The only evidence is
      the routed board read back and measured -- route_accept.py and verify/.
    * Whether a width is physically right.  It writes the number you give it.
    * Nets that do not appear as a `(class ...)` block.  The rewrite counts what it
      changed and asserts a floor (`--min-classes`); a silent zero-match regex is how
      this whole family of faults hides.
    * Anything about the placement.  A width the channels cannot hold will simply not
      route -- run placement/channels.py FIRST and read the lane histogram.

A NOTE ON ASKING FOR THE EXACT RULE
    FreeRouting works in 1/1000 mil integers and lands tracks EXACTLY on whatever
    clearance the DSN asks for.  Asking for the board's own rule therefore produced gaps
    0.1 to 1.6 micrometres SHORT of it.  Ask for a little more than the rule in the DSN
    (`clearance`), and measure the finished board against the real rule.

HOW IT WAS VALIDATED
    Ported from the DSN rewriter of a released 4-layer board; the class-binding fix is
    the difference between "every track at the default width" and the widths the design
    review approved.  `--selftest` builds a miniature DSN in memory and checks each edit.

USAGE
    python3 dsn_rewrite.py in.dsn out.dsn [--config route.json] [--min-classes 1]
    python3 dsn_rewrite.py --selftest

CONFIG (all lengths in MILLIMETRES; the DSN is written in mil)
    {
      "plane_layers":     ["Inner1"],
      "default_width":    0.10,
      "clearance":        0.115,
      "widths":           {"USB_DP": 0.20, "VSYS": 0.30},
      "width_patterns":   [["^MIPI_", 0.19]],
      "extra_clearance":  {"HV_RAIL": 0.30},
      "edge_keepout":     {"ring": 0.20, "board": [41.4, 100.0],
                           "layers": ["TopLayer","Inner1","Inner2","BottomLayer"]}
    }
    The numbers above are the EXAMPLE project's, shown so the shape is clear.  They are
    not defaults you should inherit -- every one of them is a property of that board.
"""
from __future__ import print_function

import json
import re
import sys

MM2MIL = 1.0 / 0.0254

DEFAULT_CONFIG = {
    "plane_layers": [],
    "default_width": 0.10,
    "clearance": 0.102,
    "widths": {},
    "width_patterns": [],
    "extra_clearance": {},
    "edge_keepout": None,
}

CLASS_RE = re.compile(
    r"\(class (?P<cls>\S+) '(?P<net>[^']*)'\s*\n"
    r"\s*\(circuit\s*\n\s*\(use_via (?P<via>[^)]*)\)\s*\n\s*\)\s*\n"
    r"\s*\(rule\s*\n\s*\(width [\d.]+\)\s*\n\s*\(clearance [\d.]+\)\s*\n\s*\)\s*\n\s*\)")


def width_for(net, cfg):
    if net in cfg["widths"]:
        return cfg["widths"][net]
    for pat, w in cfg["width_patterns"]:
        if re.search(pat, net):
            return w
    return cfg["default_width"]


def rewrite(text, cfg, min_classes=1, verbose=True):
    report = {"planes": [], "classes": 0, "widths": {}, "extra_clearance": 0,
              "keepouts": 0}

    # ---- 1. solid planes
    for name in cfg["plane_layers"]:
        pat = "(layer %s\n      (type signal)" % name
        if pat not in text:
            raise SystemExit(
                "plane layer %r not found as '(type signal)'.  Either it is already a\n"
                "power layer, or the export format changed -- STOP and look, because\n"
                "every other edit in this file is now unverified." % name)
        text = text.replace(pat, "(layer %s\n      (type power)" % name)
        report["planes"].append(name)

    # ---- 4. board-edge keepout ring (before the class rewrite; it edits the structure)
    ko = cfg.get("edge_keepout")
    if ko:
        ring = float(ko["ring"]) * MM2MIL
        bx = float(ko["board"][0]) * MM2MIL
        by = float(ko["board"][1]) * MM2MIL
        rects = [(0, 0, bx, ring), (0, by - ring, bx, by),
                 (0, 0, ring, by), (bx - ring, 0, bx, by)]
        lines = []
        for lname in ko["layers"]:
            for x0, y0, x1, y1 in rects:
                lines.append('    (keepout "" (rect %s %.4f %.4f %.4f %.4f))'
                             % (lname, x0, y0, x1, y1))
        anchor = "    (layer %s" % ko["layers"][0]
        if anchor not in text:
            raise SystemExit("keepout anchor %r not found in the DSN" % anchor)
        text = text.replace(anchor, "\n".join(lines) + "\n" + anchor, 1)
        report["keepouts"] = len(lines)

    # ---- 2 + 3. per-class width, clearance, and BARE member names
    def fix(m):
        net = m.group("net")
        w = width_for(net, cfg)
        c = cfg["extra_clearance"].get(net, cfg["clearance"])
        report["classes"] += 1
        report["widths"][round(w, 4)] = report["widths"].get(round(w, 4), 0) + 1
        if net in cfg["extra_clearance"]:
            report["extra_clearance"] += 1
        # THE NET NAME IS EMITTED BARE.  See edit 3 in the module docstring.
        return ("(class %s %s\n      (circuit \n        (use_via %s)\n      )\n"
                "      (rule \n        (width %.4f)\n        (clearance %.4f)\n      )\n    )"
                % (m.group("cls"), net, m.group("via"), w * MM2MIL, c * MM2MIL))

    text, n = CLASS_RE.subn(fix, text)
    if n < min_classes:
        raise SystemExit(
            "only %d net class(es) rewritten, expected at least %d.\n"
            "A regex that matches nothing is indistinguishable from a file that needed\n"
            "no change -- which is why this is an error and not a warning." % (n, min_classes))

    # ---- structure-level defaults follow the same numbers.
    # Exporters write these either as one chained rule -- (rule(width W)(clear C)...) --
    # or as separate (rule(width W)) / (rule(clear C)) forms.  These substitutions match
    # the TOKENS, not the whole rule, so both shapes are handled.  `(clear ...)` is the
    # structure spelling; a net class uses `(clearance ...)`, which is left alone here.
    cl = cfg["clearance"] * MM2MIL
    dw = cfg["default_width"] * MM2MIL
    text = re.sub(r"\(rule\(width [\d.]+\)", "(rule(width %.4f)" % dw, text, count=1)
    text = re.sub(r"\(clear [\d.]+ \(type ([A-Za-z_]+)\)\)",
                  lambda m: "(clear %.4f (type %s))" % (cl, m.group(1)), text)
    text = re.sub(r"\(clear [\d.]+\)", "(clear %.4f)" % cl, text)

    if verbose:
        print("plane layers -> (type power) : %s" % (report["planes"] or "none"))
        print("net classes rewritten        : %d" % report["classes"])
        print("width histogram (mm)         : %s"
              % {k: v for k, v in sorted(report["widths"].items())})
        print("nets with extra clearance    : %d" % report["extra_clearance"])
        print("board-edge keepout rects     : %d" % report["keepouts"])
        if ko:
            print("  -> closest routed copper to the real edge will be %.4f mm"
                  % (float(ko["ring"]) + cfg["clearance"]))
    return text, report


def load_config(path):
    cfg = dict(DEFAULT_CONFIG)
    if path:
        with open(path, encoding="utf-8") as fh:
            cfg.update(json.load(fh))
    return cfg


_MINI_DSN = """(pcb board.dsn
  (parser
    (string_quote ")
    (space_in_quoted_tokens on)
    (host_cad "EDA")
  )
  (resolution mil 1000)
  (structure
    (layer TopLayer
      (type signal)
    )
    (layer Inner1
      (type signal)
    )
    (layer BottomLayer
      (type signal)
    )
    (boundary (rect pcb 0 0 1630 3937))
    (via "via0")
    (rule(width 10)(clear 4.02)(clear 4.02 (type default_smd))(clear 4.02 (type smd_smd)))
  )
  (placement
  )
  (library
  )
  (network
    (net 'GND'
      (pins U1-1 U2-1)
    )
    (net 'USB_DP'
      (pins U1-2 J1-1)
    )
    (net 'MIPI_D0P'
      (pins U1-3 J2-1)
    )
    (class GND 'GND'
      (circuit 
        (use_via via0)
      )
      (rule 
        (width 10.0000)
        (clearance 4.0200)
      )
    )
    (class USB_DP 'USB_DP'
      (circuit 
        (use_via via0)
      )
      (rule 
        (width 10.0000)
        (clearance 4.0200)
      )
    )
    (class MIPI_D0P 'MIPI_D0P'
      (circuit 
        (use_via via0)
      )
      (rule 
        (width 10.0000)
        (clearance 4.0200)
      )
    )
  )
  (wiring
  )
)
"""


def _selftest():
    ok = True
    print("dsn_rewrite selftest")
    cfg = dict(DEFAULT_CONFIG)
    cfg.update({
        "plane_layers": ["Inner1"],
        "default_width": 0.10,
        "clearance": 0.115,
        "widths": {"USB_DP": 0.20, "GND": 0.30},
        "width_patterns": [["^MIPI_", 0.19]],
        "extra_clearance": {"GND": 0.30},
        "edge_keepout": {"ring": 0.20, "board": [41.4, 100.0],
                         "layers": ["TopLayer", "Inner1", "BottomLayer"]},
    })
    out, rep = rewrite(_MINI_DSN, cfg, min_classes=3, verbose=False)

    good = "(layer Inner1\n      (type power)" in out
    print("  solid plane became (type power)               : %s" % ("OK" if good else "FAIL"))
    ok &= good
    good = "(layer TopLayer\n      (type signal)" in out
    print("  signal layers left alone                      : %s" % ("OK" if good else "FAIL"))
    ok &= good

    good = "(class USB_DP USB_DP" in out and "'USB_DP'" not in out.split("(class")[2]
    print("  class member emitted BARE (the 40-minute fault): %s" % ("OK" if good else "FAIL"))
    ok &= good
    good = "'" not in re.sub(r"\(net '[^']*'", "", out).split("(class")[1]
    print("  ...no single quotes left inside any class     : %s" % ("OK" if good else "FAIL"))
    ok &= good

    m = re.search(r"\(class USB_DP USB_DP.*?\(width ([\d.]+)\)", out, re.S)
    w = float(m.group(1)) * 0.0254
    good = abs(w - 0.20) < 1e-6
    print("  USB_DP width 0.20 mm -> %.4f mil               : %s"
          % (float(m.group(1)), "OK" if good else "FAIL"))
    ok &= good
    m = re.search(r"\(class MIPI_D0P MIPI_D0P.*?\(width ([\d.]+)\)", out, re.S)
    good = abs(float(m.group(1)) * 0.0254 - 0.19) < 1e-6
    print("  MIPI_ pattern width 0.19 mm                   : %s" % ("OK" if good else "FAIL"))
    ok &= good
    m = re.search(r"\(class GND GND.*?\(clearance ([\d.]+)\)", out, re.S)
    good = abs(float(m.group(1)) * 0.0254 - 0.30) < 1e-6
    print("  GND extra clearance 0.30 mm                   : %s" % ("OK" if good else "FAIL"))
    ok &= good

    good = rep["keepouts"] == 12 and out.count("(keepout") == 12
    print("  edge keepout: 3 layers x 4 rects = %d          : %s"
          % (rep["keepouts"], "OK" if good else "FAIL"))
    ok &= good

    good = "(rule(width 3.9370)" in out and "(clear 4.5276)" in out
    print("  structure defaults follow (width + clear)     : %s" % ("OK" if good else "FAIL"))
    ok &= good

    # a config that matches nothing must ERROR, not pass quietly
    try:
        rewrite(_MINI_DSN.replace("(class", "(klass"), cfg, min_classes=3, verbose=False)
        good = False
    except SystemExit:
        good = True
    print("  zero matched classes raises, not warns        : %s" % ("OK" if good else "FAIL"))
    ok &= good

    print("dsn_rewrite selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 3:
        print(__doc__)
        return 2
    cfg = load_config(argv[argv.index("--config") + 1] if "--config" in argv else None)
    minc = int(argv[argv.index("--min-classes") + 1]) if "--min-classes" in argv else 1
    with open(argv[1], encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    out, _rep = rewrite(text, cfg, min_classes=minc)
    with open(argv[2], "w", encoding="utf-8") as fh:
        fh.write(out)
    print("wrote %s" % argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
