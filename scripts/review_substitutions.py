"""Review declared substitution evidence. No supplier query, purchasing or automatic part replacement."""
import argparse
from pathlib import Path
import workflow_io as io
import evidence_binding as binding
from component_cost import calculate

IMPACTS = {'electrical', 'pinout', 'footprint', 'firmware', 'mechanical', 'supporting_bom'}
STATES = {'MEETS', 'UNCHANGED', 'UNKNOWN', 'DOES_NOT_MEET'}


def evaluate(root, requirements, review):
    root = io.no_link(root).resolve(strict=True)
    for doc in (requirements, review):
        if not isinstance(doc, dict) or doc.get('schema') != 1: raise ValueError('Expected schema 1 object')
        io.text(doc.get('project_id'), 'project ID'); io.text(doc.get('baseline_id'), 'baseline ID')
    for key in ('project_id', 'baseline_id'):
        if review[key] != requirements[key]: raise ValueError('Substitution project/baseline mismatch')
    if review.get('requirements_digest') != io.digest(requirements): raise ValueError('Requirements changed')
    expected = set()
    reqs = requirements.get('requirements')
    if not isinstance(reqs, list) or not reqs: raise ValueError('Nonempty requirements required')
    for req in reqs:
        if not isinstance(req,dict):raise ValueError('Requirement must be an object')
        ident = io.text(req.get('id'), 'requirement ID')
        if ident in expected: raise ValueError('Duplicate requirement ID')
        io.text(req.get('statement'), 'requirement statement')
        binding.reference(root, req.get('source')); expected.add(ident)
    io.text(review.get('reviewer'), 'reviewer')
    io.text(review.get('change_scope'), 'change scope')
    issues = []

    def assessments(rows, key, wanted):
        if not isinstance(rows, list): raise ValueError('Assessments must be a list')
        seen = set()
        for row in rows:
            if not isinstance(row, dict): raise ValueError('Assessment must be an object')
            ident = io.text(row.get(key), key)
            if ident in seen or ident not in wanted: raise ValueError('Duplicate or unknown assessment')
            seen.add(ident)
            state = row.get('status')
            if state not in STATES: raise ValueError('Invalid assessment status')
            io.text(row.get('reason'), 'assessment reason')
            sources = row.get('sources')
            if not isinstance(sources, list) or not sources: raise ValueError('Assessment sources required')
            for source in sources: binding.reference(root, source)
            if state in ('UNKNOWN', 'DOES_NOT_MEET'): issues.append({'item':ident,'reason':state})
        for ident in sorted(wanted - seen): issues.append({'item':ident,'reason':'UNASSESSED'})

    assessments(review.get('requirements'), 'requirement_id', expected)
    assessments(review.get('impacts'), 'area', IMPACTS)
    estimates = {}
    selected = {}
    documents = {}
    for side in ('before', 'after'):
        entry = review.get(side)
        if not isinstance(entry, dict): raise ValueError('Before/after comparison required')
        data = io.read(binding.reference(root, entry.get('quote_file')))
        if data.get('baseline_id') != requirements['baseline_id']: raise ValueError('Quote baseline mismatch')
        result = calculate(data); estimates[side] = result; documents[side] = data
        sku = io.text(entry.get('supplier_code'), 'supplier code')
        parts = [p for p in data['parts'] if p['supplier_code'] == sku]
        if len(parts) != 1: raise ValueError('Selected SKU missing from quote')
        selected[side] = parts[0]
        observations = entry.get('observations')
        if not isinstance(observations, list): raise ValueError('Raw observation references required')
        observed = {}
        for ref in observations:
            record = io.read(binding.reference(root, ref))
            if not isinstance(record, dict): raise ValueError('Observation must be an object')
            code = io.text(record.get('supplier_code'), 'observed SKU')
            if code in observed: raise ValueError('Duplicate observation SKU')
            observed[code] = record
        if set(observed) != {p['supplier_code'] for p in data['parts']}: raise ValueError('Observation coverage differs from quote BOM')
        for part in data['parts']:
            record = observed[part['supplier_code']]
            if record.get('mpn') != part['mpn'] or record.get('quote') != part.get('quote') or record.get('quote') is None:
                raise ValueError('Quote does not match captured SKU observation')
            # Keep the actual response/page capture separately from its normalized fields.
            binding.reference(root, record.get('raw_source'))
    if selected['before']['supplier_code'] == selected['after']['supplier_code']: raise ValueError('Expected a changed supplier SKU')
    for key in ('board_quantity', 'currency', 'tax_basis'):
        if documents['before'][key] != documents['after'][key]: raise ValueError('Compare the same quantity/currency/tax basis')
    fields = ('mpn', 'package', 'spec', 'qty_per_board', 'spares')
    def inventory(data):
        return {p['supplier_code']:{k:p.get(k,0) if k=='spares' else p[k] for k in fields} for p in data['parts']}
    old,new=inventory(documents['before']),inventory(documents['after'])
    changes={sku:{'before':old.get(sku),'after':new.get(sku)} for sku in sorted(set(old)|set(new)) if old.get(sku)!=new.get(sku)}
    declared=review.get('bom_changes')
    if not isinstance(declared,list):raise ValueError('Explicit BOM change review required')
    seen=set()
    for row in declared:
        if not isinstance(row,dict):raise ValueError('BOM change must be an object')
        sku=io.text(row.get('supplier_code'),'changed SKU')
        if sku in seen or sku not in changes:raise ValueError('Duplicate or unexpected BOM change')
        seen.add(sku)
        if any(row.get(key)!=changes[sku][key] for key in ('before','after')):raise ValueError('Declared BOM delta differs from quotes')
        io.text(row.get('reason'),'BOM change reason')
        sources=row.get('sources')
        if not isinstance(sources,list) or not sources:raise ValueError('BOM change sources required')
        for source in sources:binding.reference(root,source)
    for sku in sorted(set(changes)-seen):issues.append({'item':sku,'reason':'UNREVIEWED_BOM_CHANGE'})
    if changes and any(row.get('area')=='supporting_bom' and row.get('status')=='UNCHANGED' for row in review['impacts']):
        issues.append({'item':'supporting_bom','reason':'DECLARED_UNCHANGED_BUT_DIFFERS'})
    if sum(p['spares'] for p in new.values()) < sum(p['spares'] for p in old.values()):
        if not review.get('spares_decision'):issues.append({'item':'spares','reason':'REDUCTION_NEEDS_EXPLICIT_DECISION'})
        else:binding.reference(root,review['spares_decision'])
    if estimates['after']['status'] != 'COMPLETE_QUOTE': issues.append({'item':'after_quote','reason':'INCOMPLETE'})
    from decimal import Decimal
    savings = None
    if all(estimates[s]['purchase_total'] is not None for s in estimates):
        savings = str(Decimal(estimates['before']['purchase_total']) - Decimal(estimates['after']['purchase_total']))
    return {'state':'REVIEW_RECORD_COMPLETE' if not issues else 'BLOCKED', 'issues':issues,
            'project_id':requirements['project_id'], 'baseline_id':requirements['baseline_id'],
            'requirements_digest':io.digest(requirements), 'review_digest':io.digest(review),
            'purchase_savings':savings, 'estimates':estimates, 'bom_changes':changes,
            'scope':'declared requirement/impact coverage and retained quote consistency',
            'electrical_equivalence':'REQUIRES_ENGINEERING_REVIEW', 'live_price_authenticity':'NOT_ASSESSED',
            'replacement_applied':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True);p.add_argument('--requirements',default='requirements.json')
    p.add_argument('--review',default='substitution-review.json');a=p.parse_args()
    try:
        root=io.no_link(a.root).resolve(strict=True)
        result=evaluate(root,io.read(binding.local(root,a.requirements)),io.read(binding.local(root,a.review)))
        import sys;sys.stdout.buffer.write(io.encoded(result)+b'\n')
        return 0 if result['state']=='REVIEW_RECORD_COMPLETE' else 1
    except (ValueError,KeyError,TypeError,OSError) as exc:p.exit(2,'ERROR: '+str(exc)+'\n')
if __name__=='__main__':raise SystemExit(main())
