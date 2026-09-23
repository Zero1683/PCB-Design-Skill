"""Run supported offline checks locally; cache exact inputs and return bounded summaries."""
import argparse,collections,json,os,re,subprocess,sys,uuid
from pathlib import Path
import workflow_io as io
from evidence_binding import local

STATE_DIR='.pcb-local'
SCRIPTS=Path(__file__).resolve().parent
ROOT_TOOLS={'intake','mechanical','gates','project-reviews'}
DEFINITIONS={'geometry':('audit_design.py',1,{'clearance_mm'}),
             'compare':('audit_design.py',2,set()),'connectivity':('check_connectivity.py',2,set()),
             'electrical':('electrical_calcs.py',1,set()),'intake':('intake_review.py',0,{'baseline'}),
             'mechanical':('mechanical_envelope.py',0,{'baseline'}),
             'gates':('check_evidence.py',0,{'baseline','through'}),
             'project-reviews':('project_reviews.py',1,{'baseline'})}

def file_input(root,name):
    if not isinstance(name,str) or (Path(name).parts and Path(name).parts[0].casefold()==STATE_DIR):raise ValueError('Managed reports cannot be checker inputs')
    return local(root,name)

def command(root,job):
    if not isinstance(job,dict) or set(job)!={'id','kind','inputs','options'}:raise ValueError('Job needs exact id/kind/inputs/options fields')
    if not isinstance(job['id'],str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',job['id']):raise ValueError('Invalid job ID')
    kind=job['kind']
    if not isinstance(kind,str) or kind not in DEFINITIONS:raise ValueError('Unsupported offline checker')
    script,count,fields=DEFINITIONS[kind]
    if not isinstance(job['inputs'],list) or len(job['inputs'])!=count:raise ValueError('Wrong checker input count')
    files=[str(file_input(root,name)) for name in job['inputs']]
    opt=job['options']
    if not isinstance(opt,dict) or set(opt)!=fields:raise ValueError('Unexpected/missing checker options')
    args=[]
    if kind=='geometry':
        clearance=io.finite(opt['clearance_mm'],'clearance')
        if clearance<0:raise ValueError('Negative clearance')
        args=['geometry',*files,'--clearance-mm',str(clearance)]
    elif kind=='compare':args=['compare',*files]
    elif kind=='connectivity':args=files
    elif kind=='electrical':args=['--input',*files]
    else:
        io.text(opt['baseline'],'baseline')
        if opt['baseline'].startswith('-'):raise ValueError('Invalid baseline argument')
        args=(['check'] if kind=='mechanical' else [])+['--root',str(root),'--baseline',opt['baseline']]
        if kind=='project-reviews': args+=['--plan',job['inputs'][0]]
        if kind=='gates':
            if opt['through'] not in {f'G{i}' for i in range(10)}:raise ValueError('Invalid stage')
            args+=['--through',opt['through'],'--design-gates']
    return [sys.executable,'-B','-X','utf8',str(SCRIPTS/script),*args]

def dependencies(root,job):
    if job['kind'] not in ROOT_TOOLS:return {name:io.file_hash(file_input(root,name)) for name in job['inputs']}
    # Root-based checkers follow hashed references. Include their entire project,
    # excluding only our managed output directory; do not guess dependency closure.
    result={}
    def unreadable(error):raise error
    for base,dirs,files in os.walk(root,followlinks=False,onerror=unreadable):
        if Path(base)==root:dirs[:]=[d for d in dirs if d.casefold()!=STATE_DIR]
        for name in dirs+files:io.no_link(Path(base)/name)
        for name in files:
            path=Path(base)/name;result[path.relative_to(root).as_posix()]=io.file_hash(path)
            if path.suffix.lower()=='.json':
                # Reject indirect references into excluded cache output as well.
                # Otherwise a valid old report could hide a changed source file.
                def inspect(value):
                    if isinstance(value,str):
                        parts=value.replace('\\','/').casefold().split('/')
                        if STATE_DIR in parts:raise ValueError('Project inputs cannot reference managed reports')
                    elif isinstance(value,dict):
                        for item in value.values():inspect(item)
                    elif isinstance(value,list):
                        for item in value:inspect(item)
                try:inspect(io.read(path))
                except ValueError as exc:raise ValueError(f'{path.relative_to(root).as_posix()}: {exc}') from exc
    return result

def tool_revision():
    files=[p for p in SCRIPTS.iterdir() if p.is_file() and p.suffix in ('.py','.mjs','.cjs')]
    files+=list((SCRIPTS.parent/'vendor/pcb-skill-toolkit/scripts').rglob('*.py'))
    files+=list((SCRIPTS.parent/'assets').rglob('*.json'))
    return io.digest({p.relative_to(SCRIPTS.parent).as_posix():io.file_hash(p) for p in sorted(files)})

def execute(root,job,cache,revision,force=False,timeout=120):
    cmd=command(root,job);before=dependencies(root,job)
    key=io.digest({'job':job,'inputs':before,'code':revision,'python':sys.version,'root':str(root)})
    meta=cache/(key+'.json');report=cache/(key+'.stdout');error=cache/(key+'.stderr')
    for p in (meta,report,error):io.no_link(p)
    saved=None
    if not force and meta.exists():
        try:
            candidate=io.read(meta)
            if candidate['key']==key and type(candidate['exit_code']) is int and candidate['exit_code'] in (0,1) and io.file_hash(report)==candidate['stdout_sha256'] and io.file_hash(error)==candidate['stderr_sha256'] and isinstance(io.read(report),dict):saved=candidate
        except (OSError,ValueError,KeyError,TypeError):pass
    if saved is None:
        # Fixed scripts only, no shell, output streams go to disk rather than model context.
        with report.open('wb') as out,error.open('wb') as err:
            try:result=subprocess.run(cmd,cwd=root,stdout=out,stderr=err,timeout=timeout,shell=False)
            except subprocess.TimeoutExpired:
                return {'id':job['id'],'state':'TIMEOUT','cached':False,'report':report.relative_to(root).as_posix(),'exit_code':2}
        code=result.returncode
        try:parsed=io.read(report);valid=isinstance(parsed,dict)
        except (ValueError,OSError):valid=False
        if not valid and code in (0,1):code=2
        if dependencies(root,job)!=before or tool_revision()!=revision:
            return {'id':job['id'],'state':'INPUT_CHANGED','cached':False,'report':report.relative_to(root).as_posix(),'exit_code':2}
        if code in (0,1) and valid:
            io.save(meta,{'key':key,'exit_code':code,'stdout_sha256':io.file_hash(report),'stderr_sha256':io.file_hash(error)})
    else:
        code=saved['exit_code']
        if dependencies(root,job)!=before or tool_revision()!=revision:
            return {'id':job['id'],'state':'INPUT_CHANGED','cached':True,'exit_code':2}
    state=('CALCULATED' if job['kind']=='electrical' else 'CHECK_OK') if code==0 else 'CHECK_FAILED' if code==1 else 'ERROR'
    return {'id':job['id'],'state':state,'cached':saved is not None,'exit_code':code,
            'report':report.relative_to(root).as_posix(),'stderr':error.relative_to(root).as_posix(),
            'report_bytes':report.stat().st_size,'report_sha256':io.file_hash(report)}

def run(root,plan,force=False):
    root=io.no_link(root).resolve(strict=True)
    if not isinstance(plan,dict) or type(plan.get('schema')) is not int or plan['schema']!=1 or set(plan)!={'schema','jobs'}:raise ValueError('Plan needs schema=1 and jobs')
    jobs=plan['jobs']
    if not isinstance(jobs,list) or not 1<=len(jobs)<=64:raise ValueError('Provide 1-64 offline jobs')
    for job in jobs:command(root,job)
    if len({j['id'] for j in jobs})!=len(jobs):raise ValueError('Duplicate job IDs')
    cache=io.no_link(root/STATE_DIR);cache.mkdir(exist_ok=True)
    lock=io.no_link(cache/'run.lock')
    try:
        with lock.open('x') as f:f.write(str(os.getpid()))
    except FileExistsError as exc:
        raise FileExistsError('Another check run owns .pcb-local/run.lock. Wait for it to finish; if it crashed, confirm its process has stopped before removing this lock and retrying.') from exc
    try:
        revision=tool_revision();results=[]
        for job in jobs:
            try:result=execute(root,job,cache,revision,force)
            except (ValueError,TypeError,KeyError,OSError) as exc:
                # Preserve independent check results without ever accepting a failed job.
                detail=io.no_link(cache/(job['id']+'.error.txt'))
                detail.write_text(str(exc),encoding='utf-8')
                result={'id':job['id'],'state':'ERROR','cached':False,'exit_code':2,
                        'stderr':detail.relative_to(root).as_posix()}
            if result['exit_code']!=0:
                result['next_action']=('Read the report/stderr for this job, correct its inputs or reported issue, then rerun. Do not treat this batch as approved.')
            results.append(result)
        summary={'scope':'offline checker execution; no live EDA, web prices or whole-board approval',
                 'jobs':results,'counts':dict(collections.Counter(r['state'] for r in results)),
                 'cached_jobs':sum(r['cached'] for r in results),'report_bytes':sum(r.get('report_bytes',0) for r in results)}
        io.save(cache/'latest.json',summary);return summary
    finally:lock.unlink()

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--plan',required=True)
    p.add_argument('--force',action='store_true');p.add_argument('--offset',type=int,default=0);p.add_argument('--limit',type=int,default=8)
    a=p.parse_args()
    try:
        if a.offset<0 or not 1<=a.limit<=8:raise ValueError('offset >= 0 and limit 1-8 required')
        root=io.no_link(a.root).resolve(strict=True);summary=run(root,io.read(file_input(root,a.plan)),a.force)
        output={k:v for k,v in summary.items() if k!='jobs'};output['total_jobs']=len(summary['jobs'])
        output['jobs']=summary['jobs'][a.offset:a.offset+a.limit]
        output['next_offset']=a.offset+a.limit if a.offset+a.limit<len(summary['jobs']) else None
        output['full_summary']=STATE_DIR+'/latest.json'
        payload=io.encoded(output)
        if len(payload)>8192:raise ValueError('Summary exceeds 8192 bytes; reduce --limit')
        print(payload.decode());return int(any(r['exit_code']!=0 for r in summary['jobs']))
    except (ValueError,TypeError,KeyError,OSError) as exc:p.exit(2,'ERROR: '+str(exc)+'\n')
if __name__=='__main__':raise SystemExit(main())
