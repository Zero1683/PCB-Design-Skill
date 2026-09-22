"""Physical assertion and strict inspection entry regressions."""
import copy
import sys
import unittest
from unittest.mock import patch
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'vendor/pcb-skill-toolkit/scripts'
sys.path[:0]=[str(ROOT/'scripts'),str(KIT/'placement'),str(KIT/'verify')]
import boardmodel as BM
import netlist_assert as N
import pcb_toolkit as ENTRY

def fixture(short=False):
    return {'units':'mm','footprints':{'A':{'pads':[
        {'num':'1','elem':'a','x':6 if short else 20,'y':0,'w':1,'h':1},
        {'num':'1','elem':'b','x':0,'y':0,'w':1,'h':1}]},
        'B':{'pads':[{'num':'1','x':0,'y':0,'w':1,'h':1}]}},
        'components':[{'des':'A','footprint':'A','x':2,'y':5},
                      {'des':'B','footprint':'B','x':8,'y':5}],
        'pad_nets':{'A#a':'N','A#b':'N','B.1':'M' if short else 'N'},
        'nets':{'N':[['A','1']]} if short else {'N':[['A','1'],['B','1']]},
        'tracks':[] if short else [{'net':'N','layer':1,'x1':2,'y1':5,'x2':8,'y2':5,'w':.2}]}

class Assertions(unittest.TestCase):
    def verdict(self,doc,rules): return all(x[2] for x in N.evaluate(BM.Board(doc),rules))
    def test_disconnected_repeated_land_in_both_orders(self):
        d=fixture()
        for _ in range(2):
            self.assertFalse(self.verdict(d,{'must_connect':[['A.1','B.1']]}))
            d['footprints']['A']['pads'].reverse()
    def test_all_repeated_lands_connected(self):
        d=fixture();d['tracks'][0]['x2']=22
        self.assertTrue(self.verdict(d,{'must_connect':[['A.1','B.1']]}))
    def test_negative_assertion_all_lands(self):
        d=fixture(True)
        for _ in range(2):
            self.assertFalse(self.verdict(d,{'must_not_connect':[['A.1','B.1']]}))
            d['footprints']['A']['pads'].reverse()
    def test_open_assertion_all_lands(self):
        self.assertFalse(self.verdict(fixture(True),{'must_be_open':['A.1']}))
    def test_floating_repeated_lands_still_open(self):
        d=fixture();d['tracks']=[]
        self.assertTrue(self.verdict(d,{'must_be_open':['A.1']}))
    def test_same_logical_lands_touching_are_not_foreign_copper(self):
        d=fixture();d['tracks']=[];d['footprints']['A']['pads'][0]['x']=0
        self.assertTrue(self.verdict(d,{'must_be_open':['A.1']}))
    def test_npth_cannot_bridge_but_pth_can(self):
        d=fixture();d['footprints']['A']['pads']= [{'num':'1','x':0,'y':0,'w':1,'h':1,
             'layer':12,'hole':{'w':.3,'h':.3,'plated':False}}]
        d['pad_nets']={'A.1':'N','B.1':'N'}
        d['components'][1].update(x=2,side='bottom');d['tracks']=[]
        self.assertFalse(self.verdict(d,{'must_connect':[['A.1','B.1']]}))
        d['footprints']['A']['pads'][0]['hole']['plated']=True
        self.assertTrue(self.verdict(d,{'must_connect':[['A.1','B.1']]}))
    def test_blind_via_does_not_bridge_to_bottom(self):
        d=fixture();d['footprints']['A']['pads']=[{'num':'1','x':0,'y':0,'w':1,'h':1}]
        d['pad_nets']={'A.1':'N','B.1':'N'};d['tracks']=[]
        d['components'][1].update(x=2,side='bottom')
        d['vias']=[{'x':2,'y':5,'net':'N','pad':.5,'drill':.3,'layers':[1,15]}]
        self.assertFalse(self.verdict(d,{'must_connect':[['A.1','B.1']]}))
        d['vias'][0]['layers']=[1,15,16,2]
        self.assertTrue(self.verdict(d,{'must_connect':[['A.1','B.1']]}))

    def test_plane_assumption_requires_actual_span(self):
        d=fixture(); d['footprints']['A']['pads']=[{'num':'1','x':0,'y':0,'w':1,'h':1}]
        d['pad_nets']={'A.1':'N','B.1':'N'}; d['tracks']=[]
        d['vias']=[{'x':x,'y':5,'net':'N','pad':.5,'drill':.3,'layers':[1,15]} for x in (2,8)]
        d['layers']={'solid_planes':[16]}
        result=N.evaluate(BM.Board(d),{'must_connect':[['A.1','B.1']]},['N'])
        self.assertFalse(result[0][2])
        for v in d['vias']:v['layers']=[1,15,16]
        result=N.evaluate(BM.Board(d),{'must_connect':[['A.1','B.1']]},['N'])
        self.assertTrue(result[0][2])

class Entry(unittest.TestCase):
    def test_child_uses_utf8_without_environment_override(self):
        with patch.object(ENTRY.subprocess,'run') as run:
            run.return_value.returncode=0
            self.assertEqual(ENTRY.main(['nets','a','b']),0)
            self.assertEqual(run.call_args.args[0][1:4],['-B','-X','utf8'])
    def test_valid_cases(self):
        for tool,args in [('route-accept',['a.json','--protected','VCC,GND','--baseline','b.json']),
                          ('mask',['a.GTL','b.GTS','--tol','0','--allow-partial-openings']),
                          ('nets',['a.json','rules.json','--plane-nets','GND'])]:
            ENTRY.preflight(tool,args)
    def test_unknown_and_duplicate_options(self):
        for args in [['a','--protect','N'],['a','--protected','N','--protected','GND']]:
            with self.assertRaises(ValueError): ENTRY.preflight('route-accept',args)
    def test_invalid_numeric_options(self):
        for val in ['nan','inf','-1','0']:
            with self.assertRaises(ValueError):ENTRY.preflight('route-accept',['a','--clearance',val])
        for val in ['nan','inf','-1']:
            with self.assertRaises(ValueError):ENTRY.preflight('mask',['a','b','--tol',val])
    def test_missing_or_duplicate_net_names(self):
        for val in ['', 'N,', ',N', 'N,N', 'N, N']:
            with self.assertRaises(ValueError):ENTRY.preflight('route-accept',['a','--protected',val])
    def test_files_must_precede_options(self):
        with self.assertRaises(ValueError):ENTRY.preflight('mask',['--json','out','a','b'])
    def test_wrong_input_counts_and_missing_values(self):
        for tool,args in [('mask',['a']),('route-accept',['a','b']),('nets',['a','b','--json'])]:
            with self.assertRaises(ValueError):ENTRY.preflight(tool,args)
    def test_selftest_cannot_hide_real_inputs(self):
        ENTRY.preflight('route-accept',['--selftest'])
        with self.assertRaises(ValueError): ENTRY.preflight('route-accept',['a','--selftest'])

if __name__=='__main__':unittest.main()
