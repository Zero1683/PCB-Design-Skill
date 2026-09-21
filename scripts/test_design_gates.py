import csv,tempfile,sys,unittest,argparse
from pathlib import Path
WORKDIR = None
from check_evidence import audit,FIELDS
class GateTests(unittest.TestCase):
 def test_gate_outcomes(self):
  with tempfile.TemporaryDirectory(dir=WORKDIR) as tmp:
   root=Path(tmp);(root/'evidence.txt').write_text('fixture')
   ids=['SCH-FORMAT','SCH-PAGE-BOUNDS','SCH-BLOCKS','SCH-TEXT','PCB-PAD-GAP','PCB-SILK-GAP','PCB-SILK-MASK','PART-IDENTITY','ROUTING-READY','RELEASE-FREEZE']
   rows=[]
   for ident in ids:
    r=dict.fromkeys(FIELDS,'');r.update(id=ident,stage='G5' if ident=='RELEASE-FREEZE' else 'G2' if ident.startswith('SCH') or ident=='PART-IDENTITY' else 'G3',check='review',applicability='required',status='PASS',baseline_id='A',method='fixture',conditions='fixture',acceptance='fixture',actual='free-layout' if ident=='SCH-FORMAT' else 'fixture',evidence_path='evidence.txt',checked_at='2026-09-21T00:00:00+00:00');rows.append(r)
   def run(items,through='G5'):
    with (root/'CHECKS.csv').open('w',encoding='utf-8',newline='') as f:
     w=csv.DictWriter(f,fieldnames=sorted(FIELDS));w.writeheader();w.writerows(items)
    return audit(root,'A',through,design_gates=True)
   self.assertTrue(run(rows)['records_complete'])
   rows[0]['actual']='framed-layout';self.assertTrue(run(rows)['records_complete'])
   rows[0]['actual']='unpartitioned';self.assertFalse(run(rows)['records_complete'])
   rows[0]['actual']='free-layout'
   for ident in ids:
    self.assertFalse(run([r for r in rows if r['id']!=ident])['records_complete'],ident)
   self.assertTrue(run([r for r in rows if r['stage']=='G2'],'G2')['records_complete'])
   rows[1]['status']='N_A';rows[1]['limitation']='minor';self.assertFalse(run(rows)['records_complete'])
   rows[1]['status']='PASS';rows[1]['stage']='G9';self.assertFalse(run(rows)['records_complete'])
   rows[1]['stage']='G2';rows[1]['baseline_id']='OLD';self.assertFalse(run(rows)['records_complete'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--workdir',type=Path,required=True)
 WORKDIR=str(p.parse_args().workdir.resolve(strict=True));unittest.main(argv=[sys.argv[0]],verbosity=2)
