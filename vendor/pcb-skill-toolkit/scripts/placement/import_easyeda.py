# -*- coding: utf-8 -*-
"""Adapter: an EasyEDA Pro export -> the neutral board JSON of boardmodel.py.

WHAT THIS MEASURES
    Nothing.  It translates.  Every downstream gate in this toolkit reads board JSON,
    so porting the toolkit to another EDA means writing a sibling of THIS file only.

    Two on-disk dialects are handled, auto-detected from the first non-blank line:
      RECORD form  `{"type":"PAD",...}||{...}|`   -- what `document_save_to_file` writes
                                                     for a single .epcb / .epru document
      ARRAY  form  `["PAD",id,...]`               -- what `project_export_file` writes
                                                     inside a .epro archive (NDJSON per
                                                     document, one file per PCB/FOOTPRINT)
    Give it any number of paths and/or directories; footprint documents and the PCB
    document may live in separate files.

WHAT THIS CANNOT SEE
    * Schematic nets.  `pad_nets` comes from the PCB's own PAD_NET records, i.e. what
      the board holds.  To get `nets` (what the schematic INTENDS) export the netlist
      separately and merge it with --netlist; `verify/pad_reconcile.py` then compares
      the two.  Without --netlist the reconciliation cannot run, by design: this adapter
      must not invent the second opinion it is supposed to be checked against.
    * Pour FILL geometry in the record dialect is carried through only when present;
      an unpoured board simply has none.  Placement gates do not use it.
    * Anything the exporter omitted.  A footprint with no assembly outline arrives with
      `outline: null` and boardmodel falls back to silk, which it reports.
    * Arcs are flattened to `arc_segments` chords (default 12 per arc).  A tighter
      number costs time; a looser one understates a curved courtyard.

TRAPS THIS FILE ENCODES (each cost real time on the reference project)
    1. A pad is keyed to its net by the footprint ELEMENT id, not by the pad NUMBER.
       They coincide for most parts and do NOT for a USB-C receptacle whose four shell
       legs all carry pad number "1"; keying by number put a net on the wrong pin.
       Both keys are emitted (`num` and `elem`) so a consumer can choose.
    2. `padAngle` is the pad's real render rotation.  A "relativeAngle" field, where the
       format has one, is NOT the rotation -- reading it made half a module's pads
       overlap.
    3. A drilled slot can be WIDER than the pad carrying it (measured: 1.7 mm slots
       inside 1.0 mm pads), so hole geometry must reach the courtyard union.
    4. A zero-width `hole` dict is not a hole; 88 SMD lands each carried one.
    5. Stored units are MIL in both dialects, including inside footprint documents whose
       CANVAS record claims "mm".  Everything is converted to mm here, once.

HOW IT WAS VALIDATED
    Run against two real exports of the same released board -- one record-dialect .epcb
    and one array-dialect .epro tree -- the component count, pad count, drill census and
    net set produced from the two agree with each other and with the two independent
    board models written for that project.  `--selftest` round-trips synthetic records
    of both dialects through the parser.

USAGE
    python3 import_easyeda.py OUT.json PATH [PATH ...] [--netlist netlist.json]
                              [--rules rules.json] [--layers layers.json]
                              [--arc-segments 12]
    PATH may be a file or a directory (searched recursively for .epcb/.epru/.efoo/.json).
"""
from __future__ import print_function

import json
import math
import os
import sys

MIL = 0.0254                     # mm per mil
_DEC = json.JSONDecoder()

FOOTPRINT_EXT = (".efoo", ".epru", ".epcb", ".json", ".txt")


# --------------------------------------------------------------------------- readers

def _iter_lines(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            s = line.strip()
            if s:
                yield s


def detect_dialect(path):
    for s in _iter_lines(path):
        if s.startswith("["):
            return "array"
        if s.startswith("{"):
            return "record"
        return "unknown"
    return "empty"


def read_record_docs(path):
    """RECORD dialect -> [(dochead, [(header, body), ...]), ...].

    One file may hold several documents; a DOCHEAD record starts each.
    """
    docs = []
    cur_head, cur_recs = None, None
    for s in _iter_lines(path):
        h, _sep, b = s.partition("||")
        b = b.rstrip("|")
        try:
            hh = json.loads(h)
        except Exception:
            continue
        bb = {}
        if b:
            try:
                bb, _e = _DEC.raw_decode(b)
            except Exception:
                bb = {}
        if hh.get("type") == "DOCHEAD":
            if cur_head is not None:
                docs.append((cur_head, cur_recs))
            cur_head, cur_recs = bb, []
            continue
        if cur_recs is None:
            cur_head, cur_recs = {}, []
        cur_recs.append((hh, bb))
    if cur_head is not None:
        docs.append((cur_head, cur_recs))
    return docs


def read_array_doc(path):
    """ARRAY dialect -> (doctype, head_dict, [row, ...])."""
    rows = []
    doctype, head = None, {}
    for s in _iter_lines(path):
        try:
            r = json.loads(s)
        except Exception:
            continue
        if not isinstance(r, list) or not r:
            continue
        if r[0] == "DOCTYPE":
            doctype = r[1] if len(r) > 1 else None
            continue
        if r[0] == "HEAD":
            head = r[1] if len(r) > 1 and isinstance(r[1], dict) else {}
            continue
        rows.append(r)
    return doctype, head, rows


# --------------------------------------------------------------------------- geometry

def flatten_path(path, arc_segments=12):
    """EasyEDA path token list -> [(x, y)] in stored units.

    Tokens: bare coordinate pairs, 'L' (line-to, skipped), and
    ['ARC', sweepAngleDeg, endX, endY].
    """
    pts = []
    i = 0
    n = len(path)
    cur = None
    while i < n:
        v = path[i]
        if v == "L":
            i += 1
            continue
        if v == "ARC":
            ang = float(path[i + 1])
            ex, ey = float(path[i + 2]), float(path[i + 3])
            if cur is not None and abs(ang) > 1e-9:
                sx, sy = cur
                a = math.radians(ang)
                dx, dy = ex - sx, ey - sy
                chord = math.hypot(dx, dy)
                if chord > 1e-12 and abs(math.sin(a / 2.0)) > 1e-12:
                    r = chord / (2.0 * math.sin(abs(a) / 2.0))
                    hgt = math.sqrt(max(r * r - (chord / 2.0) ** 2, 0.0))
                    mx, my = (sx + ex) / 2.0, (sy + ey) / 2.0
                    nx, ny = -dy / chord, dx / chord
                    sign = 1.0 if a > 0 else -1.0
                    if abs(a) > math.pi:
                        sign = -sign
                    ccx, ccy = mx + sign * nx * hgt, my + sign * ny * hgt
                    a0 = math.atan2(sy - ccy, sx - ccx)
                    for k in range(1, arc_segments + 1):
                        aa = a0 + a * k / arc_segments
                        pts.append((ccx + r * math.cos(aa), ccy + r * math.sin(aa)))
                else:
                    pts.append((ex, ey))
            else:
                pts.append((ex, ey))
            cur = (ex, ey)
            i += 4
            continue
        x, y = float(path[i]), float(path[i + 1])
        pts.append((x, y))
        cur = (x, y)
        i += 2
    return pts


def _geom_points(body, arc_segments):
    """Every coordinate a record-dialect drawing primitive mentions, in stored units."""
    out = []
    p = body.get("path")
    if p:
        segs = p if (p and isinstance(p[0], list)) else [p]
        for seg in segs:
            if seg and isinstance(seg[0], str) and seg[0] in ("CIRCLE", "RECT"):
                out += _shape_points(seg, arc_segments)
                continue
            try:
                out += flatten_path(seg, arc_segments)
            except Exception:
                nums = [v for v in seg if isinstance(v, (int, float))]
                out += [(nums[i], nums[i + 1]) for i in range(0, len(nums) - 1, 2)]
    for ax, ay in (("startX", "startY"), ("endX", "endY"),
                   ("centerX", "centerY"), ("x", "y")):
        if isinstance(body.get(ax), (int, float)) and isinstance(body.get(ay), (int, float)):
            out.append((body[ax], body[ay]))
    r = body.get("radius")
    if isinstance(r, (int, float)) and r and isinstance(body.get("centerX"), (int, float)):
        cx, cy = body["centerX"], body["centerY"]
        out += [(cx - r, cy - r), (cx + r, cy + r)]
    return out


def _shape_points(sh, arc_segments):
    """One entry of an array-dialect FILL shape list -> points."""
    if not sh:
        return []
    if sh[0] == "CIRCLE":
        cx, cy, r = float(sh[1]), float(sh[2]), float(sh[3])
        return [(cx + r * math.cos(2 * math.pi * k / 24),
                 cy + r * math.sin(2 * math.pi * k / 24)) for k in range(24)]
    if sh[0] == "RECT":
        x, y, w, h = (float(v) for v in sh[1:5])
        return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    if sh[0] in ("POLY", "PATH"):
        return flatten_path(sh[1], arc_segments)
    if isinstance(sh[0], (int, float)):
        return flatten_path(sh, arc_segments)
    return []


def rot_rect_bbox(cx, cy, w, h, ang_deg):
    a = math.radians(ang_deg or 0.0)
    c, s = abs(math.cos(a)), abs(math.sin(a))
    hw = (w * c + h * s) / 2.0
    hh = (w * s + h * c) / 2.0
    return (cx - hw, cy - hh, cx + hw, cy + hh)


# --------------------------------------------------------------------------- footprints

def _fp_from_record(head, recs, layers, arc_segments):
    uuid = head.get("uuid") or head.get("title") or "?"
    name = head.get("title") or uuid
    outline_pts, silk_pts = [], []
    pads, npth = [], []
    seen = {}
    for h, b in recs:
        t = h.get("type")
        lid = b.get("layerId")
        if t == "META":
            if b.get("title"):
                name = b["title"]
            continue
        if t == "PAD":
            dp = b.get("defaultPad") or {}
            cx = (b.get("centerX") or 0.0) + (b.get("padOffsetX") or 0.0)
            cy = (b.get("centerY") or 0.0) + (b.get("padOffsetY") or 0.0)
            hole = b.get("hole") or {}
            hw = float(hole.get("width") or 0.0)
            hh = float(hole.get("height") or 0.0)
            num = str(b.get("num", ""))
            rec = {
                "num": num,
                "elem": h.get("id"),
                "x": cx * MIL, "y": cy * MIL,
                "w": float(dp.get("width") or 0.0) * MIL,
                "h": float(dp.get("height") or 0.0) * MIL,
                "angle": float(b.get("padAngle") or 0.0),
                "shape": dp.get("padType", "RECT"),
                "corner_radius": float(dp.get("cornerRadius") or 0.0) * MIL,
                "layer": lid,
            }
            if hw > 0.0 or hh > 0.0:
                rec["hole"] = {"w": hw * MIL, "h": max(hh, hw) * MIL,
                               "plated": bool(b.get("plated", True))}
            # trap 1: several lands may share one pad NUMBER; keep them all, keyed by elem
            key = (num, h.get("id"))
            if key not in seen:
                seen[key] = True
                pads.append(rec)
            continue
        if t in ("POLY", "LINE", "ARC", "FILL", "REGION", "CIRCLE", "RECT", "SOLIDREGION"):
            if lid == layers["assembly_outline"]:
                outline_pts += _geom_points(b, arc_segments)
            elif lid in layers["silkscreen"]:
                silk_pts += _geom_points(b, arc_segments)
            elif lid == layers["multi"]:
                # NPTH locating posts: real drill hits that obstruct BOTH faces
                p = b.get("path")
                subs = p if (p and isinstance(p[0], list)) else ([p] if p else [])
                for sub in subs:
                    if sub and sub[0] == "CIRCLE" and len(sub) >= 4:
                        npth.append({"x": float(sub[1]) * MIL, "y": float(sub[2]) * MIL,
                                     "d": float(sub[3]) * 2.0 * MIL})
                outline_pts += _geom_points(b, arc_segments)
    # stored units are MIL in this dialect too (trap 5) -- convert once, here
    return uuid, {
        "name": name,
        "outline": _ring([(x * MIL, y * MIL) for x, y in outline_pts]),
        "silk": _ring([(x * MIL, y * MIL) for x, y in silk_pts]),
        "pads": pads,
        "npth": npth,
    }


def _fp_from_array(head, rows, layers, arc_segments):
    uuid = head.get("uuid") or "?"
    name = head.get("title") or uuid
    outline_pts, silk_pts, pads, npth = [], [], [], []
    for r in rows:
        t = r[0]
        if t == "PAD":
            # PAD, id, ?, net, layer, num, x, y, rot, holeShape, padShape, ...
            shape = r[10] if len(r) > 10 else None
            kind = shape[0] if shape else "RECT"
            w = h = cr = 0.0
            poly = None
            if shape and kind in ("RECT", "OVAL", "ELLIPSE", "ROUNDRECT"):
                w = float(shape[1] or 0.0) * MIL
                h = float(shape[2] or 0.0) * MIL
                cr = (float(shape[3]) * MIL) if (len(shape) > 3 and shape[3]) else 0.0
            elif shape and kind == "POLY":
                pts = flatten_path(shape[1], arc_segments)
                poly = [((q[0] - float(r[6])) * MIL, (q[1] - float(r[7])) * MIL)
                        for q in pts]
                xs = [q[0] for q in pts]
                ys = [q[1] for q in pts]
                w = (max(xs) - min(xs)) * MIL
                h = (max(ys) - min(ys)) * MIL
            rec = {"num": str(r[5]), "elem": r[1],
                   "x": float(r[6]) * MIL, "y": float(r[7]) * MIL,
                   "w": w, "h": h, "angle": float(r[8] or 0.0),
                   "shape": kind, "corner_radius": cr, "layer": r[4]}
            if poly:
                rec["polygon"] = poly
            hole = r[9] if len(r) > 9 else None
            if hole and hole[0] in ("ROUND", "SLOT"):
                hw = float(hole[1] or 0.0) * MIL
                hl = float(hole[2] or 0.0) * MIL if len(hole) > 2 and hole[2] else hw
                if hw > 0.0:
                    rec["hole"] = {"w": hw, "h": max(hl, hw), "plated": True}
            pads.append(rec)
            continue
        if len(r) > 4 and r[0] in ("POLY", "FILL", "LINE", "ARC", "CIRCLE", "RECT"):
            lid = r[4]
            pts = []
            if r[0] == "FILL" and len(r) > 7 and isinstance(r[7], list):
                for sh in r[7]:
                    pts += _shape_points(sh, arc_segments)
                    if lid == layers["multi"] and sh and sh[0] == "CIRCLE":
                        npth.append({"x": float(sh[1]) * MIL, "y": float(sh[2]) * MIL,
                                     "d": float(sh[3]) * 2.0 * MIL})
            elif r[0] == "POLY" and len(r) > 6:
                try:
                    pts = flatten_path(r[6], arc_segments)
                except Exception:
                    pts = []
            if lid == layers["assembly_outline"]:
                outline_pts += pts
            elif lid in layers["silkscreen"]:
                silk_pts += pts
            elif lid == layers["multi"]:
                outline_pts += pts
    return uuid, {
        "name": name,
        "outline": _ring([(x * MIL, y * MIL) for x, y in outline_pts]),
        "silk": _ring([(x * MIL, y * MIL) for x, y in silk_pts]),
        "pads": pads,
        "npth": npth,
    }


def _ring(pts):
    """Reduce a bag of drawing points to a convex-ish closed ring: its bbox.

    HONEST LIMITATION.  An assembly outline is generally drawn as several primitives
    (four lines, or a polyline plus a pin-1 marker).  Stitching them into the true
    concave polygon needs edge-following that the source project never had either; it
    used the bounding box.  So does this.  A part with a genuinely L-shaped body is
    therefore modelled as its bounding rectangle -- CONSERVATIVE for containment checks
    (it can report a false overlap, never a false clearance) and WRONG if you need the
    real notch.  When you need the real notch, use the 3D solid from verify/mesh3d.py.
    """
    if not pts:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


# --------------------------------------------------------------------------- pcb

def _pcb_from_record(recs, layers, arc_segments):
    comps, attrs, pad_nets = {}, {}, {}
    tracks, vias, pours = [], [], []
    outline = None
    for h, b in recs:
        t = h.get("type")
        if t == "COMPONENT":
            comps[h["id"]] = b
        elif t == "ATTR" and b:
            key, val, parent = b.get("key"), b.get("value"), b.get("parentId")
            if parent is not None:
                attrs.setdefault(parent, {})[key] = val
        elif t == "PAD_NET":
            try:
                k = json.loads(h["id"])          # ["PAD_NET", compId, padNum, elemId]
            except Exception:
                continue
            pad_nets[(k[1], str(k[2]), k[3])] = (b or {}).get("padNet", "") or ""
        elif t == "LINE" and b:
            tracks.append({"net": b.get("netName", ""), "layer": b.get("layerId"),
                           "x1": b["startX"] * MIL, "y1": b["startY"] * MIL,
                           "x2": b["endX"] * MIL, "y2": b["endY"] * MIL,
                           "w": b["width"] * MIL})
        elif t == "VIA" and b:
            vias.append({"net": b.get("netName", ""),
                         "x": b["centerX"] * MIL, "y": b["centerY"] * MIL,
                         "drill": b["holeDiameter"] * MIL, "pad": b["viaDiameter"] * MIL})
        elif t == "POLY" and b and b.get("layerId") == layers["board_outline"]:
            pts = _geom_points(b, arc_segments)
            if len(pts) >= 3:
                outline = [[x * MIL, y * MIL] for x, y in pts]
        elif t == "POUR" and b:
            pours.append({"net": b.get("netName", ""), "layer": b.get("layerId"),
                          "name": b.get("name"), "polygons": []})
    return comps, attrs, pad_nets, tracks, vias, pours, outline


def _pcb_from_array(rows, layers, arc_segments):
    comps, attrs, pad_nets = {}, {}, {}
    tracks, vias, pours = [], [], []
    outline = None
    for r in rows:
        t = r[0]
        if t == "COMPONENT":
            comps[r[1]] = {"layerId": r[3], "x": float(r[4]), "y": float(r[5]),
                           "angle": float(r[6] or 0.0)}
        elif t == "ATTR" and len(r) > 8:
            attrs.setdefault(r[3], {})[r[7]] = r[8]
        elif t == "PAD_NET" and len(r) > 4:
            # PAD_NET, compId, padNumber, netName, padElemId, flag
            if r[3]:
                pad_nets[(r[1], str(r[2]), r[4])] = r[3]
        elif t == "LINE" and len(r) > 9:
            tracks.append({"net": r[3] or "", "layer": r[4],
                           "x1": float(r[5]) * MIL, "y1": float(r[6]) * MIL,
                           "x2": float(r[7]) * MIL, "y2": float(r[8]) * MIL,
                           "w": float(r[9]) * MIL})
        elif t == "VIA" and len(r) > 8:
            vias.append({"net": r[3] or "", "x": float(r[5]) * MIL,
                         "y": float(r[6]) * MIL, "drill": float(r[7]) * MIL,
                         "pad": float(r[8]) * MIL})
        elif t == "POLY" and len(r) > 6 and r[4] == layers["board_outline"]:
            pts = flatten_path(r[6], arc_segments)
            if len(pts) >= 3:
                outline = [[x * MIL, y * MIL] for x, y in pts]
        elif t == "POUR" and len(r) > 4:
            pours.append({"net": r[3], "layer": r[4],
                          "name": r[6] if len(r) > 6 else None, "polygons": []})
    return comps, attrs, pad_nets, tracks, vias, pours, outline


# --------------------------------------------------------------------------- driver

def _walk(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _d, files in os.walk(p):
                for fn in sorted(files):
                    if fn.lower().endswith(FOOTPRINT_EXT):
                        yield os.path.join(root, fn)
        elif os.path.isfile(p):
            yield p


def convert(paths, rules=None, layers=None, netlist=None, arc_segments=12,
            verbose=True):
    import boardmodel as BM
    lay = dict(BM.DEFAULT_LAYERS)
    lay.update(layers or {})
    footprints = {}
    comps = attrs = pad_nets = None
    tracks, vias, pours, outline = [], [], [], None
    stats = {"files": 0, "footprint_docs": 0, "pcb_docs": 0}

    for path in _walk(paths):
        d = detect_dialect(path)
        stats["files"] += 1
        if d == "record":
            for head, recs in read_record_docs(path):
                dt = (head or {}).get("docType")
                if dt == "FOOTPRINT":
                    uid, fp = _fp_from_record(head, recs, lay, arc_segments)
                    footprints[uid] = fp
                    stats["footprint_docs"] += 1
                elif dt == "PCB" or (dt is None and any(h.get("type") == "COMPONENT"
                                                        for h, _ in recs)):
                    got = _pcb_from_record(recs, lay, arc_segments)
                    comps, attrs, pad_nets = got[0], got[1], got[2]
                    tracks, vias, pours = got[3], got[4], got[5]
                    outline = got[6] or outline
                    stats["pcb_docs"] += 1
        elif d == "array":
            dt, head, rows = read_array_doc(path)
            if dt == "FOOTPRINT":
                uid, fp = _fp_from_array(head, rows, lay, arc_segments)
                footprints[uid] = fp
                stats["footprint_docs"] += 1
            elif dt == "PCB":
                got = _pcb_from_array(rows, lay, arc_segments)
                comps, attrs, pad_nets = got[0], got[1], got[2]
                tracks, vias, pours = got[3], got[4], got[5]
                outline = got[6] or outline
                stats["pcb_docs"] += 1

    if stats["pcb_docs"] != 1:
        raise ValueError("Expected exactly one PCB document; found %d" % stats["pcb_docs"])
    if not comps:
        raise ValueError("PCB contains no components; no placement coverage")

    components, flat_nets = [], {}
    for cid, cb in comps.items():
        a = attrs.get(cid, {})
        des = a.get("Designator") or a.get("designator") or str(cid)
        fpid = a.get("Footprint") or a.get("footprint")
        if fpid not in footprints:
            raise ValueError("%s references missing footprint %r; incomplete export" % (des, fpid))
        if any(c["des"] == des for c in components):
            raise ValueError("Duplicate component designator: %s" % des)
        components.append({"des": des, "native_id": str(cid), "footprint": fpid,
                           "x": float(cb["x"]) * MIL, "y": float(cb["y"]) * MIL,
                           "angle": float(cb.get("angle") or 0.0),
                           "side": "bottom" if cb.get("layerId") == lay["bottom"] else "top"})
        # PAD_NET is keyed (compId, padNum, elemId).  Emit "DES.NUM" for the common case
        # and keep the element key too, so a footprint with repeated pad numbers can be
        # resolved without guessing (trap 1).
        for (kc, knum, kelem), net in pad_nets.items():
            if kc != cid or not net:
                continue
            flat_nets["%s.%s" % (des, knum)] = net
            flat_nets["%s#%s" % (des, kelem)] = net

    doc = {
        "units": "mm",
        "schema": BM.SCHEMA_VERSION,
        "rules": dict(BM.DEFAULT_RULES),
        "layers": lay,
        "outline": {"polygon": outline} if outline else {},
        "footprints": footprints,
        "components": components,
        "pad_nets": flat_nets,
        "nets": netlist or {},
        "tracks": tracks,
        "vias": vias,
        "pours": pours,
    }
    doc["rules"].update(rules or {})
    doc["import_coverage"] = {
        "pcb_documents": stats["pcb_docs"], "source_components": len(comps),
        "imported_components": len(components), "missing_footprints": 0,
        "scope": "supported-records-only; independently reconcile raw counts and geometry"
    }
    if verbose:
        print("read %(files)d file(s): %(footprint_docs)d footprint doc(s), "
              "%(pcb_docs)d PCB doc(s)" % stats)
    return doc


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 3:
        print(__doc__)
        return 2
    out = argv[1]
    paths, rules, layers, netlist, arcs = [], None, None, None, 12
    i = 2
    while i < len(argv):
        a = argv[i]
        if a == "--rules":
            rules = json.load(open(argv[i + 1], encoding="utf-8")); i += 2
        elif a == "--layers":
            layers = json.load(open(argv[i + 1], encoding="utf-8")); i += 2
        elif a == "--netlist":
            netlist = json.load(open(argv[i + 1], encoding="utf-8")); i += 2
        elif a == "--arc-segments":
            arcs = int(argv[i + 1]); i += 2
        else:
            paths.append(a); i += 1
    doc = convert(paths, rules, layers, netlist, arcs)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1)
    import boardmodel as BM
    b = BM.Board(doc, source=out)
    print("wrote %s" % out)
    for k, v in sorted(b.summary().items()):
        print("  %-16s %s" % (k, v))
    return 0


def _selftest():
    """Round-trip synthetic records of both dialects."""
    import tempfile
    import boardmodel as BM
    ok = True
    tmp = tempfile.mkdtemp(prefix="pcbkit-")

    # --- record dialect
    rec = os.path.join(tmp, "rec.epcb")
    lines = [
        '{"type":"DOCHEAD"}||{"docType":"FOOTPRINT","uuid":"FP1","title":"R0603"}|',
        '{"type":"PAD","id":"e1"}||{"num":"1","centerX":-29.5276,"centerY":0,'
        '"padAngle":0,"layerId":1,"defaultPad":{"width":27.5591,"height":31.4961,'
        '"padType":"RECT"}}|',
        '{"type":"PAD","id":"e2"}||{"num":"2","centerX":29.5276,"centerY":0,'
        '"padAngle":0,"layerId":1,"defaultPad":{"width":27.5591,"height":31.4961,'
        '"padType":"RECT"}}|',
        '{"type":"POLY","id":"o1"}||{"layerId":48,"path":[-31.4961,-15.748,"L",'
        '31.4961,-15.748,"L",31.4961,15.748,"L",-31.4961,15.748]}|',
        '{"type":"DOCHEAD"}||{"docType":"PCB","uuid":"PCB1"}|',
        '{"type":"COMPONENT","id":"c1"}||{"x":393.7008,"y":393.7008,"angle":0,'
        '"layerId":1}|',
        '{"type":"ATTR","id":"a1"}||{"parentId":"c1","key":"Designator","value":"R1"}|',
        '{"type":"ATTR","id":"a2"}||{"parentId":"c1","key":"Footprint","value":"FP1"}|',
        '{"type":"PAD_NET","id":"[\\"PAD_NET\\",\\"c1\\",\\"1\\",\\"e1\\"]"}||'
        '{"padNet":"VCC"}|',
        '{"type":"POLY","id":"ol"}||{"layerId":11,"path":[0,0,"L",1181.1024,0,"L",'
        '1181.1024,787.4016,"L",0,787.4016]}|',
    ]
    open(rec, "w", encoding="utf-8").write("\n".join(lines))
    doc = convert([rec], verbose=False)
    b = BM.Board(doc)
    good = (len(b.parts) == 1 and b.parts["R1"].des == "R1" and
            abs(b.parts["R1"].x - 10.0) < 1e-6)
    print("  record dialect: 1 part at (%.3f, %.3f)  %s"
          % (b.parts["R1"].x, b.parts["R1"].y, "OK" if good else "FAIL"))
    ok &= good
    # the declared layer-48 outline is 1.600 mm wide; the real pads span 2.200 mm.
    # The union rule must report 2.200, which is the whole point of it.
    court = b.parts["R1"].court
    good = abs((court[2] - court[0]) - 2.2) < 1e-3
    print("  record dialect: courtyard %.3f x %.3f mm (outline says 1.600)  %s"
          % (court[2] - court[0], court[3] - court[1], "OK" if good else "FAIL"))
    ok &= good
    good = b.parts["R1"].pads[0]["net"] == "VCC"
    print("  record dialect: PAD_NET keyed by element -> %r  %s"
          % (b.parts["R1"].pads[0]["net"], "OK" if good else "FAIL"))
    ok &= good
    good = abs(b.outline_bbox()[2] - 30.0) < 1e-3
    print("  record dialect: outline %s  %s"
          % ([round(v, 3) for v in b.outline_bbox()], "OK" if good else "FAIL"))
    ok &= good

    # --- array dialect
    fpp = os.path.join(tmp, "fp.efoo")
    open(fpp, "w", encoding="utf-8").write("\n".join([
        '["DOCTYPE","FOOTPRINT","1.8"]',
        '["HEAD",{"uuid":"FPA","title":"C0402"}]',
        '["PAD","e1",0,"",1,"1",-19.685,0,0,null,["RECT",19.685,23.622]]',
        '["PAD","e2",0,"",1,"2",19.685,0,0,null,["RECT",19.685,23.622]]',
        '["POLY","o1",0,0,48,0,[-23.622,-11.811,"L",23.622,-11.811,"L",'
        '23.622,11.811,"L",-23.622,11.811]]',
    ]))
    pcbp = os.path.join(tmp, "pcb.epcb")
    open(pcbp, "w", encoding="utf-8").write("\n".join([
        '["DOCTYPE","PCB","1.8"]',
        '["HEAD",{"uuid":"PCBA"}]',
        '["COMPONENT","c1",0,1,196.8504,196.8504,90]',
        '["ATTR","a1",0,"c1",0,0,0,"Designator","C9"]',
        '["ATTR","a2",0,"c1",0,0,0,"Footprint","FPA"]',
        '["PAD_NET","c1","1","GND","e1",0]',
        '["LINE","t1",0,"GND",1,0,0,100,0,7.874]',
        '["VIA","v1",0,"GND",0,50,50,11.811,19.685]',
        '["POLY","ol",0,0,11,0,[0,0,"L",787.4016,0,"L",787.4016,787.4016,"L",'
        '0,787.4016]]',
    ]))
    doc = convert([fpp, pcbp], verbose=False)
    b = BM.Board(doc)
    p = b.parts["C9"]
    good = (abs(p.x - 5.0) < 1e-6 and abs(p.y - 5.0) < 1e-6)
    print("  array  dialect: 1 part at (%.3f, %.3f)  %s"
          % (p.x, p.y, "OK" if good else "FAIL"))
    ok &= good
    w, h = p.court[2] - p.court[0], p.court[3] - p.court[1]
    good = h > w
    print("  array  dialect: 90 deg courtyard %.3f x %.3f  %s"
          % (w, h, "OK" if good else "FAIL"))
    ok &= good
    good = len(b.tracks) == 1 and len(b.vias) == 1 and p.pads[0]["net"] == "GND"
    print("  array  dialect: %d track, %d via, pad1 net %r  %s"
          % (len(b.tracks), len(b.vias), p.pads[0]["net"], "OK" if good else "FAIL"))
    ok &= good

    print("import_easyeda selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main(sys.argv))
