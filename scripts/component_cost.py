"""Compute component-only estimates from observed distributor quotes. No network or purchasing."""
import argparse
from datetime import datetime
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
from urllib.parse import urlsplit
import workflow_io as io
from report_provenance import read_source


def integer(value, name, minimum=1):
    if type(value) is not int or value < minimum:
        raise ValueError(name + ' must be an integer >= ' + str(minimum))
    return value


def money(value):
    if not isinstance(value, str):
        raise ValueError('unit_price must be a decimal string in currency per piece')
    try:
        result = Decimal(value)
    except InvalidOperation:
        raise ValueError('Invalid unit_price') from None
    if not result.is_finite() or result < 0 or result > Decimal('1000000000') or result.as_tuple().exponent < -8:
        raise ValueError('Invalid unit_price range or precision')
    return result


def calculate(data):
    if not isinstance(data, dict) or data.get('schema') != 1:
        raise ValueError('Expected schema 1 object')
    count = integer(data.get('board_quantity'), 'board_quantity')
    baseline = io.text(data.get('baseline_id'), 'baseline_id')
    currency = io.text(data.get('currency'), 'currency')
    tax = data.get('tax_basis')
    if tax not in ('included', 'excluded'):
        raise ValueError('Use one explicit tax_basis: included or excluded')
    parts = data.get('parts')
    if not isinstance(parts, list) or not parts:
        raise ValueError('Nonempty parts required')
    rows, seen = [], set()
    material = Decimal(0)
    purchase = Decimal(0)
    issues = []
    for part in parts:
        if not isinstance(part, dict): raise ValueError('Part must be an object')
        for key in ('id', 'function', 'mpn', 'supplier_code', 'package', 'spec'):
            io.text(part.get(key), key)
        if part['supplier_code'] in seen: raise ValueError('Aggregate repeated supplier_code before calculation')
        seen.add(part['supplier_code'])
        each = integer(part.get('qty_per_board'), 'qty_per_board')
        spare = integer(part.get('spares', 0), 'spares', 0)
        required = count * each + spare
        row = {key:part[key] for key in ('id','function','mpn','supplier_code','package','spec')}
        row.update(qty_per_board=each, spares=spare, required_quantity=required)
        quote = part.get('quote')
        if quote is None:
            row.update(status='UNPRICED', purchase_quantity=None, unit_price=None, board_material_cost=None, purchase_cost=None)
            issues.append({'id':part['id'], 'reason':'MISSING_QUOTE'})
            rows.append(row)
            continue
        if not isinstance(quote, dict): raise ValueError('Quote must be an object or null')
        allowed = {'url','queried_at','stock','moq','multiple','currency','tax_basis','price_unit','tiers'}
        if set(quote) != allowed: raise ValueError('Quote fields must match the documented schema')
        link = urlsplit(io.text(quote['url'], 'quote URL'))
        if link.scheme != 'https' or not link.netloc: raise ValueError('Quote needs an HTTPS source URL')
        stamp = datetime.fromisoformat(io.text(quote['queried_at'], 'queried_at').replace('Z','+00:00'))
        if stamp.tzinfo is None: raise ValueError('queried_at needs timezone')
        if quote['currency'] != currency or quote['tax_basis'] != tax or quote['price_unit'] != 'piece':
            raise ValueError('Normalize currency, tax basis and per-piece prices before summing')
        moq = integer(quote['moq'], 'moq')
        multiple = integer(quote['multiple'], 'multiple')
        qty = ((max(required, moq) + multiple - 1) // multiple) * multiple
        tiers = quote['tiers']
        if not isinstance(tiers, list) or not tiers: raise ValueError('Price tiers required')
        breaks = {}
        for tier in tiers:
            if not isinstance(tier, dict) or set(tier) != {'min_qty','unit_price'}: raise ValueError('Invalid tier')
            minimum = integer(tier['min_qty'], 'tier min_qty')
            if minimum in breaks: raise ValueError('Duplicate price break')
            breaks[minimum] = money(tier['unit_price'])
        eligible = [n for n in breaks if n <= qty]
        if not eligible: raise ValueError('No quoted tier covers actual purchase quantity')
        selected = max(eligible)
        price = breaks[selected]
        stock = quote['stock']
        if stock is not None: integer(stock, 'stock', 0)
        status = 'QUOTED' if stock is not None and stock >= qty else 'STOCK_UNKNOWN' if stock is None else 'INSUFFICIENT_STOCK'
        if status != 'QUOTED': issues.append({'id':part['id'],'reason':status})
        consumed, bought = price * each, price * qty
        material += consumed
        purchase += bought
        row.update(status=status, moq=moq, multiple=multiple, stock=stock, purchase_quantity=qty,
                   selected_tier_min=selected, unit_price=str(price), board_material_cost=str(consumed),
                   purchase_cost=str(bought), surplus_quantity=qty-count*each, url=quote['url'], queried_at=quote['queried_at'])
        rows.append(row)
    priced = all(row['status'] != 'UNPRICED' for row in rows)
    return {'scope':'components only; excludes PCB, assembly, stencil, shipping and tools',
            'baseline_id':baseline,'board_quantity':count,'currency':currency,'tax_basis':tax,'rows':rows,
            'known_board_material_subtotal':str(material),'known_purchase_subtotal':str(purchase),
            'board_material_total':str(material) if priced else None,
            'purchase_total':str(purchase) if priced else None,
            'status':'COMPLETE_QUOTE' if not issues else 'INCOMPLETE', 'issues':issues,
            'price_verification':'DECLARED_INPUT_ONLY', 'bom_completeness':'REQUIRES_DESIGN_REVIEW',
            'availability':'AS_QUERIED_NOT_RESERVED'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    args=p.parse_args()
    try:
        data, source = read_source(args.input, 'quote')
        result=calculate(data)
        result['source_inputs'] = [source]
        import sys
        sys.stdout.buffer.write(io.encoded(result)+b'\n')
        return 0 if result['status']=='COMPLETE_QUOTE' else 1
    except (ValueError,TypeError,KeyError,OSError) as exc:
        p.exit(2,'ERROR: '+str(exc)+'\n')
if __name__=='__main__':raise SystemExit(main())
