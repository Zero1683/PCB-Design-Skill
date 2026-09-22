"""Synthetic test support only. Never use fixture PASS records for a real project."""
import csv
from pathlib import Path
import workflow_io as io
import evidence_binding as eb
import check_evidence as ce


def prepare(root, project='fixture', baseline='A', evidence='evidence.txt'):
    root=Path(root)
    (root/evidence).write_text('Synthetic audit evidence only.',encoding='utf8')
    (root/'native.json').write_text('{"synthetic":true}',encoding='utf8')
    ref=lambda name:{'path':name,'sha256':io.file_hash(root/name)}
    state=eb.snapshot(root,project,['synthetic-document'],baseline,['native.json'])
    io.save(root/'design-baseline.json',state)
    req={'schema':1,'project_id':project,'baseline_id':baseline,'requirements':[{'id':'REQ-1','statement':'Synthetic requirement','source':ref(evidence)}]}
    io.save(root/'requirements.json',req)
    io.save(root/'requirement-checks.json',{'schema':1,'project_id':project,'baseline_id':baseline,'requirements_digest':io.digest(req),'checks':[{'id':'MECHANICAL','requirement_ids':['REQ-1'],'method':'fixture','subjects':['U1'],'status':'PASS','evidence':ref(evidence)}]})
    rows=[];bindings=[]
    for gate in io.read(Path(ce.__file__).resolve().parents[1]/'assets/design-check-registry.json')['checks']:
        if int(gate['stage'][1:])>5:continue
        row=dict.fromkeys(ce.FIELDS,'');row.update(id=gate['id'],stage=gate['stage'],check='synthetic',applicability=gate['applicability'],status='PASS',baseline_id=baseline,method='fixture',conditions='fixture',acceptance='fixture',actual='free-layout' if gate['id']=='SCH-FORMAT' else 'fixture',evidence_path=evidence,checked_at='2026-09-22T00:00:00+00:00')
        rows.append(row)
        bindings.append({'id':row['id'],'status':'PASS','mode':'manual','design_digest':io.digest(state),'checked_at':row['checked_at'],'method':'fixture','reviewer':'synthetic test','finding':'fixture only','basis':'fixture only','inputs':[ref('native.json')],'evidence':[ref(evidence)]})
    io.save(root/'check-bindings.json',{'schema':1,'project_id':project,'baseline_id':baseline,'checks':bindings})
    write_rows(root,rows)
    return rows


def write_rows(root,rows):
    with (Path(root)/'CHECKS.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=sorted(ce.FIELDS));w.writeheader();w.writerows(rows)
