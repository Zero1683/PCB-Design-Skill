import copy
from decimal import Decimal
import unittest

from component_cost import calculate as component_calculate
from product_total_cost import calculate
from test_component_cost import fixture as component_fixture


def item(ident, covers, price, timing='batch'):
    return {'id': ident, 'covers': covers, 'amount': price, 'timing': timing,
            'description': ident + ' for the declared build lot', 'source': 'synthetic test quote',
            'currency': 'CNY', 'tax_basis': 'included'}


def plan():
    return {'schema': 1, 'baseline_id': 'A', 'board_quantity': 1,
            'currency': 'CNY', 'tax_basis': 'included',
            'delivery': 'bare_pcb', 'target_delivery': 'usable_device',
            'components': 'separate_purchase',
            'required_costs': ['battery', 'enclosure', 'tools', 'software_api'],
            'not_required_costs': {'stencil': 'hand soldering'},
            'line_items': [item('pcb', ['pcb_fabrication'], '12'),
                           item('assembly', ['assembly'], '20'),
                           item('freight', ['shipping'], '8'),
                           item('cell', ['battery'], '5'),
                           item('case', ['enclosure'], '7'),
                           item('soldering-iron', ['tools'], '30', 'one_time'),
                           item('api', ['software_api'], '2')]}


class ProductTotalCostTests(unittest.TestCase):
    def test_separate_components_first_cash_and_repurchase(self):
        p = plan()
        before = copy.deepcopy(p)
        result = calculate(p, component_calculate(component_fixture()))
        self.assertEqual(p, before)
        self.assertEqual(result['status'], 'COMPLETE_DECLARED_ESTIMATE')
        self.assertEqual(Decimal(result['first_cash_outlay_total']), Decimal('85'))
        self.assertEqual(Decimal(result['repeat_batch_total_at_quantity']), Decimal('55'))
        self.assertEqual(Decimal(result['first_unit_at_quantity']), Decimal('85'))
        self.assertIn('bare boards only', result['payment_gets'])
        self.assertEqual(result['planned_delivery'], 'usable_device')

    def test_turnkey_pcba_is_not_charged_for_components_twice(self):
        p = plan()
        p['delivery'] = 'assembled_pcb'
        p['components'] = 'included_in_bundle'
        p['line_items'] = [item('pcba', ['pcb_fabrication', 'assembly', 'components'], '50'),
                           item('freight', ['shipping'], '8')]
        p['required_costs'] = []
        p['not_required_costs'] = {name: 'not used in this synthetic open-board example'
                                   for name in ('stencil', 'battery', 'enclosure', 'tools', 'software_api')}
        result = calculate(p, component_calculate(component_fixture()))
        self.assertEqual(result['status'], 'COMPLETE_DECLARED_ESTIMATE')
        self.assertEqual(result['first_cash_outlay_total'], '58')
        self.assertFalse(any(row['id'] == 'components' for row in result['rows']))
        p['line_items'].append(item('bare-boards', ['pcb_fabrication'], '12'))
        with self.assertRaisesRegex(ValueError, 'counted twice'):
            calculate(p)

    def test_missing_or_unpriced_needed_cost_keeps_full_total_unknown(self):
        p = plan()
        p['line_items'] = [row for row in p['line_items'] if row['id'] != 'case']
        p['line_items'][0]['amount'] = None
        result = calculate(p, component_calculate(component_fixture()))
        self.assertEqual(result['status'], 'INCOMPLETE')
        self.assertIsNone(result['first_cash_outlay_total'])
        self.assertEqual(result['known_first_cash_subtotal'], '66.00')
        self.assertEqual({issue['reason'] for issue in result['issues']},
                         {'MISSING_PRICE', 'REQUIRED_COST_MISSING'})

    def test_incomplete_component_report_keeps_full_total_unknown(self):
        quoted = component_fixture()
        quoted['parts'][0]['quote'] = None
        result = calculate(plan(), component_calculate(quoted))
        self.assertIsNone(result['first_cash_outlay_total'])
        self.assertIn({'id': 'components', 'reason': 'COMPONENT_QUOTE_INCOMPLETE'}, result['issues'])

    def test_bare_pcb_payment_scope(self):
        p = plan()
        p.update(delivery='bare_pcb', target_delivery='bare_pcb',
                 components='not_in_delivery', required_costs=[],
                 not_required_costs={name: 'bare board only'
                                     for name in ('stencil', 'battery', 'enclosure', 'tools', 'software_api')},
                 line_items=[item('pcb', ['pcb_fabrication'], '12'),
                             item('freight', ['shipping'], '8')])
        result = calculate(p)
        self.assertEqual(result['first_cash_outlay_total'], '20')
        self.assertIn('bare boards only', result['payment_gets'])
        p['line_items'][0]['covers'] = ['pcb_fabrication', 'assembly']
        with self.assertRaisesRegex(ValueError, 'Bare PCB'):
            calculate(p)

    def test_bare_board_quote_plus_separate_parts_and_soldering(self):
        p = plan()
        p['required_costs'] = []
        p['not_required_costs'] = {name: 'not used in this synthetic open-board example'
                                   for name in ('stencil', 'battery', 'enclosure', 'tools', 'software_api')}
        p['line_items'] = [item('bare-boards', ['pcb_fabrication'], '12'),
                           item('manual-soldering', ['assembly'], '0'),
                           item('shipping', ['shipping'], '8')]
        result = calculate(p, component_calculate(component_fixture()))
        self.assertEqual(result['status'], 'COMPLETE_DECLARED_ESTIMATE')
        self.assertEqual(result['first_cash_outlay_total'], '21.00')
        self.assertEqual(result['quoted_delivery'], 'bare_pcb')
        self.assertEqual(result['planned_delivery'], 'usable_device')

    def test_separate_assembly_charge_does_not_turn_bare_quote_into_pcba(self):
        p = plan()
        p['delivery'] = 'assembled_pcb'
        with self.assertRaisesRegex(ValueError, 'fabrication and assembly together'):
            calculate(p, component_calculate(component_fixture()))

    def test_component_identity_and_price_basis_must_match(self):
        report = component_calculate(component_fixture())
        for key, bad in (('baseline_id', 'B'), ('board_quantity', 2),
                         ('currency', 'USD'), ('tax_basis', 'excluded')):
            altered = dict(report)
            altered[key] = bad
            with self.assertRaisesRegex(ValueError, key):
                calculate(plan(), altered)
        p = plan()
        p['line_items'][0]['currency'] = 'USD'
        with self.assertRaisesRegex(ValueError, 'Normalize'):
            calculate(p, report)

    def test_invalid_price_is_not_silently_accepted(self):
        for price in ('-1', 'NaN', 'Infinity', 1.0):
            p = plan()
            p['line_items'][0]['amount'] = price
            with self.assertRaises(ValueError):
                calculate(p, component_calculate(component_fixture()))

    def test_unconsidered_optional_cost_keeps_total_unknown(self):
        p = plan()
        del p['not_required_costs']['stencil']
        result = calculate(p, component_calculate(component_fixture()))
        self.assertIsNone(result['first_cash_outlay_total'])
        self.assertIn({'id': 'stencil', 'reason': 'APPLICABILITY_UNKNOWN'}, result['issues'])


if __name__ == '__main__':
    unittest.main()
