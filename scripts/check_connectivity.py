#!/usr/bin/env python3
"""Check explicit pin-net expectations against a normalized native EDA snapshot."""
import argparse
import json
from pathlib import Path

from audit_design import load_snapshot, read_json
from report_provenance import read_source


def check(snapshot, contract):
    if not isinstance(snapshot, dict) or not isinstance(contract, dict):
        raise ValueError('Snapshot and contract must be JSON objects')
    if snapshot.get('kind') not in {'schematic', 'pcb'}:
        raise ValueError('Connectivity requires a schematic or PCB snapshot, not a BOM')
    if (not isinstance(snapshot.get('components'), list)
            or any(not isinstance(p, dict) for p in snapshot['components'])):
        raise ValueError('Components must be objects')
    parts = load_snapshot(snapshot)
    if type(contract.get('schema')) is not int or contract['schema'] != 1:
        raise ValueError('Expected contract schema=1')
    if contract.get('baseline_id') != snapshot['baseline_id']:
        raise ValueError('Contract and snapshot must share the reviewed baseline')
    if not isinstance(contract.get('source'), str) or not contract['source'].strip():
        raise ValueError('Contract needs an independent requirements/datasheet source')
    rules = contract.get('rules')
    if not isinstance(rules, list) or not rules:
        raise ValueError('An empty rule set cannot establish connectivity checks')
    nets = {}
    for ref, part in parts.items():
        for pin, net in part['pins'].items():
            if not isinstance(pin, str) or not pin.strip():
                raise ValueError(f'{ref}: pin numbers must be nonempty strings')
            if net is not None:
                if not net.strip():
                    raise ValueError(f'{ref}.{pin}: net name must be nonempty')
                nets.setdefault(net, set()).add((ref, pin))
    results, ids = [], set()
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError('Each rule must be an object')
        name = rule.get('id')
        if not isinstance(name, str) or not name.strip() or name in ids:
            raise ValueError('Rule IDs must be nonempty and unique')
        ids.add(name)
        if not isinstance(rule.get('basis'), str) or not rule['basis'].strip():
            raise ValueError(f'{name}: state the design basis for this expectation')
        kind = rule.get('kind')
        if kind not in {'same_net', 'different_nets', 'exact_net', 'no_connect'}:
            raise ValueError(f'{name}: unsupported rule kind')
        endpoints = rule.get('pins')
        if not isinstance(endpoints, list) or not endpoints:
            raise ValueError(f'{name}: pins must be a nonempty list of [reference, pin] pairs')
        pins = []
        for endpoint in endpoints:
            if (not isinstance(endpoint, list) or len(endpoint) != 2
                    or any(not isinstance(x, str) or not x.strip() for x in endpoint)):
                raise ValueError(f'{name}: invalid [reference, pin] pair')
            pair = tuple(endpoint)
            if pair in pins:
                raise ValueError(f'{name}: duplicate pin endpoint')
            ref, pin = pair
            if ref not in parts or pin not in parts[ref]['pins']:
                raise ValueError(f'{name}: missing endpoint {ref}.{pin}; export/contract needs review')
            pins.append(pair)
        if kind in {'same_net', 'different_nets'} and len(pins) < 2:
            raise ValueError(f'{name}: this rule needs at least two distinct pins')
        values = [parts[ref]['pins'][pin] for ref, pin in pins]
        connected = all(net is not None for net in values)
        common = connected and len(set(values)) == 1
        result = {'id': name, 'kind': kind, 'basis': rule['basis'],
                  'actual': [{'ref': ref, 'pin': pin, 'net': net}
                             for (ref, pin), net in zip(pins, values)]}
        if kind == 'same_net':
            passed = common
        elif kind == 'different_nets':
            passed = connected and len(set(values)) == len(values)
        elif kind == 'no_connect':
            passed = all(net is None for net in values)
        else:
            members = set().union(*(nets[net] for net in values if net is not None))
            passed = common and members == set(pins)
            result['observed_members'] = [list(pin) for pin in sorted(members)]
            result['unexpected_members'] = [list(pin) for pin in sorted(members - set(pins))]
        result['status'] = 'PASS' if passed else 'FAIL'
        if not passed:
            messages = {
                'same_net': ('EXPECTED_SHARED_NET', 'Locate the broken or wrong connection using these observed endpoints.'),
                'different_nets': ('EXPECTED_SEPARATE_NETS', 'Inspect the shared net or unconnected endpoint; preserve the independent power/pin intent.'),
                'no_connect': ('UNEXPECTED_CONNECTION', 'Inspect the unintended connection; confirm the exact-part NC requirement before repair.'),
                'exact_net': ('NET_MEMBERSHIP_MISMATCH', 'Inspect missing connections and unexpected members; do not edit the contract to match the faulty export.'),
            }
            code, hint = messages[kind]
            result['repair'] = {'code': code, 'subjects': [list(pin) for pin in pins],
                                'hint': hint, 'requires_fresh_readback': True,
                                'automatic_mutation_authorized': False}
        results.append(result)
    return {'scope': 'declared-pin-net-expectations-only', 'baseline_id': snapshot['baseline_id'],
            'sources': [contract['source'], snapshot['source']], 'rules': results,
            'expectations_match': all(r['status'] == 'PASS' for r in results),
            'ratings_timing_geometry_and_physical_continuity': 'NOT_ASSESSED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot', type=Path)
    parser.add_argument('contract', type=Path)
    args = parser.parse_args()
    try:
        snapshot, sp = read_source(args.snapshot, 'snapshot')
        contract, cp = read_source(args.contract, 'contract')
        result = check(snapshot, contract)
        result['source_inputs'] = [sp, cp]
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f'ERROR: {error}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return int(not result['expectations_match'])


if __name__ == '__main__':
    raise SystemExit(main())
