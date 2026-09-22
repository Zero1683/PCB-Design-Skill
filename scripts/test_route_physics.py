#!/usr/bin/env python3
"""Physical routing regressions through the public CLI and importer boundaries."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / 'vendor/pcb-skill-toolkit/scripts'
sys.path[:0] = [str(VENDOR/'placement'), str(VENDOR/'routing')]
import boardmodel as BM
import import_easyeda as IE
import route_accept as RA


def board():
    return {'units': 'mm', 'layers': dict(BM.DEFAULT_LAYERS),
            'rules': dict(BM.DEFAULT_RULES),
            'footprints': {'ONE': {'pads': [{'num':'1','x':0,'y':0,'w':1,'h':1}]}},
            'components': [{'des':'P1','footprint':'ONE','x':2,'y':5},
                           {'des':'P2','footprint':'ONE','x':8,'y':5}],
            'pad_nets': {'P1.1':'N','P2.1':'N'}, 'nets': {'N':[['P1','1'],['P2','1']]},
            'tracks': [{'net':'N','layer':1,'x1':2,'y1':5,'x2':8,'y2':5,'w':0.2}], 'vias':[]}


def bridge(plated):
    d=board()
    d['components'][1]['side']='bottom'
    d['footprints']['HOLE']={'pads':[{'num':'1','x':0,'y':0,'w':1.2,'h':1.2,
                                     'hole':{'w':0.6,'h':0.6,'plated':plated}}]}
    d['components'].append({'des':'H1','footprint':'HOLE','x':5,'y':5})
    d['pad_nets']['H1.1']='N'
    d['tracks'][0]['x2']=5
    d['tracks'].append({'net':'N','layer':2,'x1':5,'y1':5,'x2':8,'y2':5,'w':0.2})
    return d


class RoutePhysics(unittest.TestCase):
    def cli(self, d, expected='PASS', options=(), baseline=None):
        with tempfile.TemporaryDirectory(prefix='route-physics-') as tmp:
            root=Path(tmp); src=root/'board.json'; out=root/'result.json'
            src.write_text(json.dumps(d), encoding='utf-8')
            cmd=[sys.executable,'-B',str(ROOT/'scripts/pcb_toolkit.py'),'route-accept',str(src),
                 '--json',str(out),*options]
            if baseline is not None:
                old=root/'baseline.json';old.write_text(json.dumps(baseline),encoding='utf-8')
                cmd += ['--baseline',str(old)]
            result=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',
                                  env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'})
            self.assertTrue(out.exists(),result.stdout+result.stderr)
            report=json.loads(out.read_text(encoding='utf-8'))
            self.assertEqual(report['state'],expected,result.stdout+result.stderr)
            self.assertEqual(result.returncode==0,expected=='PASS',result.stdout+result.stderr)
            self.assertIn('coverage',report)
            return report

    def test_clean_control(self): self.cli(board())
    def test_pth_bridges_layers(self): self.cli(bridge(True))
    def test_npth_cannot_bridge(self): self.cli(bridge(False),'FAIL')
    def test_npth_multilayer_has_separate_nodes(self):
        d=bridge(False);d['footprints']['HOLE']['pads'][0]['layers']=[1,2]
        r=self.cli(d,'FAIL');self.assertEqual(r['split']['N'],2)
    def test_legal_unnetted_npth(self):
        d=board();d['footprints']['ONE']['npth']=[{'x':0,'y':2,'d':0.5}]
        self.cli(d)
    def test_missing_plating(self):
        d=bridge(True);del d['footprints']['HOLE']['pads'][0]['hole']['plated']
        self.cli(d,'NOT_CHECKED')
    def test_string_plating(self):
        d=bridge(True);d['footprints']['HOLE']['pads'][0]['hole']['plated']='false'
        self.cli(d,'NOT_CHECKED')
    def test_zero_hole_is_not_barrel(self):
        d=board();d['footprints']['ONE']['pads'][0]['hole']={'w':0,'h':0}
        self.cli(d)
    def test_empty_has_no_coverage(self): self.cli({},'NOT_CHECKED')
    def test_tracks_only_have_no_pad_coverage(self):
        d=board();d['components']=[];d['pad_nets']={};self.cli(d,'NOT_CHECKED')
    def test_protected_unchanged(self): self.cli(board(),options=['--protected','N'],baseline=board())
    def test_protected_without_baseline(self): self.cli(board(),'NOT_CHECKED',['--protected','N'])
    def test_protected_changed_route(self):
        d=board();d['tracks'][0]['x2']=5;d['tracks'][0]['y2']=7
        d['tracks'].append({'net':'N','layer':1,'x1':5,'y1':7,'x2':8,'y2':5,'w':0.2})
        r=self.cli(d,'FAIL',['--protected','N'],board());self.assertEqual(r['protected_changed'],['N'])
    def test_protected_width(self):
        d=board();d['tracks'][0]['w']=0.3;self.cli(d,'FAIL',['--protected','N'],board())
    def test_protected_layer(self):
        d=board();d['tracks'][0]['layer']=2;self.cli(d,'FAIL',['--protected','N'],board())
    def test_protected_segment_order_direction(self):
        d=board();d['tracks'][0]['x2']=5
        d['tracks'].insert(0,{'net':'N','layer':1,'x1':8,'y1':5,'x2':5,'y2':5,'w':0.2})
        self.cli(d,options=['--protected','N'],baseline=board())
    def test_protected_diagonal_segment_equivalence(self):
        old=board();old['components'][1]['y']=8;old['tracks'][0]['y2']=8
        d=copy.deepcopy(old);d['tracks'][0]['x2']=5;d['tracks'][0]['y2']=6.5
        d['tracks'].append({'net':'N','layer':1,'x1':5,'y1':6.5,'x2':8,'y2':8,'w':0.2})
        self.cli(d,options=['--protected','N'],baseline=old)
    def test_protected_via_change(self):
        old=board();old['vias']=[{'net':'N','x':5,'y':5,'pad':0.5,'drill':0.3}]
        d=copy.deepcopy(old);d['vias'][0]['pad']=0.6
        self.cli(d,'FAIL',['--protected','N'],old)
    def test_protected_pad_change(self):
        d=board();d['footprints']['ONE']['pads'][0]['w']=1.1
        self.cli(d,'FAIL',['--protected','N'],board())
    def test_protected_pad_polygon_edge_topology(self):
        old=board();p=old['footprints']['ONE']['pads'][0]
        p.update(shape='POLYGON',polygon=[[-1,-1],[1,-1],[1,1],[0,0],[-1,1]])
        d=copy.deepcopy(old)
        d['footprints']['ONE']['pads'][0]['polygon']=[[-1,-1],[0,0],[1,-1],[1,1],[-1,1]]
        self.cli(d,'FAIL',['--protected','N'],old)
    def test_protected_polygon_cycle_and_direction_equivalent(self):
        old=board();p=old['footprints']['ONE']['pads'][0]
        p.update(shape='POLYGON',polygon=[[-1,-1],[1,-1],[1,1],[0,0],[-1,1]])
        d=copy.deepcopy(old);pts=d['footprints']['ONE']['pads'][0]['polygon']
        d['footprints']['ONE']['pads'][0]['polygon']=list(reversed(pts[2:]+pts[:2]))
        self.cli(d,options=['--protected','N'],baseline=old)
    def test_protected_pour_unsupported(self):
        d=board();d['pours']=[{'net':'N','layer':1}]
        self.cli(d,'NOT_CHECKED',['--protected','N'],d)
    def test_unknown_net_options(self):
        for flag in ('--protected','--plane-nets','--expect-open'):
            with self.subTest(flag=flag):self.cli(board(),'NOT_CHECKED',[flag,'TYPO'])
    def test_nan_inf_negative_geometry(self):
        for n in (float('nan'),float('inf'),-0.1,0):
            with self.subTest(value=n):
                d=board();d['tracks'][0]['w']=n;self.cli(d,'NOT_CHECKED')
    def test_zero_clearance_cannot_hide_overlapping_nets(self):
        d=board();d['rules']['clearance']=0;d['components'][1]['x']=2
        d['pad_nets']['P2.1']='OTHER'
        self.cli(d,'NOT_CHECKED')
    def test_degenerate_and_self_intersecting_polygon_rejected(self):
        for pts in ([[0,0],[1,0],[2,0]], [[0,0],[2,2],[0,2],[2,0]],
                    [[0,0],[2,0],[2,2],[0,0],[0,2]],
                    [[0,0],[3,0],[0,3],[3,3],[1,1]]):
            with self.subTest(points=pts):
                d=board();d['footprints']['ONE']['pads'][0].update(shape='POLYGON',polygon=pts)
                self.cli(d,'NOT_CHECKED')
    def test_bad_rules_and_weakened_override(self):
        for n in (float('nan'),float('inf'),-1):
            d=board();d['rules']['clearance']=n;self.cli(d,'NOT_CHECKED')
        self.cli(board(),'NOT_CHECKED',['--clearance','0.001'])
    def test_blind_via_does_not_reach_bottom(self):
        d=bridge(True);d['components'].pop();del d['pad_nets']['H1.1']
        d['vias']=[{'net':'N','x':5,'y':5,'pad':0.8,'drill':0.3,'layers':[1,15],'viaType':'BLIND'}]
        self.cli(d,'FAIL')
    def test_explicit_through_via_control(self):
        d=bridge(True);d['components'].pop();del d['pad_nets']['H1.1']
        d['vias']=[{'net':'N','x':5,'y':5,'pad':0.8,'drill':0.3,'start_layer':1,'end_layer':2}]
        self.cli(d)
    def test_unknown_span_rejected(self):
        for fields in ({'viaType':'BLIND'},{'layers':[1,2]},{'start_layer':1},
                       {'viaType':'BOGUS'},{'layers':[1,15],'start_layer':1,'end_layer':2}):
            d=board();d['vias']=[{'net':'N','x':5,'y':5,**fields}]
            self.cli(d,'NOT_CHECKED')
    def test_imported_record_plating_required(self):
        body={'num':'1','centerX':0,'centerY':0,'layerId':12,'hole':{'width':10,'height':10},
              'defaultPad':{'width':20,'height':20,'padType':'RECT'}}
        with self.assertRaisesRegex(ValueError,'plated'):
            IE._fp_from_record({'uuid':'FP'},[({'type':'PAD','id':'p'},body)],BM.DEFAULT_LAYERS,12)
        body['plated']=False
        _,fp=IE._fp_from_record({'uuid':'FP'},[({'type':'PAD','id':'p'},body)],BM.DEFAULT_LAYERS,12)
        self.assertIs(fp['pads'][0]['hole']['plated'],False)
    def test_importer_record_blind_via_rejected(self):
        for typ in ('BLIND',None):
            with self.assertRaisesRegex(ValueError,'span/type'):
                IE._pcb_from_record([({'type':'VIA'},{'viaType':typ})],BM.DEFAULT_LAYERS,12)
    def test_importer_array_unverified_via_rejected(self):
        with self.assertRaisesRegex(ValueError,'array VIA'):
            IE._pcb_from_array([['VIA','v',0,'N',0,0,0,12,20]],BM.DEFAULT_LAYERS,12)
    def test_importer_array_drilled_pad_rejected(self):
        row=['PAD','p',0,'',12,'1',0,0,0,['ROUND',12,12],['RECT',20,20]]
        with self.assertRaisesRegex(ValueError,'drilled array PAD'):
            IE._fp_from_array({'uuid':'FP'},[row],BM.DEFAULT_LAYERS,12)
    def test_importer_negative_hole_rejected(self):
        body={'num':'1','layerId':12,'hole':{'width':-1,'height':0},
              'defaultPad':{'width':20,'height':20,'padType':'RECT'}}
        with self.assertRaisesRegex(ValueError,'hole geometry'):
            IE._fp_from_record({'uuid':'FP'},[({'type':'PAD','id':'p'},body)],BM.DEFAULT_LAYERS,12)
    def test_via_must_have_annular_ring(self):
        d=board();d['vias']=[{'net':'N','x':5,'y':5,'pad':0.3,'drill':0.3}]
        self.cli(d,'NOT_CHECKED')
    def test_blind_span_does_not_reach_unrelated_plane(self):
        d=board();d['layers']['solid_planes']=[16]
        d['vias']=[{'net':'N','x':5,'y':5,'layers':[1,15]},
                   {'net':'N','x':10,'y':5,'layers':[1,15]}]
        self.cli(d,'FAIL',['--plane-nets','N'])
    def test_protected_via_span_changed(self):
        old=board();old['vias']=[{'net':'N','x':5,'y':5,'layers':[1,15,16,2]}]
        d=copy.deepcopy(old);d['vias'][0]['layers']=[1,15]
        self.cli(d,'FAIL',['--protected','N'],old)
    def test_actual_buried_via_layers(self):
        d=board();b=BM.Board(d)
        self.assertEqual(b.via_layers({'type':'BURIED','layers':[15,16]}),(15,16))
    def test_importer_normal_via_control(self):
        body={'viaType':'NORMAL','ruleName':'','centerX':0,'centerY':0,'holeDiameter':12,'viaDiameter':20}
        got=IE._pcb_from_record([({'type':'VIA'},body)],BM.DEFAULT_LAYERS,12)
        self.assertEqual(got[4][0]['layers'],BM.DEFAULT_LAYERS['copper'])


if __name__=='__main__': unittest.main()
