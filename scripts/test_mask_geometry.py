#!/usr/bin/env python3
"""Geometry and public-CLI regression cases; no optional geometry dependency."""
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / 'vendor/pcb-skill-toolkit/scripts/verify'
sys.path.insert(0, str(VERIFY))
import gerber as GB
import mask_check as MC

HEADER = '%FSLAX26Y26*%\n%MOMM*%\n'


def flash(x=2, y=2, aperture='C,0.5', section='Pad'):
    return (HEADER + '%ADD10' + aperture + '*%\nD10*\n' +
            ('G04 '+section+' Start*\n' if section else '') +
            'X%dY%dD03*\nM02*\n' % (round(x*1e6), round(y*1e6)))


def region(points):
    return HEADER + 'G36*\n' + ''.join('X%dY%dD0%d*\n' %
        (round(x*1e6), round(y*1e6), 2 if i == 0 else 1)
        for i, (x, y) in enumerate(points)) + 'G37*\nM02*\n'


class GeometryTests(unittest.TestCase):
    def check(self, p, m, expected):
        self.assertEqual(MC._classify(p, m), expected)

    def test_triangle_bbox_false_positive(self):
        self.check([MC._disk(8,8,.25)], [MC._polygon([(0,0),(10,0),(0,10)])], 'none')

    def test_offset_large_circle(self):
        self.check([MC._disk(2,2,.25)], [MC._disk(2.1,2,1)], 'full')

    def test_offset_partial_circle(self):
        self.check([MC._disk(0,0,1)], [MC._disk(1,0,1)], 'partial')

    def test_circle_tangent_is_not_open(self):
        self.check([MC._disk(0,0,1)], [MC._disk(2,0,1)], 'none')

    def test_internal_tangent_full(self):
        self.check([MC._disk(1,0,1)], [MC._disk(0,0,2)], 'full')

    def test_identical_circle(self):
        self.check([MC._disk(0,0,1)], [MC._disk(0,0,1)], 'full')

    def test_concave_notch(self):
        shape = MC._polygon([(0,0),(4,0),(4,4),(3,4),(3,1),(1,1),(1,4),(0,4)])
        self.check([MC._disk(2,3,.25)], [shape], 'none')

    def test_concave_crosses_pad(self):
        shape = MC._polygon([(0,0),(4,0),(4,4),(3,4),(3,1),(1,1),(1,4),(0,4)])
        self.check([MC._rect(2,2,3,3)], [shape], 'partial')

    def test_two_regions_joint_full(self):
        self.check([MC._rect(0,0,2,2)], [MC._rect(-.5,0,1,2),MC._rect(.5,0,1,2)], 'full')

    def test_two_regions_gap(self):
        self.check([MC._rect(0,0,2,2)], [MC._rect(-.6,0,1,2),MC._rect(.6,0,1,2)], 'partial')

    def test_region_and_flash_union(self):
        self.check([MC._disk(0,0,1)], [MC._rect(-.5,0,1,2),MC._disk(.5,0,1.12)], 'full')

    def test_circle_union_does_not_cover_square_corners(self):
        self.check([MC._rect(0,0,2,2)], [MC._disk(0,0,1)], 'partial')

    def test_boundary_touch_rectangle(self):
        self.check([MC._rect(0,0,2,2)], [MC._rect(2,0,2,2)], 'none')

    def test_mask_inside_pad(self):
        self.check([MC._disk(0,0,1)], [MC._disk(0,0,.5)], 'partial')

    def test_empty_mask(self):
        self.check([MC._disk(0,0,1)], [], 'none')

    def test_polygon_rotation_translation_order(self):
        for angle in (0,.15,.77,math.pi/2,math.pi):
            for shift in ((0,0),(17,-43)):
                def p(x,y):
                    return (x*math.cos(angle)-y*math.sin(angle)+shift[0],
                            x*math.sin(angle)+y*math.cos(angle)+shift[1])
                pad = MC._polygon([p(-1,-1),p(1,-1),p(1,1),p(-1,1)])
                masks = [MC._polygon([p(-2,-2),p(0,-2),p(0,2),p(-2,2)]),
                         MC._polygon([p(0,-2),p(2,-2),p(2,2),p(0,2)])]
                for order in (masks, masks[::-1]):
                    with self.subTest(angle=angle, shift=shift):
                        self.check([pad], order, 'full')

    def test_polygon_reverse_winding(self):
        p = [(0,0),(10,0),(0,10)]
        for points in (p,p[::-1]):
            self.check([MC._disk(2,2,.25)], [MC._polygon(points)], 'full')

    def test_rounded_apertures(self):
        for kind in ('O','RR'):
            ap = GB.Aperture(10,kind,2,1,r=.4)
            parts = MC._flash(GB.Flash(ap,0,0,'Pad'))
            self.check(parts, parts, 'full')
            self.check(parts, [MC._rect(0,0,3,2)], 'full')

    def test_invalid_polygons(self):
        for points in ([(0,0),(1,1),(0,1),(1,0)],[(0,0),(1,0),(2,0)],
                       [(0,0),(1,0),(1,1),(0,0),(0,1)],
                       [(0,0),(2,0),(1,0),(1,1),(0,1)]):
            with self.assertRaises(ValueError): MC._polygon(points)

    def test_circle_distance_oracle(self):
        rng=random.Random(922)
        for _ in range(500):
            r,rr=rng.uniform(.1,4),rng.uniform(.1,4)
            dx,dy=rng.uniform(-5,5),rng.uniform(-5,5)
            distance=math.hypot(dx,dy)
            expected='none' if distance >= r+rr else 'full' if distance+r <= rr else 'partial'
            self.check([MC._disk(0,0,r)],[MC._disk(dx,dy,rr)],expected)

    def test_rectangle_inequality_oracle(self):
        rng=random.Random(923)
        for _ in range(500):
            w,h,ww,hh=[rng.uniform(.1,4) for _ in range(4)]
            dx,dy=rng.uniform(-3,3),rng.uniform(-3,3)
            intersects=abs(dx)<(w+ww)/2 and abs(dy)<(h+hh)/2
            contains=abs(dx)+w/2 <= ww/2 and abs(dy)+h/2 <= hh/2
            expected='none' if not intersects else 'full' if contains else 'partial'
            self.check([MC._rect(0,0,w,h)],[MC._rect(dx,dy,ww,hh)],expected)


class PublicCliTests(unittest.TestCase):
    def run_case(self, copper, mask, expected, *flags):
        with tempfile.TemporaryDirectory(prefix='mask-test-', dir=Path.cwd()) as tmp:
            d = Path(tmp)
            (d/'cu.gtl').write_text(copper,encoding='utf-8')
            (d/'mk.gts').write_text(mask,encoding='utf-8')
            cmd = [sys.executable,'-B',str(ROOT/'scripts/pcb_toolkit.py'),'mask',
                   str(d/'cu.gtl'),str(d/'mk.gts'),'--json',str(d/'out.json'),*flags]
            proc = subprocess.run(cmd,capture_output=True,text=True)
            data = json.loads((d/'out.json').read_text(encoding='utf-8'))
            self.assertEqual(data['state'],expected,proc.stdout+proc.stderr)
            self.assertEqual(proc.returncode == 0,expected == 'PASS',proc.stdout+proc.stderr)
            self.assertIn('coverage',data)
            return data

    def test_public_bbox_regression(self):
        self.run_case(flash(8,8),region([(0,0),(10,0),(0,10),(0,0)]),'FAIL')

    def test_public_offset_regression(self):
        self.run_case(flash(),flash(2.1,2,'C,2'),'PASS')

    def test_public_partial_requires_policy(self):
        self.run_case(flash(),flash(2,2,'C,0.2'),'NOT_CHECKED')

    def test_public_partial_declared_policy(self):
        r = self.run_case(flash(),flash(2,2,'C,0.2'),'PASS','--allow-partial-openings')
        self.assertEqual(r['partial'],1)

    def test_public_empty_copper(self):
        self.run_case(HEADER+'M02*\n',flash(),'NOT_CHECKED')

    def test_public_no_pad_scope(self):
        self.run_case(flash(section='Via'),flash(),'NOT_CHECKED')

    def test_public_empty_mask_fails(self):
        self.run_case(flash(),HEADER+'M02*\n','FAIL')

    def test_public_untagged_requires_assumption(self):
        self.run_case(flash(section=''),flash(),'NOT_CHECKED')

    def test_public_explicit_assumption(self):
        r = self.run_case(flash(section=''),flash(),'PASS','--assume-all-pads')
        self.assertIsNone(r['vias'])

    def test_public_via_regions(self):
        copper = flash().replace('M02*','G04 Via Start*\nX3000000Y2000000D03*\nM02*')
        r = self.run_case(copper,region([(1,1),(4,1),(4,3),(1,3),(1,1)]),'PASS')
        self.assertEqual((r['pads'],r['vias'],r['vias_open']),(1,1,1))

    def test_public_compound_region_not_unioned(self):
        mask = region([(0,0),(5,0),(5,5),(0,5),(0,0)]).replace('G37*',
            'X1000000Y1000000D02*\nX3000000Y1000000D01*\nX3000000Y3000000D01*\nX1000000Y1000000D01*\nG37*')
        self.run_case(flash(),mask,'NOT_CHECKED')

    def test_public_clear_polarity(self):
        self.run_case(flash(),flash().replace('D10*','%LPC*%\nD10*'),'NOT_CHECKED')

    def test_public_arc_region(self):
        mask = region([(0,0),(5,0),(5,5),(0,0)]).replace('X5000000Y0D01*','G02X5000000Y0I2500000J0D01*')
        self.run_case(flash(),mask,'NOT_CHECKED')

    def test_public_aperture_hole(self):
        self.run_case(flash(),flash(aperture='C,2X0.5'),'NOT_CHECKED')

    def test_public_copper_region(self):
        self.run_case(region([(0,0),(3,0),(3,3),(0,0)]),flash(),'NOT_CHECKED')

    def test_public_invalid_tolerances(self):
        for tol in ('NaN','inf','-0.02'):
            with self.subTest(tol=tol):
                # Wrapper may reject invalid flags before child report creation.
                with tempfile.TemporaryDirectory(prefix='mask-test-',dir=Path.cwd()) as tmp:
                    p=Path(tmp)
                    (p/'cu').write_text(flash(),encoding='utf-8')
                    (p/'mk').write_text(flash(),encoding='utf-8')
                    run=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/pcb_toolkit.py'),'mask',
                        str(p/'cu'),str(p/'mk'),'--tol',tol],capture_output=True,text=True)
                    self.assertNotEqual(run.returncode,0)
                    self.assertNotIn('verdict: PASS',run.stdout)

    def test_public_zero_tol(self):
        self.run_case(flash(),flash(),'PASS','--tol','0')

    def test_public_unknown_gcode(self):
        self.run_case(flash(),flash().replace('D10*','G99*\nD10*'),'NOT_CHECKED')

    def test_public_macro_name_invariance_outside(self):
        for name in ('CustomOutline', 'RoundRect'):
            mask = (HEADER + '%AM' + name + '*4,1,3,10,10,11,10,10,11,10,10,0*%\n' +
                    '%ADD10' + name + ',0.2X-1X-1X1X-1X1X1X-1X1*%\n' +
                    'D10*\nX2000000Y2000000D03*\nM02*\n')
            with self.subTest(macro=name):
                self.run_case(flash(),mask,'FAIL')

    def test_public_macro_name_invariance_inside(self):
        for name in ('CustomOutline', 'RoundRect'):
            mask = (HEADER + '%AM' + name + '*4,1,4,-1,-1,1,-1,1,1,-1,1,-1,-1,0*%\n' +
                    '%ADD10' + name + '*%\nD10*\nX2000000Y2000000D03*\nM02*\n')
            with self.subTest(macro=name):
                self.run_case(flash(),mask,'PASS')

    def test_public_roundrect_undefined(self):
        self.run_case(flash(),flash(aperture='RoundRect,0.2X-1X-1X1X-1X1X1X-1X1'),
                      'NOT_CHECKED')

    def test_public_roundrect_unmodeled_macro(self):
        mask=flash(aperture='RoundRect,0.2X-1X-1X1X-1X1X1X-1X1').replace(
            '%ADD10','%AMRoundRect*21,1,2,2,0,0,0*%\n%ADD10')
        self.run_case(flash(),mask,'NOT_CHECKED')

    def test_public_roundrect_parameterized_macro(self):
        mask = (HEADER + '%AMRoundRect*4,1,3,$1,$2,$3,$4,$5,$6,$1,$2,0*%\n' +
                '%ADD10RoundRect,0X0X4X0X0X4*%\nD10*\nX2000000Y2000000D03*\nM02*\n')
        r=self.run_case(flash(),mask,'NOT_CHECKED')
        self.assertIn('independent capable checker',r['reason'])

    def test_public_selftest(self):
        p=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/pcb_toolkit.py'),'mask','--selftest'],
                         capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
