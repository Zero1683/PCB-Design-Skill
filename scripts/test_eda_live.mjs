import assert from 'node:assert/strict';
import test from 'node:test';
import {liveRuntime} from './eda_live_runtime.mjs';
function fixture() {
 delete globalThis.__pcbSkillLive16;
 const fields='PrimitiveId ComponentType X Y Rotation Mirror AddIntoBom AddIntoPcb Component Symbol Footprint Designator Name UniqueId SubPartName Manufacturer ManufacturerId Supplier SupplierId OtherProperty Net'.split(' ');
 const parts=['a','b'].map((id,i)=>Object.fromEntries(fields.map(k=>[k,k==='PrimitiveId'?id:k==='ComponentType'?'part':k==='X'?i*100:k==='Y'?0:k==='OtherProperty'?{Value:'10k'}:k==='SupplierId'?'C123':null])));
 let count=0;const hooks={};
 const obj=p=>Object.assign(Object.fromEntries(fields.map(k=>['getState_'+k,()=>p[k]])),{getAllPins:async()=>[]});
 const eda={dmt_SelectControl:{getCurrentDocumentInfo:async()=>({uuid:'doc',parentProjectUuid:'project',documentType:1,tabId:'tab'})},sch_PrimitiveComponent:{getAll:async()=>parts.map(obj),modify:async(id,v)=>{count++;if(hooks.modify)await hooks.modify(count,parts);const p=parts.find(p=>p.PrimitiveId===id);for(const [k,val]of Object.entries(v))p[k[0].toUpperCase()+k.slice(1)]=val;return obj(p);}},sch_PrimitiveAttribute:{getAll:async()=>[]},sch_Primitive:{getPrimitivesBBox:async([id])=>{const p=parts.find(p=>p.PrimitiveId===id);return {minX:p.X-5,minY:p.Y-5,maxX:p.X+5,maxY:p.Y+5};}},sch_Document:{save:async()=>true},dmt_EditorControl:{closeDocument:async()=>true,openDocument:async()=>{if(hooks.reopen)hooks.reopen(parts);return 'tab';}}};
 for(const kind of ['Arc','Circle','Polygon','Rectangle','Text','Object','Pin','Wire','Bus'])eda['sch_Primitive'+kind]={getAll:async()=>[]};
 const run=(action,extra={})=>liveRuntime(eda,{action,projectId:'project',documentId:'doc',operationId:'op',...extra});
 const plan=async()=>({source:(await run('capture')).snapshot,moves:[{id:'a',x:0,y:40},{id:'b',x:100,y:40}],bounds:[-20,-20,150,100],gap:5});
 return {eda,parts,hooks,run,plan,count:()=>count};
}
test('apply, native property preservation, save/reopen and persisted inverse',async()=>{const f=fixture(),p=await f.plan();assert.equal((await f.run('apply',p)).state,'APPLIED');assert.equal(f.parts[0].SupplierId,'C123');assert.deepEqual(f.parts[0].OtherProperty,{Value:'10k'});assert.equal((await f.run('reopen')).state,'RELOADED_MATCH');const r=await f.run('rollback');assert.equal(r.state,'ROLLED_BACK');assert.equal(r.restoreSaved,true);assert.deepEqual((await f.run('capture')).snapshot,p.source);});
for(const [name,change] of [['collision',p=>p.moves[0]={id:'a',x:100,y:40}],['bounds',p=>p.moves[0].y=200],['extra mutation',p=>p.moves[0].rotation=90],['stale source',p=>p.source.components[0].props.SupplierId='wrong'],['duplicate',p=>p.moves[1].id='a']])test(name+' rejected without writes',async()=>{const f=fixture(),p=await f.plan();change(p);assert.equal((await f.run('apply',p)).state,'REJECTED');assert.equal(f.count(),0);});
test('wired page rejected',async()=>{const f=fixture();f.eda.sch_PrimitiveWire.getAll=async()=>[{}];assert.equal((await f.run('apply',await f.plan())).state,'REJECTED');assert.equal(f.count(),0);});
test('second write failure compensates first',async()=>{const f=fixture(),p=await f.plan();f.hooks.modify=n=>{if(n===2)throw Error('injected native failure');};const r=await f.run('apply',p);assert.equal(r.state,'ROLLED_BACK');assert.match(r.error,/injected/);assert.deepEqual((await f.run('capture')).snapshot,p.source);});
test('unexpected concurrent edit blocks compensation',async()=>{const f=fixture(),p=await f.plan();f.hooks.modify=(n,parts)=>{if(n===2){parts[0].SupplierId='external';throw Error('failure');}};assert.equal((await f.run('apply',p)).state,'RECOVERY_BLOCKED');assert.equal(f.parts[0].SupplierId,'external');});
test('inverse failure is not reported as restored',async()=>{const f=fixture();await f.run('apply',await f.plan());f.hooks.modify=()=>{throw Error('inverse rejected');};assert.equal((await f.run('rollback')).state,'RECOVERY_BLOCKED');});
test('idempotent operation does not write twice',async()=>{const f=fixture(),p=await f.plan();await f.run('apply',p);await f.run('apply',p);assert.equal(f.count(),2);await assert.rejects(()=>f.run('apply',{...p,gap:8}),/REUSED/);});
test('wrong document never writes',async()=>{const f=fixture(),p=await f.plan();f.eda.dmt_SelectControl.getCurrentDocumentInfo=async()=>({documentType:1,uuid:'other',parentProjectUuid:'project'});assert.equal((await f.run('apply',p)).state,'REJECTED');assert.equal(f.count(),0);});
test('reload mismatch retained',async()=>{const f=fixture();await f.run('apply',await f.plan());f.hooks.reopen=p=>p[0].X++;assert.equal((await f.run('reopen')).state,'RELOAD_MISMATCH');});
test('serialized function works without module scope',async()=>{const f=fixture();const remote=new Function('return ('+liveRuntime.toString()+')')();assert.equal((await remote(f.eda,{action:'capture',projectId:'project',documentId:'doc'})).state,'CAPTURED');});
