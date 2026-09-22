import unittest,tempfile,copy,csv
from pathlib import Path
import requirement_coverage as rc
import workflow_io as io
import check_evidence as ce
class CoverageTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=Path.cwd(),prefix='coverage-test-');self.root=Path(self.tmp.name)
  (self.root/'input.md').write_text('USB connector must be at the specified mating face.',encoding='utf8')
  (self.root/'result.json').write_text('{"observed":"synthetic"}',encoding='utf8')
  self.req={'schema':1,'project_id':'p','baseline_id':'A','requirements':[{'id':'MECH-1','statement':'Connector placement','source':self.ev('input.md')}]}
  self.checks={'schema':1,'project_id':'p','baseline_id':'A','requirements_digest':io.digest(self.req),'checks':[{'id':'C1','requirement_ids':['MECH-1'],'method':'synthetic geometry','subjects':['J1'],'status':'PASS','evidence':self.ev('result.json')}]}
 def tearDown(self):self.tmp.cleanup()
 def ev(self,name):return {'path':name,'sha256':io.file_hash(self.root/name)}
 def run_check(self):return rc.evaluate(self.root,self.req,self.checks,'A')
 def test_mapped_evidence_integrity_not_electrical_acceptance(self):
  r=self.run_check();self.assertEqual(r['state'],'COVERED_WITH_CURRENT_EVIDENCE');self.assertEqual(r['engineering_correctness'],'NOT_ASSESSED')
 def test_unmapped_requirement(self):
  self.checks['checks']=[];self.assertEqual(self.run_check()['results'][0]['state'],'UNMAPPED')
 def test_pending_or_failed_check_cannot_be_hidden_by_pass(self):
  for status in ('NOT_RUN','FAIL','BLOCKED'):
   c=copy.deepcopy(self.checks['checks'][0]);c['id']='C2';c['status']=status;self.checks['checks']=[self.checks['checks'][0],c];self.assertEqual(self.run_check()['state'],'INCOMPLETE')
 def test_changed_evidence_and_source(self):
  for name in ('result.json','input.md'):
   old=(self.root/name).read_bytes();(self.root/name).write_bytes(b'changed')
   with self.assertRaises(ValueError):self.run_check()
   (self.root/name).write_bytes(old)
 def test_changed_requirement_or_baseline(self):
  self.req['requirements'][0]['statement']='changed'
  with self.assertRaises(ValueError):self.run_check()
 def test_unknown_mapping_duplicate_and_missing_subject(self):
  original=copy.deepcopy(self.checks)
  for mode in ('unknown','duplicate','subjects'):
   self.checks=copy.deepcopy(original)
   if mode=='unknown':self.checks['checks'][0]['requirement_ids']=['other']
   if mode=='duplicate':self.checks['checks']*=2
   if mode=='subjects':self.checks['checks'][0]['subjects']=[]
   with self.assertRaises(ValueError):self.run_check()
 def test_outside_evidence_rejected(self):
  self.checks['checks'][0]['evidence']['path']='../outside.json'
  with self.assertRaises(ValueError):self.run_check()
 def test_g5_requires_coverage_and_detects_later_evidence_edit(self):
  from test_evidence_fixture import prepare
  prepare(self.root,project='p',evidence='result.json')
  (self.root/'requirement-checks.json').unlink()
  self.assertFalse(ce.audit(self.root,'A',design_gates=True)['records_complete'])
  prepare(self.root,project='p',evidence='result.json')
  self.assertTrue(ce.audit(self.root,'A',design_gates=True)['records_complete'])
  (self.root/'result.json').write_text('changed',encoding='utf8');self.assertFalse(ce.audit(self.root,'A',design_gates=True)['records_complete'])
 def test_separator_only_evidence_does_not_pass(self):
  with (self.root/'CHECKS.csv').open('w',newline='',encoding='utf8') as f:
   w=csv.DictWriter(f,fieldnames=sorted(ce.FIELDS));w.writeheader()
   row=dict.fromkeys(ce.FIELDS,'');row.update(id='one',stage='G2',check='fixture',applicability='required',status='PASS',baseline_id='A',method='fixture',conditions='fixture',acceptance='fixture',actual='fixture',evidence_path='; ;',checked_at='2026-09-22T00:00:00+00:00');w.writerow(row)
  result=ce.audit(self.root,'A',through='G2');self.assertFalse(result['records_complete']);self.assertTrue(any('evidence list' in e for e in result['record_errors']))
 def test_malformed_records_fail_explicitly(self):
  for req,checks in (([],self.checks),(self.req,[])):
   with self.assertRaises(ValueError):rc.evaluate(self.root,req,checks,'A')
  self.req['requirements']=[None];self.checks['requirements_digest']=io.digest(self.req)
  with self.assertRaises(ValueError):self.run_check()
if __name__=='__main__':unittest.main()
