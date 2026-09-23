"""Synthetic test support only. Never use fixture PASS records for a real project."""
import csv
from pathlib import Path
import workflow_io as io
import evidence_binding as eb
import check_evidence as ce
import intake_review as intake


def prepare_intake(root, project='fixture', baseline='A', evidence='evidence.txt'):
    data = intake.template(project, baseline)
    ref = {'path': evidence, 'sha256': io.file_hash(root / evidence)}
    for topic in data['topics'].values():
        topic.update(state='confirmed', value='Synthetic user choice only', source=ref)
    proposal = {'topics_digest': io.digest(data['topics']), 'document': ref,
                'choices': {name: 'Synthetic proposed choice' for name in intake.TOPICS},
                'assembly_envelope_mm': {'board_length': 50, 'board_width': 30, 'assembled_height': 12},
                'created_at': '2026-09-22T00:00:00Z'}
    data['proposal'] = proposal
    data['decision'] = {'proposal_digest': io.digest(proposal), 'status': 'accepted',
                        'source': ref, 'recorded_at': '2026-09-22T00:01:00Z'}
    io.save(root/'intake.json', data)
    return data


def prepare(root, project='fixture', baseline='A', evidence='evidence.txt'):
    root=Path(root)
    (root/evidence).write_text('Synthetic audit evidence only.',encoding='utf8')
    (root/'native.json').write_text('{"synthetic":true}',encoding='utf8')
    (root/'outline.GKO').write_text('%FSLAX26Y26*%\n%MOMM*%\n%ADD10C,0.2*%\nD10*\nX0Y0D02*\nX50000000Y0D01*\nX50000000Y30000000D01*\nX0Y30000000D01*\nX0Y0D01*\nM02*\n',encoding='utf8')
    prepare_intake(root, project, baseline, evidence)
    ref=lambda name:{'path':name,'sha256':io.file_hash(root/name)}
    state=eb.snapshot(root,project,['synthetic-document'],baseline,['native.json','outline.GKO'])
    io.save(root/'design-baseline.json',state)
    import mechanical_envelope
    io.save(root/'mechanical-contract.json',mechanical_envelope.derive(root,baseline))
    io.save(root/'mechanical-observation.json',{'schema':1,'project_id':project,'baseline_id':baseline,'units':'mm','coverage':'complete',
        'source':ref('native.json'),'outline':ref('outline.GKO'),'board_bounds_mm':[0,0,50,30],'assembled_height_mm':12})
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
