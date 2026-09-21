#!/usr/bin/env python3
"""Audit PCB check records and local evidence. Does not certify engineering correctness."""
import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

STATES = {'NOT_RUN', 'PASS', 'FAIL', 'BLOCKED', 'N_A', 'ACCEPTED_LIMITATION', 'STALE'}
FIELDS = {'id', 'stage', 'check', 'applicability', 'status', 'baseline_id', 'board_id',
          'firmware_id', 'method', 'conditions', 'acceptance', 'actual', 'evidence_path',
          'checked_at', 'limitation', 'next_action'}


def audit(root, baseline, through='G5', board=None, firmware=None):
    root = Path(root).resolve(strict=True)
    if not baseline.strip() or through not in {f'G{i}' for i in range(10)}:
        raise ValueError('Provide a nonempty baseline and a stage G0-G9')
    with (root / 'CHECKS.csv').open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)) or set(reader.fieldnames) != FIELDS:
            raise ValueError('CHECKS.csv must have the documented unique columns')
        rows = list(reader)
    errors, pending, seen, selected = [], [], set(), 0
    for index, row in enumerate(rows, 2):
        if None in row or any(v is None for v in row.values()):
            errors.append(f'row {index}: malformed CSV row'); continue
        row = {k: v.strip() for k, v in row.items()}
        label = row['id'] or f'row {index}'
        if not row['id'] or row['id'] in seen:
            errors.append(f'{label}: missing or duplicate ID')
        seen.add(row['id'])
        if row['stage'] not in {f'G{i}' for i in range(10)} or row['status'] not in STATES or row['applicability'] not in {'required', 'assess'}:
            errors.append(f'{label}: invalid stage, status, or applicability'); continue
        if int(row['stage'][1:]) > int(through[1:]):
            continue
        selected += 1
        state = row['status']
        if state == 'PASS':
            for key in ('check', 'baseline_id', 'method', 'conditions', 'acceptance', 'actual', 'evidence_path', 'checked_at'):
                if not row[key]: errors.append(f'{label}: PASS missing {key}')
            if row['baseline_id'] != baseline:
                errors.append(f'{label}: evidence baseline differs from current baseline; reassess or mark STALE')
            if int(row['stage'][1:]) >= 6 and not row['board_id']:
                errors.append(f'{label}: physical test needs board_id')
            for key, expected in (('board_id', board), ('firmware_id', firmware)):
                if expected and row[key] != expected and int(row['stage'][1:]) >= 6:
                    errors.append(f'{label}: {key} mismatch')
            try:
                stamp = datetime.fromisoformat(row['checked_at'].replace('Z', '+00:00'))
                if stamp.tzinfo is None: raise ValueError()
            except ValueError:
                errors.append(f'{label}: checked_at must be an ISO timestamp with timezone')
        if state in {'N_A', 'ACCEPTED_LIMITATION'} and not row['limitation']:
            errors.append(f'{label}: {state} needs justification/source in limitation')
        if state == 'ACCEPTED_LIMITATION' and not row['evidence_path']:
            errors.append(f'{label}: accepted limitation needs a local decision record')
        if state not in {'PASS', 'N_A'}:
            pending.append({'id': label, 'status': state, 'next_action': row['next_action']})
        for name in filter(None, (p.strip() for p in row['evidence_path'].split(';'))):
            path = (root / name).resolve()
            if Path(name).is_absolute() or not path.is_relative_to(root) or not path.is_file() or path.stat().st_size == 0:
                errors.append(f'{label}: evidence must be a nonempty project-local file: {name}')
    if selected == 0: errors.append('No check rows in selected stage range')
    return {'scope': 'record-completeness-only', 'through': through, 'selected_checks': selected,
            'record_errors': errors, 'pending': pending,
            'records_complete': not errors and not pending,
            'engineering_correctness': 'NOT_ASSESSED'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--baseline', required=True)
    p.add_argument('--through', default='G5', choices=[f'G{i}' for i in range(10)])
    p.add_argument('--board'); p.add_argument('--firmware')
    args = p.parse_args()
    try: result = audit(args.root, args.baseline, args.through, args.board, args.firmware)
    except (OSError, ValueError) as exc: p.exit(2, f'ERROR: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['records_complete'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
