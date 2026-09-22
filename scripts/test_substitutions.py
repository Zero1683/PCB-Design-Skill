import copy
from pathlib import Path
import tempfile
import unittest
import workflow_io as io
from review_substitutions import evaluate, IMPACTS
from test_component_cost import fixture

class SubstitutionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=Path.cwd());self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        (self.root/'source.txt').write_text('Synthetic requirement and datasheet evidence',encoding='utf-8')
        self.source=self.ref('source.txt')
        self.requirements={'schema':1,'project_id':'fixture','baseline_id':'A','requirements':[
            {'id':'R1','statement':'Synthetic supported feature','source':self.source},
            {'id':'R2','statement':'Synthetic mechanical requirement','source':self.source}]}
        self.review={'schema':1,'project_id':'fixture','baseline_id':'A','requirements_digest':io.digest(self.requirements),
            'reviewer':'synthetic-test','change_scope':'replace selected resistor and retain supporting BOM',
            'requirements':[{'requirement_id':v,'status':'MEETS','reason':'Synthetic only','sources':[self.source]} for v in ('R1','R2')],
            'impacts':[{'area':v,'status':'UNCHANGED','reason':'Synthetic only','sources':[self.source]} for v in sorted(IMPACTS)]}
        for side,sku in (('before','OLD'),('after','NEW')):
            d=fixture();part=d['parts'][0];part['supplier_code']=sku
            if side=='after':part['quote']['moq']=1;part['quote']['multiple']=1
            io.save(self.root/(side+'.json'),d)
            io.save(self.root/(side+'-observation.json'),{'supplier_code':sku,'mpn':part['mpn'],'quote':part['quote'],'raw_source':self.source})
            self.review[side]={'supplier_code':sku,'quote_file':self.ref(side+'.json'),'observations':[self.ref(side+'-observation.json')]}
        next(v for v in self.review['impacts'] if v['area']=='supporting_bom')['status']='MEETS'
        self.refresh_changes()
    def refresh_changes(self):
        old=io.read(self.root/'before.json')['parts'];new=io.read(self.root/'after.json')['parts']
        def inv(parts):return {p['supplier_code']:{k:p.get(k,0) if k=='spares' else p[k] for k in ('mpn','package','spec','qty_per_board','spares')} for p in parts}
        a,b=inv(old),inv(new)
        self.review['bom_changes']=[{'supplier_code':k,'before':a.get(k),'after':b.get(k),'reason':'Synthetic justified change','sources':[self.source]} for k in sorted(set(a)|set(b)) if a.get(k)!=b.get(k)]
    def ref(self,name):return {'path':name,'sha256':io.file_hash(self.root/name)}
    def run_review(self):return evaluate(self.root,self.requirements,self.review)
    def test_complete_record_does_not_claim_equivalence(self):
        result=self.run_review();self.assertEqual(result['state'],'REVIEW_RECORD_COMPLETE');self.assertEqual(result['purchase_savings'],'0.96');self.assertFalse(result['replacement_applied'])
    def test_missing_requirement_blocks(self):
        self.review['requirements'].pop();self.assertEqual(self.run_review()['state'],'BLOCKED')
    def test_unknown_or_downgraded_requirement_blocks(self):
        for state in ('UNKNOWN','DOES_NOT_MEET'):
            self.review['requirements'][0]['status']=state;self.assertEqual(self.run_review()['state'],'BLOCKED')
    def test_missing_impact_blocks(self):
        for area in IMPACTS:
            old=self.review['impacts'];self.review['impacts']=[r for r in old if r['area']!=area]
            self.assertEqual(self.run_review()['state'],'BLOCKED');self.review['impacts']=old
    def test_stale_requirement_or_source_rejected(self):
        self.requirements['requirements'][0]['statement']='Changed'
        with self.assertRaises(ValueError):self.run_review()
        self.review['requirements_digest']=io.digest(self.requirements)
        (self.root/'source.txt').write_text('Changed',encoding='utf-8')
        with self.assertRaises(ValueError):self.run_review()
    def test_wrong_identity_rejected(self):
        for key in ('project_id','baseline_id'):
            old=self.review[key];self.review[key]='OTHER'
            with self.assertRaises(ValueError):self.run_review()
            self.review[key]=old
    def test_missing_raw_capture_rejected(self):
        data=io.read(self.root/'after-observation.json');data.pop('raw_source');io.save(self.root/'after-observation.json',data)
        self.review['after']['observations']=[self.ref('after-observation.json')]
        with self.assertRaises(ValueError):self.run_review()
    def test_changed_quote_cannot_reuse_observation(self):
        d=io.read(self.root/'after.json');d['parts'][0]['quote']['moq']=100;io.save(self.root/'after.json',d)
        self.review['after']['quote_file']=self.ref('after.json')
        with self.assertRaises(ValueError):self.run_review()
    def test_board_quantity_cannot_be_reduced_to_claim_savings(self):
        d=io.read(self.root/'after.json');d['board_quantity']=2;io.save(self.root/'after.json',d)
        self.review['after']['quote_file']=self.ref('after.json')
        with self.assertRaises(ValueError):self.run_review()
    def test_insufficient_candidate_stock_blocks(self):
        d=io.read(self.root/'after.json');d['parts'][0]['quote']['stock']=0;io.save(self.root/'after.json',d)
        self.review['after']['quote_file']=self.ref('after.json')
        o=io.read(self.root/'after-observation.json');o['quote']=d['parts'][0]['quote'];io.save(self.root/'after-observation.json',o)
        self.review['after']['observations']=[self.ref('after-observation.json')]
        self.assertEqual(self.run_review()['state'],'BLOCKED')
    def test_duplicate_or_unmapped_ids_rejected(self):
        self.review['requirements'].append(copy.deepcopy(self.review['requirements'][0]))
        with self.assertRaises(ValueError):self.run_review()
    def test_missing_bom_change_blocks(self):
        self.review['bom_changes'].pop();self.assertEqual(self.run_review()['state'],'BLOCKED')
    def test_unchanged_supporting_bom_cannot_hide_change(self):
        next(v for v in self.review['impacts'] if v['area']=='supporting_bom')['status']='UNCHANGED'
        self.assertEqual(self.run_review()['state'],'BLOCKED')
    def test_invented_quantity_delta_rejected(self):
        self.review['bom_changes'][0]['after']={'qty_per_board':999}
        with self.assertRaises(ValueError):self.run_review()
    def test_reduced_spares_require_decision(self):
        d=io.read(self.root/'before.json');d['parts'][0]['spares']=100;io.save(self.root/'before.json',d)
        self.review['before']['quote_file']=self.ref('before.json');self.refresh_changes()
        self.assertEqual(self.run_review()['state'],'BLOCKED')
        self.review['spares_decision']=self.source
        self.assertEqual(self.run_review()['state'],'REVIEW_RECORD_COMPLETE')
    def test_missing_sources_or_reasons_rejected(self):
        self.review['impacts'][0]['sources']=[]
        with self.assertRaises(ValueError):self.run_review()
if __name__=='__main__':unittest.main()
