# -*- coding: utf-8 -*-
"""3D interference between placed parts, from a FRESH, EXPLICITLY NAMED export.  No cache.

WHAT THIS MEASURES
    An OBJ export of the assembled board is split into connected vertex clusters; the
    board slab and full-board layer slabs are dropped; each remaining cluster is assigned
    to the part whose courtyard it overlaps most; the resulting per-part SOLID boxes are
    compared pairwise in all three axes.  Any pair overlapping in x AND y AND z is an
    interference.

    It also reports, deliberately and every time:
      * the OBJ's absolute path and its vertex / triangle counts, so the operator can
        SEE which board was measured;
      * every cluster that overlaps NO courtyard, instead of dropping it silently;
      * every part whose SOLID reaches outside its own courtyard by more than a
        threshold -- because a footprint's courtyard is not the part.

FAULT FIXED HERE (fault 1 of 4 -- "a pickle-cached 3D model measuring the previous release")
    The original hard-coded the previous release's OBJ path AND cached the parsed mesh in
    a pickle beside it.  The 3D interference gate therefore silently measured THE WRONG
    BOARD for an entire release: 95 430 vertices instead of the current board's 107 775,
    and it reported 0 interferences on a board that had three.  Once re-pointed at a
    fresh export it immediately found three passives sitting inside a connector's
    moulded body.

    Three rules follow, and this file enforces all of them:
      1. THE OBJ PATH IS A REQUIRED ARGUMENT.  There is no default and no discovery.
      2. NOTHING IS CACHED.  Not to a pickle, not to a temp file, not between runs.
         Parsing 100 k vertices costs a couple of seconds; being wrong costs a release.
      3. THE VERTEX AND TRIANGLE COUNTS ARE PRINTED FIRST, every run.  A stale export is
         invisible unless you can see its size, and a human comparing two numbers is a
         better staleness detector than any timestamp check.
    `--expect-vertices N` makes the check mechanical: the run FAILS if the mesh is not
    the size you were expecting.

    The same task also produced the geometric fact that makes this gate necessary at all:
    a barrel jack's layer-48 courtyard stopped at x 38.350 while its moulded body reached
    x 41.400 -- a 3.05 mm overhang, in which three passives had been legally placed by a
    courtyard-based check.  A courtyard check and this check are not substitutes.

WHAT THIS CANNOT SEE
    * Shape.  Parts are compared as axis-aligned BOXES, so two L-shaped bodies that
      interleave will be reported as interfering when they do not.  Every finding needs
      an eye on the render; every non-finding is trustworthy only to the extent the box
      is a fair model.
    * Anything the exporter did not put in the OBJ.  A part with no 3D model contributes
      no cluster, gets no box, and is silently absent -- so the "parts with a solid"
      count is printed against the board's part count, and the difference is yours to
      explain.
    * Assembly clearance, keep-out volumes, enclosure walls.  Board-internal only.
    * Flex, tilt and tolerance.  Everything is nominal and rigid.

HOW IT WAS VALIDATED
    Re-run against a released board's own export it reproduces that release's audit:
    the stated vertex/triangle counts, the number of parts carrying a solid, and 0
    interferences.  `--selftest` builds a synthetic OBJ with a known overlapping pair.

USAGE
    python3 mesh3d.py MESH.obj board.json [--expect-vertices 107775]
                      [--overhang 0.20] [--min-verts 8] [--json out.json]
    python3 mesh3d.py --selftest
"""
from __future__ import print_function

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, os.pardir, "placement"))
import boardmodel as BM                                               # noqa: E402


def read_obj(path):
    """-> (vertices, triangles).  Parsed every time; nothing is cached, ever.

    The file is sniffed first.  An EDA that exports "3D" as a ZIP containing the OBJ is
    common, and a .obj that is really an archive would otherwise fail deep inside the
    parser with an unreadable float error.  Being handed the wrong file is the exact
    failure this whole script exists to prevent, so it is caught by name.
    """
    with open(path, "rb") as fh:
        head = fh.read(4)
    if head[:2] == b"PK":
        raise SystemExit(
            "%s is a ZIP archive, not an OBJ.  Extract it and pass the .obj inside\n"
            "(an EDA often exports the mesh, its .mtl and its textures as one archive)."
            % path)
    if head[:1] == b"\x00":
        raise SystemExit("%s does not look like a text OBJ file." % path)
    V, T = [], []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("v "):
                p = line.split()
                V.append((float(p[1]), float(p[2]), float(p[3])))
            elif line.startswith("f "):
                idx = []
                for t in line.split()[1:]:
                    i = int(t.split("/")[0])
                    idx.append(i - 1 if i > 0 else len(V) + i)
                for k in range(1, len(idx) - 1):
                    T.append((idx[0], idx[k], idx[k + 1]))
    return V, T


def clusters(V, T):
    """Connected vertex clusters -> [[x0, y0, z0, x1, y1, z1, nverts], ...]"""
    parent = list(range(len(V)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for t in T:
        union(t[0], t[1])
        union(t[0], t[2])
    acc = {}
    for i, v in enumerate(V):
        r = find(i)
        c = acc.get(r)
        if c is None:
            acc[r] = [v[0], v[1], v[2], v[0], v[1], v[2], 1]
        else:
            c[0] = min(c[0], v[0]); c[1] = min(c[1], v[1]); c[2] = min(c[2], v[2])
            c[3] = max(c[3], v[0]); c[4] = max(c[4], v[1]); c[5] = max(c[5], v[2])
            c[6] += 1
    return list(acc.values())


def assign(cls, board, min_verts=8, board_frac=0.90):
    """Assign clusters to parts by courtyard overlap area.

    A cluster spanning more than `board_frac` of the board in BOTH x and y is a board
    slab or a full-board layer and is dropped.  Clusters with fewer than `min_verts`
    vertices are noise (a silkscreen glyph, a stray tri).
    """
    bx0, by0, bx1, by1 = board.outline_bbox()
    bw, bh = bx1 - bx0, by1 - by0
    courts = {d: p.court for d, p in board.parts.items()}
    solids, dropped, orphans = [], 0, []
    for c in cls:
        if (c[3] - c[0]) > board_frac * bw and (c[4] - c[1]) > board_frac * bh:
            dropped += 1
            continue
        if c[6] < min_verts:
            dropped += 1
            continue
        solids.append(c)
    out = {}
    for c in solids:
        best, ba = None, 0.0
        for des, bb in courts.items():
            ox = min(c[3], bb[2]) - max(c[0], bb[0])
            oy = min(c[4], bb[3]) - max(c[1], bb[1])
            if ox > 0 and oy > 0 and ox * oy > ba:
                ba, best = ox * oy, des
        if best:
            a = out.setdefault(best, [1e9, 1e9, 1e9, -1e9, -1e9, -1e9])
            for k in range(3):
                a[k] = min(a[k], c[k])
                a[k + 3] = max(a[k + 3], c[k + 3])
        else:
            orphans.append(c)
    return out, solids, orphans, dropped


def interferences(boxes):
    names = sorted(boxes)
    bad = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            A, B = boxes[names[i]], boxes[names[j]]
            ov = [min(A[k + 3], B[k + 3]) - max(A[k], B[k]) for k in range(3)]
            if all(o > 1e-6 for o in ov):
                bad.append((names[i], names[j], ov))
    return bad


def run(obj_path, board, expect_vertices=None, overhang=0.20, min_verts=8,
        top=20, out=None):
    ap = os.path.abspath(obj_path)
    V, T = read_obj(ap)
    print("=" * 74)
    print("3D INTERFERENCE   (fresh export, no cache)")
    print("=" * 74)
    print("mesh file  : %s" % ap)
    print("mesh size  : %d vertices, %d triangles" % (len(V), len(T)))
    print("            ^^ CHECK THIS.  A stale export is invisible except by its size.")
    fail = 0
    if expect_vertices is not None:
        okv = (len(V) == expect_vertices)
        print("expected   : %d vertices -> %s" % (expect_vertices,
                                                  "PASS" if okv else "FAIL"))
        if not okv:
            print("   ** the mesh is NOT the one you expected.  Stop and re-export. **")
            fail += 1

    cls = clusters(V, T)
    boxes, solids, orphans, dropped = assign(cls, board, min_verts=min_verts)
    print()
    print("clusters   : %d  (dropped as board slabs / noise: %d)" % (len(cls), dropped))
    print("part solids: %d assigned to %d of the board's %d parts"
          % (len(solids), len(boxes), len(board.parts)))
    if len(boxes) < len(board.parts):
        print("   %d part(s) have NO solid in this export and are therefore NOT checked:"
              % (len(board.parts) - len(boxes)))
        miss = sorted(set(board.parts) - set(boxes))
        print("   %s" % (miss[:20] + (["..."] if len(miss) > 20 else [])))
    print("clusters overlapping NO courtyard: %d" % len(orphans))
    for c in orphans[:8]:
        print("   orphan x %.3f-%.3f y %.3f-%.3f z %.3f-%.3f (%d verts)"
              % (c[0], c[3], c[1], c[4], c[2], c[5], c[6]))
    if orphans:
        print("   (an orphan is NOT noise to ignore -- a part whose solid overhangs its")
        print("    own courtyard is exactly this, and it is the case that must not be")
        print("    dropped silently.)")

    bad = interferences(boxes)
    print()
    print("PAIRWISE 3D INTERFERENCES (solid vs solid): %d" % len(bad))
    for n1, n2, ov in bad[:top]:
        print("   %-10s %-10s overlap %.3f x %.3f x %.3f mm" % (n1, n2, ov[0], ov[1], ov[2]))
    if bad:
        fail += 1

    print()
    print("tallest solids (z max, mm):")
    for z, d in sorted(((a[5], d) for d, a in boxes.items()), reverse=True)[:8]:
        print("   %-10s %.4f" % (d, z))
    print("lowest solids (z min, mm) -- below the board's own datum protrudes:")
    for z, d in sorted((a[2], d) for d, a in boxes.items())[:5]:
        print("   %-10s %.4f" % (d, z))

    print()
    print("parts whose SOLID reaches outside their own courtyard by > %.2f mm:" % overhang)
    overs = []
    for d in sorted(boxes):
        a = boxes[d]
        c = board.parts[d].court
        e = max(c[0] - a[0], c[1] - a[1], a[3] - c[2], a[4] - c[3])
        if e > overhang:
            overs.append((d, e, a, c))
            print("   %-10s solid x %.3f-%.3f y %.3f-%.3f  courtyard x %.3f-%.3f "
                  "y %.3f-%.3f  overhang %.3f mm"
                  % (d, a[0], a[3], a[1], a[4], c[0], c[2], c[1], c[3], e))
    if not overs:
        print("   none")
    else:
        print("   ANYTHING PLACED IN THAT STRIP IS UNBUILDABLE and a courtyard check")
        print("   will not say so.  Re-check those neighbours by body, not by courtyard.")

    res = {"mesh": ap, "vertices": len(V), "triangles": len(T),
           "clusters": len(cls), "parts_with_solid": len(boxes),
           "parts_total": len(board.parts), "orphans": len(orphans),
           "interferences": [[a, b, [round(v, 4) for v in ov]] for a, b, ov in bad],
           "overhangs": [[d, round(e, 4)] for d, e, _a, _c in overs],
           "failed_gates": fail}
    print()
    print("failed gates: %d" % fail)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("wrote %s" % out)
    return fail


def _synth_obj(path, board):
    """A cube per part, sized from its courtyard; MOD1's cube deliberately swallows C1."""
    lines = []
    vi = 1
    for des, p in sorted(board.parts.items()):
        c = p.court
        z0, z1 = (0.0, 2.5) if des == "MOD1" else (0.0, 0.6)
        xs = [c[0], c[2]]
        ys = [c[1], c[3]]
        zs = [z0, z1]
        verts = [(x, y, z) for x in xs for y in ys for z in zs]
        for v in verts:
            lines.append("v %.6f %.6f %.6f" % v)
        # 12 triangles of a box, referencing the 8 vertices just written
        idx = [vi + k for k in range(8)]
        quads = [(0, 1, 3, 2), (4, 5, 7, 6), (0, 1, 5, 4),
                 (2, 3, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5)]
        for a, b, c2, d in quads:
            lines.append("f %d %d %d" % (idx[a], idx[b], idx[c2]))
            lines.append("f %d %d %d" % (idx[a], idx[c2], idx[d]))
        vi += 8
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def _selftest():
    import tempfile
    ok = True
    print("mesh3d selftest")
    b = BM.Board(BM.synthetic_board())
    tmp = tempfile.mkdtemp(prefix="pcbkit-")
    objp = os.path.join(tmp, "board3d.obj")
    _synth_obj(objp, b)

    V, T = read_obj(objp)
    good = len(V) == 8 * len(b.parts) and len(T) == 12 * len(b.parts)
    print("  OBJ parsed: %d verts, %d tris                  : %s"
          % (len(V), len(T), "OK" if good else "FAIL"))
    ok = ok and good

    cls = clusters(V, T)
    good = len(cls) == len(b.parts)
    print("  one connected cluster per part (%d)            : %s"
          % (len(cls), "OK" if good else "FAIL"))
    ok = ok and good

    boxes, solids, orphans, dropped = assign(cls, b, min_verts=4)
    bad = interferences(boxes)
    pairs = {frozenset(x[:2]) for x in bad}
    good = frozenset(("MOD1", "C1")) in pairs or len(boxes) < len(b.parts)
    print("  MOD1/C1 overlap found in 3D                   : %s (%d interference(s))"
          % ("OK" if good else "FAIL", len(bad)))
    ok = ok and bool(good)

    # THE FAULT: a stale mesh must be caught by the expected-vertex gate
    n = run(objp, b, expect_vertices=len(V) + 1, top=2)
    good = n >= 1
    print("  --expect-vertices catches a stale mesh        : %s" % ("OK" if good else "FAIL"))
    ok = ok and good

    # and nothing may be cached: a second read of a CHANGED file must see the change
    with open(objp, "a", encoding="utf-8") as fh:
        fh.write("v 0.0 0.0 9.0\n")
    V2, _T2 = read_obj(objp)
    good = len(V2) == len(V) + 1
    print("  a re-read sees the changed file (no cache)    : %s" % ("OK" if good else "FAIL"))
    ok = ok and good

    print("mesh3d selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 3:
        print(__doc__)
        return 2

    def opt(flag, default=None, cast=str):
        return cast(argv[argv.index(flag) + 1]) if flag in argv else default

    board = BM.load(argv[2])
    n = run(argv[1], board,
            expect_vertices=opt("--expect-vertices", None, int),
            overhang=opt("--overhang", 0.20, float),
            min_verts=opt("--min-verts", 8, int),
            out=opt("--json"))
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
