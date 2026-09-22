// Validate exported geometry only. Does not write to an EDA project.
import {readFileSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {checkConstraints} from './design_constraints.mjs';
try {
 const argv=process.argv.slice(2),a={};
 for(let i=0;i<argv.length;i+=2){const k=argv[i];if(!['--snapshot','--constraints','--output'].includes(k)||!argv[i+1]||a[k])throw Error('Use --snapshot file --constraints file --output new-report.json');a[k]=argv[i+1];}
 for(const k of ['--snapshot','--constraints','--output'])if(!a[k])throw Error('Missing '+k);
 const raw=readFileSync(a['--snapshot']),rules=readFileSync(a['--constraints']);
 const parse=b=>JSON.parse(b.toString('utf8').replace(/^\uFEFF/,''));
 const snapshot=parse(raw),contract=parse(rules),hash=b=>createHash('sha256').update(b).digest('hex');
 if(snapshot.baseline_id!==contract.baseline_id)throw Error('Snapshot and constraints baseline mismatch');
 const {baseline_id: snapshotBaseline,...snapshotGeometry}=snapshot,{baseline_id: contractBaseline,...contractGeometry}=contract;
 const result={...checkConstraints(snapshotGeometry,contractGeometry),baseline_id:snapshot.baseline_id,project_id:snapshot.projectId,document_id:snapshot.documentId,snapshotSha256:hash(raw),constraintsSha256:hash(rules),source_inputs:[{role:'snapshot',sha256:hash(raw)},{role:'constraints',sha256:hash(rules)}],scope:'provided geometry only; no native execution or electrical acceptance'};
 writeFileSync(a['--output'],JSON.stringify(result,null,2)+'\n',{flag:'wx'});
 console.log(JSON.stringify({state:result.state,checked:result.checked,violations:result.violations.length,report:resolve(a['--output'])}));if(result.state!=='PASS')process.exitCode=1;
}catch(e){console.error(e.message);process.exitCode=2;}
