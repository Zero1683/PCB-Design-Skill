#!/usr/bin/env python3
"""Show a bounded beginner-facing next step from existing project records.

Navigation only: this script never changes checks or certifies a PCB.
"""
import argparse
import csv
import json
from pathlib import Path

import check_evidence
import intake_review
import workflow_io as io


TOPIC_ZH = {
    'purpose': '用途和要实现的功能', 'carrier': '装在哪里、怎么拿或固定',
    'board_size': '板子尺寸或可用空间', 'power': '供电方式',
    'controls_connectors': '按钮、接口和指示灯的位置', 'assembly': '自己焊接还是委托贴装',
}
TOPIC_EN = {
    'purpose': 'intended functions', 'carrier': 'enclosure or mounting',
    'board_size': 'board size or available space', 'power': 'power source',
    'controls_connectors': 'controls and connector access', 'assembly': 'assembly method',
}
STAGES_ZH = ('需求与尺寸', '电路方案和元件', '原理图', 'PCB 摆放', '布线', '打板文件',
             '焊接与断电检查', '限流上电与烧录', '功能测试', '交付记录')
STAGES_EN = ('Requirements', 'Circuit and parts', 'Schematic', 'Placement', 'Routing',
             'Fabrication files', 'Assembly', 'Power-up', 'Functional tests', 'Handoff')
NEXT_ZH = (
    '把用途、空间、供电和装配方式整理清楚，并留存确定依据。',
    '核对电路方案、具体器件和元件预算。',
    '完成原理图，并核对每个关键引脚和封装。',
    '摆好元件，检查接口能否接入、器件是否互相干涉。',
    '完成布线，检查电源路径、信号和全部连接。',
    '核对打板、焊接所需文件与当前设计版本一致。',
    '按装配说明焊接，并在上电前检查短路和极性。',
    '限流上电，测量电压并验证复位与烧录。',
    '逐项测试要求的功能和使用边界。',
    '整理可交付文件、已验证范围和后续步骤。',
)


def snapshot(root, baseline, through='G5', lang='zh'):
    root = io.no_link(root).resolve(strict=True)
    if lang not in ('zh', 'en'):
        raise ValueError('Language must be zh or en')
    if through not in {f'G{i}' for i in range(10)}:
        raise ValueError('Stage must be G0-G9')
    if not isinstance(baseline, str) or not baseline.strip() or baseline == 'UNSET':
        return {'scope': 'navigation-only', 'state': 'SET_BASELINE',
                'next_owner': 'agent', 'next_step': ('先确定当前设计版本，再继续整理需求。' if lang == 'zh'
                                                   else 'Set the current design revision, then continue the brief.'),
                'fabrication_evidence_complete': False,
                'engineering_correctness': 'NOT_ASSESSED', 'physical_board_test': 'NOT_ASSESSED'}

    # The strict auditor detects malformed records and stale or absent evidence.
    audit = check_evidence.audit(root, baseline, through=through)
    with io.no_link(root / 'CHECKS.csv').open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    selected = [r for r in rows if r['stage'] in {f'G{i}' for i in range(int(through[1:])+1)}]
    unfinished = [r for r in selected if r['status'] not in {'PASS', 'N_A'} or
                  (r['status'] == 'N_A' and r['applicability'] == 'required')]
    names = STAGES_ZH if lang == 'zh' else STAGES_EN
    current = unfinished[0]['stage'] if unfinished else through
    stage_name = names[int(current[1:])]
    intake_issue = None
    intake_record_issue = False
    plan_rejected = False
    plan_not_prepared = False
    try:
        intake_data = io.read(io.no_link(root / 'intake.json'))
        review = intake_review.evaluate(root, intake_data, baseline)
        if review['pending_topics']:
            labels = TOPIC_ZH if lang == 'zh' else TOPIC_EN
            ordered = [name for name in intake_review.TOPICS if name in review['pending_topics']]
            short = ordered[:3]
            more = len(ordered) > len(short)
            intake_issue = (('还需要确认：' + '、'.join(labels[t] for t in short) + ('等。' if more else '。'))
                            if lang == 'zh' else ('Please clarify: ' + ', '.join(labels[t] for t in short)
                                                  + (' and more.' if more else '.')))
        elif review['state'] == 'NEEDS_PLAN_DECISION':
            if isinstance(intake_data.get('proposal'), dict) and intake_data['proposal'].get('document'):
                intake_issue = ('请看尺寸和元件预算方案，告诉我是否照此制作或要改哪里。' if lang == 'zh'
                                else 'Review the dimensioned plan and parts estimate; accept it or request changes.')
            else:
                plan_not_prepared = True
        elif review['state'] == 'PLAN_REJECTED':
            plan_rejected = True  # An agent prepares a revised plan before asking again.
    except (OSError, ValueError, KeyError, TypeError):
        # A missing/malformed record is an agent repair task, not implied user consent.
        intake_record_issue = True

    # Fully populated rows can still point to stale upstream inputs or have
    # incomplete source/requirement bindings. Surface those gate errors too.
    fabrication_verified = False
    gate_errors = []
    if int(through[1:]) >= 5 and not unfinished and not audit['record_errors'] and not intake_record_issue:
        gate = check_evidence.audit(root, baseline, through='G5', design_gates=True)
        fabrication_verified = gate['records_complete']
        gate_errors = gate['record_errors']

    if intake_issue:
        owner, step = 'user', intake_issue
    elif plan_rejected:
        owner = 'agent'
        step = ('根据用户的修改意见重做方案，再请用户查看。' if lang == 'zh'
                else 'Revise the plan from the user\'s feedback before presenting it again.')
    elif plan_not_prepared:
        owner = 'agent'
        step = ('先整理尺寸、电源、元件和预算方案，再给用户查看。' if lang == 'zh'
                else 'Prepare the dimensioned, powered parts-and-cost plan for review.')
    elif audit['record_errors'] or intake_record_issue or gate_errors:
        owner = 'agent'
        step = ('先核对工程记录与证据，再继续设计。' if lang == 'zh'
                else 'Reconcile project records and evidence before continuing.')
    elif unfinished:
        owner = 'agent'
        item = unfinished[0]
        step = (NEXT_ZH[int(item['stage'][1:])] if lang == 'zh'
                else f'Complete the {stage_name.lower()} check and record its evidence next.')
    else:
        owner = 'agent'
        step = ('当前阶段的记录已填齐，请复查设计证据和实物测试范围。' if lang == 'zh'
                else 'Recorded checks are filled; review design evidence and physical-test scope.')

    return {'scope': 'navigation-only', 'state': 'IN_PROGRESS' if unfinished or audit['record_errors'] or gate_errors
            or intake_issue or plan_rejected or plan_not_prepared or intake_record_issue else 'RECORDS_FILLED', 'baseline_id': baseline,
            'stage': current, 'stage_name': stage_name, 'next_owner': owner,
            'next_step': step, 'selected_checks': len(selected),
            'unfinished_checks': len(unfinished), 'record_issues': len(audit['record_errors']) + len(gate_errors) + int(intake_record_issue),
            'first_record_issues': (audit['record_errors'] + gate_errors)[:3],
            'fabrication_evidence_complete': fabrication_verified,
            'engineering_correctness': 'NOT_ASSESSED', 'physical_board_test': 'NOT_ASSESSED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--baseline', required=True)
    parser.add_argument('--through', choices=[f'G{i}' for i in range(10)], default='G5')
    parser.add_argument('--lang', choices=('zh', 'en'), default='zh')
    args = parser.parse_args()
    try:
        result = snapshot(args.root, args.baseline, args.through, args.lang)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, 'ERROR: ' + str(exc) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
