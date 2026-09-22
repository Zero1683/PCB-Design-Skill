// Run the same Python intake checker used at release, before a guarded live write.
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';

// Narrow existing-page maintenance binds the exact batch. It grants no design gate.
export function checkMaintenance(record, expected, authorizationBytes) {
  const keys=['schema','kind','project_id','document_id','source_sha256','moves_sha256','constraints_sha256','authorization','purpose'];
  if(!record||Object.keys(record).sort().join()!==keys.sort().join()||record.schema!==1||record.kind!=='scoped-schematic-maintenance')throw Error('Invalid maintenance scope');
  if(typeof record.purpose!=='string'||!record.purpose.trim())throw Error('Maintenance purpose required');
  for(const key of ['project_id','document_id','source_sha256','moves_sha256','constraints_sha256']) {
    if(typeof expected[key]!=='string'||!expected[key]||record[key]!==expected[key])throw Error('Maintenance scope mismatch: '+key);
  }
  const a=record.authorization;
  if(!a||Object.keys(a).sort().join()!=='path,sha256'||typeof a.path!=='string'||!a.path.trim()||!(/^[a-f0-9]{64}$/).test(a.sha256??''))throw Error('Authorization reference required');
  if(!authorizationBytes?.length||createHash('sha256').update(authorizationBytes).digest('hex')!==a.sha256)throw Error('Authorization evidence changed');
  return {state:'MAINTENANCE_SCOPE_RECORDED',detailed_design_allowed:false,
    user_intent_authenticity:'REQUIRES_CONVERSATION_REVIEW',intake_digest:createHash('sha256').update(JSON.stringify(record)).digest('hex')};
}

export function checkIntake({root, baseline, project, python}, runner=spawnSync) {
  for(const [key,value] of Object.entries({root,baseline,project,python})) {
    if(typeof value!=='string'||!value.trim())throw Error('Live apply requires intake '+key);
  }
  const script=fileURLToPath(new URL('./intake_review.py',import.meta.url));
  const reply=runner(python,['-B','-X','utf8',script,'--root',root,'--baseline',baseline],
    {encoding:'utf8',timeout:30000,maxBuffer:1024*1024,windowsHide:true,shell:false});
  if(reply.error||reply.status!==0)throw Error('Intake check failed: '+(reply.error?.message??reply.stderr??reply.stdout??'no output'));
  let report;try{report=JSON.parse(reply.stdout);}catch{throw Error('Invalid intake checker output');}
  if(report.state!=='PLAN_RECORDED'||report.detailed_design_allowed!==true||report.project_id!==project||report.baseline_id!==baseline||!/^[a-f0-9]{64}$/.test(report.intake_digest??'')) {
    throw Error('Intake is incomplete or belongs to another project/baseline');
  }
  return report;
}
