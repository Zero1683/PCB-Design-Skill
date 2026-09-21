"""Scoped layout batch preview, repair evidence and bounded attempt ledger. No EDA writer."""
import argparse
import copy
from pathlib import Path
import workflow_io as io
import schematic_layout as layout
from operation_state import lock


def identity(plan):
    return {k:plan['source'][k] for k in ('project_id','document_id','baseline_id','scope_id')}


def seal(value):
    value['digest']=io.digest(value)
    return value


def valid_report(report):
    if report.get('digest')!=io.digest({k:v for k,v in report.items() if k!='digest'}):
        raise ValueError('Changed report')
    if report.get('kind')!='layout-repair-report':raise ValueError('Wrong report kind')


def preview(plan, fresh, adapter_id='unrecorded'):
    io.text(adapter_id,'adapter revision')
    layout.validate_plan(plan);layout.source_check(fresh)
    if io.digest(fresh)!=plan['source_digest']:raise ValueError('STALE: recapture and replan')
    candidate=copy.deepcopy(fresh)
    candidate['objects']=[copy.deepcopy(m['expected']) for m in plan['moves']]
    candidate['frames']=copy.deepcopy(plan['frames']);candidate['capture_stage']='after-apply'
    # Check the complete target state, not transient positions during a swap.
    checked=layout.verify(plan,candidate)
    if checked['status']!='MATCH':raise ValueError('Full target failed: '+str(checked['failures']))
    return seal({'schema':1,'kind':'layout-batch','identity':identity(plan),
        'plan_digest':plan['digest'],'source_digest':plan['source_digest'],'adapter_id':adapter_id,
        'candidate_digest':io.digest(candidate),'candidate':candidate,
        'moves':[{'id':m['id'],'expected_from':m['from'],'target_anchor':m['to'],
                  'preserve_facts_digest':io.digest(m['expected']['facts'])} for m in plan['moves']],
        'status':'PREFLIGHT_ONLY','execution':'Use supported scoped native operations; read back after apply and reload',
        'scope':'unwired rigid layout target; does not validate intermediate native states or electrical intent'})


def diagnose(plan, observed, attempt_id, adapter_id='unrecorded'):
    io.text(attempt_id,'attempt ID')
    io.text(adapter_id,'adapter revision')
    checked=layout.verify(plan,observed)
    actual={o['id']:o for o in observed['objects']}
    expected={m['id']:m['expected'] for m in plan['moves']}
    issues=[]
    for key in ('project_id','document_id','baseline_id','scope_id','units','axis'):
        if observed.get(key)!=plan['source'].get(key):
            issues.append({'code':'IDENTITY','object_id':None,'field':key,'expected':plan['source'].get(key),
                'actual':observed.get(key),'action':'Select correct native scope; capture again','candidate':None})
    for oid in sorted(set(actual)|set(expected)):
        a,e=actual.get(oid),expected.get(oid)
        if a is None or e is None:
            issues.append({'code':'INVENTORY','object_id':oid,'expected':e,'actual':a,
                'action':'Reconcile native inventory before any movement','candidate':None});continue
        for key in ('facts','anchor','bbox'):
            if a[key]==e[key]:continue
            # Exact difference is evidence; the verifier remains authoritative for tolerance.
            facts_ok=a['facts']==e['facts']
            candidate={'target_anchor':e['anchor'],'require_observed_digest':io.digest(observed)} if key=='anchor' and facts_ok else None
            issues.append({'code':'PROTECTED_FACTS' if key=='facts' else 'GEOMETRY','object_id':oid,
                'field':key,'expected':e[key],'actual':a[key],'candidate':candidate,
                'action':'Investigate pin/library/property mapping; preserve independent intent' if key=='facts'
                else ('Investigate persistence; do not repeat placement' if observed['capture_stage']=='after-reload'
                      else 'Check native units/anchor mapping and rebuild a full candidate')})
    if observed.get('frames')!=plan['frames']:
        issues.append({'code':'ANNOTATIONS','object_id':None,'expected':plan['frames'],'actual':observed.get('frames'),
            'action':'Read mapped native frame/title IDs; repair only affected annotations without duplicating them','candidate':None})
    if checked['status']=='MATCH':issues=[]
    if any(x['code'] in ('IDENTITY','PROTECTED_FACTS','INVENTORY') for x in issues) or observed['capture_stage']=='after-reload':
        for issue in issues:issue['candidate']=None
    return seal({'schema':1,'kind':'layout-repair-report','identity':identity(plan),'attempt_id':attempt_id,
        'plan_digest':plan['digest'],'observed_digest':io.digest(observed),'capture_stage':observed['capture_stage'],'adapter_id':adapter_id,
        'status':checked['status'],'issues':issues,'failed_checks':checked['failures'],
        'failure_signature':io.digest({'stage':observed['capture_stage'],'checks':sorted(checked['failures']),
                                      'issues':[{k:v for k,v in x.items() if k not in ('candidate','action')} for x in issues]}),
        'scope':'repair proposals only; no native edits, causality proof or electrical acceptance'})


def ledger_read(path, ident):
    data=io.read(path) if path.exists() else {'schema':1,'identity':ident,'attempts':[]}
    if data.get('schema')!=1 or data.get('identity')!=ident or not isinstance(data.get('attempts'),list):
        raise ValueError('Ledger scope mismatch')
    ids=set()
    for entry in data['attempts']:
        valid_report(entry)
        if entry['identity']!=ident or entry['attempt_id'] in ids:raise ValueError('Invalid ledger entry')
        ids.add(entry['attempt_id'])
    return data


def decision(data, plan_digest, adapter_id='unrecorded'):
    failed=[]
    for entry in reversed(data['attempts']):
        if entry['status']=='MATCH' and entry['capture_stage']=='after-reload':break
        if entry['status']=='MISMATCH':failed.append(entry)
    if len(failed)>=3:return 'STOP_NO_PROGRESS'
    if len(failed)>=2 and failed[0]['failure_signature']==failed[1]['failure_signature']:
        return 'STOP_REPEATED_FAILURE'
    if any(e['plan_digest']==plan_digest and e['adapter_id']==adapter_id for e in failed):return 'CHANGE_PLAN_OR_ADAPTER'
    return 'ALLOW_PREFLIGHT'


def run(args):
    plan=io.read(args.plan);layout.validate_plan(plan)
    root=io.no_link(Path(args.ledger_dir));root.mkdir(parents=True,exist_ok=True)
    with lock(root):
        path=root/'layout-attempts.json';data=ledger_read(path,identity(plan))
        if args.action=='prepare':
            state=decision(data,plan['digest'],args.adapter_id)
            if state!='ALLOW_PREFLIGHT':return {'status':state,'scope':'No write allowed by this helper; inspect recorded failures'},1
            result=preview(plan,io.read(args.fresh),args.adapter_id);io.save(args.output,result,exclusive=True)
            return {'status':result['status'],'digest':result['digest']},0
        report=diagnose(plan,io.read(args.observed),args.attempt_id,args.adapter_id)
        existing=next((e for e in data['attempts'] if e['attempt_id']==args.attempt_id),None)
        if existing and existing!=report:raise ValueError('Attempt ID already belongs to another observation')
        if not existing:
            data['attempts'].append(report);io.save(path,data)
        # Idempotent recording remains possible if output creation was interrupted.
        output=io.no_link(Path(args.output))
        if output.exists():
            if io.read(output)!=report:raise ValueError('Output already contains another report')
        else:io.save(output,report,exclusive=True)
        return {'status':report['status'],'next':decision(data,plan['digest'],args.adapter_id),'report':str(output)},0 if report['status']=='MATCH' else 1


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='action',required=True)
    for action in ('prepare','record'):
        a=sub.add_parser(action);a.add_argument('--plan',required=True);a.add_argument('--ledger-dir',required=True);a.add_argument('--output',required=True);a.add_argument('--adapter-id',required=True)
        if action=='prepare':a.add_argument('--fresh',required=True)
        else:a.add_argument('--observed',required=True);a.add_argument('--attempt-id',required=True)
    args=p.parse_args()
    try:
        result,code=run(args);print(io.encoded(result).decode());return code
    except (OSError,ValueError,TypeError,KeyError) as e:p.exit(2,'ERROR: '+str(e)+'\n')


if __name__=='__main__':raise SystemExit(main())
