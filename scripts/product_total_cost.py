"""Combine declared component and build quotes into a scoped product cash estimate."""

import argparse
from decimal import Decimal, InvalidOperation
from pathlib import Path

import workflow_io as io
from report_provenance import read_source


COSTS = frozenset({
    'pcb_fabrication', 'components', 'assembly', 'stencil', 'shipping',
    'battery', 'enclosure', 'tools', 'software_api', 'other',
})
EXCLUSIVE = COSTS - {'shipping', 'tools', 'software_api', 'other'}
OPTIONAL = frozenset({'stencil', 'battery', 'enclosure', 'tools', 'software_api'})
DELIVERY = {
    'bare_pcb': {'pcb_fabrication', 'shipping'},
    'assembled_pcb': {'pcb_fabrication', 'components', 'assembly', 'shipping'},
    'usable_device': {'pcb_fabrication', 'components', 'assembly', 'shipping'},
}
CONTENTS = {
    'bare_pcb': 'the PCB fabrication quote buys bare boards only; separately listed purchases may be needed for the planned product',
    'assembled_pcb': 'the selected board/assembly quote buys fitted boards as stated by its source; other product work may remain',
    'usable_device': 'the selected quote claims a usable device; cost arithmetic does not verify firmware or functional tests',
}


def amount(value, label):
    if not isinstance(value, str):
        raise ValueError(label + ' must be a nonnegative decimal string or null')
    try:
        result = Decimal(value)
    except InvalidOperation:
        raise ValueError('Invalid ' + label) from None
    if (not result.is_finite() or result < 0 or result > Decimal('1000000000')
            or result.as_tuple().exponent < -8):
        raise ValueError('Invalid ' + label + ' range or precision')
    return result


def strings(value, label, allowed):
    if not isinstance(value, list) or any(not isinstance(x, str) or x not in allowed for x in value):
        raise ValueError(label + ' must be a list of known cost categories')
    if len(value) != len(set(value)):
        raise ValueError('Duplicate ' + label)
    return value


def calculate(plan, component_report=None):
    if not isinstance(plan, dict) or plan.get('schema') != 1:
        raise ValueError('Expected schema 1 plan')
    baseline = io.text(plan.get('baseline_id'), 'baseline_id')
    count = plan.get('board_quantity')
    if type(count) is not int or count < 1:
        raise ValueError('board_quantity must be a positive integer')
    currency = io.text(plan.get('currency'), 'currency')
    tax = plan.get('tax_basis')
    if tax not in ('included', 'excluded'):
        raise ValueError('Use one explicit tax_basis: included or excluded')
    delivery = plan.get('delivery')
    target = plan.get('target_delivery')
    if delivery not in DELIVERY or target not in DELIVERY:
        raise ValueError('delivery must be bare_pcb, assembled_pcb or usable_device')
    levels = {'bare_pcb': 0, 'assembled_pcb': 1, 'usable_device': 2}
    if levels[delivery] > levels[target]:
        raise ValueError('Quoted delivery cannot exceed the planned target delivery')
    components = plan.get('components')
    if components not in ('separate_purchase', 'included_in_bundle', 'not_in_delivery'):
        raise ValueError('components must state separate_purchase, included_in_bundle or not_in_delivery')
    if target == 'bare_pcb' and components != 'not_in_delivery':
        raise ValueError('A bare PCB target does not include components')
    if target != 'bare_pcb' and components == 'not_in_delivery':
        raise ValueError('An assembled target must account for components')
    required = set(strings(plan.get('required_costs'), 'required_costs', COSTS)) | DELIVERY[target]
    if target == 'bare_pcb' and required & {'components', 'assembly'}:
        raise ValueError('A bare PCB target cannot require component or assembly costs; choose the intended assembled target')
    not_required = plan.get('not_required_costs')
    if not isinstance(not_required, dict) or any(key not in OPTIONAL for key in not_required):
        raise ValueError('not_required_costs must map optional categories to reasons')
    for key, reason in not_required.items():
        io.text(reason, 'reason for not requiring ' + key)
    if required & set(not_required):
        raise ValueError('A cost cannot be required and not required')
    items = plan.get('line_items')
    if not isinstance(items, list):
        raise ValueError('line_items must be a list')

    rows, seen_ids, exclusive_seen, covered, issues = [], set(), set(), set(), []
    known_first = Decimal(0)
    known_repeat = Decimal(0)
    for item in items:
        if not isinstance(item, dict):
            raise ValueError('Each line item must be an object')
        ident = io.text(item.get('id'), 'line item id')
        if ident in seen_ids:
            raise ValueError('Duplicate line item id: ' + ident)
        seen_ids.add(ident)
        covers = strings(item.get('covers'), 'covers', COSTS)
        if not covers:
            raise ValueError('Each line item needs at least one covered cost category')
        if target == 'bare_pcb' and set(covers) & {'components', 'assembly'}:
            raise ValueError('A bare PCB target cannot charge for components or assembly; choose the intended assembled target')
        repeated = exclusive_seen & set(covers)
        if repeated:
            raise ValueError('Quote coverage counted twice: ' + ', '.join(sorted(repeated)))
        exclusive_seen.update(set(covers) & EXCLUSIVE)
        covered.update(covers)
        if delivery == 'bare_pcb' and 'pcb_fabrication' in covers and ({'components', 'assembly'} & set(covers)):
            raise ValueError('Bare PCB quote cannot bundle component or assembly charges with fabrication')
        if item.get('currency') != currency or item.get('tax_basis') != tax:
            raise ValueError('Normalize every line item to the plan currency and tax basis')
        timing = item.get('timing')
        if timing not in ('batch', 'one_time'):
            raise ValueError('timing must be batch or one_time')
        description = io.text(item.get('description'), 'line item description')
        source = io.text(item.get('source'), 'line item source')
        raw = item.get('amount')
        price = None if raw is None else amount(raw, 'line item amount')
        if price is None:
            issues.append({'id': ident, 'reason': 'MISSING_PRICE'})
        else:
            known_first += price
            if timing == 'batch':
                known_repeat += price
        rows.append({'id': ident, 'covers': covers, 'timing': timing,
                     'description': description, 'source': source,
                     'amount': str(price) if price is not None else None})

    if components == 'separate_purchase':
        if 'components' in covered:
            raise ValueError('Separate component purchase overlaps a bundled component charge')
        covered.add('components')
        if component_report is None:
            issues.append({'id': 'components', 'reason': 'MISSING_COMPONENT_REPORT'})
        else:
            if not isinstance(component_report, dict):
                raise ValueError('Component report must be an object')
            for key, expected in (('baseline_id', baseline), ('board_quantity', count),
                                  ('currency', currency), ('tax_basis', tax)):
                if component_report.get(key) != expected:
                    raise ValueError('Component report ' + key + ' does not match plan')
            component_known = amount(component_report.get('known_purchase_subtotal'), 'component known_purchase_subtotal')
            known_first += component_known
            known_repeat += component_known
            complete = component_report.get('status') == 'COMPLETE_QUOTE'
            if complete:
                total = amount(component_report.get('purchase_total'), 'component purchase_total')
                if total != component_known:
                    raise ValueError('Component report totals disagree')
            else:
                issues.append({'id': 'components', 'reason': 'COMPONENT_QUOTE_INCOMPLETE'})
            rows.append({'id': 'components', 'covers': ['components'], 'timing': 'batch',
                         'description': 'Separate component purchase from component_cost.py',
                         'source': 'component_cost report',
                         'amount': str(component_known) if complete else None,
                         'known_subtotal': str(component_known)})
    elif components == 'included_in_bundle' and 'components' not in covered:
        issues.append({'id': 'components', 'reason': 'BUNDLE_COMPONENT_COVERAGE_MISSING'})
    fabrication_lines = [set(row['covers']) for row in rows if 'pcb_fabrication' in row['covers']]
    if delivery in ('assembled_pcb', 'usable_device') and fabrication_lines and not any(
            'assembly' in covers for covers in fabrication_lines):
        raise ValueError('An assembled PCB quote must cover fabrication and assembly together')
    if covered & set(not_required):
        raise ValueError('A charged cost cannot also be marked not required')
    for cost in sorted(OPTIONAL - covered - required - set(not_required)):
        issues.append({'id': cost, 'reason': 'APPLICABILITY_UNKNOWN'})
    for cost in sorted(required - covered):
        issues.append({'id': cost, 'reason': 'REQUIRED_COST_MISSING'})

    full = not issues
    return {
        'scope': 'declared build-lot cash estimate; physical completion and quote accuracy require separate review',
        'baseline_id': baseline, 'board_quantity': count, 'currency': currency,
        'tax_basis': tax, 'quoted_delivery': delivery, 'planned_delivery': target,
        'payment_gets': CONTENTS[delivery],
        'components': components, 'required_costs': sorted(required),
        'not_required_costs': not_required, 'rows': rows,
        'known_first_cash_subtotal': str(known_first),
        'known_repeat_batch_subtotal': str(known_repeat),
        'first_cash_outlay_total': str(known_first) if full else None,
        'first_unit_at_quantity': str(known_first / count) if full else None,
        'repeat_batch_total_at_quantity': str(known_repeat) if full else None,
        'repeat_unit_at_quantity': str(known_repeat / count) if full else None,
        'status': 'COMPLETE_DECLARED_ESTIMATE' if full else 'INCOMPLETE', 'issues': issues,
        'price_verification': 'DECLARED_INPUT_ONLY',
        'coverage_note': 'Completeness covers declared categories only; review the actual device for omitted costs and what the seller supplies.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True, help='Product cost plan JSON')
    parser.add_argument('--component-report', type=Path, help='JSON output from component_cost.py')
    args = parser.parse_args()
    try:
        plan, plan_source = read_source(args.input, 'product-cost-plan')
        component_report, component_source = (None, None)
        if args.component_report:
            component_report, component_source = read_source(args.component_report, 'component-cost-report')
        result = calculate(plan, component_report)
        result['source_inputs'] = [plan_source] + ([component_source] if component_source else [])
        import sys
        sys.stdout.buffer.write(io.encoded(result) + b'\n')
        return 0 if result['status'] == 'COMPLETE_DECLARED_ESTIMATE' else 1
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.exit(2, 'ERROR: ' + str(exc) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
