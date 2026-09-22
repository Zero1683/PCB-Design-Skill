import unittest, copy
from decimal import Decimal
from component_cost import calculate

def fixture():
    return {'schema':1,'baseline_id':'A','board_quantity':1,'currency':'CNY','tax_basis':'included',
        'parts':[{'id':'R1,R2','function':'pull-up','mpn':'TEST-R','supplier_code':'SYNTHETIC-R','package':'0603','spec':'10k 1%','qty_per_board':2,'spares':0,
          'quote':{'url':'https://example.com/synthetic-only','queried_at':'2026-09-22T12:00:00+08:00','stock':1000,'moq':100,'multiple':100,'currency':'CNY','tax_basis':'included','price_unit':'piece',
                   'tiers':[{'min_qty':1,'unit_price':'0.02'},{'min_qty':100,'unit_price':'0.01'}]}}]}
class CostTests(unittest.TestCase):
    def test_moq_is_not_board_consumption(self):
        r=calculate(fixture());self.assertEqual(Decimal(r['board_material_total']),Decimal('0.02'));self.assertEqual(Decimal(r['purchase_total']),Decimal('1'));self.assertEqual(r['rows'][0]['surplus_quantity'],98)
    def test_multiple_rounding_and_actual_tier(self):
        d=fixture();d['board_quantity']=51;r=calculate(d)['rows'][0];self.assertEqual(r['purchase_quantity'],200);self.assertEqual(r['selected_tier_min'],100)
    def test_spares_are_purchased_not_consumed_per_board(self):
        d=fixture();d['parts'][0]['spares']=100;r=calculate(d);self.assertEqual(r['rows'][0]['purchase_quantity'],200);self.assertEqual(Decimal(r['board_material_total']),Decimal('0.02'))
    def test_lower_moq_can_reduce_cash_despite_higher_unit_price(self):
        a=calculate(fixture());d=fixture();q=d['parts'][0]['quote'];q['moq']=1;q['multiple']=1;b=calculate(d);self.assertLess(Decimal(b['purchase_total']),Decimal(a['purchase_total']));self.assertGreater(Decimal(b['board_material_total']),Decimal(a['board_material_total']))
    def test_missing_quote_is_not_zero_total(self):
        d=fixture();d['parts'][0]['quote']=None;r=calculate(d);self.assertIsNone(r['purchase_total']);self.assertEqual(r['status'],'INCOMPLETE')
    def test_stock_compared_with_purchase_not_consumption(self):
        for stock,status in ((2,'INSUFFICIENT_STOCK'),(0,'INSUFFICIENT_STOCK'),(None,'STOCK_UNKNOWN')):
            d=fixture();d['parts'][0]['quote']['stock']=stock;r=calculate(d);self.assertEqual(r['rows'][0]['status'],status);self.assertEqual(r['status'],'INCOMPLETE')
    def test_mixed_currency_tax_or_pack_prices_rejected(self):
        for k,v in (('currency','USD'),('tax_basis','excluded'),('price_unit','pack')):
            d=fixture();d['parts'][0]['quote'][k]=v
            with self.assertRaises(ValueError):calculate(d)
    def test_duplicate_supplier_code_requires_aggregation(self):
        d=fixture();d['parts']*=2
        with self.assertRaises(ValueError):calculate(d)
    def test_wrong_tier_not_advertised_minimum(self):
        d=fixture();q=d['parts'][0]['quote'];q['moq']=1;q['multiple']=1;q['tiers']=[{'min_qty':100,'unit_price':'0.01'}]
        with self.assertRaises(ValueError):calculate(d)
    def test_bad_values_and_missing_source_rejected(self):
        for field,value in (('moq',0),('multiple',True),('stock',-1),('queried_at','2026-09-22'),('url','')):
            d=fixture();d['parts'][0]['quote'][field]=value
            with self.assertRaises(ValueError):calculate(d)
        for price in ('NaN','-0.1','Infinity',0.1):
            d=fixture();d['parts'][0]['quote']['tiers'][0]['unit_price']=price
            with self.assertRaises(ValueError):calculate(d)
    def test_does_not_mutate_input_or_claim_live_verification(self):
        d=fixture();old=copy.deepcopy(d);r=calculate(d);self.assertEqual(d,old);self.assertEqual(r['price_verification'],'DECLARED_INPUT_ONLY')
if __name__=='__main__':unittest.main()
