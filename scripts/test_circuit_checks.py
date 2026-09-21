#!/usr/bin/env python3
"""Regression cases for declared connections and component/pin revision review."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import audit_design
import check_connectivity

WORKDIR = None


def snapshot():
    def part(ref, pins):
        return {'ref': ref, 'part': 'synthetic fixture', 'value': '',
                'footprint': 'test-only', 'fitted': True, 'in_bom': True, 'pins': pins}
    return {'schema': 1, 'kind': 'schematic', 'baseline_id': 'A',
            'source': 'synthetic native export fixture', 'coverage': 'complete',
            'components': [part('J1', {'1': 'VCC', '2': 'GND'}),
                           part('R1', {'1': 'VCC', '2': 'SENSE'}),
                           part('R2', {'1': 'SENSE', '2': 'GND'}),
                           part('U1', {'1': 'SENSE', '2': None})]}


def contract():
    def rule(name, kind, pins):
        return {'id': name, 'kind': kind, 'pins': pins, 'basis': 'Synthetic test topology'}
    return {'schema': 1, 'baseline_id': 'A', 'source': 'independent synthetic design requirement',
            'rules': [rule('supply', 'same_net', [['J1', '1'], ['R1', '1']]),
                      rule('rails', 'different_nets', [['J1', '1'], ['J1', '2']]),
                      rule('sense', 'exact_net', [['R1', '2'], ['R2', '1'], ['U1', '1']]),
                      rule('unused', 'no_connect', [['U1', '2']])]}


class CircuitChecks(unittest.TestCase):
    def test_known_topology_and_renamed_nets(self):
        data = snapshot()
        for part in data['components']:
            part['pins'] = {pin: ('renamed_' + net if net else None) for pin, net in part['pins'].items()}
        result = check_connectivity.check(data, contract())
        self.assertTrue(result['expectations_match'])
        self.assertEqual(result['ratings_timing_geometry_and_physical_continuity'], 'NOT_ASSESSED')

    def test_wrong_pin_connection_fails(self):
        data = snapshot(); data['components'][1]['pins']['1'] = 'GND'
        self.assertFalse(check_connectivity.check(data, contract())['expectations_match'])

    def test_short_between_rails_fails(self):
        data = snapshot(); data['components'][0]['pins']['2'] = 'VCC'
        results = check_connectivity.check(data, contract())['rules']
        self.assertEqual(results[1]['status'], 'FAIL')

    def test_extra_branch_including_dnp_detected(self):
        data = snapshot()
        extra = copy.deepcopy(data['components'][1]); extra.update(ref='R9', fitted=False)
        data['components'].append(extra)
        result = check_connectivity.check(data, contract())['rules'][2]
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn(['R9', '2'], result['unexpected_members'])

    def test_disconnected_endpoints_do_not_match(self):
        for kind in ('same_net', 'different_nets', 'exact_net'):
            data = snapshot(); data['components'][0]['pins'] = {'1': None, '2': None}
            expected = contract()
            expected['rules'] = [{'id': 'disconnect', 'kind': kind,
                                  'pins': [['J1', '1'], ['J1', '2']], 'basis': 'test'}]
            with self.subTest(kind=kind):
                self.assertFalse(check_connectivity.check(data, expected)['expectations_match'])

    def test_intended_nc_connected_fails(self):
        data = snapshot(); data['components'][3]['pins']['2'] = 'VCC'
        self.assertEqual(check_connectivity.check(data, contract())['rules'][3]['status'], 'FAIL')

    def test_missing_endpoint_is_invalid_not_pass(self):
        data = snapshot(); del data['components'][3]['pins']['2']
        with self.assertRaises(ValueError): check_connectivity.check(data, contract())

    def test_partial_stale_and_bom_inputs_rejected(self):
        for field, value in [('coverage', 'partial'), ('baseline_id', 'B'), ('kind', 'bom')]:
            data = snapshot(); data[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                check_connectivity.check(data, contract())

    def test_bad_contracts_rejected(self):
        cases = []
        for key, value in [('rules', []), ('source', ''), ('schema', True)]:
            bad = contract(); bad[key] = value; cases.append(bad)
        for key, value in [('kind', 'typo'), ('basis', ''), ('pins', [['J1', '1']]),
                           ('pins', [['J1', '1'], ['J1', '1']])]:
            bad = contract(); bad['rules'][0][key] = value; cases.append(bad)
        bad = contract(); bad['rules'].append(copy.deepcopy(bad['rules'][0])); cases.append(bad)
        for bad in cases:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                check_connectivity.check(snapshot(), bad)

    def test_revision_diff_and_baseline_guards(self):
        before = snapshot(); after = copy.deepcopy(before); after['baseline_id'] = 'B'
        after['components'][1]['pins']['1'] = 'GND'
        after['components'][1]['value'] = 'changed'
        result = audit_design.revision_diff(before, after)
        self.assertEqual({item['field'] for item in result['differences']}, {'pins', 'value'})
        self.assertEqual(result['geometry_routing_and_rule_changes'], 'NOT_ASSESSED')
        with self.assertRaises(ValueError): audit_design.compare(before, after)
        with self.assertRaises(ValueError): audit_design.revision_diff(before, before)
        after['kind'] = 'pcb'
        with self.assertRaises(ValueError): audit_design.revision_diff(before, after)

    def test_added_removed_parts_and_order_only_change(self):
        before = snapshot(); after = copy.deepcopy(before); after['baseline_id'] = 'B'
        after['components'].reverse()
        self.assertTrue(audit_design.revision_diff(before, after)['records_match'])
        after['components'][0]['ref'] = 'U9'
        changes = audit_design.revision_diff(before, after)['differences']
        self.assertEqual({(r['ref'], r['only_in']) for r in changes}, {('U1', 'left'), ('U9', 'right')})

    def test_bom_revision_includes_exclusion_changes(self):
        before = snapshot(); before['kind'] = 'bom'
        after = copy.deepcopy(before); after['baseline_id'] = 'B'
        after['components'][0]['in_bom'] = False
        changes = audit_design.revision_diff(before, after)['differences']
        self.assertEqual(changes, [{'ref': 'J1', 'field': 'in_bom', 'left': True, 'right': False}])

    def test_cli_exit_codes_and_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory(prefix='pcb-connectivity-', dir=WORKDIR) as td:
            folder = Path(td).resolve()
            self.assertTrue(folder.is_relative_to(Path(WORKDIR).resolve()))
            actual, expected = folder/'actual.json', folder/'expected.json'
            expected.write_text(json.dumps(contract()), encoding='utf-8')
            script = str(Path(check_connectivity.__file__).resolve())
            def run():
                return subprocess.run([sys.executable, '-X', 'utf8', script, str(actual), str(expected)],
                                      capture_output=True, text=True, encoding='utf-8')
            data = snapshot(); actual.write_text(json.dumps(data), encoding='utf-8')
            self.assertEqual(run().returncode, 0)
            data['components'][0]['pins']['2'] = 'VCC'
            actual.write_text(json.dumps(data), encoding='utf-8')
            failed = run(); self.assertEqual(failed.returncode, 1)
            self.assertFalse(json.loads(failed.stdout)['expectations_match'])
            expected.write_text('{"schema":1,"schema":1}', encoding='utf-8')
            invalid = run(); self.assertEqual(invalid.returncode, 2)
            self.assertIn('Duplicate JSON key', invalid.stderr)

    def test_diff_cli_and_malformed_snapshot(self):
        with tempfile.TemporaryDirectory(prefix='pcb-revision-', dir=WORKDIR) as td:
            folder = Path(td).resolve()
            self.assertTrue(folder.is_relative_to(Path(WORKDIR).resolve()))
            before, after = folder/'before.json', folder/'after.json'
            data = snapshot(); before.write_text(json.dumps(data), encoding='utf-8')
            data['baseline_id'] = 'B'; after.write_text(json.dumps(data), encoding='utf-8')
            def run():
                return subprocess.run([sys.executable, '-X', 'utf8', str(Path(audit_design.__file__).resolve()),
                                       'diff', str(before), str(after)], capture_output=True, text=True)
            self.assertEqual(run().returncode, 0)
            data['components'][0]['value'] = 'changed'
            after.write_text(json.dumps(data), encoding='utf-8')
            self.assertEqual(run().returncode, 1)
            for text in ('null', '[]', '{"schema":1,"schema":1}',
                         json.dumps({**data, 'components': [1]})):
                after.write_text(text, encoding='utf-8')
                with self.subTest(text=text): self.assertEqual(run().returncode, 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workdir', type=Path, required=True)
    args = parser.parse_args()
    WORKDIR = args.workdir.resolve(strict=True)
    if not WORKDIR.is_dir(): parser.error('--workdir must be a directory')
    unittest.main(argv=[sys.argv[0]], verbosity=2)
