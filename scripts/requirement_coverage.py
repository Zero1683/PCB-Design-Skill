"""Requirement mapping and evidence integrity. Does not certify design correctness."""
import argparse
from pathlib import Path
import workflow_io as io


def evaluate(root, requirements, checks, baseline):
    root=io.no_link(root).resolve(strict=True)
    for doc in (requirements,checks):
        if not isinstance(doc,dict):raise ValueError('Requirement/check document must be an object')
        io.text(doc.get('project_id'),'project ID')
        if doc.get('schema')!=1 or doc.get('baseline_id')!=baseline or not doc.get('project_id'):
            raise ValueError('Requirement/check baseline or schema mismatch')
    if requirements['project_id']!=checks['project_id']:raise ValueError('Cross-project mapping')
    if checks.get('requirements_digest')!=io.digest(requirements):raise ValueError('Requirements changed; rebuild mapping')
    def evidence(item):
        if not isinstance(item,dict) or set(item)!={'path','sha256'}:raise ValueError('Evidence needs path and sha256')
        name=io.text(item['path'],'evidence path');p=io.no_link(root/name)
        if Path(name).is_absolute() or not p.resolve().is_relative_to(root) or not p.is_file() or p.stat().st_size==0:
            raise ValueError('Evidence must be a nonempty project-local file')
        if io.file_hash(p)!=item['sha256']:raise ValueError('Evidence hash mismatch: '+name)
    entries=requirements.get('requirements');records=checks.get('checks')
    if not isinstance(entries,list) or not entries or not isinstance(records,list):raise ValueError('Nonempty requirements and check list required')
    expected={}
    for req in entries:
        if not isinstance(req,dict):raise ValueError('Requirement must be an object')
        ident=io.text(req.get('id'),'requirement ID')
        if ident in expected:raise ValueError('Duplicate requirement ID')
        io.text(req.get('statement'),'requirement statement');evidence(req.get('source'));expected[ident]=req
    matched={key:[] for key in expected};ids=set()
    for check in records:
        if not isinstance(check,dict):raise ValueError('Check must be an object')
        ident=io.text(check.get('id'),'check ID')
        if ident in ids:raise ValueError('Duplicate check ID')
        ids.add(ident)
        targets=check.get('requirement_ids')
        if not isinstance(targets,list) or not targets or any(not isinstance(t,str) for t in targets) or len(set(targets))!=len(targets):raise ValueError('Invalid requirement mapping')
        if set(targets)-set(expected):raise ValueError('Unknown requirement in check')
        state=check.get('status')
        if state not in ('PASS','FAIL','NOT_RUN','BLOCKED'):raise ValueError('Invalid check status')
        io.text(check.get('method'),'check method')
        if not isinstance(check.get('subjects'),list) or not check['subjects'] or any(not isinstance(t,str) or not t.strip() for t in check['subjects']):raise ValueError('Explicit check subjects required')
        if state in ('PASS','FAIL'):evidence(check.get('evidence'))
        for target in targets:matched[target].append(check)
    result=[]
    for ident,records in matched.items():
        state='UNMAPPED' if not records else 'FAILED' if any(c['status']=='FAIL' for c in records) else 'MAPPED_UNVERIFIED' if any(c['status']!='PASS' for c in records) else 'COVERED_WITH_CURRENT_EVIDENCE'
        result.append({'requirement_id':ident,'state':state,'checks':[c['id']for c in records]})
    return {'state':'COVERED_WITH_CURRENT_EVIDENCE' if all(r['state']=='COVERED_WITH_CURRENT_EVIDENCE' for r in result) else 'INCOMPLETE',
            'baseline_id':baseline,'requirements_digest':io.digest(requirements),'results':result,
            'scope':'declared requirements, mappings and evidence integrity only','engineering_correctness':'NOT_ASSESSED',
            'intake_completeness':'REQUIRES_REQUIREMENTS_REVIEW'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--baseline',required=True)
    p.add_argument('--requirements',default='requirements.json');p.add_argument('--checks',default='requirement-checks.json')
    a=p.parse_args()
    try:
        for name in (a.requirements,a.checks):
            if Path(name).is_absolute() or not (a.root/name).resolve().is_relative_to(a.root.resolve()):raise ValueError('Inputs must be project-local')
        result=evaluate(a.root,io.read(a.root/a.requirements),io.read(a.root/a.checks),a.baseline)
        import sys;sys.stdout.buffer.write(io.encoded(result)+b'\n');return 0 if result['state']=='COVERED_WITH_CURRENT_EVIDENCE' else 1
    except (ValueError,KeyError,TypeError,OSError) as exc:p.exit(2,'ERROR: '+str(exc)+'\n')
if __name__=='__main__':raise SystemExit(main())
