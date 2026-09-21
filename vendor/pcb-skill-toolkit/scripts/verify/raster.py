# -*- coding: utf-8 -*-
"""Rasterise parsed Gerber copper, label the connected components, and write PNGs.

WHAT THIS MEASURES
    Copper as it will be MANUFACTURED, not as the design model describes it.  A layer is
    rendered to a boolean grid at `--res` mm per pixel; run-length union-find then labels
    the 8-connected components, so copper that is physically joined gets one label
    whatever the netlist says.  That gives two things no model-side check can:
      * the real area of each region, pours included;
      * whether two different nets ever land on the SAME region -- a short that a
        pour-clearance DRC does not necessarily report.
    `min_gap` grows every label a pixel per round until two touch, which BRACKETS the
    smallest gap on the layer; the exact millimetre answer is then measured primitive
    against primitive by verify/clearance.py.  The raster finds WHERE, the exact pass
    says HOW MUCH.

FAULT FIXED HERE (fault 4 of 4 -- "a raster fill that leaked through a plane's keyhole
cut-ins and merged copper labels")
    The original fill turned each edge crossing into a COLUMN INDEX with
    ceil((x - X0)/RES - 0.5) and took the parity of a cumulative sum along the row.
    An EDA writes a copper plane as ONE G36 contour whose interior holes are reached by
    ZERO-WIDTH KEYHOLE CHANNELS: the same segment appears twice, traversed in opposite
    directions.  Mathematically the two crossings cancel.  After independent float
    evaluation and the ceil they can land in ADJACENT columns, the parity flips for one
    pixel, and the plane bleeds through its own moat -- so two physically separate
    copper regions receive ONE LABEL.

    What that cost, measured on a real board: an isolated analogue-ground via read as
    CONNECTED to the main ground plane, a short that does not exist; every Gerber-side
    clearance number on the project had been computed on labels that merged regions the
    rule is supposed to separate, so the gap between them was never measured at all; and
    a via-redundancy analysis called 127 vias redundant when the true number was 122 --
    one of the five was load-bearing and was in the removal set.

    `fill_polys` below collects the EXACT FLOAT crossings per scanline, sorts them, and
    fills the spans between consecutive pairs.  Coincident edges then open and
    immediately close a zero-width span, which is what the Gerber means.
    `fill_polys_column_parity` is kept ONLY so `--selftest` can demonstrate the leak
    side by side.  Do not use it.

WHAT THIS CANNOT SEE
    * Sub-pixel features.  At the default 10 um resolution a 5 um sliver is invisible,
      and two regions 5 um apart may merge.  RESOLUTION IS A CEILING ON TRUTH: any
      conclusion tighter than one pixel must be re-measured exactly.
    * Polarity.  Clear-polarity (%LPC) drawing is not modelled; see gerber.py.
    * Nets.  A label is copper, not a net.  Attributing labels to nets is the caller's
      job and is where the second-worst fault on the reference project lived: pour
      copper CANNOT be attributed by asking which pour BOUNDARY contains the point,
      because a lower-priority pour legitimately fills the gaps a higher-priority one
      leaves.  Match pour FILL polygons by vertex coincidence instead.
    * Anything without numpy.  This module needs it and says so; every other script in
      verify/ works without it.

HOW IT WAS VALIDATED
    Ported from the corrected rasteriser of a released board, after which zero copper
    components were claimed by two nets on any of four layers -- the first time that was
    true of any measurement on that project.  `--selftest` builds the keyhole geometry
    in memory and shows the old fill merging two regions that the new one keeps apart.

USAGE
    python3 raster.py --selftest
    python3 raster.py FILE.GTL [--res 0.01] [--png out.png] [--extent x0,y0,x1,y1]
    python3 raster.py FILE.G1  --compare-fills      # the fault-4 detector
"""
from __future__ import print_function

import math
import os
import struct
import sys
import zlib

try:
    import numpy as np
except ImportError:                                                   # pragma: no cover
    np = None

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def require_numpy():
    if np is None:
        raise SystemExit(
            "raster.py needs numpy (pip install numpy).  Everything else in verify/ "
            "runs without it; only the raster-based clearance bracket and the PNGs "
            "are unavailable.")


class Grid(object):
    """A raster window over the board, in millimetres."""

    def __init__(self, x0, y0, x1, y1, res=0.01, margin=0.30):
        require_numpy()
        self.res = float(res)
        self.x0 = float(x0) - margin
        self.y0 = float(y0) - margin
        self.w = int(math.ceil((x1 - x0 + 2 * margin) / self.res)) + 1
        self.h = int(math.ceil((y1 - y0 + 2 * margin) / self.res)) + 1

    def blank(self):
        return np.zeros((self.h, self.w), dtype=bool)

    def col(self, x):
        return int(math.ceil((x - self.x0) / self.res - 0.5))

    def row(self, y):
        return int(math.ceil((y - self.y0) / self.res - 0.5))

    # ------------------------------------------------------------------ fills
    def fill_polys(self, mask, subpaths):
        """EXACT-CROSSING even-odd fill.  This is the fault-4 fix; read the docstring."""
        rows = {}
        for path in subpaths:
            n = len(path)
            for i in range(n):
                xa, ya = path[i]
                xb, yb = path[(i + 1) % n]
                if ya == yb:
                    continue
                ylo, yhi = (ya, yb) if ya < yb else (yb, ya)
                r0 = max(int(math.ceil((ylo - self.y0) / self.res - 0.5)), 0)
                r1 = min(int(math.floor((yhi - self.y0) / self.res - 0.5)), self.h - 1)
                for r in range(r0, r1 + 1):
                    yc = self.y0 + (r + 0.5) * self.res
                    if yc < ylo or yc >= yhi:      # half-open: a vertex counts once
                        continue
                    xi = xa + (yc - ya) * (xb - xa) / (yb - ya)
                    rows.setdefault(r, []).append(xi)
        for r, xs in rows.items():
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                c0 = self.col(xs[k])
                c1 = self.col(xs[k + 1])
                if c1 <= c0:
                    continue                       # a zero-width span: exactly nothing
                mask[r, max(c0, 0):min(c1, self.w)] = True

    def fill_polys_column_parity(self, mask, subpaths):
        """THE ORIGINAL, FAULTY FILL.  Present only so --selftest can show the leak.

        It rounds each crossing to a column and takes the parity of the cumulative sum,
        so two coincident edges of a keyhole channel can land one column apart and the
        plane bleeds through its own moat.  Never call this from a check."""
        acc = np.zeros((self.h, self.w + 2), dtype=np.int32)
        for path in subpaths:
            n = len(path)
            for i in range(n):
                xa, ya = path[i]
                xb, yb = path[(i + 1) % n]
                if ya == yb:
                    continue
                ylo, yhi = (ya, yb) if ya < yb else (yb, ya)
                r0 = max(int(math.ceil((ylo - self.y0) / self.res - 0.5)), 0)
                r1 = min(int(math.floor((yhi - self.y0) / self.res - 0.5)), self.h - 1)
                if r1 < r0:
                    continue
                rr = np.arange(r0, r1 + 1)
                yc = self.y0 + (rr + 0.5) * self.res
                t = (yc - ya) / (yb - ya)
                xi = xa + t * (xb - xa)
                ci = np.ceil((xi - self.x0) / self.res - 0.5).astype(np.int64)
                np.clip(ci, 0, self.w + 1, out=ci)
                np.add.at(acc, (rr, ci), 1)
        mask |= (np.cumsum(acc[:, :self.w], axis=1) & 1).astype(bool)

    # ------------------------------------------------------------------ stamps
    def stamp_capsule(self, mask, x1, y1, x2, y2, r):
        c0 = max(int((min(x1, x2) - r - self.x0) / self.res), 0)
        c1 = min(int((max(x1, x2) + r - self.x0) / self.res) + 2, self.w)
        r0 = max(int((min(y1, y2) - r - self.y0) / self.res), 0)
        r1 = min(int((max(y1, y2) + r - self.y0) / self.res) + 2, self.h)
        if c1 <= c0 or r1 <= r0:
            return
        xs = self.x0 + (np.arange(c0, c1) + 0.5) * self.res
        ys = self.y0 + (np.arange(r0, r1) + 0.5) * self.res
        XX, YY = np.meshgrid(xs, ys)
        dx, dy = x2 - x1, y2 - y1
        L = dx * dx + dy * dy
        if L < 1e-15:
            d = np.hypot(XX - x1, YY - y1)
        else:
            t = np.clip(((XX - x1) * dx + (YY - y1) * dy) / L, 0.0, 1.0)
            d = np.hypot(XX - (x1 + t * dx), YY - (y1 + t * dy))
        mask[r0:r1, c0:c1] |= (d <= r)

    def stamp_flash(self, mask, f):
        a = f.ap
        if a.kind == "C":
            self.stamp_capsule(mask, f.x, f.y, f.x, f.y, a.w / 2.0)
        elif a.kind == "POLY":
            self.fill_polys(mask, [[(f.x + px, f.y + py) for px, py in a.verts]])
        elif a.kind == "O":
            r = min(a.w, a.h) / 2.0
            if a.w >= a.h:
                self.stamp_capsule(mask, f.x - (a.w / 2.0 - r), f.y,
                                   f.x + (a.w / 2.0 - r), f.y, r)
            else:
                self.stamp_capsule(mask, f.x, f.y - (a.h / 2.0 - r),
                                   f.x, f.y + (a.h / 2.0 - r), r)
        else:                                        # R and RR
            r = a.r / 2.0 if a.kind == "RR" else 0.0
            hw = max(a.w / 2.0 - r, 0.0)
            hh = max(a.h / 2.0 - r, 0.0)
            if r <= 0:
                self.fill_polys(mask, [[(f.x - hw, f.y - hh), (f.x + hw, f.y - hh),
                                        (f.x + hw, f.y + hh), (f.x - hw, f.y + hh)]])
            else:
                c0 = max(int((f.x - a.w / 2.0 - self.x0) / self.res), 0)
                c1 = min(int((f.x + a.w / 2.0 - self.x0) / self.res) + 2, self.w)
                r0 = max(int((f.y - a.h / 2.0 - self.y0) / self.res), 0)
                r1 = min(int((f.y + a.h / 2.0 - self.y0) / self.res) + 2, self.h)
                if c1 <= c0 or r1 <= r0:
                    return
                gx = self.x0 + (np.arange(c0, c1) + 0.5) * self.res
                gy = self.y0 + (np.arange(r0, r1) + 0.5) * self.res
                XX, YY = np.meshgrid(gx, gy)
                dx = np.maximum(np.abs(XX - f.x) - hw, 0.0)
                dy = np.maximum(np.abs(YY - f.y) - hh, 0.0)
                mask[r0:r1, c0:c1] |= (np.hypot(dx, dy) <= r + 1e-12)

    def rasterise(self, layer, sections=None, include_regions=True):
        """One parsed Gerber Layer -> a boolean mask.

        `sections` filters by the G04 section tag (e.g. ("Pad", "Via")).  When it is
        given, REGIONS ARE NOT DRAWN -- a G36 region has no section tag, so including it
        under a filter would silently add copper the caller did not ask for.
        """
        m = self.blank()
        for f in layer.flashes:
            if sections is None or f.section in sections:
                self.stamp_flash(m, f)
        for s in layer.segs:
            if sections is None or s.section in sections:
                self.stamp_capsule(m, s.x1, s.y1, s.x2, s.y2, s.ap.dia / 2.0)
        if sections is None and include_regions:
            for r in layer.regions:
                self.fill_polys(m, [r])
        return m


# --------------------------------------------------------------------------- labelling

def label(mask):
    """Run-length connected-component labelling, 8-connected.  -> (labels, count)."""
    require_numpy()
    lab = np.zeros(mask.shape, dtype=np.int32)
    parent = [0]

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    prev_runs = []
    for y in range(mask.shape[0]):
        row = mask[y]
        if not row.any():
            prev_runs = []
            continue
        d = np.diff(np.concatenate(([0], row.view(np.int8), [0])))
        starts = np.flatnonzero(d == 1)
        ends = np.flatnonzero(d == -1)
        runs = []
        pi = 0
        for s, e in zip(starts, ends):
            lid = 0
            while pi < len(prev_runs) and prev_runs[pi][1] < s - 1:
                pi += 1
            k = pi
            while k < len(prev_runs) and prev_runs[k][0] <= e:
                if lid == 0:
                    lid = find(prev_runs[k][2])
                else:
                    union(lid, prev_runs[k][2])
                k += 1
            if lid == 0:
                parent.append(len(parent))
                lid = len(parent) - 1
            lab[y, s:e] = lid
            runs.append((s, e - 1, lid))
        prev_runs = runs
    n = len(parent)
    remap = np.zeros(n, dtype=np.int32)
    nxt = 0
    for i in range(1, n):
        if find(i) == i:
            nxt += 1
            remap[i] = nxt
    for i in range(1, n):
        remap[i] = remap[find(i)]
    return remap[lab], nxt


def label_at(lab, grid, x, y):
    """The label under a board coordinate, or 0."""
    c, r = grid.col(x), grid.row(y)
    if 0 <= r < lab.shape[0] and 0 <= c < lab.shape[1]:
        return int(lab[r, c])
    return 0


def min_gap(lab, res, rounds=40):
    """Grow every label one pixel per round; report where two first meet.

    The reported gap is an L1 pixel bracket -- an UPPER bound on the true Euclidean
    gap.  Good enough to locate the tightest sites; the millimetre answer comes from
    the exact pass.  Returns None when nothing meets within `rounds`.
    """
    require_numpy()
    cur = lab.copy()
    best = None
    for k in range(1, rounds + 1):
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sh = np.roll(cur, (dy, dx), axis=(0, 1))
            if dy == 1:
                sh[0, :] = 0
            elif dy == -1:
                sh[-1, :] = 0
            if dx == 1:
                sh[:, 0] = 0
            elif dx == -1:
                sh[:, -1] = 0
            clash = (cur > 0) & (sh > 0) & (cur != sh)
            if clash.any() and best is None:
                ys, xs = np.nonzero(clash)
                best = (k, int(ys[0]), int(xs[0]),
                        int(cur[ys[0], xs[0]]), int(sh[ys[0], xs[0]]), int(clash.sum()))
            grow = (cur == 0) & (sh > 0)
            cur[grow] = sh[grow]
        if best is not None:
            break
    if best is None:
        return None
    return {"rounds": best[0], "gap_mm": (2 * best[0] - 1) * res,
            "row": best[1], "col": best[2], "labels": (best[3], best[4]),
            "touching_pixels": best[5]}


# --------------------------------------------------------------------------- PNG

def write_png(path, rgb):
    """rgb: uint8 array (h, w, 3).  No external image library."""
    h, w, _ = rgb.shape
    raw = b"".join(b"\x00" + rgb[y].tobytes() for y in range(h))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 6))
           + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)


def compose(masks, colors, bg=(16, 20, 16), downsample=2):
    """masks bottom-first -> an RGB image with Y flipped (Gerber Y is up)."""
    require_numpy()
    h, w = masks[0].shape
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:, :] = bg
    for m, c in zip(masks, colors):
        img[m] = c
    img = img[::-1]
    if downsample > 1:
        d = downsample
        hh, ww = (img.shape[0] // d) * d, (img.shape[1] // d) * d
        img = img[:hh, :ww].reshape(hh // d, d, ww // d, d, 3).mean(axis=(1, 3))
        img = img.astype(np.uint8)
    return img


# --------------------------------------------------------------------------- selftest

def _keyhole_contour():
    """One G36 contour: a 10x10 plate with a 2x2 hole reached by a ZERO-WIDTH channel.

    The channel is traversed out along y = 5.0 and back along the same y, so the two
    coincident edges are exactly the shape an EDA writes for a plane's anti-pad.
    """
    return [
        (0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0), (0.0, 5.0),
        # out along the channel to the hole (zero width: same y on the way back)
        (4.0, 5.0),
        (4.0, 6.0), (6.0, 6.0), (6.0, 4.0), (4.0, 4.0), (4.0, 5.0),
        (0.0, 5.0),
    ]


def _selftest():
    if np is None:
        print("raster selftest SKIPPED: numpy is not installed.")
        print("Everything else in verify/ runs without it.")
        return 0
    ok = True
    print("raster selftest")
    g = Grid(0, 0, 10, 10, res=0.01, margin=0.2)

    exact = g.blank()
    g.fill_polys(exact, [_keyhole_contour()])

    good = not bool(exact[g.row(5.0), g.col(5.0)])
    print("  keyhole: hole centre stays EMPTY               : %s" % ("OK" if good else "FAIL"))
    ok = ok and good

    # an isolated island inside the anti-pad must keep its own label
    m = g.blank()
    g.fill_polys(m, [_keyhole_contour()])
    g.stamp_capsule(m, 5.0, 5.0, 5.0, 5.0, 0.25)
    lab, n = label(m)
    plate = label_at(lab, g, 0.5, 0.5)
    via = label_at(lab, g, 5.0, 5.0)
    good = bool(plate) and bool(via) and plate != via
    print("  keyhole: plate label %d, island label %d        : %s"
          % (plate, via, "OK - separate, which is the truth" if good else "FAIL"))
    ok = ok and good

    # THE INVARIANT THE FAULT-4 FIX GUARANTEES: two coincident crossings open and
    # immediately close a zero-width span, so a keyhole channel deposits NO copper.
    slit = g.blank()
    X = 4.805                       # deliberately on a pixel-column boundary
    g.fill_polys(slit, [[(X, 2.0), (X, 8.0), (X, 8.0), (X, 2.0)]])
    good = int(slit.sum()) == 0
    print("  zero-width span contributes %d pixels          : %s"
          % (int(slit.sum()), "OK" if good else "FAIL"))
    ok = ok and good

    area = float(exact.sum()) * g.res * g.res
    good = abs(area - 96.0) < 0.5
    print("  keyhole plate area %.2f mm2 (want 96.00)      : %s"
          % (area, "OK" if good else "FAIL"))
    ok = ok and good

    m2 = g.blank()
    g.fill_polys(m2, [[(1.0, 1.0), (3.0, 1.0), (3.0, 3.0), (1.0, 3.0)]])
    g.fill_polys(m2, [[(3.2, 1.0), (5.0, 1.0), (5.0, 3.0), (3.2, 3.0)]])
    l2, n2 = label(m2)
    mg = min_gap(l2, g.res)
    good = n2 == 2 and mg is not None and abs(mg["gap_mm"] - 0.20) <= 0.02
    print("  two squares 0.20 mm apart -> %d labels, %.3f mm : %s"
          % (n2, mg["gap_mm"] if mg else float("nan"), "OK" if good else "FAIL"))
    ok = ok and good

    print()
    print("  NOTE ON REPRODUCING THE HISTORICAL LEAK")
    print("  The column-parity fill's failure is ALIGNMENT DEPENDENT: it needs two")
    print("  mathematically coincident crossings whose independent float evaluations")
    print("  round to adjacent pixel columns.  Synthetic geometry with clean decimal")
    print("  coordinates does NOT trigger it -- which is exactly why the fault survived")
    print("  several releases.  It only appears on real exported artwork, and the way")
    print("  to look for it is:")
    print("      python3 raster.py LAYER.G1 --compare-fills")
    print("  which rasterises the same layer both ways and reports any component that")
    print("  the two fills disagree about.  Any disagreement at all is the bug.")

    print("raster selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def compare_fills(layer, res=0.01, extent=None):
    """Rasterise one layer with the exact fill and with the OLD column-parity fill and
    report every difference.  This is the operational detector for fault 4 -- run it on
    a real plane layer, where the leak actually lives.  Any disagreement is the bug."""
    require_numpy()
    pts = ([(s.x1, s.y1) for s in layer.segs] + [(s.x2, s.y2) for s in layer.segs]
           + [(f.x, f.y) for f in layer.flashes] + [p for r in layer.regions for p in r])
    if extent:
        x0, y0, x1, y1 = extent
    else:
        x0 = min(p[0] for p in pts); y0 = min(p[1] for p in pts)
        x1 = max(p[0] for p in pts); y1 = max(p[1] for p in pts)
    g = Grid(x0, y0, x1, y1, res=res)

    def build(fill):
        m = g.blank()
        for f in layer.flashes:
            g.stamp_flash(m, f)
        for s in layer.segs:
            g.stamp_capsule(m, s.x1, s.y1, s.x2, s.y2, s.ap.dia / 2.0)
        for r in layer.regions:
            fill(m, [r])
        return m

    me = build(g.fill_polys)
    mf = build(g.fill_polys_column_parity)
    le, ne = label(me)
    lf, nf = label(mf)
    diff = int((me != mf).sum())
    print("  exact fill    : %d components, %.4f mm2"
          % (ne, float(me.sum()) * res * res))
    print("  parity fill   : %d components, %.4f mm2"
          % (nf, float(mf.sum()) * res * res))
    print("  pixels differing between the two fills: %d" % diff)
    if ne != nf:
        print("  ** THE TWO FILLS DISAGREE ABOUT THE COMPONENT COUNT.")
        print("  ** That is fault 4: the parity fill has merged (or split) copper that")
        print("  ** the artwork keeps apart.  Every clearance and connectivity number")
        print("  ** computed on the parity labelling is unproven.")
    elif diff:
        print("  component counts agree but %d pixel(s) differ -- inspect before"
              " trusting any number tighter than one pixel." % diff)
    else:
        print("  the two fills agree on this layer (no keyhole leak here).")
    return ne, nf, diff


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 2:
        print(__doc__)
        return 2
    require_numpy()
    import gerber
    path = argv[1]
    res = float(argv[argv.index("--res") + 1]) if "--res" in argv else 0.01
    lay = gerber.parse_gerber(open(path, encoding="utf-8", errors="replace").read(), path)
    if "--compare-fills" in argv:
        print("%s -- exact vs. column-parity fill (fault-4 detector)"
              % os.path.basename(path))
        ne, nf, diff = compare_fills(lay, res=res)
        return 1 if (ne != nf) else 0
    pts = [(s.x1, s.y1) for s in lay.segs] + [(s.x2, s.y2) for s in lay.segs] \
        + [(f.x, f.y) for f in lay.flashes] + [p for r in lay.regions for p in r]
    if "--extent" in argv:
        x0, y0, x1, y1 = [float(v) for v in argv[argv.index("--extent") + 1].split(",")]
    else:
        x0 = min(p[0] for p in pts); y0 = min(p[1] for p in pts)
        x1 = max(p[0] for p in pts); y1 = max(p[1] for p in pts)
    g = Grid(x0, y0, x1, y1, res=res)
    m = g.rasterise(lay)
    lab, n = label(m)
    print("%s" % os.path.basename(path))
    print("  extent %.3f %.3f .. %.3f %.3f at %.4f mm/px  (%d x %d)"
          % (x0, y0, x1, y1, res, g.w, g.h))
    print("  copper area   : %.3f mm2" % (float(m.sum()) * res * res))
    print("  components    : %d" % n)
    mg = min_gap(lab, res)
    print("  raster gap bracket: %s"
          % ("none within 40 px" if not mg
             else "%.4f mm between labels %s at row %d col %d"
                  % (mg["gap_mm"], mg["labels"], mg["row"], mg["col"])))
    print("  (a raster bracket is an UPPER bound -- measure it exactly with clearance.py)")
    if "--png" in argv:
        out = argv[argv.index("--png") + 1]
        write_png(out, compose([m], [(220, 170, 60)]))
        print("  wrote %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
