#!/usr/bin/env python3
"""Independent CLI acceptance regressions for board outlines; no EDA connection.

Run with a TEMP/TMP directory on the desired work drive. All fixtures are generated
in a TemporaryDirectory and removed. Every case runs the public pcb_toolkit.py CLI.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/pcb_toolkit.py"
HEADER = "%FSLAX26Y26*%\n%MOMM*%\n%ADD10C,0.2*%\nD10*\n"
RECT = [(0, 0), (20, 0), (20, 10), (0, 10)]
U = [(0, 0), (10, 0), (10, 10), (7, 10), (7, 3), (3, 3), (3, 10), (0, 10)]


def coord(point, op):
    return "X%dY%dD0%d*\n" % (round(point[0] * 1e6), round(point[1] * 1e6), op)


def segments(lines):
    return HEADER + "".join(coord(a, 2) + coord(b, 1) for a, b in lines) + "M02*\n"


def ring(points):
    return segments(list(zip(points, points[1:] + points[:1])))


def region(points):
    return HEADER + "G36*\n" + coord(points[0], 2) + "".join(
        coord(p, 1) for p in points[1:] + points[:1]) + "G37*\nM02*\n"


def flash(x, y, aperture="C,0.2"):
    return HEADER.replace("C,0.2", aperture) + coord((x, y), 3) + "M02*\n"


def drill(x, y, dia=.2, end=None):
    line = "X%.6fY%.6f" % (x, y)
    if end is not None:
        line += "G85X%.6fY%.6f" % end
    return "M48\nMETRIC,LZ\nT1C%.6f\n%%\nT1\n%s\nM30\n" % (dia, line)


class OutlineAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="outline-acceptance-")
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.serial = 0

    def cli(self, outline=None, copper=None, drills=None, args=(), code=0):
        self.serial += 1
        op = self.folder / ("outline%d.GKO" % self.serial)
        op.write_text(ring(RECT) if outline is None else outline, encoding="utf-8")
        report = self.folder / ("result%d.json" % self.serial)
        command = [sys.executable, "-B", "-X", "utf8", str(CLI), "outline", str(op),
                   "--json", str(report), *args]
        for flag, contents in (("--copper", copper), ("--drills", drills)):
            if contents is not None:
                path = self.folder / (flag[2:] + str(self.serial))
                path.write_text(contents, encoding="utf-8")
                command.extend([flag, str(path)])
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
        result = subprocess.run(command, text=True, capture_output=True, env=env)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        return json.loads(report.read_text(encoding="utf-8")), result.stdout + result.stderr

    def test_closed_centreline_size_and_missing_coverage(self):
        result, output = self.cli(args=("--size", "20,10"))
        self.assertEqual(result["size"], [20, 10])
        self.assertTrue(result["closed"])
        self.assertEqual(result["copper_status"], "not_supplied")
        self.assertEqual(result["drill_status"], "not_supplied")
        self.assertEqual(output.count("NOT CHECKED"), 2)
        self.assertNotIn("19.8000", output)
        self.assertIn("approximation", result)

    def test_reversed_shuffled_segments(self):
        lines = list(zip(RECT, RECT[1:] + RECT[:1]))
        text = segments([(lines[i][1], lines[i][0]) if i % 2 else lines[i]
                         for i in (2, 0, 3, 1)])
        self.cli(outline=text)

    def test_gap_previously_falsely_closed(self):
        lines = [((0, 0), (20, 0)), ((20, 0), (20, 10)),
                 ((20, 10), (0, 10)), ((0, 5), (0, 0))]
        result, output = self.cli(outline=segments(lines), code=2)
        self.assertEqual(result["status"], "not_checked")
        self.assertIn("open or branched", output)

    def test_self_intersection(self):
        self.cli(outline=ring([(0, 0), (10, 10), (0, 10), (10, 0)]), code=2)

    def test_adjacent_overlap(self):
        self.cli(outline=ring([(0, 0), (10, 0), (5, 0), (5, 10), (0, 10)]), code=2)

    def test_duplicate_segment(self):
        self.cli(outline=ring(RECT).replace("M02*", coord((0, 0), 2) + coord((20, 0), 1)), code=2)

    def test_zero_length_segment(self):
        self.cli(outline=ring(RECT).replace("M02*", coord((0, 0), 1)), code=2)

    def test_multiple_outer_rings(self):
        self.cli(outline=ring(RECT).replace("M02*", "") +
                 ring([(30, 0), (40, 0), (40, 10), (30, 10)]), code=2)

    def test_inner_cutout_rejected(self):
        self.cli(outline=ring(RECT).replace("M02*", "") +
                 ring([(5, 3), (7, 3), (7, 5), (5, 5)]), code=2)

    def test_region_outline_rejected(self):
        self.cli(outline=region(RECT), code=2)

    def test_flash_outline_rejected(self):
        self.cli(outline=flash(1, 1), code=2)

    def test_empty_outline(self):
        self.cli(outline=HEADER + "M02*\n", code=2)

    def test_size_violation(self):
        self.cli(args=("--size", "21,10"), code=1)

    def test_copper_inside_margin_fails(self):
        result, _ = self.cli(copper=flash(.2, 5), code=1)
        self.assertAlmostEqual(result["min_copper_margin"], .1)
        self.assertEqual(result["copper_outside"], 0)
        self.assertEqual(result["copper_margin_violations"], 1)

    def test_copper_exact_threshold_passes(self):
        result, _ = self.cli(copper=flash(.4, 5))
        self.assertAlmostEqual(result["min_copper_margin"], .3)

    def test_copper_outside_even_zero_margin(self):
        self.cli(copper=flash(.05, 5), args=("--edge", "0"), code=1)

    def test_copper_rect_vertices_inside_edges_cross_concavity(self):
        result, _ = self.cli(outline=ring(U), copper=flash(5, 7, "R,8X1"),
                             args=("--edge", "0"), code=1)
        self.assertLess(result["min_copper_margin"], 0)

    def test_copper_region_edges_cross_concavity(self):
        self.cli(outline=ring(U), copper=region([(1, 6), (9, 6), (9, 7), (1, 7)]), code=1)

    def test_region_full_edges_too_close_but_vertices_far(self):
        # Notch tip (3,3)-(7,3) lies 0.1 above this region's top edge.
        result, _ = self.cli(outline=ring(U), copper=region([(1, 1), (9, 1), (9, 2.9), (1, 2.9)]), code=1)
        self.assertAlmostEqual(result["min_copper_margin"], .1)

    def test_concave_safe_copper(self):
        self.cli(outline=ring(U), copper=flash(1.5, 7, "R,1X1"))

    def test_copper_track_crossing_notch(self):
        self.cli(outline=ring(U), copper=segments([((1, 7), (9, 7))]), code=1)

    def test_drill_inside_margin_fails(self):
        result, _ = self.cli(drills=drill(.2, 5), code=1)
        self.assertAlmostEqual(result["min_drill_margin"], .1)
        self.assertEqual(result["drill_outside"], 0)

    def test_drill_exact_threshold_passes(self):
        self.cli(drills=drill(.4, 5))

    def test_slot_endpoints_inside_crosses_notch(self):
        self.cli(outline=ring(U), drills=drill(1, 7, end=(9, 7)), args=("--edge", "0"), code=1)

    def test_slot_midpoint_edge_distance(self):
        result, _ = self.cli(outline=ring(U), drills=drill(1, 2.8, end=(9, 2.8)), code=1)
        self.assertAlmostEqual(result["min_drill_margin"], .1)

    def test_safe_slot(self):
        self.cli(drills=drill(2, 5, end=(18, 5)))

    def test_empty_copper(self):
        result, output = self.cli(copper=HEADER + "M02*\n", code=1)
        self.assertEqual(result["copper_status"], "incomplete")
        self.assertIsNone(result["min_copper_margin"])
        self.assertIn("NOT CHECKED", output)

    def test_empty_drills(self):
        result, output = self.cli(drills="M48\nMETRIC,LZ\nM30\n", code=1)
        self.assertEqual(result["drill_status"], "incomplete")
        self.assertIsNone(result["min_drill_margin"])
        self.assertIn("NOT CHECKED", output)

    def test_undefined_drill_tool(self):
        self.cli(drills="M48\nMETRIC,LZ\nT1\nX2Y5\nM30\n", code=2)

    def test_negative_or_nonfinite_options(self):
        for args in (("--edge", "nan"), ("--edge", "inf"), ("--edge", "-0.1"),
                     ("--tol", "nan"), ("--tol", "0"), ("--tol", "-1"),
                     ("--size", "nan,10"), ("--size", "20,inf"),
                     ("--size", "-20,10"), ("--size", "20"), ("--size", "20,10,1")):
            with self.subTest(args=args):
                # '=' keeps a negative comma-separated value from looking like a flag.
                self.cli(args=(args[0] + "=" + args[1],), code=2)

    def test_invalid_copper_aperture(self):
        for value in ("nan", "inf", "-1", "0"):
            with self.subTest(value=value):
                self.cli(copper=flash(5, 5, "C," + value), code=2)

    def test_invalid_outline_pen(self):
        for value in ("nan", "inf", "-1"):
            with self.subTest(value=value):
                self.cli(outline=ring(RECT).replace("C,0.2", "C," + value), code=2)

    def test_zero_drill_diameter(self):
        self.cli(drills=drill(5, 5, dia=0), code=2)

    def test_nonround_copper_stroke_rejected(self):
        self.cli(copper=segments([((2, 5), (18, 5))]).replace("C,0.2", "R,1X2"), code=2)

    def test_rounded_flash_and_obround(self):
        self.cli(copper=flash(5, 5, "O,2X1"))
        self.cli(copper=flash(5, 5, "RoundRect,0.2X-1X-0.5X1X-0.5X1X0.5X-1X0.5"))

    def test_circular_outline(self):
        text = HEADER + "G75*\nX10000000Y5000000D02*\nG03X10000000Y5000000I-5000000J0D01*\nM02*\n"
        self.cli(outline=text, copper=flash(5, 5))

    def test_multiple_files_counted_individually(self):
        # Explicitly supplied empty layers must not disappear behind another layer.
        extra = self.folder / "empty.GTL"
        extra.write_text(HEADER + "M02*\n", encoding="utf-8")
        full = self.folder / "full.GTL"
        full.write_text(flash(5, 5), encoding="utf-8")
        result, _ = self.cli(args=("--copper", str(full), str(extra)), code=1)
        self.assertEqual(len(result["coverage"]["copper"]), 2)
        self.assertEqual(result["copper_status"], "incomplete")


if __name__ == "__main__":
    unittest.main(verbosity=2)
