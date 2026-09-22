import copy,json,tempfile,subprocess,sys,unittest
from pathlib import Path
import electrical_calcs as ec
import line_models as lm

ROOT=Path(__file__).resolve().parents[1]
def example():
    return {'id':'line','source':'synthetic stackup','conditions':'uncoated isolated test line',
            'kind':'microstrip','geometry':'isolated_microstrip','soldermask':False,'nearby_coplanar_copper':False,
            'width_mm':1,'height_mm':.5,'copper_mm':.035,'er':4.5}

class LineTests(unittest.TestCase):
    def test_independent_skrf_vectors(self):
        data=json.loads((ROOT/'assets/microstrip-reference.json').read_text())
        for vector in data['vectors']:
            with self.subTest(vector=vector):
                result=lm.microstrip(**{k:vector[k] for k in lm.KEYS})
                self.assertAlmostEqual(result['impedance_ohm'],vector['impedance_ohm'],delta=1e-6)
                self.assertAlmostEqual(result['effective_er'],vector['effective_er'],delta=1e-8)

    def test_scale_invariance_and_monotonicity(self):
        a=lm.microstrip(1,.5,.035,4.5)['impedance_ohm']
        self.assertAlmostEqual(a,lm.microstrip(10,5,.35,4.5)['impedance_ohm'])
        self.assertLess(lm.microstrip(1.2,.5,.035,4.5)['impedance_ohm'],a)
        self.assertGreater(lm.microstrip(1,.6,.035,4.5)['impedance_ohm'],a)
        self.assertLess(lm.microstrip(1,.5,.035,5)['impedance_ohm'],a)

    def test_width_synthesis_roundtrip(self):
        data=example();data.update(kind='microstrip_width',target_ohm=50,width_bounds_mm=[.3,2])
        result=ec.calculate(data)
        self.assertAlmostEqual(result['results']['impedance_ohm'],50,places=9)
        self.assertEqual(result['status'],'CALCULATED')

    def test_no_false_success_outside_domain_or_model(self):
        for key,value in [('er',.99),('width_mm',0),('copper_mm',.2),('height_mm',float('nan')),
                          ('soldermask',True),('nearby_coplanar_copper',True),('geometry','differential')]:
            data=example();data[key]=value
            with self.assertRaises(ValueError):ec.calculate(data)

    def test_tolerances_need_all_ranges(self):
        data=example();data['ranges']={k:[v*.95,v*1.05] for k,v in data.items() if k in lm.KEYS}
        r=ec.calculate(data)['results']
        self.assertLess(r['sampled_corner_min_ohm'],r['impedance_ohm'])
        self.assertGreater(r['sampled_corner_max_ohm'],r['impedance_ohm'])
        del data['ranges']['er']
        with self.assertRaises(ValueError):ec.calculate(data)

    def test_unbracketed_and_invalid_corner_not_hidden(self):
        data=example();data.update(kind='microstrip_width',target_ohm=500,width_bounds_mm=[.3,2])
        with self.assertRaises(ValueError):ec.calculate(data)
        data=example();data['ranges']={k:[v,v] for k,v in data.items() if k in lm.KEYS};data['ranges']['copper_mm']=[.035,.5]
        with self.assertRaises(ValueError):ec.calculate(data)

    def test_i2c_interval_and_bad_fit(self):
        data={'id':'i2c','kind':'i2c_pullup','supply_max_V':3.3,'vol_max_V':.4,'sink_A':.003,
              'bus_capacitance_F':200e-12,'rise_time_max_s':300e-9,'resistance_ohm':1500,'tolerance':.05}
        r=ec.calculate(data)['results'];self.assertAlmostEqual(r['r_min_ohm'],966.6666667,places=4)
        self.assertGreater(r['sink_margin_ohm'],0);self.assertGreater(r['rise_margin_ohm'],0)
        data['resistance_ohm']=4700;self.assertLess(ec.calculate(data)['results']['rise_margin_ohm'],0)

    def test_nonfinite_arithmetic_and_malformed_documents(self):
        with self.assertRaises(ValueError):ec.calculate({'id':'x','kind':'converter','vin_V':1,'vout_V':1e308,'iout_A':1e308,'efficiency':.8})
        for doc in (None,[],{'schema':True,'baseline_id':'A','calculations':[example()]}, {'schema':1,'baseline_id':'A','calculations':[None]}):
            with self.assertRaises(ValueError):ec.run(doc)

    def test_cli_duplicate_keys_rejected(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as folder:
            path=Path(folder)/'bad.json';path.write_text('{"schema":1,"schema":1}')
            result=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/electrical_calcs.py'),'--input',str(path)],capture_output=True)
            self.assertEqual(result.returncode,2)

if __name__=='__main__':unittest.main()
