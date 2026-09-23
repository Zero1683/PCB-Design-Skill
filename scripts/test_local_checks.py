import copy,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import local_checks as lc
import workflow_io as io
from test_geometry_sweep import board

class LocalChecksTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        io.save(self.root/'board.json',board([('top',[0,0,1,1]),('top',[4,0,5,1])]))
        self.job={'id':'geometry','kind':'geometry','inputs':['board.json'],'options':{'clearance_mm':.2}}
        self.plan={'schema':1,'jobs':[self.job]}
    def run_plan(self):return lc.run(self.root,self.plan)
    def test_reuse_preserves_report(self):
        first=self.run_plan();second=self.run_plan()
        self.assertEqual(first['cached_jobs'],0);self.assertEqual(second['cached_jobs'],1)
        self.assertEqual(first['jobs'][0]['report_sha256'],second['jobs'][0]['report_sha256'])
    def test_changed_geometry_recomputes_and_fails(self):
        self.run_plan();io.save(self.root/'board.json',board([('top',[0,0,1,1]),('top',[.5,0,1.5,1])]))
        result=self.run_plan();self.assertEqual(result['cached_jobs'],0);self.assertEqual(result['jobs'][0]['state'],'CHECK_FAILED')
    def test_changed_rules_and_code_invalidate(self):
        self.run_plan();self.job['options']['clearance_mm']=5
        result=self.run_plan();self.assertEqual(result['cached_jobs'],0);self.assertEqual(result['jobs'][0]['state'],'CHECK_FAILED')
        with patch.object(lc,'tool_revision',return_value='different-tool-code'):
            self.assertEqual(self.run_plan()['cached_jobs'],0)
    def test_tampered_report_reruns(self):
        first=self.run_plan();(self.root/first['jobs'][0]['report']).write_text('{}')
        self.assertEqual(self.run_plan()['cached_jobs'],0)
    def test_force_reruns(self):
        self.run_plan();self.assertEqual(lc.run(self.root,self.plan,True)['cached_jobs'],0)
    def test_no_arbitrary_commands_or_paths(self):
        for mutate in [lambda j:j.update(kind='shell'),lambda j:j.update(inputs=['../outside.json']),
                       lambda j:j.update(inputs=['.PCB-LOCAL/test.json']),lambda j:j['options'].update(command='anything')]:
            job=copy.deepcopy(self.job);mutate(job)
            with self.assertRaises(ValueError):lc.run(self.root,{'schema':1,'jobs':[job]})
    def test_error_is_not_cached_or_promoted(self):
        (self.root/'board.json').write_text('{"malformed":true}')
        for _ in range(2):
            result=self.run_plan();self.assertEqual(result['cached_jobs'],0);self.assertEqual(result['jobs'][0]['state'],'ERROR')
    def test_root_evidence_changes_invalidate(self):
        from test_evidence_fixture import prepare
        prepare(self.root)
        self.plan={'schema':1,'jobs':[{'id':'size','kind':'mechanical','inputs':[],'options':{'baseline':'A'}}]}
        self.assertEqual(self.run_plan()['jobs'][0]['state'],'CHECK_OK')
        self.assertEqual(self.run_plan()['cached_jobs'],1)
        obs=io.read(self.root/'mechanical-observation.json');obs['assembled_height_mm']=15;io.save(self.root/'mechanical-observation.json',obs)
        result=self.run_plan();self.assertEqual(result['cached_jobs'],0);self.assertEqual(result['jobs'][0]['state'],'CHECK_FAILED')
    def test_busy_lock_never_removed_by_another_run(self):
        cache=self.root/lc.STATE_DIR;cache.mkdir();(cache/'run.lock').write_text('test')
        with self.assertRaises(FileExistsError):self.run_plan()
        self.assertTrue((cache/'run.lock').exists())
    def test_indirect_managed_source_rejected_before_cache(self):
        from test_evidence_fixture import prepare
        prepare(self.root)
        self.plan={'schema':1,'jobs':[{'id':'size','kind':'mechanical','inputs':[],'options':{'baseline':'A'}}]}
        self.run_plan()
        obs=io.read(self.root/'mechanical-observation.json')
        obs['source']['path']='.pcb-local/source.json'
        io.save(self.root/'mechanical-observation.json',obs)
        with self.assertRaisesRegex(ValueError,'managed reports'):self.run_plan()

if __name__=='__main__':unittest.main()
