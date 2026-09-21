#!/usr/bin/env python3
"""Regression tests for dimension semantics and infeasible fabrication geometry."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

import electrical_calcs as calcs

ROOT = Path(__file__).resolve().parents[1]


class FabricationCalculations(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/'assets/fabrication-calcs.example.json').read_text(encoding='utf-8'))

    def result(self, index, **changes):
        item = copy.deepcopy(self.data['calculations'][index])
        item.update(changes)
        return calcs.calculate(item)['results']

    def test_mask_expands_on_both_sides(self):
        result = self.result(0)
        self.assertAlmostEqual(result['left_opening_mm'], .49)
        self.assertAlmostEqual(result['nominal_web_mm'], .11)
        self.assertAlmostEqual(result['web_margin_mm'], .01)

    def test_larger_mask_opening_consumes_dam(self):
        result = self.result(0, left_expansion_per_side_mm=.05, right_expansion_per_side_mm=.05)
        self.assertAlmostEqual(result['left_opening_mm'], .55)
        self.assertLess(result['web_margin_mm'], 0)

    def test_negative_mask_expansion_is_supported(self):
        result = self.result(0, left_expansion_per_side_mm=-.05)
        self.assertAlmostEqual(result['left_opening_mm'], .35)
        self.assertAlmostEqual(result['nominal_web_mm'], .18)

    def test_closed_mask_and_nonfinite_expansion_rejected(self):
        for value in (-.225, -.3, float('nan'), float('inf'), True, '0.02'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.result(0, left_expansion_per_side_mm=value)

    def test_article_escape_is_infeasible(self):
        result = self.result(1)
        self.assertAlmostEqual(result['gap_mm'], .35)
        self.assertAlmostEqual(result['single_trace_max_width_mm'], -.01)
        self.assertAlmostEqual(result['gap_margin_mm'], -.16)

    def test_unequal_pads_and_multiple_traces(self):
        result = self.result(1, pitch_mm=1.0, left_pad_width_mm=.3, right_pad_width_mm=.5,
                             clearance_mm=.1, trace_width_mm=.1, trace_count=2)
        self.assertAlmostEqual(result['gap_mm'], .6)
        self.assertAlmostEqual(result['required_gap_mm'], .5)
        self.assertAlmostEqual(result['gap_margin_mm'], .1)

    def test_invalid_count_or_clearance_rejected(self):
        for value in (True, 0, -1, 1.5):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.result(1, trace_count=value)
        for value in (0, -1, float('nan')):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.result(1, clearance_mm=value)

    def test_hole_offset_consumes_radial_ring(self):
        result = self.result(2)
        self.assertAlmostEqual(result['nominal_ring_mm'], .15)
        self.assertAlmostEqual(result['offset_adjusted_ring_mm'], .1)
        self.assertAlmostEqual(result['ring_margin_mm'], 0)
        self.assertLess(self.result(2, radial_offset_mm=.06)['ring_margin_mm'], 0)
        self.assertLess(self.result(2, hole_diameter_mm=.7)['nominal_ring_mm'], 0)

    def test_missing_hole_basis_not_inferred(self):
        item = copy.deepcopy(self.data['calculations'][2]); del item['hole_basis']
        with self.assertRaises(KeyError): calcs.calculate(item)
        for value in ('unknown', '', None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.result(2, hole_basis=value)

    def test_cli_returns_calculations_not_approval(self):
        result = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT/'scripts/electrical_calcs.py'),
                                 '--input', str(ROOT/'assets/fabrication-calcs.example.json')],
                                capture_output=True, text=True, check=True)
        items = json.loads(result.stdout)['calculations']
        self.assertEqual(len(items), 3)
        self.assertTrue(all(item['status']=='CALCULATED' and item['hardware_validation']=='NOT_RUN' for item in items))
        self.assertLess(items[1]['results']['gap_margin_mm'], 0)
        bad = copy.deepcopy(self.data); bad['calculations'][0]['source'] = ''
        with self.assertRaises(ValueError): calcs.run(bad)


if __name__ == '__main__':
    unittest.main(verbosity=2)
