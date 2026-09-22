import test from 'node:test';
import assert from 'node:assert/strict';
import {checkIntake,checkMaintenance} from './intake_guard.mjs';
import {createHash} from 'node:crypto';
const args={root:'test project',baseline:'A',project:'P',python:'python3'};
const report={state:'PLAN_RECORDED',detailed_design_allowed:true,project_id:'P',baseline_id:'A',intake_digest:'a'.repeat(64)};
const auth=Buffer.from('user permits a bounded test');
const expected={project_id:'P',document_id:'D',source_sha256:'a'.repeat(64),moves_sha256:'b'.repeat(64),constraints_sha256:'c'.repeat(64)};
const maintenance={schema:1,kind:'scoped-schematic-maintenance',...expected,purpose:'reversible test',authorization:{path:'authorization.txt',sha256:createHash('sha256').update(auth).digest('hex')}};
test('maintenance cannot grant new-design acceptance',()=>assert.equal(checkMaintenance(maintenance,expected,auth).detailed_design_allowed,false));
for(const key of Object.keys(expected))test('maintenance binds '+key,()=>assert.throws(()=>checkMaintenance({...maintenance,[key]:'changed'},expected,auth)));
test('maintenance rejects changed authorization',()=>assert.throws(()=>checkMaintenance(maintenance,expected,Buffer.from('other'))));
test('maintenance rejects unspecified extra scope',()=>assert.throws(()=>checkMaintenance({...maintenance,create_parts:true},expected,auth)));
test('valid intake before write, no shell interpolation',()=>{
  let observed;
  assert.equal(checkIntake(args,(...call)=>{observed=call;return {status:0,stdout:JSON.stringify(report)};}).state,'PLAN_RECORDED');
  assert.equal(observed[2].shell,false);assert.ok(observed[1].includes('test project'));
});
for(const key of Object.keys(args))test('missing '+key+' never invokes checker',()=>{
  assert.throws(()=>checkIntake({...args,[key]:''},()=>{assert.fail('must not run');}));
});
for(const [name,value] of [['timeout',{error:Error('timeout')}],['failure',{status:1,stdout:JSON.stringify(report)}],['garbage',{status:0,stdout:'not json'}],['wrong project',{status:0,stdout:JSON.stringify({...report,project_id:'other'})}],['unconfirmed',{status:0,stdout:JSON.stringify({...report,detailed_design_allowed:false})}]]) {
  test(name+' cannot authorize write',()=>assert.throws(()=>checkIntake(args,()=>value)));
}
