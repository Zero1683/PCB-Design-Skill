import unittest, copy, tempfile, subprocess, sys, json
from pathlib import Path
from test_data_operations import fixture, bind
import design_data as d
import workflow_io as io
class BudgetTests(unittest.TestCase):
 def page(self,items,offset=0,total=None):return {'digest':'a'*64,'baseline_id':'A','section':'components','total':len(items) if total is None else total,'offset':offset,'items':items,'next_offset':None}
 def test_unicode_limit(self):
  p=self.page([{'id':str(i),'data':'元件'*100}for i in range(10)])
  q=d.bounded_output(p,1024,'items');self.assertLessEqual(len(io.encoded(q))+1,1024);self.assertGreater(q['next_offset'],0);self.assertLess(q['next_offset'],10)
 def test_large_record_explicit_handle(self):
  p=self.page([{'id':'a','data':'大'*10000},{'id':'b','data':4}]);before=copy.deepcopy(p)
  q=d.bounded_output(p,1024,'items');self.assertTrue(q['items'][0]['oversized']);self.assertEqual(q['items'][0]['record_digest'],io.digest(p['items'][0]));self.assertEqual(p,before);self.assertLessEqual(len(io.encoded(q))+1,1024)
 def test_pagination_no_skips(self):
  records=[{'id':str(i),'data':'x'*600} for i in range(12)];offset=0;seen=[]
  while offset is not None:
   p=self.page(records[offset:offset+4],offset,len(records));q=d.bounded_output(p,1024,'items',offset);seen.extend(v['id']for v in q['items']);offset=q['next_offset']
  self.assertEqual(seen,[str(i)for i in range(12)])
 def test_diff_budget(self):
  p={'before':'a','after':'b','total':30,'changes':[{'id':str(i),'data':'z'*500}for i in range(30)],'next_offset':None};q=d.bounded_output(p,1024,'changes');self.assertLessEqual(len(io.encoded(q))+1,1024);self.assertEqual(q['next_offset'],len(q['changes']))
 def test_no_results_and_past_end(self):
  self.assertIsNone(d.bounded_output(self.page([],12,2),1024,'items',12)['next_offset'])
 def test_oversized_metadata_fails_explicitly(self):
  with self.assertRaises(ValueError):d.bounded_output({'data':'x'*2000},1024)
 def test_cli_utf8_bytes_including_newline(self):
  snap,board=fixture();board['footprints']['fp1']['custom_visual']='元件'*10000
  data=d.build(snap,board,bind(snap,board))
  with tempfile.TemporaryDirectory(dir=Path.cwd(),prefix='budget-test-') as td:
   path=Path(td)/'data.json';path.write_bytes(io.encoded(data))
   p=subprocess.run([sys.executable,str(Path(d.__file__)),'query',str(path),'--section','footprints','--max-bytes','1024'],capture_output=True)
   self.assertEqual(p.returncode,0,p.stderr);self.assertLessEqual(len(p.stdout),1024)
   self.assertTrue(json.loads(p.stdout.decode('utf8'))['items'][0]['oversized']);self.assertNotIn(b'\r\n',p.stdout)
 def test_invalid_budget(self):
  for n in [0,True,100,1048577]:
   with self.assertRaises(ValueError):d.bounded_output({},n)
if __name__=='__main__':unittest.main()
