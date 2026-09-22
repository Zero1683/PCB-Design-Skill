"""Adversarial imported-report and execution identity regressions using real checkers."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import evidence_binding as eb
import workflow_io as io
import run_bound_check as runner
from test_circuit_checks import snapshot
from test_component_cost import fixture

SCRIPTS=Path(__file__).resolve().parent
class ProvenanceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=Path.cwd(),prefix='report-proof-');self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  left=snapshot();left.update(project_id='P',document_id='S');right=copy.deepcopy(left);right.update(kind='pcb',document_id='B')
  io.save(self.root/'left.json',left);io.save(self.root/'right.json',right)
  self.refresh()
  result=subprocess.run([sys.executable,'-B','-X','utf8',str(SCRIPTS/'audit_design.py'),'compare',str(self.root/'left.json'),str(self.root/'right.json')],capture_output=True,check=True)
  self.output=json.loads(result.stdout);self.bind()
 def refresh(self):
  self.current=eb.snapshot(self.root,'P',['S','B'],'A',['left.json','right.json']);io.save(self.root/'design-baseline.json',self.current)
 def bind(self):
  io.save(self.root/'report.json',self.output)
  self.ref={'path':'report.json','sha256':io.file_hash(self.root/'report.json')}
  self.report={'output':self.ref,'tool':{'name':'audit_design.py','sha256':eb.tool_digest('audit_design.py')}}
 def status(self):return eb.machine_status(self.root,self.report)
 def mutate_output(self,key,value):self.output[key]=value;self.bind()
 def test_genuine_import_and_gate_pass(self):
  self.assertEqual(self.status(),'PASS')
  b={'id':'CUSTOM-IMPORT','status':'PASS','mode':'machine','design_digest':io.digest(self.current),'checked_at':'2026-09-22T00:00:00Z','method':'real CLI comparison','inputs':self.current['inputs'],'evidence':[self.ref],'report':self.report}
  io.save(self.root/'check-bindings.json',{'schema':1,'project_id':'P','baseline_id':'A','checks':[b]})
  row={'id':b['id'],'status':'PASS','stage':'G2','baseline_id':'A','evidence_path':'report.json'}
  self.assertEqual(eb.evaluate(self.root,'A',[row],'G2')['state'],'BOUND_TO_CURRENT_FILES')
  self.mutate_output('baseline_id','OLD');b['report']=self.report;b['evidence']=[self.ref]
  io.save(self.root/'check-bindings.json',{'schema':1,'project_id':'P','baseline_id':'A','checks':[b]})
  with self.assertRaisesRegex(ValueError,'baseline mismatch'):eb.evaluate(self.root,'A',[row],'G2')
 def test_old_and_missing_report_baselines_rejected(self):
  for v in ('OLD',None):
   self.mutate_output('baseline_id',v)
   with self.assertRaisesRegex(ValueError,'baseline mismatch'):self.status()
 def test_report_project_and_document_mismatch_rejected(self):
  for k in ('project_id','projectId','document_id','documentId','document_ids'):
   with self.subTest(k=k):
    self.mutate_output(k,['OTHER'] if k=='document_ids' else 'OTHER')
    with self.assertRaises(ValueError):self.status()
    del self.output[k]
 def test_legacy_report_without_source_hashes_rejected(self):
  del self.output['source_inputs'];self.bind()
  with self.assertRaisesRegex(ValueError,'every actual checker input'):self.status()
 def test_changed_source_cannot_reuse_old_report_after_rebinding(self):
  with (self.root/'left.json').open('ab') as f:f.write(b' ')
  self.refresh()
  with self.assertRaisesRegex(ValueError,'current bound design'):self.status()
 def test_unrelated_current_inputs_cannot_support_archived_report(self):
  for name in ('left.json','right.json'):
   data=io.read(self.root/name);data['source']='new export';io.save(self.root/name,data)
  self.refresh()
  with self.assertRaises(ValueError):self.status()
 def test_source_identity_cannot_be_relabelled_by_envelope(self):
  original=io.read(self.root/'left.json')
  for key,value in [('baseline_id','OLD'),('project_id','OTHER'),('document_id','OTHER')]:
   data=copy.deepcopy(original);data[key]=value;io.save(self.root/'left.json',data);self.refresh()
   self.output['source_inputs'][0]['sha256']=io.file_hash(self.root/'left.json');self.bind()
   with self.subTest(key=key),self.assertRaises(ValueError):self.status()
 def test_invalid_role_missing_hash_and_extra_source_rejected(self):
  original=copy.deepcopy(self.output['source_inputs'])
  for value in ([],original[::-1],original+[original[0]],[{'role':'left','sha256':[]},original[1]]):
   self.mutate_output('source_inputs',value)
   with self.assertRaises(ValueError):self.status()
 def test_report_fail_preserved(self):
  self.output.update(records_match=False,differences=[{'ref':'U1','field':'pins'}]);self.bind();self.assertEqual(self.status(),'FAIL')
 def test_bound_runner_rejects_wrong_document_before_launch(self):
  data=io.read(self.root/'left.json');data['document_id']='OTHER';io.save(self.root/'left.json',data);self.refresh()
  with self.assertRaisesRegex(ValueError,'document mismatch'):runner.run(self.root,'P','A','CUSTOM','run','compare',['left.json','right.json'])
  self.assertFalse((self.root/'run').exists())
 def test_geometry_no_fitted_parts_is_not_pass(self):
  data=io.read(self.root/'right.json')
  for part in data['components']:part['fitted']=False
  io.save(self.root/'right.json',data);self.refresh()
  record=runner.run(self.root,'P','A','CUSTOM','run','geometry',['right.json'],clearance_mm=0.2)
  self.assertEqual(record['status'],'BLOCKED')
 def test_constraints_bom_encoded_input_exact_hashes(self):
  s={'schema':1,'baseline_id':'A','domain':'pcb','coverage':'complete','projectId':'P','documentId':'B','units':'mm','axis':'y-up','objects':[{'id':'J1','anchor':[5,5],'rotation':0,'side':'top','bbox':[4,4,6,6],'height':3}]}
  c={'schema':1,'baseline_id':'A','revision':'mech-A','domain':'pcb','projectId':'P','documentId':'B','units':'mm','axis':'y-up','source':'drawing A','bounds':[0,0,20,20],'rules':[]}
  (self.root/'left.json').write_text(json.dumps(s),encoding='utf-8-sig');io.save(self.root/'right.json',c);self.refresh()
  p=subprocess.run(['node',str(SCRIPTS/'check_constraints.mjs'),'--snapshot',str(self.root/'left.json'),'--constraints',str(self.root/'right.json'),'--output',str(self.root/'geometry.json')],capture_output=True)
  self.assertEqual(p.returncode,0,p.stderr)
  report={'output':{'path':'geometry.json','sha256':io.file_hash(self.root/'geometry.json')},'tool':{'name':'check_constraints.mjs','sha256':eb.tool_digest('check_constraints.mjs')}}
  self.assertEqual(eb.machine_status(self.root,report),'PASS')
  out=io.read(self.root/'geometry.json');self.assertEqual(out['source_inputs'][0]['sha256'],io.file_hash(self.root/'left.json'))
 def test_cost_aggregate_cannot_hide_unpriced_row(self):
  io.save(self.root/'left.json',fixture());self.refresh()
  record=runner.run(self.root,'P','A','COST','run','cost',['left.json'])
  out=io.read(self.root/'run/report.json');out['rows'][0]['status']='UNPRICED';io.save(self.root/'run/report.json',out)
  record['report']['output']['sha256']=io.file_hash(self.root/'run/report.json')
  self.assertEqual(eb.machine_status(self.root,record['report'],inputs=record['inputs']),'FAIL')
if __name__=='__main__':unittest.main(verbosity=2)
