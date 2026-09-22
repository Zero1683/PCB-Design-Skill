// Typed Gateway client. Does not expose arbitrary JavaScript execution.
import {readFileSync,writeFileSync,renameSync,existsSync,lstatSync,unlinkSync} from 'node:fs';
import {resolve,dirname,relative,isAbsolute} from 'node:path';
import {randomUUID,createHash} from 'node:crypto';
import {checkConstraints} from './design_constraints.mjs';
import {liveRuntime} from './eda_live_runtime.mjs';
import {checkIntake,checkMaintenance} from './intake_guard.mjs';

let lockPath;
const [action,...rest]=process.argv.slice(2),args={};
function noLink(p) {for(let cur=resolve(p);;cur=dirname(cur)){if(existsSync(cur)&&lstatSync(cur).isSymbolicLink())throw Error('Link path refused');if(dirname(cur)===cur)break;}return resolve(p);}
function read(p){return JSON.parse(readFileSync(noLink(p),'utf8'));}
const shaFile=p=>createHash('sha256').update(readFileSync(noLink(p))).digest('hex');
function scopeReview() {
  if(!args['maintenance-scope'])return checkIntake({root:args['intake-root'],baseline:args.baseline,project:args.project,python:args.python});
  if(args['intake-root']||args.baseline||args.python)throw Error('Choose new-design intake or scoped maintenance, not both');
  const file=noLink(args['maintenance-scope']),record=read(file),name=record?.authorization?.path;
  if(typeof name!=='string'||isAbsolute(name)||name.includes(':'))throw Error('Expected local authorization reference');
  const auth=resolve(dirname(file),name),rel=relative(dirname(file),auth);
  if(rel.startsWith('..')||isAbsolute(rel))throw Error('Authorization outside scope directory');
  return checkMaintenance(record,{project_id:args.project,document_id:args.document,
    source_sha256:shaFile(args.source),moves_sha256:shaFile(args.moves),constraints_sha256:shaFile(args.constraints)},readFileSync(noLink(auth)));
}
function save(p,data,exclusive=false) {
  p=noLink(p);const bytes=JSON.stringify(data,null,2)+'\n';
  if(exclusive){writeFileSync(p,bytes,{flag:'wx'});return;}
  const tmp=p+'.'+randomUUID()+'.tmp';writeFileSync(tmp,bytes,{flag:'wx'});renameSync(tmp,p);
}
async function call(port,route,body) {
  const response=await fetch(`http://127.0.0.1:${port}${route}`,{method:body?'POST':'GET',
    headers:body?{'Content-Type':'application/json'}:{},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(60000)});
  if(!response.ok)throw Error('HTTP '+response.status);
  return await response.json();
}
try {
  if(!['capture','apply','status','rollback','reopen','resume'].includes(action))throw Error('Use capture|apply|status|rollback|reopen|resume; see reference 23');
  for(let i=0;i<rest.length;i+=2){if(!rest[i]?.startsWith('--')||!rest[i+1]||args[rest[i].slice(2)])throw Error('Expected unique --key value arguments');args[rest[i].slice(2)]=rest[i+1];}
  if(!args.journal)throw Error('--journal file required');
  for(const key of Object.keys(args))if(!['journal','port','window','project','document','source','moves','constraints','intake-root','baseline','python','maintenance-scope'].includes(key))throw Error('Unknown argument: '+key);
  const candidate=noLink(args.journal)+'.lock';writeFileSync(candidate,String(process.pid),{flag:'wx'});lockPath=candidate;
  let journal,request,target,constraintFile,intakeReport;
  if(['status','rollback','reopen','resume'].includes(action)) {
    journal=read(args.journal);target=journal.target;

    if(createHash('sha256').update(JSON.stringify(journal.request)).digest('hex')!==journal.requestSha256)throw Error('Journal request checksum mismatch');
    request={action,projectId:target.projectId,documentId:target.documentId,operationId:journal.request.operationId};
    if(!request.operationId)throw Error('No operation ID in journal');
  } else {
    if(!/^4962[0-9]$/.test(args.port??'')||!args.window||!args.project||!args.document)throw Error('Explicit port/window/project/document required');
    target={port:Number(args.port),windowId:args.window,projectId:args.project,documentId:args.document};
    request={action,projectId:args.project,documentId:args.document};
    if(action==='apply') {
      intakeReport=scopeReview();
      if(!args.constraints)throw Error('--constraints required for every new live batch');
      const captured=read(args.source),plan=read(args.moves),rawConstraints=readFileSync(noLink(args.constraints));
      const constraints=JSON.parse(rawConstraints.toString('utf8').replace(/^\uFEFF/,''));
      constraintFile={path:noLink(args.constraints),sha256:createHash('sha256').update(rawConstraints).digest('hex')};
      if(captured.state!=='CAPTURED'||captured.target.projectId!==args.project||captured.target.documentId!==args.document||captured.target.windowId!==args.window)throw Error('Capture target mismatch');
      request={...request,operationId:randomUUID(),source:captured.result.snapshot,moves:plan.moves,bounds:plan.bounds,gap:plan.gap,constraints,...(plan.repair===undefined?{}:{repair:plan.repair})};
    }
    journal={schema:1,target,request,state:'PENDING',requestSha256:createHash('sha256').update(JSON.stringify(request)).digest('hex')};
    if(action==='apply')journal.constraintFile=constraintFile;
    if(action==='apply')journal.intakeReview=intakeReport;
    save(args.journal,journal,true);
  }
  if(!Number.isInteger(target.port)||target.port<49620||target.port>49629)throw Error('Invalid local bridge port');
  const health=await call(target.port,'/health');
  if(health.service!=='easyeda-bridge'||!health.edaConnected)throw Error('Selected bridge not connected');
  const windows=await call(target.port,'/eda-windows');
  if(!windows.windows?.some(w=>w.windowId===target.windowId&&w.connected))throw Error('Selected window unavailable');
  if(journal.constraintFile){
    let changed=true;
    try{changed=createHash('sha256').update(readFileSync(noLink(journal.constraintFile.path))).digest('hex')!==journal.constraintFile.sha256;}catch{}
    if(changed&&!['status','resume'].includes(action))throw Error('Constraint file changed/missing; reconcile before mutation');
    if(action==='resume')request.constraintsChanged=changed;
  }
  const body={windowId:target.windowId,code:`return await (${liveRuntime.toString()})(eda,${JSON.stringify(request)},(${checkConstraints.toString()}));`};
  if(action==='apply') {
    const fresh=scopeReview();
    if(fresh.intake_digest!==intakeReport.intake_digest)throw Error('Intake changed during preflight; no live write sent');
  }
  try {
    const reply=await call(target.port,'/execute',body);
    if(reply.success!==true||reply.windowId!==target.windowId)throw Error(reply.error??'Gateway rejected request or window identity');
    journal.result=reply.result;journal.state=reply.result.state;journal.lastAction=action;
    save(args.journal,journal);
    console.log(JSON.stringify({state:journal.state,operationId:request.operationId,journal:resolve(args.journal),error:reply.result.error??null}));
    if(['REJECTED','RECOVERY_BLOCKED','FAILED','RELOAD_MISMATCH','RECONCILIATION_REQUIRED','NOT_FOUND'].includes(journal.state)||reply.result.error)process.exitCode=1;
  } catch(e) {
    journal.state='UNKNOWN';journal.transportError=e.message;journal.lastAction=action;save(args.journal,journal);
    throw Error('Execution uncertain/rejected: '+e.message+'; inspect journal and status before any retry');
  }
} catch(e) {console.error(e.message);process.exitCode=1;} finally {if(lockPath)unlinkSync(lockPath);}
