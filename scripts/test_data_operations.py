#!/usr/bin/env python3
"""Observed data and isolated recovery regressions; synthetic files, no EDA client."""
import argparse
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import design_data as data
import operation_state as ops
import workflow_io as io

WORKDIR=None


def fixture():
    snapshot={'schema':1,'kind':'pcb','baseline_id':'A','source':'synthetic actual readback',
              'coverage':'complete','components':[{'ref':'R1','part':'R','value':'10k','footprint':'R0603',
              'fitted':True,'in_bom':True,'pins':{'1':'VCC','2':'OUT'}}]}
    board={'schema':1,'units':'mm','components':[{'des':'R1','native_id':'native1','footprint':'fp1',
            'x':1.0,'y':2.0,'angle':0.0,'side':'top'}],
           'footprints':{'fp1':{'pads':[{'num':'1','elem':'p1','x':-1,'y':0,'w':.6,'h':.8},
                                             {'num':'2','elem':'p2','x':1,'y':0,'w':.6,'h':.8}],
                                'silk':[[0,0],[1,1]],'custom_visual':'preserve'}},
           'pad_nets':{'R1.1':'VCC','R1#p1':'VCC','R1.2':'OUT','R1#p2':'OUT'},
           'tracks':[{'net':'OUT','w':.2,'x1':1,'y1':2,'x2':3,'y2':4,'layer':1}],
           'vias':[],'pours':[],'rules':{'clearance':.2},'layers':{'top':1,'bottom':2},
           'import_coverage':{'pcb_documents':1,'source_components':1,'imported_components':1,'missing_footprints':0}}
    return snapshot,board


def bind(snapshot,board):
    return {'schema':1,'role':'observed','project_id':'project','document_id':'pcb',
            'baseline_id':snapshot['baseline_id'],'snapshot_digest':io.digest(snapshot),'board_digest':io.digest(board),
            'readback_evidence':'synthetic native readback fixture',
            'footprint_map':{p['ref']:{'snapshot':p['footprint'],'toolkit':next(c['footprint'] for c in board['components'] if c['des']==p['ref'])} for p in snapshot['components']}}


class DataTests(unittest.TestCase):
    def test_build_and_exact_roundtrip(self):
        s,b=fixture();result=data.build(s,b,bind(s,b))
        self.assertEqual(data.validate(result),result)
        self.assertEqual(result['normalized'],s);self.assertEqual(result['board'],b)
        self.assertEqual(result['coverage']['electrical_acceptance'],'NOT_ASSESSED')

    def test_intent_and_stale_binding_rejected(self):
        s,b=fixture();binding=bind(s,b);binding['role']='intent'
        with self.assertRaises(ValueError):data.build(s,b,binding)
        binding=bind(s,b);b['rules']['clearance']=.01
        with self.assertRaises(ValueError):data.build(s,b,binding)

    def test_conflicting_element_and_duplicate_pin(self):
        s,b=fixture();b['pad_nets']['R1#p1']='OUT'
        with self.assertRaises(ValueError):data.build(s,b,bind(s,b))
        s,b=fixture();b['footprints']['fp1']['pads'].append({'num':'1','elem':'p3'})
        b['pad_nets']['R1#p3']='GND'
        with self.assertRaises(ValueError):data.build(s,b,bind(s,b))

    def test_same_number_multiple_lands_preserved(self):
        s,b=fixture();b['footprints']['fp1']['pads'].append({'num':'1','elem':'p3'})
        b['pad_nets']['R1#p3']='VCC'
        self.assertEqual(data.build(s,b,bind(s,b))['components']['R1']['physical_pad_count'],3)

    def test_missing_repeated_pad_element_cannot_borrow_net(self):
        s,b=fixture();b['footprints']['fp1']['pads'].append({'num':'1','elem':'p3'})
        with self.assertRaises(ValueError):data.build(s,b,bind(s,b))

    def test_missing_is_not_nc(self):
        s,b=fixture();s['components'][0]['pins']['2']=None
        del b['pad_nets']['R1.2'];del b['pad_nets']['R1#p2']
        with self.assertRaises(ValueError):data.build(s,b,bind(s,b))
        binding=bind(s,b);binding['unconnected_pins']=[['R1','2']]
        self.assertIsNone(data.build(s,b,binding)['components']['R1']['record']['pins']['2'])

    def test_extra_pad_and_missing_native_id_rejected(self):
        s,b=fixture();b['pad_nets']['R1#missing']='VCC'
        with self.assertRaises(ValueError):data.build(s,b,bind(s,b))
        s,b=fixture();del b['components'][0]['native_id']
        with self.assertRaises(ValueError):data.build(s,b,bind(s,b))

    def test_partial_and_wrong_footprint_rejected(self):
        s,b=fixture();b['import_coverage']['source_components']=2
        with self.assertRaises(ValueError):data.build(s,b,bind(s,b))
        s,b=fixture();binding=bind(s,b);binding['footprint_map']['R1']['snapshot']='wrong'
        with self.assertRaises(ValueError):data.build(s,b,binding)

    def test_pagination_net_filter_and_lossless_visual_detail(self):
        s,b=fixture();result=data.build(s,b,bind(s,b))
        self.assertEqual(data.query(result,net='OUT',limit=1)['total'],1)
        self.assertEqual(data.query(result,net='missing')['total'],0)
        self.assertEqual(data.query(result,offset=1)['items'],[])
        self.assertEqual(data.query(result,section='footprints')['items'][0]['data']['custom_visual'],'preserve')
        with self.assertRaises(ValueError):data.query(result,limit=101)
        self.assertLess(len(io.encoded(data.summary(result))),len(io.encoded(result)))

    def test_delta_includes_geometry_rules_and_foreign_identity(self):
        s,b=fixture();before=data.build(s,b,bind(s,b))
        b['tracks'][0]['w']=.3;b['rules']['clearance']=.3
        after=data.build(s,b,bind(s,b))
        sections={c['section'] for c in data.delta(before,after)['changes']}
        self.assertEqual(sections,{'tracks','rules'})
        binding=bind(s,b);binding['document_id']='other';foreign=data.build(s,b,binding)
        with self.assertRaises(ValueError):data.delta(before,foreign)

    def test_tamper_and_malformed_json(self):
        s,b=fixture();result=data.build(s,b,bind(s,b));result['board']['tracks']=[]
        with self.assertRaises(ValueError):data.validate(result)
        with self.assertRaises(ValueError):io.pairs([('a',1),('a',2)])
        s,b=fixture();b['components'][0]['x']=float('nan')
        with self.assertRaises(ValueError):data.build(s,b,bind(s,b))


class OperationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=WORKDIR,prefix='operation-test-');self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name);self.source=self.folder/'source';self.source.mkdir()
        (self.source/'board.native').write_text('baseline copper',encoding='utf-8')
        (self.source/'reopen.txt').write_text('synthetic reopen evidence',encoding='utf-8')
        self.plan={'project_id':'p','document_id':'d','baseline_id':'A','phase':'G3','closed_file_project':True,
                   'dependencies_complete':True,'native_files':['board.native'],'required_checks':['PAD-GAP'],
                   'reopen_evidence':{'path':'reopen.txt','sha256':io.file_hash(self.source/'reopen.txt')}}
        self.tx=self.folder/'transaction'
        self.before=io.inventory(self.source)

    def begin(self):return ops.begin(self.source,self.tx,self.plan)

    def edited(self):
        self.begin();ops.advance(self.tx,'start')
        (self.tx/'candidate'/'board.native').write_text('edited copper',encoding='utf-8')
        return io.digest(io.inventory(self.tx/'candidate'))

    def failure(self):
        digest=self.edited();ops.advance(self.tx,'fail',expected=digest,reason='synthetic failed batch')

    def report(self,status='PASS',**changes):
        evidence=self.folder/'check.txt';evidence.write_text('synthetic check output',encoding='utf-8')
        report={k:self.plan[k] for k in ('project_id','document_id','baseline_id','phase')}
        report.update(candidate_digest=ops.status(self.tx)['candidate_digest'],checks=[{'id':'PAD-GAP','status':status,
                      'evidence':[{'path':'check.txt','sha256':io.file_hash(evidence)}]}]);report.update(changes)
        path=self.folder/'report.json';io.save(path,report);return path

    def test_accept_never_replaces_original(self):
        digest=self.edited();ops.advance(self.tx,'capture',expected=digest)
        result=ops.advance(self.tx,'decide',report=self.report())
        self.assertEqual(result['state'],'ACCEPTED');self.assertEqual(io.inventory(self.source),self.before)

    def test_archived_evidence_remains_resolvable(self):
        digest=self.edited();ops.advance(self.tx,'capture',expected=digest)
        state=ops.advance(self.tx,'decide',report=self.report())
        report=self.tx/state['verification']['report'];body=io.read(report)
        for item in body['checks'][0]['evidence']:
            self.assertEqual(io.file_hash(report.parent/item['path']),item['sha256'])
        self.assertEqual(ops.advance(self.tx,'status')['state'],'ACCEPTED')

    def test_status_detects_accepted_file_and_evidence_drift(self):
        digest=self.edited();ops.advance(self.tx,'capture',expected=digest)
        state=ops.advance(self.tx,'decide',report=self.report())
        candidate=self.tx/'candidate'/'board.native';original=candidate.read_bytes();candidate.write_text('changed')
        current=ops.advance(self.tx,'status');self.assertEqual(current['state'],'STALE')
        self.assertEqual(current['recorded_state'],'ACCEPTED')
        candidate.write_bytes(original)
        report=self.tx/state['verification']['report'];report.write_text('{}')
        self.assertEqual(ops.advance(self.tx,'status')['current_integrity'],'MISMATCH')

    def test_failed_check_and_recovery_preserve_failed_files(self):
        digest=self.edited();ops.advance(self.tx,'capture',expected=digest)
        self.assertEqual(ops.advance(self.tx,'decide',report=self.report('FAIL'))['state'],'FAILED')
        result=ops.advance(self.tx,'recover');self.assertEqual(result['state'],'RECOVERED')
        self.assertEqual(io.inventory(self.tx/'candidate'),self.before)
        self.assertEqual(io.inventory(self.source),self.before)
        self.assertEqual((self.tx/result['failed_dir']/'board.native').read_text(),'edited copper')

    def test_source_user_change_blocks_recovery(self):
        self.failure();(self.source/'board.native').write_text('user edit')
        with self.assertRaises(ValueError):ops.advance(self.tx,'recover')
        self.assertEqual((self.source/'board.native').read_text(),'user edit')

    def test_candidate_user_change_blocks_recovery(self):
        self.failure();(self.tx/'candidate'/'new.native').write_text('user added file')
        with self.assertRaises(ValueError):ops.advance(self.tx,'recover')
        self.assertEqual(ops.status(self.tx)['state'],'FAILED')

    def test_empty_failed_candidate_can_recover(self):
        self.edited()
        for path in (self.tx/'candidate').iterdir():path.unlink()
        ops.advance(self.tx,'fail',expected=io.digest({}),reason='writer removed all files')
        state=ops.advance(self.tx,'recover')
        self.assertEqual(state['state'],'RECOVERED')
        self.assertEqual(state['candidate_digest'],state['checkpoint_digest'])

    def test_missing_native_file_cannot_be_accepted(self):
        self.edited();(self.tx/'candidate'/'board.native').unlink()
        digest=io.digest(io.inventory(self.tx/'candidate'))
        ops.advance(self.tx,'capture',expected=digest)
        self.assertEqual(ops.advance(self.tx,'decide',report=self.report())['state'],'FAILED')

    def test_changed_plan_blocks_resume(self):
        self.begin();state=ops.status(self.tx);state['plan']['phase']='G4';io.save(self.tx/'state.json',state)
        with self.assertRaises(ValueError):ops.advance(self.tx,'start')

    def test_checkpoint_tamper_blocks_recovery(self):
        self.failure();(self.tx/'checkpoint'/'board.native').write_text('tampered')
        with self.assertRaises(ValueError):ops.advance(self.tx,'recover')

    def test_crash_between_renames_can_resume(self):
        self.failure();original=Path.rename
        def interrupt(path,target):
            result=original(path,target)
            if path.name=='candidate':raise RuntimeError('simulated interruption after first rename')
            return result
        with patch.object(Path,'rename',interrupt),self.assertRaises(RuntimeError):ops.advance(self.tx,'recover')
        self.assertEqual(ops.status(self.tx)['state'],'RECOVERING')
        self.assertEqual(ops.advance(self.tx,'recover')['state'],'RECOVERED')
        self.assertEqual(io.inventory(self.tx/'candidate'),self.before)

    def test_stale_capture_and_report_rejected(self):
        digest=self.edited()
        with self.assertRaises(ValueError):ops.advance(self.tx,'capture',expected='wrong')
        ops.advance(self.tx,'capture',expected=digest)
        with self.assertRaises(ValueError):ops.advance(self.tx,'decide',report=self.report(candidate_digest='stale'))
        with self.assertRaises(ValueError):ops.advance(self.tx,'decide',report=self.report(checks=[]))

    def test_phase_and_evidence_not_replaceable(self):
        digest=self.edited();ops.advance(self.tx,'capture',expected=digest)
        with self.assertRaises(ValueError):ops.advance(self.tx,'decide',report=self.report(phase='G4'))
        report=self.report();(self.folder/'check.txt').write_text('changed evidence')
        with self.assertRaises(ValueError):ops.advance(self.tx,'decide',report=report)

    def test_missing_required_result_and_repeated_start(self):
        self.begin();ops.advance(self.tx,'start')
        with self.assertRaises(ValueError):ops.advance(self.tx,'start')
        with self.assertRaises(ValueError):ops.advance(self.tx,'recover')

    def test_incomplete_or_nested_source_rejected(self):
        self.plan['dependencies_complete']=False
        with self.assertRaises(ValueError):self.begin()
        self.plan['dependencies_complete']=True
        with self.assertRaises(ValueError):ops.begin(self.source,self.source/'nested',self.plan)

    def test_cli_state_survives_process_boundary(self):
        self.begin()
        result=subprocess.run([sys.executable,str(Path(ops.__file__)),'start',str(self.tx)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)['state'],'APPLYING')
        self.assertEqual(ops.status(self.tx)['state'],'APPLYING')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--workdir',type=Path,required=True);args=parser.parse_args()
    WORKDIR=args.workdir.resolve(strict=True)
    unittest.main(argv=[sys.argv[0]],verbosity=2)
