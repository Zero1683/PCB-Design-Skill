import unittest,tempfile,copy,subprocess,os
from pathlib import Path
import workflow_io as io
import check_evidence as ce
import evidence_binding as eb
from test_evidence_fixture import prepare,write_rows

class BindingTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=Path.cwd(),prefix='binding-test-');self.root=Path(self.tmp.name);self.rows=prepare(self.root)
 def tearDown(self):self.tmp.cleanup()
 def audit(self):return ce.audit(self.root,'A',through='G5',design_gates=True)
 def test_complete_fixture(self):
  result=self.audit();self.assertTrue(result['records_complete']);self.assertIsInstance(result['selected_checks'],int)
 def test_removing_each_required_check_fails(self):
  for row in self.rows:
   write_rows(self.root,[r for r in self.rows if r['id']!=row['id']]);self.assertFalse(self.audit()['records_complete'],row['id'])
 def test_fail_does_not_disappear_by_deletion(self):
  row=next(r for r in self.rows if r['id']=='PCB-DRC');row['status']='FAIL';write_rows(self.root,self.rows);self.assertFalse(self.audit()['records_complete']);write_rows(self.root,[r for r in self.rows if r['id']!='PCB-DRC']);self.assertFalse(self.audit()['records_complete'])
 def test_required_cannot_be_reclassified_or_na(self):
  row=next(r for r in self.rows if r['id']=='PCB-DRC');row.update(status='N_A',applicability='assess',limitation='skip');write_rows(self.root,self.rows);self.assertFalse(self.audit()['records_complete'])
 def test_conditional_na_needs_bound_decision(self):
  row=next(r for r in self.rows if r['id']=='DENSE-ESCAPE');row.update(status='N_A',limitation='No dense package');write_rows(self.root,self.rows);self.assertFalse(self.audit()['records_complete'])
  data=io.read(self.root/'check-bindings.json');next(b for b in data['checks'] if b['id']=='DENSE-ESCAPE')['status']='N_A';io.save(self.root/'check-bindings.json',data);self.assertTrue(self.audit()['records_complete'])
 def test_design_edit_invalidates_unchanged_report(self):
  (self.root/'native.json').write_text('{"changed":true}');self.assertFalse(self.audit()['records_complete'])
 def test_refreshing_manifest_does_not_refresh_reports(self):
  (self.root/'native.json').write_text('{"changed":true}');io.save(self.root/'design-baseline.json',eb.snapshot(self.root,'fixture',['synthetic-document'],'A',['native.json']));self.assertFalse(self.audit()['records_complete'])
 def test_report_edit_invalidates_binding(self):
  (self.root/'evidence.txt').write_text('changed');self.assertFalse(self.audit()['records_complete'])
 def test_manual_fields_required(self):
  for key in ('reviewer','basis','finding'):
   data=io.read(self.root/'check-bindings.json');old=data['checks'][0].pop(key);io.save(self.root/'check-bindings.json',data);self.assertFalse(self.audit()['records_complete']);data['checks'][0][key]=old;io.save(self.root/'check-bindings.json',data)
 def test_cross_project_mapping_fails(self):
  for name in ('requirements.json','requirement-checks.json'):
   d=io.read(self.root/name);d['project_id']='other';io.save(self.root/name,d)
  d=io.read(self.root/'requirement-checks.json');d['requirements_digest']=io.digest(io.read(self.root/'requirements.json'));io.save(self.root/'requirement-checks.json',d);self.assertFalse(self.audit()['records_complete'])
 def test_machine_fail_cannot_be_marked_pass(self):
  output={'scope':'normalized-record-comparison','records_match':False,'differences':[{'ref':'U1'}]};io.save(self.root/'machine.json',output)
  ref={'path':'machine.json','sha256':io.file_hash(self.root/'machine.json')}
  b=io.read(self.root/'check-bindings.json');entry=copy.deepcopy(b['checks'][0]);entry.update(id='CUSTOM-COMPARE',mode='machine',evidence=[ref],report={'output':ref,'tool':{'name':'audit_design.py','sha256':eb.tool_digest('audit_design.py')}});b['checks'].append(entry);io.save(self.root/'check-bindings.json',b)
  row=copy.deepcopy(self.rows[0]);row.update(id='CUSTOM-COMPARE',evidence_path='machine.json');write_rows(self.root,self.rows+[row]);self.assertFalse(self.audit()['records_complete'])
 def test_whitespace_custom_pass_cannot_skip_binding(self):
  row=copy.deepcopy(self.rows[0]);row.update(id='CUSTOM-UNBOUND',status='PASS ',stage='G2 ');write_rows(self.root,self.rows+[row]);self.assertFalse(self.audit()['records_complete'])
 def test_na_with_wrong_baseline_fails(self):
  row=next(r for r in self.rows if r['id']=='DENSE-ESCAPE');row.update(status='N_A',baseline_id='OLD',limitation='No dense package');write_rows(self.root,self.rows)
  data=io.read(self.root/'check-bindings.json');next(b for b in data['checks'] if b['id']=='DENSE-ESCAPE')['status']='N_A';io.save(self.root/'check-bindings.json',data);self.assertFalse(self.audit()['records_complete'])
 def test_junction_root_rejected_before_resolution(self):
  if os.name!='nt':self.skipTest('Windows junction regression')
  link=self.root/'linked';target=self.root/'target';target.mkdir();prepare(target)
  # mklink is only used to create a directory junction inside this temporary workspace.
  result=subprocess.run(['cmd','/c','mklink','/J',str(link),str(target)],capture_output=True)
  if result.returncode:self.skipTest('Junction creation unavailable')
  try:
   with self.assertRaises(ValueError):ce.audit(link,'A',design_gates=True)
  finally:os.rmdir(link)
if __name__=='__main__':unittest.main()
