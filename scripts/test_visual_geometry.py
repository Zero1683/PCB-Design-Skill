import copy
import unittest
from screen_visual_geometry import screen


class VisualGeometryTests(unittest.TestCase):
    def pcb(self):
        return dict(schema=1, kind='pcb', unit='mm', baseline_id='A', source='fixture',
                    coverage='complete', missing=[],
                    limits={'pad-pad': .15, 'silk-silk': .2, 'mask-silk': .2}, objects=[
                        dict(id='p1', kind='pad', layers=['top','bottom'], bbox=[0,0,1,1], net='GND'),
                        dict(id='p2', kind='pad', layers=['top'], bbox=[2,0,3,1], net='GND'),
                        dict(id='s1', kind='silk', layers=['top'], bbox=[0,2,1,3]),
                        dict(id='s2', kind='silk', layers=['top'], bbox=[2,2,3,3]),
                        dict(id='m1', kind='mask', layers=['top'], bbox=[0,0,1,1])])

    def test_clear_and_no_acceptance_claim(self):
        r=screen(self.pcb()); self.assertTrue(r['screen_clear']); self.assertEqual(r['engineering_acceptance'],'NOT_ASSESSED')

    def test_same_net_touching_pads(self):
        d=self.pcb();d['objects'][1]['bbox']=[1,0,2,1]
        self.assertEqual(screen(d)['suspects'][0]['rule'],'pad-pad')

    def test_through_hole_bottom_collision(self):
        d=self.pcb(); d['objects'][1].update(layers=['bottom'],bbox=[.5,0,1.5,1])
        self.assertFalse(screen(d)['screen_clear'])

    def test_separate_layers(self):
        d=self.pcb();d['objects'][0]['layers']=['top'];d['objects'][1].update(layers=['bottom'],bbox=[0,0,1,1])
        self.assertTrue(screen(d)['screen_clear'])

    def test_silk_and_mask_gaps(self):
        d=self.pcb();d['objects'][3]['bbox']=[1.1,2,2,3];d['objects'][4]['bbox']=[0,1.85,1,1.9]
        self.assertEqual({s['rule'] for s in screen(d)['suspects']},{'silk-silk','mask-silk'})

    def test_page_attributes_and_title_block(self):
        d=dict(schema=1,kind='schematic',unit='sheet',baseline_id='A',source='fixture',coverage='complete',missing=[],usable=[0,0,100,100],reserved=[[60,0,100,20]],objects=[dict(id='pin-attribute',kind='text',bbox=[-1,30,5,40]),dict(id='label',kind='text',bbox=[70,10,80,25])])
        self.assertEqual({s['reason'] for s in screen(d)['suspects']},{'outside-usable-page','reserved-area'})

    def test_missing_and_partial_fail(self):
        for field,value in [('coverage','partial'),('missing',['R1 body'])]:
            d=self.pcb();d[field]=value;self.assertFalse(screen(d)['screen_clear'])
        d=self.pcb();d['objects']=d['objects'][:2];self.assertFalse(screen(d)['screen_clear'])

    def test_bad_input_rejected(self):
        base=self.pcb()
        variants=[None,[],{**base,'objects':[]},{**base,'unit':'mil'}]
        for val in [0,-.1,float('nan')]:
            d=copy.deepcopy(base);d['limits']['pad-pad']=val;variants.append(d)
        d=copy.deepcopy(base);d['objects'][1]['id']='p1';variants.append(d)
        d=copy.deepcopy(base);d['objects'][0]['bbox']=[0,0,float('inf'),1];variants.append(d)
        for d in variants:
            with self.subTest(d=d), self.assertRaises(ValueError):screen(d)


if __name__=='__main__':unittest.main(verbosity=2)
