"""Synthetic planner and persisted-readback contract tests; no live EDA."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import schematic_layout as layout


def fixture():
    source={'schema':1,'phase':'G2-A','role':'observed','units':'raw-0.01inch','axis':'y-up',
            'project_id':'p','document_id':'d','baseline_id':'rev1','scope_id':'new-blocks',
            'complete_scope':True,'wire_count':0,'bus_count':0,'objects':[]}
    for i in range(3):
        source['objects'].append({'id':str(i),'bbox':[0,0,20,20],'anchor':[10,10],
            'facts':{'designator':'R'+str(i),'device_id':'device','footprint_id':'fp','rotation':0,
                     'pins':{'1':None,'2':None},'value':'10k'}})
    spec={'format':'framed-layout','usable_rect':[0,0,100,120],'gap':5,'padding':3,'title_height':8,
          'obstacles':[], 'blocks':[{'id':str(i),'title':'Block '+str(i),'members':[str(i)],'measured_title_width':25} for i in range(3)]}
    return source,spec


def actual(p):
    observed=copy.deepcopy(p['source']);observed['objects']=[copy.deepcopy(m['expected']) for m in p['moves']]
    observed['frames']=copy.deepcopy(p['frames']);observed['capture_stage']='after-reload'
    return observed


class LayoutTests(unittest.TestCase):
    def setUp(self):self.source,self.spec=fixture()

    def test_deterministic_order_and_margins(self):
        p=layout.plan(self.source,self.spec);self.assertEqual(p,layout.plan(self.source,self.spec))
        self.assertEqual([m['id'] for m in p['moves']],['0','1','2'])
        for i,f in enumerate(p['frames']):
            self.assertTrue(all(not layout.overlap(f['bbox'],g['bbox'],5) for g in p['frames'][:i]))
        self.assertEqual(p['frames'][0]['bbox'][3],p['frames'][1]['bbox'][3])
        self.assertLess(p['frames'][2]['bbox'][3],p['frames'][0]['bbox'][1])

    def test_both_formats_and_no_scaling(self):
        for mode in ('free-layout','framed-layout'):
            self.spec['format']=mode;p=layout.plan(self.source,self.spec)
            for m in p['moves']:
                self.assertEqual(m['expected']['bbox'][2]-m['expected']['bbox'][0],20)
                self.assertEqual(m['expected']['facts']['rotation'],0)

    def test_obstacle_avoidance(self):
        self.spec['obstacles']=[[0,80,35,120]]
        p=layout.plan(self.source,self.spec)
        for f in p['frames']:self.assertFalse(layout.overlap(f['bbox'],self.spec['obstacles'][0],5))

    def test_no_fit_does_not_mutate_input(self):
        before=copy.deepcopy(self.source);self.spec['usable_rect']=[0,0,10,10]
        with self.assertRaises(ValueError):layout.plan(self.source,self.spec)
        self.assertEqual(before,self.source)

    def test_missing_duplicate_ownership_and_local_collision(self):
        for case in ('missing','duplicate','collision'):
            spec=copy.deepcopy(self.spec)
            if case=='missing':spec['blocks'].pop()
            elif case=='duplicate':spec['blocks'][1]['members']=['0']
            else:spec['blocks'][0]['members']=['0','1'];spec['blocks'].pop(1)
            with self.assertRaises(ValueError):layout.plan(self.source,spec)

    def test_wired_unknown_units_incomplete_rejected(self):
        for key,val in [('wire_count',1),('bus_count',True),('phase','G2-B'),('units','mm'),('complete_scope',False)]:
            source=copy.deepcopy(self.source);source[key]=val
            with self.assertRaises(ValueError):layout.plan(source,self.spec)

    def test_bad_geometry_or_spacing_rejected(self):
        for key,val in [('gap',0),('padding',-1),('title_height',float('nan')),('format','unframed-random')]:
            spec=copy.deepcopy(self.spec);spec[key]=val
            with self.assertRaises(ValueError):layout.plan(self.source,spec)

    def test_native_readback_matches(self):
        p=layout.plan(self.source,self.spec)
        for stage in ('after-apply','after-reload'):
            a=actual(p);a['capture_stage']=stage
            self.assertEqual(layout.verify(p,a)['status'],'MATCH')

    def test_reload_loss_of_position_value_pin_or_frame(self):
        p=layout.plan(self.source,self.spec)
        for mode in ('position','value','pin','frame','title','extra'):
            a=actual(p)
            if mode=='position':a['objects'][0]['anchor'][0]+=1
            elif mode=='value':a['objects'][0]['facts']['value']='1k'
            elif mode=='pin':a['objects'][0]['facts']['pins']['1']='GND'
            elif mode=='frame':a['frames'].pop()
            elif mode=='title':a['frames'][0]['title']='wrong'
            else:a['objects'].append(copy.deepcopy(a['objects'][0]))
            if mode=='extra':
                with self.assertRaises(ValueError):layout.verify(p,a)
            else:self.assertEqual(layout.verify(p,a)['status'],'MISMATCH')

    def test_identity_scope_and_tolerance(self):
        p=layout.plan(self.source,self.spec);a=actual(p);a['document_id']='other'
        self.assertEqual(layout.verify(p,a)['status'],'MISMATCH')
        with self.assertRaises(ValueError):layout.verify(p,actual(p),100)

    def test_plan_tampering_rejected(self):
        p=layout.plan(self.source,self.spec);p['moves'][0]['to'][0]+=1
        with self.assertRaises(ValueError):layout.verify(p,actual(p))

    def test_native_properties_cannot_hide_outside_facts(self):
        self.source['objects'][0]['mirrored']=False
        with self.assertRaises(ValueError):layout.plan(self.source,self.spec)

    def test_tolerance_cannot_waive_sheet_bounds(self):
        p=layout.plan(self.source,self.spec);a=actual(p)
        a['frames'][0]['bbox'][3]+=0.005
        self.assertEqual(layout.verify(p,a)['status'],'MISMATCH')

    def test_cli_plan_preflight_and_mismatch_exit(self):
        with tempfile.TemporaryDirectory(prefix='layout-test-',dir=WORKDIR) as td:
            root=Path(td)
            for name,value in [('source.json',self.source),('spec.json',self.spec)]:
                (root/name).write_text(json.dumps(value),encoding='utf-8')
            def run(*args):return subprocess.run([sys.executable,layout.__file__,*map(str,args)],capture_output=True,text=True)
            r=run('plan','--source',root/'source.json','--spec',root/'spec.json','--output',root/'plan.json')
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual(run('preflight','--plan',root/'plan.json','--source',root/'source.json').returncode,0)
            self.source['objects'][0]['facts']['value']='changed'
            (root/'source.json').write_text(json.dumps(self.source),encoding='utf-8')
            self.assertEqual(run('preflight','--plan',root/'plan.json','--source',root/'source.json').returncode,2)
            p=json.loads((root/'plan.json').read_text());a=actual(p);a['frames'].pop()
            (root/'actual.json').write_text(json.dumps(a),encoding='utf-8')
            self.assertEqual(run('verify','--plan',root/'plan.json','--observed',root/'actual.json').returncode,1)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--workdir',type=Path,required=True);args=parser.parse_args()
    WORKDIR=args.workdir.resolve(strict=True)
    unittest.main(argv=[sys.argv[0]],verbosity=2)
