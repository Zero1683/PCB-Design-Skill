"""Regression tests for offline batch preview and repair/retry control."""
import copy
import argparse
from pathlib import Path
import tempfile
import unittest
import subprocess
import sys
import workflow_io as io
import schematic_layout as layout
import layout_batch as batch
from test_schematic_layout import fixture,actual


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.source,self.spec=fixture();self.plan=layout.plan(self.source,self.spec)

    def bad(self,stage='after-apply'):
        a=actual(self.plan);a['capture_stage']=stage;a['objects'][0]['anchor'][0]+=5;return a

    def test_preview_preserves_facts_and_full_target(self):
        p=batch.preview(self.plan,self.source)
        self.assertEqual(layout.verify(self.plan,p['candidate'])['status'],'MATCH')
        self.assertEqual(p['moves'][0]['preserve_facts_digest'],io.digest(self.source['objects'][0]['facts']))

    def test_stale_input_rejected(self):
        self.source['objects'][0]['facts']['value']='wrong'
        with self.assertRaises(ValueError):batch.preview(self.plan,self.source)

    def test_full_batch_does_not_test_partial_swap(self):
        # All final positions are assessed together even when a destination was occupied.
        source=copy.deepcopy(self.source)
        for i,o in enumerate(source['objects']):
            o['anchor']=[40*i,80];o['bbox']=[40*i,70,40*i+20,90]
        plan=layout.plan(source,self.spec)
        self.assertEqual(batch.preview(plan,source)['status'],'PREFLIGHT_ONLY')

    def test_geometry_repair_is_scoped_proposal(self):
        r=batch.diagnose(self.plan,self.bad(),'a')
        issue=next(x for x in r['issues'] if x.get('field')=='anchor')
        self.assertEqual(issue['candidate']['target_anchor'],self.plan['moves'][0]['to'])
        self.assertEqual(r['status'],'MISMATCH')

    def test_fact_drift_disables_all_movement_proposals(self):
        a=self.bad();a['objects'][1]['facts']['pins']['1']='GND'
        r=batch.diagnose(self.plan,a,'a')
        self.assertTrue(any(x['code']=='PROTECTED_FACTS' for x in r['issues']))
        self.assertTrue(all(x['candidate'] is None for x in r['issues']))

    def test_reload_failure_investigates_persistence(self):
        r=batch.diagnose(self.plan,self.bad('after-reload'),'a')
        self.assertTrue(all(x['candidate'] is None for x in r['issues']))

    def test_repeat_failure_and_budget(self):
        a=batch.diagnose(self.plan,self.bad(),'a');b=batch.diagnose(self.plan,self.bad(),'b')
        data={'attempts':[a]}
        self.assertEqual(batch.decision(data,self.plan['digest']),'CHANGE_PLAN_OR_ADAPTER')
        self.assertEqual(batch.decision(data,self.plan['digest'],'corrected-adapter'),'ALLOW_PREFLIGHT')
        data['attempts'].append(b)
        self.assertEqual(batch.decision(data,'new-plan'),'STOP_REPEATED_FAILURE')
        data['attempts'].append(batch.diagnose(self.plan,self.bad(),'c'))
        self.assertEqual(batch.decision(data,'new-plan'),'STOP_NO_PROGRESS')

    def test_apply_match_does_not_reset_reload_failure(self):
        good=actual(self.plan);good['capture_stage']='after-apply'
        data={'attempts':[batch.diagnose(self.plan,self.bad('after-reload'),'a'),batch.diagnose(self.plan,good,'b')]}
        self.assertEqual(batch.decision(data,self.plan['digest']),'CHANGE_PLAN_OR_ADAPTER')
        good['capture_stage']='after-reload';data['attempts'].append(batch.diagnose(self.plan,good,'c'))
        self.assertEqual(batch.decision(data,self.plan['digest']),'ALLOW_PREFLIGHT')

    def test_persistent_idempotent_ledger_and_changed_attempt(self):
        with tempfile.TemporaryDirectory(dir=WORKDIR,prefix='batch-test-') as td:
            root=Path(td);io.save(root/'plan.json',self.plan);io.save(root/'actual.json',self.bad())
            args=argparse.Namespace(action='record',plan=root/'plan.json',observed=root/'actual.json',
                ledger_dir=root/'ledger',output=root/'report.json',attempt_id='a',adapter_id='unrecorded')
            self.assertEqual(batch.run(args)[1],1);self.assertEqual(batch.run(args)[1],1)
            data=io.read(root/'ledger/layout-attempts.json');self.assertEqual(len(data['attempts']),1)
            a=self.bad();a['objects'][0]['anchor'][0]+=1;io.save(root/'actual.json',a)
            with self.assertRaises(ValueError):batch.run(args)
            data['attempts'][0]['status']='MATCH';io.save(root/'ledger/layout-attempts.json',data)
            with self.assertRaises(ValueError):batch.ledger_read(root/'ledger/layout-attempts.json',batch.identity(self.plan))

    def test_prepare_rejects_failed_plan_without_output(self):
        with tempfile.TemporaryDirectory(dir=WORKDIR,prefix='batch-test-') as td:
            root=Path(td);io.save(root/'plan.json',self.plan);io.save(root/'source.json',self.source)
            (root/'ledger').mkdir()
            io.save(root/'ledger/layout-attempts.json',{'schema':1,'identity':batch.identity(self.plan),'attempts':[batch.diagnose(self.plan,self.bad(),'a')]})
            args=argparse.Namespace(action='prepare',plan=root/'plan.json',fresh=root/'source.json',ledger_dir=root/'ledger',output=root/'batch.json',adapter_id='unrecorded')
            self.assertEqual(batch.run(args)[1],1);self.assertFalse((root/'batch.json').exists())

    def test_cli_prepare_record_and_retry_gate(self):
        with tempfile.TemporaryDirectory(dir=WORKDIR,prefix='batch-cli-') as td:
            root=Path(td);io.save(root/'plan.json',self.plan);io.save(root/'fresh.json',self.source);io.save(root/'bad.json',self.bad())
            common=['--plan',str(root/'plan.json'),'--adapter-id','adapter-r1','--ledger-dir',str(root/'ledger')]
            def call(*args):return subprocess.run([sys.executable,'-X','utf8',batch.__file__,*args,*common],capture_output=True,text=True,encoding='utf-8')
            r=call('prepare','--fresh',str(root/'fresh.json'),'--output',str(root/'batch.json'))
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertIn('PREFLIGHT_ONLY',r.stdout)
            r=call('record','--observed',str(root/'bad.json'),'--attempt-id','run1','--output',str(root/'repair.json'))
            self.assertEqual(r.returncode,1,r.stderr)
            self.assertIn('MISMATCH',r.stdout)
            r=call('prepare','--fresh',str(root/'fresh.json'),'--output',str(root/'blocked.json'))
            self.assertEqual(r.returncode,1,r.stderr);self.assertFalse((root/'blocked.json').exists())


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workdir',type=Path,required=True);args=p.parse_args()
    WORKDIR=args.workdir.resolve(strict=True)
    unittest.main(argv=[__file__],verbosity=2)
