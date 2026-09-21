# -*- coding: utf-8 -*-
"""Convert an autorouter SES session file back into board copper, offline.

WHAT THIS MEASURES
    Nothing.  It parses and converts.  The verdict on the result belongs to
    route_accept.py, run on the file the EDA HANDS BACK after the import -- never on
    the file that was pushed.

THE FOUR NUMBERS THAT COST REAL TIME
    1. SES RESOLUTION.  The session file declares `(resolution mil 1000)`, so EVERY
       integer in it -- coordinates AND widths -- is 1/1000 mil, while the EDA's own DSN
       numbers are plain mil.  Getting this wrong silently produces 2.5 mm-wide tracks
       that look like a routing disaster rather than a units bug.  This parser reads the
       `(resolution <unit> <n>)` header and refuses a file whose unit it does not know,
       rather than assuming.
    2. `(via <padstack> <x> <y>` HAS NO CLOSING PAREN ON ITS LINE.  A regex written to
       expect one matches nothing and reports "0 vias", which reads like a router that
       chose not to use any.
    3. THE ROUTER QUOTES A NET NAME ONLY WHEN IT NEEDS TO.  `(net "BT_PWR"` and
       `(net VSYS` occur in the SAME file.  A parser matching only the quoted form
       silently dropped 15 nets -- including every power rail -- which then looked like
       a router failure.
    4. PROTECTED COPPER IS ECHOED BACK.  Wiring you protected in the DSN reappears in
       the SES.  Re-adding it duplicates every segment.  `--protected` lists the nets
       already on the board; `--keep-protected` re-adds them if the base lacks them.

THE OTHER TRAP: MERGING A FROM-SCRATCH ROUTE ONTO AN OLD ONE
    When the router routed from scratch (which it does whenever the DSN carried little
    protected wiring), the result knows nothing about the copper still on the board.
    Measured: merging one such SES onto a board that still held its previous 3275 tracks
    produced 1783 clearance violations, with overlaps to -0.15 mm.  `--strip` removes
    the old routing first.  Stripping is only safe when you have checked that every
    strippable record really is routing -- see --strip's own warning below.

WHAT THIS CANNOT SEE
    * Whether the route is good.  Islands, clearance, plane integrity: route_accept.py.
    * Nets that were never in the DSN.  They are not in the SES either, and their
      absence here is invisible.  Tell route_accept.py about them with --expect-open.
    * Whether the EDA will accept the records it writes.  The `easyeda` writer produces
      the record dialect of a .epcb; a different EDA needs a different writer and the
      neutral `json` output is the place to start.

OUTPUT FORMATS
    --format json     neutral wiring JSON: {"segments": [...], "vias": [...]} in mm,
                      with layer NAMES as the SES spells them.  Always available.
    --format easyeda  appends LINE and VIA records to a base .epcb (record dialect),
                      mapping layer names to ids with --layer-map.

HOW IT WAS VALIDATED
    Ported from the converter of a released board; re-parsing that project's own session
    files reproduces its segment, via and per-width counts.  `--selftest` round-trips a
    synthetic SES covering both quoted and bare net names, the paren-less via line, and
    the 1/1000 mil scale.

USAGE
    python3 ses_import.py route.ses --format json  -o wiring.json
                          [--protected "MIPI_D0P,MIPI_D0N"] [--keep-protected]
                          [--forbid-layers "Inner1"]
    python3 ses_import.py route.ses --format easyeda -o out.epcb --base in.epcb
                          --layer-map layers.json [--strip] [--via-pad 0.5]
                          [--via-drill 0.3] [--keep-nets "GND,AGND"]
    python3 ses_import.py --selftest

    layers.json is {"TopLayer": 1, "Inner1": 15, "Inner2": 16, "BottomLayer": 2} --
    the EXAMPLE project's map, measured on that board, not a standard.
"""
from __future__ import print_function

import json
import random
import re
import sys

MIL2MM = 0.0254
MM2MIL = 1.0 / 0.0254

_RES_RE = re.compile(r"\(resolution\s+(\w+)\s+(\d+)\s*\)")
# net name, quoted OR bare -- trap 3
_NET_RE = re.compile(r'\(net\s+(?:"([^"]+)"|([^\s()]+))')
_PATH_RE = re.compile(r"\(path\s+(\S+)\s+([\d.]+)((?:\s+-?[\d.]+)+)\s*\)")
# trap 2: no closing paren on the via line
_VIA_RE = re.compile(r"\(via\s+(\S+)\s+(-?[\d.]+)\s+(-?[\d.]+)")

_UNIT_MM = {"mil": 0.0254, "inch": 25.4, "um": 0.001, "mm": 1.0}


def parse_ses(text):
    """-> (segments, vias, meta).  Lengths in MILLIMETRES.

    segments: [{"net", "layer", "w", "x1", "y1", "x2", "y2"}]
    vias:     [{"net", "padstack", "x", "y"}]
    """
    m = _RES_RE.search(text)
    if not m:
        raise SystemExit("no (resolution ...) in this SES -- refusing to guess the scale")
    unit, denom = m.group(1).lower(), float(m.group(2))
    if unit not in _UNIT_MM:
        raise SystemExit("unknown SES resolution unit %r" % unit)
    scale = _UNIT_MM[unit] / denom          # file integer -> mm
    meta = {"unit": unit, "denominator": denom, "mm_per_count": scale}

    try:
        i = text.index("(network_out")
    except ValueError:
        raise SystemExit("no (network_out section -- this is not a routed session file")
    body = text[i:]

    segments, vias = [], []
    for nm in _NET_RE.finditer(body):
        net = nm.group(1) or nm.group(2)
        # walk parens to find this net block's extent; a non-greedy regex swallows the
        # whole file because the blocks nest.
        j = nm.end()
        depth = 1
        n = len(body)
        while depth and j < n:
            ch = body[j]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            j += 1
        block = body[nm.end():j]
        for w in _PATH_RE.finditer(block):
            layer = w.group(1)
            width = float(w.group(2)) * scale
            nums = [float(c) * scale for c in w.group(3).split()]
            xy = [(nums[k], nums[k + 1]) for k in range(0, len(nums) - 1, 2)]
            for a, b in zip(xy, xy[1:]):
                if a != b:
                    segments.append({"net": net, "layer": layer, "w": width,
                                     "x1": a[0], "y1": a[1], "x2": b[0], "y2": b[1]})
        for v in _VIA_RE.finditer(block):
            vias.append({"net": net, "padstack": v.group(1),
                         "x": float(v.group(2)) * scale, "y": float(v.group(3)) * scale})
    return segments, vias, meta


def filter_wiring(segments, vias, protected=(), keep_protected=False,
                  forbid_layers=(), verbose=True):
    protected = set(protected)
    forbid = set(forbid_layers)
    if verbose:
        print("SES parsed  : %d segments, %d vias, %d nets"
              % (len(segments), len(vias),
                 len({s["net"] for s in segments} | {v["net"] for v in vias})))
    if protected and not keep_protected:
        ns, nv = len(segments), len(vias)
        segments = [s for s in segments if s["net"] not in protected]
        vias = [v for v in vias if v["net"] not in protected]
        if verbose:
            print("dropped protected copper already on the board: %d segments, %d vias"
                  % (ns - len(segments), nv - len(vias)))
    bad = [s for s in segments if s["layer"] in forbid]
    if bad:
        raise SystemExit(
            "the router put %d segment(s) on forbidden layer(s) %s.\n"
            "If that is a solid reference plane, the DSN did not declare it as one --\n"
            "see dsn_rewrite.py edit 1.  The board is not routable as this SES stands."
            % (len(bad), sorted({s['layer'] for s in bad})))
    return segments, vias


# --------------------------------------------------------------- EasyEDA record writer

def _load_records(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read().split("\n")


def strip_routing(lines, keep_nets=(), protected=(), verbose=True):
    """Remove LINE and VIA records, keeping protected copper and named nets' vias.

    WARNING, and it is not a small one: this is only safe when EVERY LINE record in the
    document is copper.  On the reference board that was checked and true -- there was
    no silkscreen or outline geometry among them, and every LINE carried a net name.
    Check yours before trusting --strip.  Records without a parseable body are kept.
    """
    keep_nets = set(keep_nets)
    protected = set(protected)
    out, dl, dv = [], 0, 0
    dec = json.JSONDecoder()
    for ln in lines:
        st = ln.strip()
        if not st:
            out.append(ln)
            continue
        h, _sep, b = st.partition("||")
        try:
            t = json.loads(h).get("type")
        except Exception:
            out.append(ln)
            continue
        if t not in ("LINE", "VIA"):
            out.append(ln)
            continue
        try:
            body, _e = dec.raw_decode(b.rstrip("|"))
        except Exception:
            out.append(ln)
            continue
        net = body.get("netName")
        if net in protected:
            out.append(ln)
            continue
        if t == "VIA" and net in keep_nets:
            out.append(ln)
            continue
        if t == "LINE":
            dl += 1
        else:
            dv += 1
    if verbose:
        print("stripped previous routing: -%d LINE, -%d VIA "
              "(kept protected copper and %s vias)"
              % (dl, dv, "/".join(sorted(keep_nets)) or "no"))
    return out


def write_easyeda(base_path, out_path, segments, vias, layer_map,
                  via_pad=0.5, via_drill=0.3, strip=False, keep_nets=(),
                  protected=(), seed=0, verbose=True):
    lines = _load_records(base_path)
    if strip:
        lines = strip_routing(lines, keep_nets=keep_nets, protected=protected,
                              verbose=verbose)
    unknown = {s["layer"] for s in segments} - set(layer_map)
    if unknown:
        raise SystemExit("SES uses layer(s) %s that --layer-map does not name"
                         % sorted(unknown))
    if lines and not lines[-1].endswith("|"):
        lines[-1] += "|"
    ticket = 0
    for ln in lines:
        if not ln.strip():
            continue
        try:
            ticket = max(ticket, json.loads(ln.partition("||")[0]).get("ticket", 0) or 0)
        except Exception:
            pass
    ticket += 1
    rng = random.Random(seed)
    new = []

    def push(t, body):
        nonlocal_ticket[0] += 1
        h = {"type": t, "ticket": nonlocal_ticket[0],
             "id": "%016x" % rng.getrandbits(64)}
        new.append(json.dumps(h, separators=(",", ":")) + "||"
                   + json.dumps(body, separators=(",", ":")) + "|")

    nonlocal_ticket = [ticket - 1]
    for s in segments:
        push("LINE", {"partitionId": "", "groupId": 0, "netName": s["net"],
                      "layerId": layer_map[s["layer"]],
                      "startX": round(s["x1"] * MM2MIL, 4),
                      "startY": round(s["y1"] * MM2MIL, 4),
                      "endX": round(s["x2"] * MM2MIL, 4),
                      "endY": round(s["y2"] * MM2MIL, 4),
                      "width": round(s["w"] * MM2MIL, 4),
                      "locked": False, "zIndex": -1})
    for v in vias:
        push("VIA", {"partitionId": "", "groupId": 0, "netName": v["net"],
                     "ruleName": "",
                     "centerX": round(v["x"] * MM2MIL, 4),
                     "centerY": round(v["y"] * MM2MIL, 4),
                     "holeDiameter": round(via_drill * MM2MIL, 4),
                     "viaDiameter": round(via_pad * MM2MIL, 4),
                     "viaType": "NORMAL",
                     "topSolderExpansion": None, "bottomSolderExpansion": None,
                     "locked": False, "unusedInnerLayers": []})
    if new:
        new[-1] = new[-1][:-1]
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(lines + new))
    if verbose:
        hist = {}
        for s in segments:
            k = round(s["w"], 3)
            hist[k] = hist.get(k, 0) + 1
        print("wrote %s  (+%d LINE, +%d VIA)" % (out_path, len(segments), len(vias)))
        print("widths laid (mm): %s" % {k: hist[k] for k in sorted(hist)})


# --------------------------------------------------------------------------- selftest

_MINI_SES = """(session route.ses
  (base_design board.dsn)
  (placement
    (resolution mil 1000)
  )
  (was_is
  )
  (routes
    (resolution mil 1000)
    (parser
      (host_cad "EDA")
    )
    (network_out
      (net "QUOTED_NET"
        (wire
          (path TopLayer 3937
            0 0
            39370 0
          )
        )
        (via via0 39370 0
        )
      )
      (net BARE_NET
        (wire
          (path BottomLayer 7874
            0 39370
            39370 39370
          )
        )
      )
      (net PROTECTED_NET
        (wire
          (path TopLayer 3937
            0 78740
            39370 78740
          )
        )
      )
    )
  )
)
"""


def _selftest():
    ok = True
    print("ses_import selftest")
    segs, vias, meta = parse_ses(_MINI_SES)
    good = abs(meta["mm_per_count"] - 0.0254 / 1000.0) < 1e-15
    print("  resolution read from the file (1/1000 mil)    : %.3g mm/count  %s"
          % (meta["mm_per_count"], "OK" if good else "FAIL"))
    ok &= good

    nets = sorted({s["net"] for s in segs})
    good = nets == ["BARE_NET", "PROTECTED_NET", "QUOTED_NET"]
    print("  quoted AND bare net names both parsed (trap 3): %s  %s"
          % (nets, "OK" if good else "FAIL"))
    ok &= good

    good = len(vias) == 1 and vias[0]["net"] == "QUOTED_NET"
    print("  via with no closing paren parsed (trap 2)     : %d via  %s"
          % (len(vias), "OK" if good else "FAIL"))
    ok &= good

    s0 = [s for s in segs if s["net"] == "QUOTED_NET"][0]
    good = abs(s0["w"] - 0.1) < 1e-5 and abs(s0["x2"] - 1.0) < 1e-5
    print("  width 3937 -> %.4f mm, x 39370 -> %.4f mm     : %s"
          % (s0["w"], s0["x2"], "OK" if good else "FAIL"))
    ok &= good
    # the fault this guards: reading the SES integers at the DSN's plain-mil scale.
    # On the reference board that turned 0.1 mm tracks into 2.5 mm ones; here the same
    # mistake would give the absurd number below, which is the point -- it is a scale
    # error, and scale errors are only obvious when you print them.
    print("  (at the DSN's plain-mil scale that width reads %.3f mm -- the units bug)"
          % (3937 * 0.0254))

    segs2, vias2 = filter_wiring(segs, vias, protected=["PROTECTED_NET"], verbose=False)
    good = "PROTECTED_NET" not in {s["net"] for s in segs2}
    print("  protected copper not re-added (trap 4)        : %s" % ("OK" if good else "FAIL"))
    ok &= good

    try:
        filter_wiring(segs, vias, forbid_layers=["TopLayer"], verbose=False)
        good = False
    except SystemExit:
        good = True
    print("  copper on a forbidden plane layer is fatal    : %s" % ("OK" if good else "FAIL"))
    ok &= good

    # easyeda writer round trip
    import tempfile
    import os
    tmp = tempfile.mkdtemp(prefix="pcbkit-")
    base = os.path.join(tmp, "base.epcb")
    open(base, "w", encoding="utf-8").write(
        '{"type":"DOCHEAD"}||{"docType":"PCB","uuid":"X"}|\n'
        '{"type":"LINE","ticket":5,"id":"old1"}||{"netName":"OLD","layerId":1,'
        '"startX":0,"startY":0,"endX":10,"endY":0,"width":4}|')
    outp = os.path.join(tmp, "out.epcb")
    write_easyeda(base, outp, segs2, vias2, {"TopLayer": 1, "BottomLayer": 2},
                  strip=True, verbose=False)
    txt = open(outp, encoding="utf-8").read()
    good = '"netName":"OLD"' not in txt and '"netName":"BARE_NET"' in txt
    print("  --strip removed old copper, added the new     : %s" % ("OK" if good else "FAIL"))
    ok &= good
    good = '"width":3.937' in txt
    print("  0.10 mm written back as %s mil                : %s"
          % ("3.937", "OK" if good else "FAIL"))
    ok &= good

    print("ses_import selftest: %s" % ("PASS" if ok else "FAIL"))
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

    def opt(flag, default=None):
        return argv[argv.index(flag) + 1] if flag in argv else default

    with open(argv[1], encoding="utf-8", errors="replace") as fh:
        segs, vias, meta = parse_ses(fh.read())
    print("SES resolution: %s 1/%g  ->  %.6g mm per count"
          % (meta["unit"], meta["denominator"], meta["mm_per_count"]))
    protected = _names(argv, "--protected")
    segs, vias = filter_wiring(segs, vias, protected=protected,
                               keep_protected=("--keep-protected" in argv),
                               forbid_layers=_names(argv, "--forbid-layers"))
    fmt = opt("--format", "json")
    out = opt("-o") or opt("--out")
    if not out:
        raise SystemExit("-o OUTPUT is required")
    if fmt == "json":
        with open(out, "w", encoding="utf-8") as fh:
            json.dump({"units": "mm", "meta": meta,
                       "segments": segs, "vias": vias}, fh, indent=1)
        print("wrote %s (%d segments, %d vias)" % (out, len(segs), len(vias)))
        return 0
    if fmt == "easyeda":
        base = opt("--base")
        lm = opt("--layer-map")
        if not base or not lm:
            raise SystemExit("--format easyeda needs --base and --layer-map")
        with open(lm, encoding="utf-8") as fh:
            layer_map = json.load(fh)
        write_easyeda(base, out, segs, vias, layer_map,
                      via_pad=float(opt("--via-pad", 0.5)),
                      via_drill=float(opt("--via-drill", 0.3)),
                      strip=("--strip" in argv),
                      keep_nets=_names(argv, "--keep-nets"),
                      protected=protected)
        return 0
    raise SystemExit("unknown --format %r" % fmt)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
