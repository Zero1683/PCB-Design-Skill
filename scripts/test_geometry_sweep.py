import math
import random
import unittest
import audit_design as audit


def board(boxes):
    return {'schema':1, 'kind':'pcb', 'baseline_id':'A', 'source':'synthetic fixture', 'coverage':'complete',
            'components':[{'ref':str(i), 'part':'fixture', 'value':'', 'footprint':'test', 'fitted':True,
                           'in_bom':True, 'pins':{'1':'GND'}, 'side':side, 'body_aabb_mm':b,
                           'geometry_source':'synthetic transformed envelope'} for i,(side,b) in enumerate(boxes)]}


def brute(boxes, clearance):
    result=[]
    for i,(side,a) in enumerate(boxes):
        for j in range(i+1,len(boxes)):
            other,b=boxes[j]
            if side!=other: continue
            gap=math.hypot(max(b[0]-a[2],a[0]-b[2],0), max(b[1]-a[3],a[1]-b[3],0))
            overlap=a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]
            if overlap or gap<clearance: result.append({'refs':[str(i),str(j)],'aabb_overlap':overlap,'aabb_gap_mm':gap})
    return result


class SweepTests(unittest.TestCase):
    def test_seeded_random_matches_brute_force(self):
        rng=random.Random(180)
        for _ in range(80):
            boxes=[]
            for i in range(60):
                x,y=rng.uniform(-30,30),rng.uniform(-30,30)
                boxes.append((rng.choice(['top','bottom']),[x,y,x+rng.uniform(.01,12),y+rng.uniform(.01,12)]))
            for gap in (0,.15,2):
                self.assertEqual(audit.geometry(board(boxes),gap)['suspect_pairs'],brute(boxes,gap))

    def test_edges_corners_nested_sides_and_exact_clearance(self):
        boxes=[('top',[0,0,1,1]),('top',[1,0,2,1]),('top',[1,1,2,2]),('top',[.2,.2,.8,.8]),('bottom',[0,0,1,1]),('top',[1.5,0,2.5,1])]
        for gap in (0,.5,.500001):
            self.assertEqual(audit.geometry(board(boxes),gap)['suspect_pairs'],brute(boxes,gap))

    def test_sparse_board_does_not_enumerate_quadratic_pairs(self):
        boxes=[('top',[i*3,0,i*3+1,1]) for i in range(5000)]
        result=audit.geometry(board(boxes),.2)
        self.assertEqual(result['candidate_pairs'],0)
        self.assertEqual(result['checked_components'],5000)

    def test_malformed_box_and_boolean_clearance(self):
        for box in (5,{},[0,0,0,1]):
            with self.assertRaises(ValueError): audit.geometry(board([('top',box)]),.2)
        with self.assertRaises(ValueError): audit.geometry(board([('top',[0,0,1,1])]),True)


if __name__=='__main__': unittest.main()
