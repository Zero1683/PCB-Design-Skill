import csv,tempfile,sys,unittest,argparse
from pathlib import Path
WORKDIR = None
from check_evidence import audit,FIELDS
import workflow_io as io
class GateTests(unittest.TestCase):
 def test_gate_outcomes(self):
  with tempfile.TemporaryDirectory(dir=WORKDIR) as tmp:
   root=Path(tmp)
   from test_evidence_fixture import prepare
   rows=prepare(root)
   ids=[r['id'] for r in rows]
   format_row=next(r for r in rows if r['id']=='SCH-FORMAT')
   def run(items,through='G5'):
    with (root/'CHECKS.csv').open('w',encoding='utf-8',newline='') as f:
     w=csv.DictWriter(f,fieldnames=sorted(FIELDS));w.writeheader();w.writerows(items)
    return audit(root,'A',through,design_gates=True)
   self.assertTrue(run(rows)['records_complete'])
   format_row['actual']='framed-layout';self.assertTrue(run(rows)['records_complete'])
   format_row['actual']='unpartitioned';self.assertFalse(run(rows)['records_complete'])
   format_row['actual']='free-layout'
   for ident in ids:
    self.assertFalse(run([r for r in rows if r['id']!=ident])['records_complete'],ident)
   self.assertTrue(run([r for r in rows if int(r['stage'][1:])<=2],'G2')['records_complete'])
   rows[1]['status']='N_A';rows[1]['limitation']='minor';self.assertFalse(run(rows)['records_complete'])
   rows[1]['status']='PASS';rows[1]['stage']='G9';self.assertFalse(run(rows)['records_complete'])
   rows[1]['stage']='G2';rows[1]['baseline_id']='OLD';self.assertFalse(run(rows)['records_complete'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--workdir',type=Path,required=True)
 WORKDIR=str(p.parse_args().workdir.resolve(strict=True));unittest.main(argv=[sys.argv[0]],verbosity=2)
