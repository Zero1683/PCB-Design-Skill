import copy,tempfile,unittest
from pathlib import Path
import calculator_observation as co
import workflow_io as io

class ObservationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=Path.cwd());self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        (self.root/'capture.txt').write_text('Synthetic browser observation only',encoding='utf8')
        self.req={'schema':1,'baseline_id':'A','calculator_url':'https://example.com/calculator','model':'test',
                  'inputs':{'W':{'value':.2,'unit':'mm'},'layer':{'value':'top','unit':'text'}},'outputs':{'impedance':'ohm'}}
        self.obs={'schema':1,'baseline_id':'A','calculator_url':self.req['calculator_url'],'model':'test',
                  'request_digest':io.digest(self.req),'displayed_inputs':copy.deepcopy(self.req['inputs']),
                  'observed_at':'2026-09-22T00:00:00Z','state':'computed','warnings':[],
                  'results':{'impedance':{'value':50,'unit':'ohm'}},
                  'evidence':{'path':'capture.txt','sha256':io.file_hash(self.root/'capture.txt')}}
    def review(self):return co.evaluate(self.root,self.req,self.obs)
    def test_valid_result_is_not_engineering_pass(self):
        self.assertEqual(self.review()['state'],'OBSERVATION_MATCHED')
        self.assertNotEqual(self.review()['engineering_acceptance'],'PASS')
    def test_wrong_unit_value_url_model_or_stale_result(self):
        original=copy.deepcopy(self.obs)
        for key,value in [('calculator_url','https://example.com/other'),('model','other'),('request_digest','0'*64),('state','loading')]:
            self.obs=copy.deepcopy(original);self.obs[key]=value
            with self.assertRaises(ValueError):self.review()
        self.obs=original;self.obs['displayed_inputs']['W']['unit']='mil'
        with self.assertRaises(ValueError):self.review()
    def test_nonfinite_empty_and_changed_capture(self):
        for value in ({}, {'x':{'value':float('nan'),'unit':'ohm'}}, {'x':{'value':True,'unit':'ohm'}}):
            self.obs['results']=value
            with self.assertRaises(ValueError):self.review()
        self.setUp();(self.root/'capture.txt').write_text('Changed')
        with self.assertRaises(ValueError):self.review()
    def test_warnings_are_retained(self):
        self.obs['warnings']=['Outside advertised process range']
        self.assertEqual(self.review()['warnings'],self.obs['warnings'])
    def test_wrong_result_unit_or_error_text_cannot_pass(self):
        self.obs['results']['impedance']['unit']='mm'
        with self.assertRaises(ValueError):self.review()
        self.obs['results']['impedance']={'value':'calculation failed','unit':'ohm'}
        with self.assertRaises(ValueError):self.review()

if __name__=='__main__':unittest.main()
