#!/usr/bin/env python3
"""Checkpointed operations on isolated, closed-file native project copies; no live EDA writes."""
import argparse
import copy
from contextlib import contextmanager
import os
from pathlib import Path
import shutil
import sys
import time
import uuid

import workflow_io as io


@contextmanager
def lock(root):
    path=io.no_link(Path(root)/'.operation.lock')
    with path.open('a+b') as stream:
        stream.seek(0,2)
        if stream.tell()==0:stream.write(b'0');stream.flush()
        stream.seek(0)
        if os.name=='nt':
            import msvcrt
            try:msvcrt.locking(stream.fileno(),msvcrt.LK_NBLCK,1)
            except OSError:raise ValueError('Another operation owns this transaction') from None
        else:
            import fcntl
            try:fcntl.flock(stream.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
            except OSError:raise ValueError('Another operation owns this transaction') from None
        try:yield
        finally:
            stream.seek(0)
            if os.name=='nt':msvcrt.locking(stream.fileno(),msvcrt.LK_UNLCK,1)
            else:fcntl.flock(stream.fileno(),fcntl.LOCK_UN)


def event(state, status, reason):
    state['state']=status
    state['history'].append({'state':status,'time_unix':time.time(),'reason':reason})


def exact(root, wanted):
    if io.inventory(root,allow_empty=not wanted)!=wanted:raise ValueError('Workspace changed or checkpoint damaged: '+str(root))


def status(root):
    state=io.read(Path(root)/'state.json')
    if state.get('schema')!=1 or state.get('mode')!='isolated-closed-file-project':raise ValueError('Unsupported transaction')
    if state.get('plan_digest')!=io.digest(state['plan']) or state.get('checkpoint_digest')!=io.digest(state['checkpoint']):
        raise ValueError('Transaction plan or checkpoint record changed')
    validate_plan(state['plan'],state['checkpoint'])
    return state


def validate_plan(plan, files):
    for key in ('project_id','document_id','baseline_id','phase'):io.text(plan.get(key),key)
    if plan['phase'] not in ('G2-A','G2-B','G3','G4','G5'):raise ValueError('Explicit design phase required')
    if plan.get('closed_file_project') is not True or plan.get('dependencies_complete') is not True:
        raise ValueError('Only complete, closed-file native projects are supported')
    required=plan.get('required_checks')
    if (not isinstance(required,list) or not required or any(not isinstance(v,str) or not v.strip() for v in required)
        or len(set(required))!=len(required)):raise ValueError('Declare unique required phase check IDs before editing')
    native=plan.get('native_files')
    if not isinstance(native,list) or not native or any(not isinstance(v,str) or v not in files for v in native):
        raise ValueError('Native project files must exist in the checkpoint')
    evidence=plan.get('reopen_evidence',{})
    if not isinstance(evidence,dict) or evidence.get('path') not in files or files[evidence['path']]['sha256']!=evidence.get('sha256'):
        raise ValueError('Provide hashed evidence of native reopen/dependency review inside the source bundle')


def begin(source, root, plan):
    source=io.no_link(source).resolve(strict=True);root=io.no_link(root)
    if root.exists():raise ValueError('Transaction directory already exists')
    if source==root or source in root.parents or root in source.parents:raise ValueError('Transaction must be outside the source tree')
    before=io.inventory(source);validate_plan(plan,before)
    root.mkdir(parents=True)
    # On an interrupted copy, leave a non-runnable incomplete directory for inspection.
    shutil.copytree(source,root/'checkpoint')
    shutil.copytree(root/'checkpoint',root/'candidate')
    exact(source,before);exact(root/'checkpoint',before);exact(root/'candidate',before)
    state={'schema':1,'mode':'isolated-closed-file-project','operation_id':uuid.uuid4().hex,
           'source':str(source),'plan':plan,'plan_digest':io.digest(plan),'checkpoint':before,'checkpoint_digest':io.digest(before),'history':[]}
    event(state,'PREPARED','Complete file checkpoint copied and hashed; native evidence supplied by caller')
    io.save(root/'state.json',state,exclusive=True)
    return state


def record_report(root, state, report_path):
    report_path=io.no_link(report_path).resolve(strict=True);report=io.read(report_path)
    for key in ('project_id','document_id','baseline_id','phase'):
        if report.get(key)!=state['plan'][key]:raise ValueError('Report identity/phase mismatch: '+key)
    if report.get('candidate_digest')!=state['candidate_digest']:raise ValueError('Report belongs to another candidate')
    checks=report.get('checks')
    if not isinstance(checks,list):raise ValueError('Missing check results')
    seen=set(); evidence=[]; passed=True
    for check in checks:
        key=io.text(check.get('id'),'check ID')
        if key in seen:raise ValueError('Duplicate check ID')
        seen.add(key)
        if check.get('status') not in ('PASS','FAIL','NOT_RUN','BLOCKED'):raise ValueError('Invalid check status')
        entries=check.get('evidence')
        if not isinstance(entries,list) or not entries:raise ValueError('Each result requires evidence')
        for item in entries:
            name=io.text(item.get('path'),'evidence path')
            rel=Path(name)
            if rel.is_absolute() or '..' in rel.parts or ':' in name:raise ValueError('Evidence must be inside report directory')
            path=io.no_link(report_path.parent/rel).resolve(strict=True)
            if not path.is_file() or report_path.parent not in path.parents:raise ValueError('Invalid evidence file')
            if io.file_hash(path)!=item.get('sha256'):raise ValueError('Evidence hash mismatch')
            evidence.append((item,path,item['sha256']))
        # Explicit failures always prevent acceptance; pending optional checks remain reported.
        if check['status']=='FAIL' or (key in state['plan']['required_checks'] and check['status']!='PASS'):passed=False
    if not set(state['plan']['required_checks'])<=seen:raise ValueError('Missing required phase check results')
    bundle=root/('evidence-'+uuid.uuid4().hex);bundle.mkdir()
    original=copy.deepcopy(report)
    for index,(item,path,expected_hash) in enumerate(evidence):
        archived_name='files/'+str(index)+'-'+path.name
        target=bundle/archived_name;target.parent.mkdir(exist_ok=True);shutil.copy2(path,target)
        if io.file_hash(target)!=expected_hash or io.file_hash(path)!=expected_hash:raise ValueError('Evidence changed during copy')
        item['path']=archived_name
    io.save(bundle/'original-report.json',original,exclusive=True)
    io.save(bundle/'report.json',report,exclusive=True)
    state['verification']={'report':str((bundle/'report.json').relative_to(root)),
                           'digest':io.digest(report),'files':io.inventory(bundle),
                           'scope':'caller-reported phase checks; not independent electrical approval'}
    return passed


def advance(root, action, expected=None, report=None, reason=None):
    root=io.no_link(root).resolve(strict=True)
    with lock(root):
        state=status(root)
        if action=='status':
            result=copy.deepcopy(state);result['recorded_state']=state['state']
            try:
                exact(Path(state['source']),state['checkpoint']);exact(root/'checkpoint',state['checkpoint'])
                expected=state.get('candidate_files',state['checkpoint'])
                if state['state'] not in ('APPLYING','RECOVERING'):exact(root/'candidate',expected)
                if 'verification' in state:
                    exact(root/Path(state['verification']['report']).parent,state['verification']['files'])
                result['current_integrity']='MATCH' if state['state'] not in ('APPLYING','RECOVERING') else 'UNFROZEN'
            except (ValueError,OSError) as error:
                result['state']='STALE';result['current_integrity']='MISMATCH';result['integrity_issue']=str(error)
            return result
        exact(Path(state['source']),state['checkpoint'])
        exact(root/'checkpoint',state['checkpoint'])
        if action=='start':
            if state['state']!='PREPARED':raise ValueError('start requires PREPARED')
            exact(root/'candidate',state['checkpoint']);event(state,'APPLYING','Edit only candidate; source remains unchanged')
        elif action in ('capture','fail'):
            if state['state'] not in ('APPLYING','VERIFYING'):raise ValueError('No active operation')
            current=io.inventory(root/'candidate',allow_empty=True)
            if io.digest(current)!=expected:raise ValueError('Candidate changed since observation')
            exact(root/'candidate',current)
            state['candidate_files']=current;state['candidate_digest']=expected
            if action=='capture':event(state,'VERIFYING','Writer stopped; candidate content frozen for scoped checks')
            else:event(state,'FAILED',io.text(reason,'failure reason'))
        elif action=='decide':
            if state['state']!='VERIFYING':raise ValueError('decide requires VERIFYING')
            exact(root/'candidate',state['candidate_files'])
            passed=record_report(root,state,report)
            if not set(state['plan']['native_files'])<=state['candidate_files'].keys():passed=False
            exact(root/'candidate',state['candidate_files'])
            event(state,'ACCEPTED' if passed else 'FAILED','Recorded phase checks; original project not replaced')
        elif action=='recover':
            if state['state']=='FAILED':
                exact(root/'candidate',state['candidate_files'])
                name='restore-'+uuid.uuid4().hex;shutil.copytree(root/'checkpoint',root/name)
                exact(root/name,state['checkpoint'])
                state['restore_dir']=name;state['failed_dir']='failed-'+uuid.uuid4().hex
                event(state,'RECOVERING','Validated checkpoint ready for isolated candidate replacement')
                io.save(root/'state.json',state)
            if state['state']!='RECOVERING':raise ValueError('recover requires FAILED or RECOVERING')
            for key,prefix in (('restore_dir','restore-'),('failed_dir','failed-')):
                value=state[key]
                if not isinstance(value,str) or not value.startswith(prefix) or len(value)!=len(prefix)+32 or any(c not in '0123456789abcdef' for c in value[len(prefix):]):
                    raise ValueError('Invalid recovery journal path')
            candidate=root/'candidate';restore=root/state['restore_dir'];failed=root/state['failed_dir']
            if failed.exists():
                exact(failed,state['candidate_files'])
            else:
                exact(candidate,state['candidate_files']);exact(restore,state['checkpoint'])
                candidate.rename(failed)
            if not candidate.exists():
                exact(restore,state['checkpoint']);restore.rename(candidate)
            exact(candidate,state['checkpoint']);exact(Path(state['source']),state['checkpoint'])
            state['failed_candidate_digest']=state['candidate_digest']
            state['candidate_digest']=state['checkpoint_digest'];state['candidate_files']=state['checkpoint']
            event(state,'RECOVERED','Candidate restored; failed copy preserved; original source unchanged')
        else:raise ValueError('Unknown operation')
        io.save(root/'state.json',state)
        return state


def compact(state):
    return {k:state[k] for k in ('operation_id','state','checkpoint_digest','plan')} | {
        'candidate_digest':state.get('candidate_digest'),'scope':'isolated files only; live EDA untouched',
        'recorded_state':state.get('recorded_state',state['state']),
        'current_integrity':state.get('current_integrity','CHECKED_DURING_OPERATION'),
        'next':'Start a new transaction after changing the plan; do not replay the same failed batch' if state['state']=='RECOVERED' else None}


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    b=sub.add_parser('begin');b.add_argument('--source',type=Path,required=True);b.add_argument('--plan',type=Path,required=True);b.add_argument('--output',type=Path,required=True)
    h=sub.add_parser('hash');h.add_argument('directory',type=Path)
    for action in ('status','start','capture','fail','decide','recover'):
        p=sub.add_parser(action);p.add_argument('transaction',type=Path)
        if action in ('capture','fail'):p.add_argument('--expected-digest',required=True)
        if action=='fail':p.add_argument('--reason',required=True)
        if action=='decide':p.add_argument('--report',type=Path,required=True)
        if action in ('capture','fail','recover'):p.add_argument('--writer-stopped',action='store_true',required=True)
    args=parser.parse_args()
    try:
        if args.action=='hash':result={'digest':io.digest(io.inventory(args.directory,allow_empty=True))}
        elif args.action=='begin':result=compact(begin(args.source,args.output,io.read(args.plan)))
        else:result=compact(advance(args.transaction,args.action,getattr(args,'expected_digest',None),getattr(args,'report',None),getattr(args,'reason',None)))
        print(io.encoded(result).decode())
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'ERROR: '+str(error)+'\n')


if __name__=='__main__':main()
