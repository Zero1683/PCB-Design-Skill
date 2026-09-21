#!/usr/bin/env python3
"""Behavior tests for calculations, records, normalized exports, and the read-only probe."""
import argparse
import copy
import csv
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import audit_design as design
import check_evidence as evidence
import electrical_calcs as electrical
import init_project

WORKDIR = None
ROOT = Path(__file__).resolve().parents[1]


def snapshot():
    return {'schema':1,'kind':'pcb','baseline_id':'A','source':'test native export','coverage':'complete',
            'components':[{'ref':'R1','part':'P','value':'10k','footprint':'R0603','fitted':True,'in_bom':True,
                           'pins':{'1':'VCC','2':'EN'},'side':'top','body_aabb_mm':[0,0,2,1],
                           'geometry_source':'test transformed outline'}]}


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='pcb-workflow-',dir=WORKDIR)
        self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.example=json.loads((ROOT/'assets/electrical.example.json').read_text(encoding='utf-8'))

    def write_rows(self,rows):
        with (self.root/'CHECKS.csv').open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=sorted(evidence.FIELDS));w.writeheader();w.writerows(rows)

    def passing(self):
        (self.root/'report.txt').write_text('actual test report',encoding='utf-8')
        row={k:'' for k in evidence.FIELDS}
        row.update(id='A',stage='G4',check='routing',applicability='required',status='PASS',baseline_id='A',
                   method='native check',conditions='test',acceptance='zero errors',actual='zero errors',
                   evidence_path='report.txt',checked_at='2026-09-21T00:00:00Z')
        return row

    def test_power_budget_units(self):
        out=electrical.run(self.example)['calculations']
        self.assertAlmostEqual(out[0]['results']['iin_A'],.99/(3*.85))
        self.assertAlmostEqual(out[1]['results']['total_resistance_ohm'],.11851428571428572)
        self.assertAlmostEqual(out[1]['results']['drop_V'],.03555428571428571)
        self.assertAlmostEqual(out[3]['results']['loss_W'],.1705)
        self.assertTrue(all(x['hardware_validation']=='NOT_RUN' for x in out))

    def test_invalid_input_not_numeric_success(self):
        for value in (0,-1,1.1,float('nan'),True):
            bad=copy.deepcopy(self.example);bad['calculations'][0]['efficiency']=value
            with self.subTest(value=value),self.assertRaises(ValueError):electrical.run(bad)

    def test_impossible_transient_budget(self):
        item=copy.deepcopy(self.example['calculations'][2]);item['esr_ohm']=1
        result=electrical.calculate(item)['results']
        self.assertFalse(result['budget_feasible_in_model']);self.assertIsNone(result['ideal_min_effective_capacitance_F'])

    def test_transient_budget_includes_parasitics(self):
        result=electrical.calculate(self.example['calculations'][2])['results']
        self.assertAlmostEqual(result['target_impedance_ohm'],.5)
        self.assertAlmostEqual(result['ideal_min_effective_capacitance_F'],.2*.0001/(.1-.01-.0002))

    def test_g5_does_not_demand_hardware(self):
        row=self.passing();later={**row,'id':'HW','stage':'G8','status':'NOT_RUN'}
        self.write_rows([row,later]);self.assertTrue(evidence.audit(self.root,'A')['records_complete'])
        self.assertFalse(evidence.audit(self.root,'A','G8')['records_complete'])

    def test_fake_pass_without_evidence_rejected(self):
        row=self.passing();row['method']='';row['evidence_path']='absent.txt'
        self.write_rows([row]);result=evidence.audit(self.root,'A')
        self.assertFalse(result['records_complete']);self.assertGreaterEqual(len(result['record_errors']),2)

    def test_old_baseline_is_not_inherited(self):
        self.write_rows([self.passing()]);self.assertFalse(evidence.audit(self.root,'B')['records_complete'])

    def test_accepted_limitation_remains_unpassed(self):
        row=self.passing();row.update(status='ACCEPTED_LIMITATION',limitation='user decision recorded')
        self.write_rows([row]);result=evidence.audit(self.root,'A')
        self.assertFalse(result['records_complete']);self.assertEqual(result['record_errors'],[])

    def test_outside_evidence_and_duplicate_ids(self):
        row=self.passing();row['evidence_path']='../outside.txt';self.write_rows([row,row])
        result=evidence.audit(self.root,'A');self.assertGreaterEqual(len(result['record_errors']),2)

    def test_hardware_identity(self):
        row=self.passing();row.update(stage='G8',board_id='board-A',firmware_id='fw1')
        self.write_rows([row])
        self.assertTrue(evidence.audit(self.root,'A','G8','board-A','fw1')['records_complete'])
        self.assertFalse(evidence.audit(self.root,'A','G8','board-B','fw1')['records_complete'])

    def test_changed_pin_is_reported(self):
        a=snapshot();b=copy.deepcopy(a);b['kind']='schematic';b['components'][0]['pins']['2']='GND'
        result=design.compare(a,b);self.assertFalse(result['records_match'])
        self.assertEqual(result['differences'][0]['field'],'pins')

    def test_bom_quantity_expansion_and_dnp(self):
        a=snapshot();b=copy.deepcopy(a);b['kind']='bom';b['components'][0].pop('pins')
        self.assertTrue(design.compare(a,b)['records_match'])
        b['components'][0]['fitted']=False;self.assertFalse(design.compare(a,b)['records_match'])

    def test_partial_and_empty_exports_rejected(self):
        for change in ({'coverage':'partial'},{'components':[]}):
            with self.assertRaises(ValueError):design.load_snapshot({**snapshot(),**change})

    def test_geometry_overlap_and_missing(self):
        a=snapshot();b=copy.deepcopy(a['components'][0]);b['ref']='R2';b['body_aabb_mm']=[1,0,3,1]
        a['components'].append(b);result=design.geometry(a,.2)
        self.assertEqual(len(result['suspect_pairs']),1)
        b.pop('geometry_source');result=design.geometry(a,.2)
        self.assertEqual(result['missing_geometry'],['R2']);self.assertEqual(result['geometry_acceptance'],'NOT_ASSESSED')

    def test_chinese_records_preserve_states(self):
        target=self.root/'中文';init_project.create_project(target,'测试板','zh')
        self.assertIn('工作范围',(target/'PROJECT.md').read_text(encoding='utf-8'))
        with (target/'CHECKS.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
        self.assertTrue(all(x['status']=='NOT_RUN' for x in rows))
        self.assertIn('SENSOR-IRQ',{x['id'] for x in rows})

    @unittest.skipUnless(shutil.which('node'),'Node is required for probe test')
    def test_probe_success_and_wrapped_failure(self):
        payloads=[];reply={'success':True,'result':{'probe':'pcb-skill-readonly-v1','project':None,'document':None,'capabilities':{}}}
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def answer(self,data):
                body=json.dumps(data).encode();self.send_response(200);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
            def do_GET(self):self.answer({'service':'easyeda-bridge','edaConnected':True})
            def do_POST(self):
                payloads.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))));self.answer(reply)
        server=None
        for port in range(49629,49619,-1):
            try:server=ThreadingHTTPServer(('127.0.0.1',port),Handler);break
            except OSError:continue
        if server is None:self.skipTest('No unused local bridge-test port')
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            command=['node',str(ROOT/'scripts/eda_probe.mjs'),str(port),'test-window']
            out=subprocess.run(command,capture_output=True,text=True,timeout=15)
            self.assertEqual(out.returncode,0,out.stderr);self.assertIsNone(json.loads(out.stdout)['project'])
            self.assertEqual(payloads[0]['windowId'],'test-window')
            reply.clear();reply.update(success=False,error='permission denied')
            out=subprocess.run(command,capture_output=True,text=True,timeout=15)
            self.assertNotEqual(out.returncode,0)
            reply.clear();reply.update(success=True,result=None)
            out=subprocess.run(command,capture_output=True,text=True,timeout=15)
            self.assertNotEqual(out.returncode,0)
        finally:server.shutdown();server.server_close();thread.join()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--workdir',type=Path,required=True)
    WORKDIR=str(parser.parse_args().workdir.resolve(strict=True));unittest.main(argv=['test_workflow.py'],verbosity=2)
