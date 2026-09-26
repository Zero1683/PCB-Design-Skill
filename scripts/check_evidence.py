#!/usr/bin/env python3
"""Audit PCB check records and local evidence. Does not certify engineering correctness."""
import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
import workflow_io as io
import evidence_binding as binding

STATES = {'NOT_RUN', 'PASS', 'FAIL', 'BLOCKED', 'N_A', 'ACCEPTED_LIMITATION', 'STALE'}
FIELDS = {'id', 'stage', 'check', 'applicability', 'status', 'baseline_id', 'board_id',
          'firmware_id', 'method', 'conditions', 'acceptance', 'actual', 'evidence_path',
          'checked_at', 'limitation', 'next_action'}


def audit(root, baseline, through='G5', board=None, firmware=None, design_gates=False):
    root = io.no_link(root).resolve(strict=True)
    if not baseline.strip() or through not in {f'G{i}' for i in range(10)}:
        raise ValueError('Provide a nonempty baseline and a stage G0-G9')
    with io.no_link(root / 'CHECKS.csv').open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)) or set(reader.fieldnames) != FIELDS:
            raise ValueError('CHECKS.csv must have the documented unique columns')
        rows = [{k: v.strip() if isinstance(v,str) else v for k,v in row.items()} for row in reader]
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
        if state == 'N_A' and row['applicability'] == 'required':
            errors.append(f'{label}: required check cannot be N_A')
        if state == 'ACCEPTED_LIMITATION' and not row['evidence_path']:
            errors.append(f'{label}: accepted limitation needs a local decision record')
        if state not in {'PASS', 'N_A'}:
            pending.append({'id': label, 'status': state, 'next_action': row['next_action']})
        evidence_names = [p.strip() for p in row['evidence_path'].split(';') if p.strip()]
        if state in {'PASS', 'ACCEPTED_LIMITATION'} and not evidence_names:
            errors.append(f'{label}: evidence list must contain a local file')
        for name in evidence_names:
            path = io.no_link(root / name).resolve()
            if Path(name).is_absolute() or not path.is_relative_to(root) or not path.is_file() or path.stat().st_size == 0:
                errors.append(f'{label}: evidence must be a nonempty project-local file: {name}')
    if design_gates:
        registry=io.read(Path(__file__).resolve().parents[1]/'assets/design-check-registry.json')
        by_id={r.get('id','').strip():r for r in rows if isinstance(r.get('id'),str)}
        for gate in registry['checks']:
            ident,stage=gate['id'],gate['stage']
            if int(stage[1:])>int(through[1:]):continue
            row=by_id.get(ident)
            if row is None:
                errors.append(f'{ident}: required registry item missing');continue
            if row.get('stage')!=stage or row.get('applicability')!=gate['applicability']:
                errors.append(f'{ident}: registry stage/applicability changed')
            allowed={'PASS'} if gate['applicability']=='required' else {'PASS','N_A'}
            if row.get('status') not in allowed:errors.append(f'{ident}: unresolved registry check')
            if row.get('status')=='N_A' and (not row.get('limitation','').strip() or not row.get('evidence_path','').strip()):
                errors.append(f'{ident}: N_A requires a scoped decision and evidence')
            if ident=='SCH-FORMAT' and row.get('actual') not in {'free-layout','framed-layout'}:
                errors.append('SCH-FORMAT: only free-layout or framed-layout is allowed')
    coverage = None
    mechanical = None
    project_reviews = None
    provenance = None
    intake = None
    if design_gates and int(through[1:]) >= 2:
        try:
            import intake_review
            intake = intake_review.evaluate(root, io.read(binding.local(root, 'intake.json')), baseline)
            if not intake['detailed_design_allowed']:
                errors.append('Beginner plan decision incomplete: ' + intake['state'])
        except (ValueError, KeyError, TypeError, OSError) as exc:
            errors.append('Intake review (legacy projects need explicit migration): ' + str(exc))
    if design_gates and int(through[1:]) >= 2:
        try:provenance=binding.evaluate(root,baseline,rows,through)
        except (ValueError,KeyError,TypeError,OSError) as exc:errors.append("Design binding: "+str(exc))
        if intake and provenance and intake['project_id'] != provenance['project_id']:
            errors.append('Intake belongs to another project')
    if design_gates and int(through[1:]) >= 3:
        try:
            import mechanical_envelope
            mechanical=mechanical_envelope.evaluate(root,baseline,require_outline=int(through[1:])>=5)
            if mechanical['state']!='DIMENSIONS_MATCH':errors.append('Accepted dimensions differ from observed geometry')
        except (ValueError,KeyError,TypeError,OSError) as exc:errors.append('Mechanical envelope: '+str(exc))
    if design_gates and int(through[1:]) >= 5 and (root/'project-reviews.json').exists():
        try:
            import project_reviews as pr
            project_reviews=pr.check(root,'project-reviews.json',baseline)
            if project_reviews['state']!='CHECK_OK':errors.append('Applicable project reviews have unresolved findings')
        except (ValueError,KeyError,TypeError,OSError) as exc:errors.append('Project reviews: '+str(exc))
    if design_gates and int(through[1:]) >= 5:
        try:
            import requirement_coverage as rc
            coverage=rc.evaluate(root,io.read(binding.local(root,'requirements.json')),io.read(binding.local(root,'requirement-checks.json')),baseline)
            reqs=io.read(binding.local(root,'requirements.json'));mapped=io.read(binding.local(root,'requirement-checks.json'))
            if provenance and reqs['project_id']!=provenance['project_id']:raise ValueError('Coverage belongs to another project')
            selected_rows={r.get('id'):r for r in rows if r.get('stage') in {f'G{i}' for i in range(int(through[1:])+1)}}
            for record in mapped['checks']:
                if record.get('status')=='PASS':
                    row=selected_rows.get(record['id'])
                    if row is None or row.get('status')!='PASS' or record['evidence']['path'] not in {p.strip() for p in row['evidence_path'].split(';')}:raise ValueError('Coverage check lacks corresponding current PASS row: '+record['id'])
            if coverage['state']!='COVERED_WITH_CURRENT_EVIDENCE':errors.append('Requirement coverage incomplete')
        except (ValueError,KeyError,TypeError,OSError) as exc:
            errors.append('Requirement coverage: '+str(exc))
    if selected == 0: errors.append('No check rows in selected stage range')
    return {'scope': 'record-completeness-only', 'through': through, 'selected_checks': selected,
            'record_errors': errors, 'pending': pending,
            'intake_review': intake, 'mechanical_envelope':mechanical, 'project_reviews':project_reviews, 'requirement_coverage': coverage,'design_binding':provenance,
            'records_complete': not errors and not pending,
            'engineering_correctness': 'NOT_ASSESSED'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--baseline', required=True)
    p.add_argument('--through', default='G5', choices=[f'G{i}' for i in range(10)])
    p.add_argument('--board'); p.add_argument('--firmware')
    p.add_argument('--design-gates', action='store_true', help='Require registered stage checks, current design bindings and G5 requirement coverage')
    args = p.parse_args()
    try: result = audit(args.root, args.baseline, args.through, args.board, args.firmware, args.design_gates)
    except (OSError, ValueError) as exc: p.exit(2, f'ERROR: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['records_complete'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
