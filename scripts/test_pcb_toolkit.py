"""Regression tests for the adapted PCB toolkit; no EDA connection required."""
from pathlib import Path
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'vendor/pcb-skill-toolkit/scripts'
sys.path[:0] = [str(KIT / p) for p in ('placement', 'verify', 'routing', 'notify')] + [str(KIT)]
import boardmodel as BM
import netlist_assert as NET
import gerber as GERBER
import route_supervise as ROUTE


class Assertions(unittest.TestCase):
    def setUp(self):
        self.board = BM.Board(BM.synthetic_board())

    def test_unresolved_references_fail(self):
        for rules in (
            {'must_not_connect': [['NOSUCH.1', 'J1.1']]},
            {'must_be_open': ['TYPO_NET']},
            {'must_connect': [['TYPO_NET', 'J1.1']]},
            {'must_connect': [['NOSUCH.1', 'J1.1']]},
            {'must_be_open': ['NOSUCH.1']},
        ):
            with self.subTest(rules=rules):
                results = NET.evaluate(self.board, rules)
                self.assertTrue(results)
                self.assertFalse(all(r[2] for r in results))

    def test_invalid_contract_rejected(self):
        for rules in ({}, [], {'must_connect': []}, {'must_conect': [['J1.1','J1.2']]},
                      {'must_connect': [['J1.1']]}, {'must_connect': [['J1.1','J1.1']]},
                      {'must_be_open': [None]}, {'must_be_open': 'J1.1'},
                      {'must_not_connect': [['J1.1', 2]]}):
            with self.subTest(rules=rules), self.assertRaises(ValueError):
                NET.evaluate(self.board, rules)

    def test_valid_negative_assertions_still_pass(self):
        results = NET.evaluate(self.board, {'must_not_connect': [['J1.1', 'J1.2']],
                                            'must_be_open': ['J1.1']})
        self.assertTrue(all(r[2] for r in results))

    def test_unknown_plane_net_rejected(self):
        with self.assertRaises(ValueError):
            NET.evaluate(self.board, {'must_be_open': ['J1.1']}, ['TYPO_NET'])


class GerberSemantics(unittest.TestCase):
    def test_dark_polarity_supported(self):
        src = GERBER._SYNTH_GERBER.replace('%MOMM*%', '%MOMM*%\n%LPD*%')
        self.assertEqual(len(GERBER.parse_gerber(src).flashes), 4)

    def test_unsupported_semantics_rejected(self):
        for cmd in ('LPC', 'IPNEG', 'MIA1B0', 'OFA1B0', 'SFA2B2', 'ASAYBX', 'SRX2Y2I1J1'):
            with self.subTest(cmd=cmd), self.assertRaises(ValueError):
                GERBER.parse_gerber(GERBER._SYNTH_GERBER.replace('%MOMM*%', '%MOMM*%\n%'+cmd+'*%'))


    def test_unmodeled_apertures_rejected(self):
        valid='4,1,4,-0.5,-0.5,0.5,-0.5,0.5,0.5,-0.5,0.5,-0.5,-0.5,0.0'
        for macro in ([valid.replace('4,1,4','4,0,4')], [valid,valid],
                      ['1,1,1,0,0'], [valid[:-3]+'90'], []):
            with self.subTest(macro=macro),self.assertRaises(ValueError):
                GERBER._macro_outline(macro)
        with self.assertRaises(ValueError):
            GERBER.parse_gerber(GERBER._SYNTH_GERBER.replace('C,0.200000','C,0.200000X0.1'))


class RouteFreshness(unittest.TestCase):
    def test_stale_and_unbound_output_not_done(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)/'old.ses'; p.write_text('(session old)')
            os.utime(p, (100, 100))
            for start in (None, 200):
                with self.subTest(start=start):
                    state, detail = ROUTE.check_once(output=str(p), started=start)
                    self.assertNotEqual(state, ROUTE.STATE_OUTPUT)
                    self.assertIn('note', detail)

    def test_fresh_stable_output_is_candidate(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)/'new.ses'; p.write_text('(session new)')
            now=time.time(); os.utime(p,(now-10,now-10))
            state, detail = ROUTE.check_once(output=str(p),started=now-20)
            self.assertEqual(state,ROUTE.STATE_OUTPUT)
            self.assertEqual(detail['coverage'],'fresh-stable-output-only')

    def test_stale_output_does_not_hide_crash(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'old.ses';p.write_text('old');os.utime(p,(100,100))
            log=Path(td)/'run.log';log.write_text('java.lang.StackOverflowError')
            state,_=ROUTE.check_once(output=str(p),log=str(log),started=200)
            self.assertEqual(state,ROUTE.STATE_CRASH)

    def test_growing_output_does_not_hide_crash(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'new.ses';p.write_text('growing')
            log=Path(td)/'run.log';log.write_text('java.lang.StackOverflowError')
            state,_=ROUTE.check_once(output=str(p),log=str(log),started=time.time()-10,
                                     _sizes={str(p):1})
            self.assertEqual(state,ROUTE.STATE_CRASH)

    def test_cli_once_is_not_success_while_running(self):
        with tempfile.TemporaryDirectory() as td:
            proc=subprocess.run([sys.executable,str(KIT/'routing/route_supervise.py'),
                                 '--output',str(Path(td)/'missing.ses'),'--once'],
                                capture_output=True,text=True)
            self.assertNotEqual(proc.returncode,0,proc.stdout)


class ProcessProbe(unittest.TestCase):
    def test_live_child_is_not_killed(self):
        from process_status import pid_alive
        flags = subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
        child = subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'],
                                 creationflags=flags)
        try:
            with patch('os.kill',side_effect=AssertionError('must not signal on Windows')) if os.name=='nt' else patch('time.monotonic',wraps=time.monotonic):
                self.assertTrue(pid_alive(child.pid))
                self.assertIsNone(child.poll())
            child.terminate(); child.wait(timeout=10)
            self.assertFalse(pid_alive(child.pid))
        finally:
            if child.poll() is None: child.terminate(); child.wait(timeout=10)

    def test_reject_invalid_pids(self):
        from process_status import pid_alive
        for pid in (0,-1,True,'abc'):
            with self.subTest(pid=pid),self.assertRaises(ValueError): pid_alive(pid)

    def test_both_watchers_use_safe_probe(self):
        import process_status, progress_relay
        self.assertIs(ROUTE.pid_alive,process_status.pid_alive)
        self.assertIs(progress_relay.pid_alive,process_status.pid_alive)


class ImportCoverage(unittest.TestCase):
    def test_missing_footprint_does_not_disappear(self):
        import import_easyeda as IMP
        with patch.object(IMP,'_walk',return_value=iter(['fixture'])), \
             patch.object(IMP,'detect_dialect',return_value='record'), \
             patch.object(IMP,'read_record_docs',return_value=[({'docType':'PCB'},[])]), \
             patch.object(IMP,'_pcb_from_record',return_value=(
                 {'c1':{'x':0,'y':0}}, {'c1':{'Designator':'U1','Footprint':'absent'}},
                 {}, [], [], [], [[0,0],[10,0],[10,10],[0,10]])):
            with self.assertRaises(ValueError): IMP.convert(['fixture'],verbose=False)

    def test_multiple_boards_not_silently_overwritten(self):
        import import_easyeda as IMP
        with patch.object(IMP,'_walk',return_value=iter(['fixture'])), \
             patch.object(IMP,'detect_dialect',return_value='record'), \
             patch.object(IMP,'read_record_docs',return_value=[({'docType':'PCB'},[])]*2), \
             patch.object(IMP,'_pcb_from_record',return_value=({}, {}, {}, [], [], [], None)):
            with self.assertRaises(ValueError): IMP.convert(['fixture'],verbose=False)


class Dispatch(unittest.TestCase):
    def test_supported_tool_has_real_entrypoint(self):
        import pcb_toolkit as CLI
        self.assertTrue(all((CLI.ROOT/p).is_file() for p in CLI.TOOLS.values()))

    def test_import_requires_project_configuration(self):
        import pcb_toolkit as CLI
        with self.assertRaises(ValueError): CLI.preflight('import',['out.json','in.epcb'])

    def test_bad_rules_and_layer_map_rejected(self):
        import pcb_toolkit as CLI
        with tempfile.TemporaryDirectory() as td:
            rules=dict(BM.DEFAULT_RULES,min_courtyard_gap=0.25)
            layers=dict(BM.DEFAULT_LAYERS)
            rp=Path(td)/'rules.json'; lp=Path(td)/'layers.json'
            def check():
                rp.write_text(json.dumps(rules));lp.write_text(json.dumps(layers))
                CLI.preflight('import',['out.json','in.epcb','--rules',str(rp),'--layers',str(lp)])
            check()
            rules['min_courtyard_gap']=0
            with self.assertRaises(ValueError):check()
            rules['min_courtyard_gap']=0.25;layers['solid_planes']=[999]
            with self.assertRaises(ValueError):check()

    def test_cli_error_and_valid_selftest_exit_codes(self):
        cli=ROOT/'scripts/pcb_toolkit.py'
        for args,expected in [(['import','out.json','in.epcb'],2),(['nets','--selftest'],0)]:
            proc=subprocess.run([sys.executable,str(cli),*args],capture_output=True,text=True)
            self.assertEqual(proc.returncode,expected,proc.stdout+proc.stderr)

if __name__=='__main__': unittest.main()
