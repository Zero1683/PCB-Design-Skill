# -*- coding: utf-8 -*-
"""The neutral board model every checker in this toolkit consumes.

WHAT THIS MEASURES
    Nothing on its own.  It defines one EDA-independent JSON document ("board JSON"),
    loads it, validates it, and derives the placed geometry the gates need:
      * each part's PAD outlines in board coordinates,
      * each part's BODY polygon (the assembly outline -- what physically sits there),
      * each part's COURTYARD box = union(assembly outline, real pad boxes, hole boxes),
      * every drilled hole on the board, plated and not.

WHAT THIS CANNOT SEE
    * Anything the exporter did not write.  If a footprint has no assembly outline this
      falls back to silkscreen, then to the pad bounding box, and says which it used in
      `court_source`.  A silk-derived body can be wrong by whatever the librarian drew.
    * The 3D solid.  A courtyard is NOT the part: on the reference board a barrel jack's
      layer-48 courtyard stopped 3.05 mm short of its own moulded body, and three
      passives were legally placed inside that overhang.  Use `verify/mesh3d.py` for the
      real solid; this module only knows the 2D library drawing.
    * Copper pours.  `pours` is carried through for the Gerber-side tools but the
      placement gates ignore it -- placement happens before the pour exists.
    * Net *intent*.  `pad_nets` is what the PCB holds; `nets` is what the schematic
      says.  Comparing them is `verify/pad_reconcile.py`'s job, not this module's.

HOW IT WAS VALIDATED
    The schema is a distillation of two independently written board models from a
    released 4-layer board (one by the designer, one by an independent reviewer), whose
    pad positions agreed to 0.0004 mm and whose drill counts agreed exactly.  The
    courtyard-union rule below is the one that caught a module whose pads span 26.114 mm
    while its nominal body outline claims 25.0 mm.  `--selftest` builds a synthetic
    board in memory and checks the derived geometry against hand-computed numbers.

COURTYARD RULE -- the important one
    court = bbox( assembly-outline points  U  real pad boxes  U  hole/slot boxes )
    Taking the nominal outline alone is ACTIVELY WRONG.  Two measured cases:
      * a castellated module whose outline says 25.0 mm and whose pads span 26.114 mm;
      * a USB-C receptacle whose 1.7 mm drilled slots are WIDER than the 1.0 mm pads
        that carry them, so the hole outline has to be in the union too.
    A tantalum's land (9.23 mm) being longer than its body (7.30 mm) is the same class
    of error seen from the other side, and is why `envelope` exists.

UNITS AND CONVENTIONS
    Millimetres everywhere.  Angles are degrees, counter-clockwise, applied to
    footprint-local coordinates.  A bottom-side part is mirrored before rotation, on the
    axis named by `layers.mirror_axis` (see geom2d.mirror_point for why that is a config
    key and not a constant).
"""
from __future__ import print_function

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom2d as G                                                    # noqa: E402

SCHEMA_VERSION = 1

DEFAULT_RULES = {
    # every one of these is a board rule, not a law of nature -- override them in the
    # board JSON.  The values shown are only the example project's.
    "clearance": 0.102,          # copper-to-copper, different nets
    "hole_to_hole": 0.2997,      # ANY two holes, same net or not (see padgap checks)
    "edge_clearance": 0.30,      # copper / drill to board outline
    "via_pad": 0.50,
    "via_drill": 0.30,
    "pad_to_outline": 0.30,
    "min_courtyard_gap": 0.0,    # 0 = "must not overlap"; raise it to demand air
}

DEFAULT_LAYERS = {
    "copper": [1, 15, 16, 2],
    "top": 1,
    "bottom": 2,
    "solid_planes": [15],        # never routed on; a router must be told
    "assembly_outline": 48,
    "silkscreen": [3, 4],
    "multi": 12,                 # through-hole / NPTH feature layer
    "board_outline": 11,
    "mirror_axis": "x",
}


class BoardError(Exception):
    pass


# --------------------------------------------------------------------------- loading

def unique_json_object(pairs):
    """Reject ambiguous JSON evidence rather than silently keeping the last value."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise BoardError("duplicate JSON key: %r" % key)
        result[key] = value
    return result


def load(path):
    """Read a board JSON file and return a validated Board."""
    with open(path, encoding="utf-8") as fh:
        return Board(json.load(fh, object_pairs_hook=unique_json_object), source=path)


class Placed(object):
    """One placed component, with everything derived once."""

    __slots__ = ("des", "fpid", "x", "y", "angle", "side", "pads", "holes",
                 "body", "court", "court_source", "envelope")

    def __repr__(self):
        return "<Placed %s %s @(%.3f,%.3f) %.0f deg>" % (
            self.des, self.fpid, self.x, self.y, self.angle)


class Board(object):
    def __init__(self, doc, source="<memory>"):
        self.source = source
        self.doc = doc
        self.rules = dict(DEFAULT_RULES)
        self.rules.update(doc.get("rules") or {})
        self.layers = dict(DEFAULT_LAYERS)
        self.layers.update(doc.get("layers") or {})
        self.footprints = doc.get("footprints") or {}
        self.pad_nets = doc.get("pad_nets", {})
        self.nets = doc.get("nets") or {}
        self.tracks = doc.get("tracks") or []
        self.vias = doc.get("vias") or []
        self.pours = doc.get("pours") or []
        self.outline = (doc.get("outline") or {}).get("polygon") or []
        self._validate(doc)
        self._known_pad_net_keys = set()
        self.parts = {}
        for c in doc.get("components") or []:
            p = self._place(c)
            if p.des in self.parts:
                raise BoardError("duplicate designator %r" % p.des)
            self.parts[p.des] = p
        unknown = set(self.pad_nets) - self._known_pad_net_keys
        if unknown:
            raise BoardError("pad-net entries reference missing physical pads: %s"
                             % sorted(unknown))

    # ------------------------------------------------------------------ validation
    def _validate(self, doc):
        def number(value, name, positive=False, nonnegative=False):
            if type(value) not in (int, float) or not math.isfinite(value):
                raise BoardError("%s must be a finite number" % name)
            if (positive and value <= 0) or (nonnegative and value < 0):
                raise BoardError("%s has invalid negative/zero geometry" % name)
        def points(value, name):
            for xy in value or []:
                if not isinstance(xy, (list, tuple)) or len(xy) != 2:
                    raise BoardError("%s requires coordinate pairs" % name)
                for v in xy: number(v, name)
        for key in DEFAULT_RULES:
            number(self.rules[key], "rules." + key, nonnegative=True,
                   positive=(key in ("clearance", "via_pad", "via_drill")))
        if self.rules["via_drill"] >= self.rules["via_pad"]:
            raise BoardError("via_drill must be smaller than via_pad")
        cu = self.layers["copper"]
        if (not isinstance(cu, list) or not cu or
                any(type(l) is not int or l <= 0 for l in cu) or len(set(cu)) != len(cu)):
            raise BoardError("copper must be an ordered list of unique positive layer IDs")
        if (self.layers["top"] not in cu or self.layers["bottom"] not in cu or
                not set(self.layers.get("solid_planes", [])) <= set(cu)):
            raise BoardError("top/bottom/solid_planes must be copper layers")
        points(self.outline, "outline")
        for c in doc.get("components") or []:
            for key in ("x", "y", "angle"):
                number(c.get(key, 0), "component." + key)
            if c.get("side", "top") not in ("top", "bottom"):
                raise BoardError("unsupported component side")
        for fp in self.footprints.values():
            for key in ("outline", "silk"): points(fp.get(key), key)
            for pad in fp.get("pads") or []:
                for key in ("x", "y", "angle"):
                    number(pad.get(key, 0), "pad." + key)
                for key in ("w", "h"):
                    number(pad.get(key, 0), "pad." + key, positive=True)
                number(pad.get("corner_radius", 0), "corner_radius", nonnegative=True)
                shape = str(pad.get("shape", "RECT")).upper()
                if shape not in ("RECT", "ROUNDRECT", "ROUND_RECT", "RR", "OVAL",
                                 "OBROUND", "ELLIPSE", "CIRCLE", "ROUND", "POLY", "POLYGON"):
                    raise BoardError("unsupported pad shape: %s" % shape)
                if shape in ("POLY", "POLYGON") and len(pad.get("polygon") or []) < 3:
                    raise BoardError("polygon pad requires at least three points")
                points(pad.get("polygon"), "pad.polygon")
                if shape in ("POLY", "POLYGON"):
                    poly = [tuple(p) for p in pad["polygon"]]
                    if poly[0] == poly[-1]: poly.pop()
                    if len(poly) < 3 or len(set(poly)) != len(poly) or G.poly_area(poly) <= 1e-12:
                        raise BoardError("degenerate/zero-area pad polygon")
                    n = len(poly)
                    for i in range(n):
                        for j in range(i + 1, n):
                            if j == i + 1 or (i == 0 and j == n - 1): continue
                            if G.dist_segment_segment(poly[i], poly[(i + 1) % n],
                                                      poly[j], poly[(j + 1) % n]) <= 1e-12:
                                raise BoardError("self-intersecting pad polygon is unsupported")
                hole = pad.get("hole") or {}
                for key in ("w", "h"):
                    number(hole.get(key, 0), "hole." + key, nonnegative=True)
                if hole.get("w", 0) > 0 and type(hole.get("plated")) is not bool:
                    raise BoardError("drilled pad requires explicit boolean hole.plated")
                if hole.get("h", 0) > 0 and not hole.get("w", 0):
                    raise BoardError("hole height without hole width")
                self._pad_layers(pad, "top")
            for hole in fp.get("npth") or []:
                for key in ("x", "y"): number(hole.get(key), "npth." + key)
                number(hole.get("d"), "npth.d", positive=True)
        for track in self.tracks:
            for key in ("x1", "y1", "x2", "y2"):
                number(track.get(key), "track." + key)
            number(track.get("w"), "track.w", positive=True)
            if track.get("layer") not in cu:
                raise BoardError("track layer is not a copper layer")
            if any(key in track for key in ("arc", "bulge", "radius", "curve")):
                raise BoardError("unsupported curved track geometry")
        for via in self.vias:
            for key in ("x", "y"): number(via.get(key), "via." + key)
            for key in ("pad", "drill"):
                number(via.get(key, self.rules["via_" + key]), "via." + key, positive=True)
            if via.get("drill", self.rules["via_drill"]) >= via.get("pad", self.rules["via_pad"]):
                raise BoardError("via drill must be smaller than pad diameter")
            self.via_layers(via)
        if not isinstance(self.pad_nets, dict):
            raise BoardError("pad_nets must be an object")
        for key, net in self.pad_nets.items():
            if not isinstance(key, str) or not key:
                raise BoardError("invalid pad-net key %r" % (key,))
            # Empty string is the neutral model's explicit unassigned net.
            if not isinstance(net, str) or (net and not net.strip()):
                raise BoardError("invalid pad net for %s: %r" % (key, net))
        if doc.get("units", "mm") != "mm":
            raise BoardError("only millimetre board JSON is supported, got units=%r"
                             % doc.get("units"))
        for des_i, c in enumerate(doc.get("components") or []):
            for k in ("des", "footprint", "x", "y"):
                if k not in c:
                    raise BoardError("component #%d is missing %r" % (des_i, k))
            if c["footprint"] not in self.footprints:
                raise BoardError("component %s references unknown footprint %r"
                                 % (c["des"], c["footprint"]))
        if self.outline and len(self.outline) < 3:
            raise BoardError("outline polygon needs at least 3 points")

    # ------------------------------------------------------------------ placement
    def _local_to_board(self, lx, ly, part_x, part_y, angle, side):
        if side == "bottom":
            lx, ly = G.mirror_point(lx, ly, self.layers.get("mirror_axis", "x"))
        dx, dy = G.rot(lx, ly, angle)
        return (part_x + dx, part_y + dy)

    def _place(self, c):
        p = Placed()
        p.des = str(c["des"])
        p.fpid = c["footprint"]
        p.x = float(c["x"])
        p.y = float(c["y"])
        p.angle = float(c.get("angle") or 0.0)
        p.side = c.get("side") or "top"
        fp = self.footprints[p.fpid]

        # --- pads
        p.pads = []
        local_pads = fp.get("pads") or []
        counts = _count([str(pad.get("num", "")) for pad in local_pads])
        elements = set()
        for pad in local_pads:
            num = str(pad.get("num", ""))
            elem = pad.get("elem")
            # Unique-number legacy neutral models need no element ID. Repeated
            # numbers require physical identities and a net record for EVERY land.
            if elem is not None:
                if not isinstance(elem, str) or not elem.strip():
                    raise BoardError("%s.%s has invalid physical pad element" % (p.des, num))
                if elem in elements:
                    raise BoardError("%s has duplicate physical pad element %r" % (p.des, elem))
                elements.add(elem)
            number_key = "%s.%s" % (p.des, num)
            element_key = "%s#%s" % (p.des, elem) if elem is not None else None
            self._known_pad_net_keys.add(number_key)
            if element_key is not None:
                self._known_pad_net_keys.add(element_key)
            if counts[num] > 1 and (element_key is None or element_key not in self.pad_nets):
                raise BoardError("repeated-number pad requires its own element net: %s (%r)"
                                 % (number_key, elem))
            if (element_key in self.pad_nets and number_key in self.pad_nets
                    and self.pad_nets[element_key] != self.pad_nets[number_key]):
                raise BoardError("number/element net mismatch: %s vs %s" % (number_key, element_key))
            net = (self.pad_nets[element_key] if element_key in self.pad_nets
                   else self.pad_nets.get(number_key, ""))
            cx, cy = self._local_to_board(float(pad["x"]), float(pad["y"]),
                                          p.x, p.y, p.angle, p.side)
            # A pad's own rotation adds to the part's.  Use the pad's RENDER angle, not
            # any "relative" angle the format may also carry: on the reference project
            # reading the relative angle made half a module's pads overlap.
            pang = p.angle + float(pad.get("angle") or 0.0)
            if p.side == "bottom":
                pang = (180.0 - float(pad.get("angle") or 0.0) - p.angle) % 360.0
            poly = G.pad_outline(pad.get("shape", "RECT"), cx, cy,
                                 float(pad.get("w") or 0.0), float(pad.get("h") or 0.0),
                                 pang, float(pad.get("corner_radius") or 0.0),
                                 pad.get("polygon"))
            num = str(pad.get("num", ""))
            rec = {
                "des": p.des, "num": num, "elem": pad.get("elem"),
                "x": cx, "y": cy, "angle": pang,
                "w": float(pad.get("w") or 0.0), "h": float(pad.get("h") or 0.0),
                "shape": pad.get("shape", "RECT"),
                "poly": poly, "bbox": G.bbox_of(poly),
                "net": net,
                "layers": self._pad_layers(pad, p.side),
                "hole": pad.get("hole"),
                "layer_bridge": bool((pad.get("hole") or {}).get("w", 0) > 0
                                     and (pad.get("hole") or {}).get("plated") is True),
            }
            p.pads.append(rec)

        # --- holes (plated pad holes + footprint NPTH)
        p.holes = []
        for rec in p.pads:
            h = rec["hole"]
            if not h:
                continue
            hw = float(h.get("w") or 0.0)
            hh = float(h.get("h") or hw)
            if hw <= 0.0:
                # A zero-width hole record is NOT a hole.  Measured: a module's 88 SMD
                # lands each carried an empty hole dict; counting them added 88 phantom
                # drills to the census.
                continue
            p.holes.append({"des": p.des, "num": rec["num"], "kind": "pad",
                            "x": rec["x"], "y": rec["y"],
                            "d": hw, "slot_len": max(hh - hw, 0.0),
                            "plated": bool(h.get("plated", True)),
                            "net": rec["net"]})
        for h in fp.get("npth") or []:
            hx, hy = self._local_to_board(float(h["x"]), float(h["y"]),
                                          p.x, p.y, p.angle, p.side)
            p.holes.append({"des": p.des, "num": None, "kind": "npth",
                            "x": hx, "y": hy, "d": float(h["d"]), "slot_len": 0.0,
                            "plated": False, "net": ""})

        # --- body polygon: the assembly outline, else silk, else the pad bbox
        body_pts, src = None, None
        if fp.get("outline"):
            body_pts = [self._local_to_board(px, py, p.x, p.y, p.angle, p.side)
                        for px, py in fp["outline"]]
            src = "assembly"
        elif fp.get("silk"):
            body_pts = [self._local_to_board(px, py, p.x, p.y, p.angle, p.side)
                        for px, py in fp["silk"]]
            src = "silk"
        if body_pts is None:
            pts = [q for rec in p.pads for q in rec["poly"]]
            if not pts:
                raise BoardError("%s has no outline, no silk and no pads" % p.des)
            bb = G.bbox_of(pts)
            body_pts = [(bb[0], bb[1]), (bb[2], bb[1]), (bb[2], bb[3]), (bb[0], bb[3])]
            src = "pads"
        p.body = body_pts

        # --- COURTYARD: the union rule.  See the module docstring.
        union = list(body_pts)
        for rec in p.pads:
            union += rec["poly"]
        for h in p.holes:
            r = h["d"] / 2.0 + h["slot_len"] / 2.0
            union += [(h["x"] - r, h["y"] - r), (h["x"] + r, h["y"] + r)]
        p.court = G.bbox_of(union)
        p.court_source = src
        p.envelope = p.court           # kept as a separate name: callers asking for the
        # "real area the part needs" should say envelope, not court, so the intent of a
        # future edit is unambiguous.
        return p

    def _pad_layers(self, pad, side):
        """Copper presence only; layer_bridge separately describes a plated barrel."""
        cu = tuple(self.layers["copper"])
        if "layers" in pad:
            ls = pad["layers"]
            if not isinstance(ls, list) or not ls or len(set(ls)) != len(ls) or not set(ls) <= set(cu):
                raise BoardError("pad.layers must list distinct copper layers")
            return tuple(ls)
        hole = pad.get("hole") or {}
        if hole.get("w", 0) > 0 and hole.get("plated") is True:
            return cu
        lay = pad.get("layer")
        if lay == self.layers.get("multi"):
            return cu
        if lay is not None and lay not in cu:
            raise BoardError("pad layer is not copper or multi")
        # A footprint's outer layer follows the placed component's side.
        if lay is None or lay in (self.layers["top"], self.layers["bottom"]):
            return (self.layers["bottom"] if side == "bottom" else
                    (lay if lay is not None else self.layers["top"]),)
        return (lay,)

    def via_layers(self, via):
        """Explicit neutral spans are supported; legacy unqualified vias are through."""
        cu = tuple(self.layers["copper"])
        if "plated" in via and via["plated"] is not True:
            raise BoardError("a via requires a plated barrel")
        typ = str(via.get("viaType", via.get("type", "THROUGH"))).upper()
        if typ not in ("NORMAL", "THROUGH", "BLIND", "BURIED", "SUTURE"):
            raise BoardError("unsupported via type: %s" % typ)
        if via.get("unusedInnerLayers"):
            raise BoardError("unsupported via with removed inner copper lands")
        endpoints = [(a, b) for a, b in (("start_layer", "end_layer"),
                     ("startLayer", "endLayer"), ("startLayerId", "endLayerId"))
                     if a in via or b in via]
        spans = []
        if "layers" in via:
            spans.append(via["layers"])
        for a, b in endpoints:
            if via.get(a) not in cu or via.get(b) not in cu:
                raise BoardError("via span endpoints must both be known copper layers")
            i, j = sorted((cu.index(via[a]), cu.index(via[b])))
            spans.append(list(cu[i:j + 1]))
        if not spans:
            if typ in ("BLIND", "BURIED") or via.get("ruleName"):
                raise BoardError("unsupported via span: layer evidence/rule resolution missing")
            return cu
        ls = spans[0]
        if (not isinstance(ls, list) or len(ls) < 2 or len(set(ls)) != len(ls)
                or not set(ls) <= set(cu)):
            raise BoardError("via.layers must contain at least two distinct copper layers")
        inds = sorted(cu.index(l) for l in ls)
        if inds != list(range(inds[0], inds[-1] + 1)):
            raise BoardError("via.layers must be a contiguous copper stack span")
        if any(set(other) != set(ls) for other in spans[1:]):
            raise BoardError("conflicting via layer spans")
        return tuple(cu[i] for i in inds)

    # ------------------------------------------------------------------ accessors
    def outline_bbox(self):
        if self.outline:
            return G.bbox_of(self.outline)
        pts = [q for p in self.parts.values() for q in p.body]
        if not pts:
            raise BoardError("board has neither an outline nor any component")
        return G.bbox_of(pts)

    def all_pads(self):
        for p in self.parts.values():
            for rec in p.pads:
                yield rec

    def all_holes(self, include_vias=True):
        """Every drilled feature on the board.

        Vias are included by default because the hole-to-hole rule does not care what a
        hole is for.  Leaving them out is exactly how three stacked router vias passed a
        clearance sweep and then failed the real DRC.
        """
        for p in self.parts.values():
            for h in p.holes:
                yield h
        if include_vias:
            for v in self.vias:
                yield {"des": None, "num": None, "kind": "via",
                       "x": float(v["x"]), "y": float(v["y"]),
                       "d": float(v.get("drill") or self.rules["via_drill"]),
                       "slot_len": 0.0, "plated": True, "net": v.get("net", "")}

    def bodies(self, min_area=0.0):
        """(designator, body polygon, area mm2) for every part.

        `min_area` defaults to 0.  Do not raise it in a gate.  See body_clearance.py:
        filtering bodies by size is fault 3.
        """
        out = []
        for des, p in sorted(self.parts.items()):
            out.append((des, p.body, G.poly_area(p.body)))
        return [t for t in out if t[2] >= min_area]

    def summary(self):
        holes = list(self.all_holes())
        return {
            "source": self.source,
            "components": len(self.parts),
            "pads": sum(len(p.pads) for p in self.parts.values()),
            "netted_pads": sum(1 for r in self.all_pads() if r["net"]),
            "nets_on_pcb": len({r["net"] for r in self.all_pads() if r["net"]}),
            "tracks": len(self.tracks),
            "vias": len(self.vias),
            "holes_total": len(holes),
            "holes_plated": sum(1 for h in holes if h["plated"]),
            "outline_bbox": [round(v, 4) for v in self.outline_bbox()],
            "court_sources": _count([p.court_source for p in self.parts.values()]),
        }


def _count(seq):
    out = {}
    for v in seq:
        out[v] = out.get(v, 0) + 1
    return out


# --------------------------------------------------------------------------- synthetic

def synthetic_board():
    """A tiny board used by --selftest here and in several sibling scripts.

    It is deliberately built to contain each fault's trigger:
      * MOD1 is a module whose PADS overhang its declared outline (courtyard union),
      * C1 sits entirely UNDER MOD1's body (module-body containment),
      * R1 is a small part whose body is only 1.6 mm2 but which still has C2 under it
        (the "only large bodies were tested" fault),
      * V1/V2 are two vias 0.05 mm apart on the SAME net (net-blind hole-to-hole).
    """
    fp_mod = {
        "name": "MODULE-CASTELLATED",
        # declared body is 6 x 6, but the pads reach x = +-3.5
        "outline": [[-3.0, -3.0], [3.0, -3.0], [3.0, 3.0], [-3.0, 3.0]],
        "pads": [{"num": "1", "x": -3.2, "y": 0.0, "w": 0.6, "h": 1.0, "shape": "RECT"},
                 {"num": "2", "x": 3.2, "y": 0.0, "w": 0.6, "h": 1.0, "shape": "RECT"}],
    }
    fp_0603 = {
        "name": "R0603",
        "outline": [[-0.8, -0.4], [0.8, -0.4], [0.8, 0.4], [-0.8, 0.4]],
        "pads": [{"num": "1", "x": -0.75, "y": 0.0, "w": 0.7, "h": 0.8, "shape": "RECT"},
                 {"num": "2", "x": 0.75, "y": 0.0, "w": 0.7, "h": 0.8, "shape": "RECT"}],
    }
    fp_th = {
        "name": "HDR-1x2",
        "outline": [[-1.27, -1.27], [1.27, -1.27], [1.27, 1.27], [-1.27, 1.27]],
        "pads": [{"num": "1", "x": -1.27, "y": 0.0, "w": 1.5, "h": 1.5,
                  "shape": "OVAL", "hole": {"w": 0.9, "h": 0.9, "plated": True}},
                 {"num": "2", "x": 1.27, "y": 0.0, "w": 1.5, "h": 1.5,
                  "shape": "OVAL", "hole": {"w": 0.9, "h": 0.9, "plated": True}}],
        "npth": [{"x": 0.0, "y": 2.0, "d": 1.0}],
    }
    return {
        "units": "mm",
        "rules": dict(DEFAULT_RULES),
        "layers": dict(DEFAULT_LAYERS),
        "outline": {"polygon": [[0, 0], [30, 0], [30, 30], [0, 30]]},
        "footprints": {"MOD": fp_mod, "R0603": fp_0603, "HDR": fp_th},
        "components": [
            {"des": "MOD1", "footprint": "MOD", "x": 10.0, "y": 10.0, "angle": 0},
            {"des": "C1", "footprint": "R0603", "x": 10.0, "y": 10.0, "angle": 0},
            {"des": "R1", "footprint": "R0603", "x": 22.0, "y": 10.0, "angle": 0},
            {"des": "C2", "footprint": "R0603", "x": 22.0, "y": 10.0, "angle": 90},
            {"des": "J1", "footprint": "HDR", "x": 5.0, "y": 25.0, "angle": 0},
        ],
        "pad_nets": {"MOD1.1": "GND", "MOD1.2": "VCC", "C1.1": "GND", "C1.2": "VCC",
                     "R1.1": "VCC", "R1.2": "OUT", "C2.1": "OUT", "C2.2": "GND",
                     "J1.1": "VCC", "J1.2": "GND"},
        "nets": {"GND": [["MOD1", "1"], ["C1", "1"], ["C2", "2"], ["J1", "2"]],
                 "VCC": [["MOD1", "2"], ["C1", "2"], ["R1", "1"], ["J1", "1"]],
                 "OUT": [["R1", "2"], ["C2", "1"]]},
        "tracks": [{"net": "VCC", "layer": 1, "x1": 10.0, "y1": 14.0,
                    "x2": 22.0, "y2": 14.0, "w": 0.2}],
        "vias": [{"net": "GND", "x": 26.0, "y": 6.0, "drill": 0.3, "pad": 0.5},
                 {"net": "GND", "x": 26.05, "y": 6.0, "drill": 0.3, "pad": 0.5}],
    }


# --------------------------------------------------------------------------- selftest

def _selftest():
    ok = True
    b = Board(synthetic_board())
    s = b.summary()
    print("boardmodel selftest")
    for k in sorted(s):
        print("  %-18s %s" % (k, s[k]))

    mod = b.parts["MOD1"]
    # courtyard union: pads reach 3.2 + 0.3 = 3.5 mm from the origin, body only 3.0
    want = [10.0 - 3.5, 10.0 - 3.0, 10.0 + 3.5, 10.0 + 3.0]
    got = [round(v, 6) for v in mod.court]
    good = all(abs(a - c) < 1e-6 for a, c in zip(want, got))
    print("  %-46s %s   %s" % ("courtyard = union(outline, pads)", got,
                               "OK" if good else "FAIL want %s" % want))
    ok &= good

    body_bb = G.bbox_of(mod.body)
    good = abs(body_bb[2] - 13.0) < 1e-9
    print("  %-46s %s   %s" % ("body stays the DECLARED 6 x 6 outline",
                               [round(v, 3) for v in body_bb], "OK" if good else "FAIL"))
    ok &= good
    good = mod.court[2] > body_bb[2]
    print("  %-46s %s" % ("courtyard is WIDER than the body",
                          "OK (%.3f > %.3f)" % (mod.court[2], body_bb[2]) if good else "FAIL"))
    ok &= good

    # C1 under MOD1
    d = G.poly_distance(mod.body, b.parts["C1"].body)
    good = d == 0.0
    print("  %-46s %.4f mm  %s" % ("C1 body vs MOD1 body (must be 0)", d,
                                   "OK" if good else "FAIL"))
    ok &= good

    # rotated part: C2 is R0603 turned 90 deg, so its courtyard is taller than wide
    c2 = b.parts["C2"]
    w, h = c2.court[2] - c2.court[0], c2.court[3] - c2.court[1]
    good = h > w
    print("  %-46s %.3f x %.3f  %s" % ("90 deg rotation swaps courtyard axes", w, h,
                                       "OK" if good else "FAIL"))
    ok &= good

    # holes: 2 plated pad holes + 1 NPTH + 2 vias = 5
    holes = list(b.all_holes())
    good = len(holes) == 5 and sum(1 for x in holes if x["kind"] == "npth") == 1
    print("  %-46s %d (%s)  %s" % ("hole census incl. vias", len(holes),
                                   _count([x["kind"] for x in holes]),
                                   "OK" if good else "FAIL"))
    ok &= good

    # a zero-width hole record must not be counted
    doc = synthetic_board()
    doc["footprints"]["R0603"]["pads"][0]["hole"] = {"w": 0.0, "h": 0.0}
    n = len(list(Board(doc).all_holes()))
    good = n == 5
    print("  %-46s %d  %s" % ("zero-width hole record ignored", n,
                              "OK" if good else "FAIL (want 5)"))
    ok &= good

    print("boardmodel selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 2:
        print(__doc__)
        print("usage: python3 boardmodel.py <board.json>   |   --selftest")
        return 2
    b = load(argv[1])
    s = b.summary()
    for k in sorted(s):
        print("%-16s %s" % (k, s[k]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
