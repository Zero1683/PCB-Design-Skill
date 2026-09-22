#!/usr/bin/env python3
"""Physical pad identity regressions, including the public reconcile CLI."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / 'vendor/pcb-skill-toolkit/scripts'
sys.path[:0] = [str(VENDOR / 'placement'), str(VENDOR / 'verify')]
import boardmodel as BM
import pad_reconcile as PR


def fixture():
    return {
        'schema': 1, 'units': 'mm',
        'components': [{'des': 'J1', 'footprint': 'FP', 'x': 0, 'y': 0}],
        'footprints': {'FP': {'pads': [
            {'num': '1', 'elem': 'land-a', 'x': 0, 'y': 0, 'w': 1, 'h': 1},
            {'num': '1', 'elem': 'land-b', 'x': 2, 'y': 0, 'w': 1, 'h': 1},
        ]}},
        'pad_nets': {'J1.1': 'VCC', 'J1#land-a': 'VCC', 'J1#land-b': 'VCC'},
        'nets': {'VCC': [['J1', '1']]},
    }


class PhysicalPadIdentityTests(unittest.TestCase):
    def clean(self, doc):
        result = PR.reconcile(BM.Board(doc))
        self.assertFalse(any(result[k] for k in ('differ', 'extra', 'missing', 'net_diff')))
        return result

    def test_legacy_unique_numbers_remain_compatible(self):
        self.clean(BM.synthetic_board())

    def test_repeated_same_net_preserves_two_lands(self):
        doc = fixture()
        result = self.clean(doc)
        self.assertEqual(result['multi_land_pads'], {'J1.1': 2})
        self.assertEqual(result['physical_have'], {'J1#land-a': 'VCC', 'J1#land-b': 'VCC'})

    def test_element_only_maps_work(self):
        doc = fixture()
        del doc['pad_nets']['J1.1']
        self.clean(doc)

    def test_original_wrong_first_land_cannot_pass(self):
        doc = fixture()
        doc['pad_nets']['J1#land-a'] = 'GND'
        with self.assertRaisesRegex(BM.BoardError, 'number/element net mismatch'):
            BM.Board(doc)

    def test_wrong_last_land_cannot_pass(self):
        doc = fixture()
        doc['pad_nets']['J1#land-b'] = 'GND'
        with self.assertRaisesRegex(BM.BoardError, 'number/element net mismatch'):
            BM.Board(doc)

    def test_element_only_mixed_nets_check_each_land(self):
        doc = fixture()
        del doc['pad_nets']['J1.1']
        doc['pad_nets']['J1#land-a'] = 'GND'
        board = BM.Board(doc)
        self.assertEqual([p['net'] for p in board.all_pads()], ['GND', 'VCC'])
        result = PR.reconcile(board)
        self.assertEqual(result['differ'], [('J1#land-a', 'VCC', 'GND')])
        self.assertEqual(result['have']['J1.1'], ['GND', 'VCC'])
        self.assertEqual(result['net_diff'], ['GND'])

    def test_repeated_missing_element_rejected(self):
        doc = fixture()
        del doc['footprints']['FP']['pads'][0]['elem']
        with self.assertRaisesRegex(BM.BoardError, 'requires its own element net'):
            BM.Board(doc)

    def test_repeated_missing_element_net_rejected(self):
        doc = fixture()
        del doc['pad_nets']['J1#land-a']
        with self.assertRaisesRegex(BM.BoardError, 'requires its own element net'):
            BM.Board(doc)

    def test_repeated_number_only_net_rejected(self):
        doc = fixture()
        doc['pad_nets'] = {'J1.1': 'VCC'}
        with self.assertRaises(BM.BoardError):
            BM.Board(doc)

    def test_duplicate_element_rejected_even_with_different_numbers(self):
        for second_number in ('1', '2'):
            with self.subTest(second_number=second_number):
                doc = fixture()
                doc['footprints']['FP']['pads'][1].update(elem='land-a', num=second_number)
                with self.assertRaisesRegex(BM.BoardError, 'duplicate physical pad element'):
                    BM.Board(doc)

    def test_invalid_element_rejected(self):
        for element in ('', ' ', 1, [], {}):
            with self.subTest(element=element):
                doc = fixture()
                doc['footprints']['FP']['pads'][0]['elem'] = element
                with self.assertRaises(BM.BoardError):
                    BM.Board(doc)

    def test_unknown_element_or_number_net_rejected(self):
        for key in ('J1#ghost', 'J1.99', 'J2.1'):
            with self.subTest(key=key):
                doc = fixture()
                doc['pad_nets'][key] = 'VCC'
                with self.assertRaisesRegex(BM.BoardError, 'missing physical pads'):
                    BM.Board(doc)

    def test_explicit_unassigned_land_is_not_hidden_by_connected_land(self):
        doc = fixture()
        del doc['pad_nets']['J1.1']
        doc['pad_nets']['J1#land-a'] = ''
        result = PR.reconcile(BM.Board(doc))
        self.assertEqual(result['differ'], [('J1#land-a', 'VCC', '')])

    def test_missing_unique_pad_net_is_mismatch(self):
        doc = BM.synthetic_board()
        del doc['pad_nets']['MOD1.1']
        result = PR.reconcile(BM.Board(doc))
        self.assertIn(('MOD1.1', 'GND', ''), result['differ'])

    def test_element_ids_are_scoped_to_component(self):
        doc = fixture()
        doc['components'].append({'des': 'J2', 'footprint': 'FP', 'x': 5, 'y': 0})
        doc['pad_nets'].update({'J2#land-a': 'VCC', 'J2#land-b': 'VCC'})
        doc['nets']['VCC'].append(['J2', '1'])
        self.assertEqual(len(self.clean(doc)['physical_have']), 4)

    def test_conflicting_schematic_members_rejected_in_either_order(self):
        for nets in ({'GND': [['J1', '1']], 'VCC': [['J1', '1']]},
                     {'VCC': [['J1', '1']], 'GND': [['J1', '1']]}):
            with self.subTest(nets=nets):
                with self.assertRaisesRegex(BM.BoardError, 'conflicting nets'):
                    PR.reconcile(BM.Board(fixture()), nets)

    def test_same_net_repeated_schematic_member_is_idempotent(self):
        doc = fixture()
        doc['nets']['VCC'].append(['J1', 1])
        self.clean(doc)

    def test_invalid_net_values_fail_clearly(self):
        for net in (None, 0, False, [], {}, ' '):
            with self.subTest(net=net):
                doc = fixture()
                doc['pad_nets']['J1#land-a'] = net
                with self.assertRaisesRegex(BM.BoardError, 'invalid pad net'):
                    BM.Board(doc)

    def test_invalid_netlists_fail_clearly(self):
        for nets in ([['VCC']], {'VCC': None}, {' ': [['J1', '1']]},
                     {'VCC': ['J1']}, {'VCC': [['J1']]}, {'VCC': [['J1', None]]}):
            with self.subTest(nets=nets):
                with self.assertRaises(BM.BoardError):
                    PR.reconcile(BM.Board(fixture()), nets)

    def test_board_file_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory(prefix='pad-duplicate-') as folder:
            path = Path(folder) / 'board.json'
            raw = json.dumps(fixture()).replace('"J1#land-a": "VCC"',
                                               '"J1#land-a": "GND", "J1#land-a": "VCC"')
            path.write_text(raw, encoding='utf-8')
            with self.assertRaisesRegex(BM.BoardError, 'duplicate JSON key'):
                BM.load(path)

    def test_public_cli_duplicate_netlist_json_key_rejected(self):
        with tempfile.TemporaryDirectory(prefix='pad-netlist-') as folder:
            board = Path(folder) / 'board.json'
            nets = Path(folder) / 'netlist.json'
            board.write_text(json.dumps(fixture()), encoding='utf-8')
            nets.write_text('{"VCC": [["J1", "99"]], "VCC": [["J1", "1"]]}', encoding='utf-8')
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/pcb_toolkit.py'),
                                     'reconcile', str(board), '--netlist', str(nets)],
                                    capture_output=True, text=True, encoding='utf-8', env=env)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn('duplicate JSON key', result.stderr)

    def test_public_cli_pass_fail_and_json_physical_evidence(self):
        # D: on Windows through TEMP/TMP; caller can override elsewhere.
        with tempfile.TemporaryDirectory(prefix='pad-identity-') as folder:
            source = Path(folder) / 'board.json'
            report = Path(folder) / 'report.json'
            netlist = Path(folder) / 'netlist.json'
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
            def run(doc, *extra):
                source.write_text(json.dumps(doc), encoding='utf-8')
                return subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/pcb_toolkit.py'),
                                       'reconcile', str(source), *extra],
                                      capture_output=True, text=True, encoding='utf-8', env=env)
            good = run(fixture(), '--json', str(report))
            self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
            self.assertEqual(len(json.loads(report.read_text())['physical_have']), 2)
            wrong = fixture()
            wrong['pad_nets']['J1#land-a'] = 'GND'
            failed = run(wrong)
            self.assertEqual(failed.returncode, 2, failed.stdout + failed.stderr)
            self.assertIn('number/element net mismatch', failed.stderr)
            del wrong['pad_nets']['J1.1']
            mismatch = run(wrong, '--json', str(report))
            self.assertEqual(mismatch.returncode, 1, mismatch.stdout + mismatch.stderr)
            self.assertEqual(json.loads(report.read_text())['differ'], [['J1#land-a', 'VCC', 'GND']])
            netlist.write_text(json.dumps({'VCC': [['J1', '1']], 'GND': [['J1', '1']]}))
            invalid = run(fixture(), '--netlist', str(netlist))
            self.assertEqual(invalid.returncode, 2, invalid.stdout + invalid.stderr)
            self.assertIn('conflicting nets', invalid.stderr)


if __name__ == '__main__':
    unittest.main()
