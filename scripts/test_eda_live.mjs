import assert from 'node:assert/strict';
import test from 'node:test';
import {checkConstraints} from './design_constraints.mjs';
import {liveRuntime} from './eda_live_runtime.mjs';
function fixture() {
 delete globalThis.__pcbSkillLive16;
 const fields='PrimitiveId ComponentType X Y Rotation Mirror AddIntoBom AddIntoPcb Component Symbol Footprint Designator Name UniqueId SubPartName Manufacturer ManufacturerId Supplier SupplierId OtherProperty Net'.split(' ');
 const parts=['a','b'].map((id,i)=>Object.fromEntries(fields.map(k=>[k,k==='PrimitiveId'?id:k==='ComponentType'?'part':k==='X'?i*100:k==='Y'?0:k==='Rotation'?0:k==='OtherProperty'?{Value:'10k'}:k==='SupplierId'?'C123':null])));
 let count=0;const hooks={};
 const obj=p=>Object.assign(Object.fromEntries(fields.map(k=>['getState_'+k,()=>p[k]])),{getAllPins:async()=>[]});
 const eda={dmt_SelectControl:{getCurrentDocumentInfo:async()=>({uuid:'doc',parentProjectUuid:'project',documentType:1,tabId:'tab'})},sch_PrimitiveComponent:{getAll:async()=>parts.map(obj),modify:async(id,v)=>{count++;if(hooks.modify)await hooks.modify(count,parts);const p=parts.find(p=>p.PrimitiveId===id);for(const [k,val]of Object.entries(v))p[k[0].toUpperCase()+k.slice(1)]=val;return obj(p);}},sch_PrimitiveAttribute:{getAll:async()=>[]},sch_Primitive:{getPrimitivesBBox:async([id])=>{const p=parts.find(p=>p.PrimitiveId===id);return {minX:p.X-5,minY:p.Y-5,maxX:p.X+5,maxY:p.Y+5};}},sch_Document:{save:async()=>true},dmt_EditorControl:{closeDocument:async()=>true,openDocument:async()=>{if(hooks.reopen)hooks.reopen(parts);return 'tab';}}};
 for(const kind of ['Arc','Circle','Polygon','Rectangle','Text','Object','Pin','Wire','Bus'])eda['sch_Primitive'+kind]={getAll:async()=>[]};
 const run=(action,extra={})=>liveRuntime(eda,{action,projectId:'project',documentId:'doc',operationId:'op',...extra});
 const plan=async()=>({source:(await run('capture')).snapshot,moves:[{id:'a',x:0,y:40},{id:'b',x:100,y:40}],bounds:[-20,-20,150,100],gap:5,constraints:{schema:1,revision:'A',domain:'schematic',projectId:'project',documentId:'doc',units:'raw-0.01inch',axis:'y-up',source:'test fixture',bounds:[-20,-20,150,100],rules:[]}});
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
test('serialized function works without module scope',async()=>{const f=fixture();const remote=new Function('return ('+liveRuntime.toString()+')')();assert.equal((await remote(f.eda,{action:'capture',projectId:'project',documentId:'doc'},checkConstraints)).state,'CAPTURED');});

test('fixed connector rejected before any native write',async()=>{const f=fixture(),p=await f.plan();p.constraints.rules=[{type:'lock',ids:['a'],source:'mechanical drawing',anchor:[0,0],rotation:0,side:'schematic'}];const r=await f.run('apply',p);assert.equal(r.state,'REJECTED');assert.equal(r.constraintReport.violations[0].code,'LOCKED_PLACEMENT');assert.equal(f.count(),0);});
test('missing contract and unknown rule block native writes',async()=>{const f=fixture(),p=await f.plan();delete p.constraints;assert.equal((await f.run('apply',p)).state,'REJECTED');assert.equal(f.count(),0);});
test('resume rereads actual state and performs no writes',async()=>{const f=fixture();await f.run('apply',await f.plan());const count=f.count();assert.equal((await f.run('resume')).state,'RESUME_INSPECTED');f.parts[0].X=20;assert.equal((await f.run('resume')).state,'RECONCILIATION_REQUIRED');assert.equal(f.count(),count);});

test('changed constraints and lost sessions require reconciliation',async()=>{const f=fixture();await f.run('apply',await f.plan());assert.equal((await f.run('resume',{constraintsChanged:true})).state,'RECONCILIATION_REQUIRED');delete globalThis.__pcbSkillLive16;const r=await f.run('resume');assert.equal(r.state,'RECONCILIATION_REQUIRED');assert.equal(r.error,'SESSION_LOST');assert.equal(f.count(),2);});

test('final capture drift cannot report success',async()=>{const f=fixture(),p=await f.plan(),old=f.eda.sch_PrimitiveComponent.getAll;let n=0;f.eda.sch_PrimitiveComponent.getAll=async()=>{if(++n===6)f.parts[0].SupplierId='late-change';return old();};const r=await f.run('apply',p);assert.equal(r.state,'RECOVERY_BLOCKED');assert.equal(r.error,'FINAL_READBACK_MISMATCH');});
function frame(f,extra={}){const props={PrimitiveId:'frame',FillStyle:'None',LineWidth:1,CornerRadius:0,Rotation:0,...extra};f.eda.sch_PrimitiveRectangle.getAll=async()=>[Object.fromEntries(Object.entries(props).map(([k,v])=>['getState_'+k,()=>v]))];const old=f.eda.sch_Primitive.getPrimitivesBBox;f.eda.sch_Primitive.getPrimitivesBBox=async ids=>ids[0]==='frame'?{minX:-20,minY:-20,maxX:150,maxY:100}:old(ids);}
test('unfilled frame permits contained moves',async()=>{const f=fixture();frame(f);assert.equal((await f.run('apply',await f.plan())).state,'APPLIED');});
for(const props of [{FillStyle:'Solid'},{LineWidth:null},{Rotation:45},{CornerRadius:10}])test('unknown or filled frame remains conservative '+JSON.stringify(props),async()=>{const f=fixture();frame(f,props);assert.equal((await f.run('apply',await f.plan())).state,'REJECTED');assert.equal(f.count(),0);});
test('frame border clearance still protected',async()=>{const f=fixture();frame(f);const p=await f.plan();p.moves[0].x=-10;assert.equal((await f.run('apply',p)).state,'REJECTED');assert.equal(f.count(),0);});
function repairPlan(p){p.constraints.bounds=[0,0,150,100];p.bounds=[0,0,150,100];p.moves[0].x=20;p.repair={reason:'Restore page containment',allow:[{code:'BOARD_OR_PAGE_BOUNDS',id:'a'},{code:'BOARD_OR_PAGE_BOUNDS',id:'b'}]};return p;}
test('scoped repair handles invalid source and reaches fully valid target',async()=>{const f=fixture();const r=await f.run('apply',repairPlan(await f.plan()));assert.equal(r.state,'APPLIED');assert.equal(checkConstraints(r.last,r.constraints).state,'PASS');const back=await f.run('rollback');assert.equal(back.state,'ROLLED_BACK');assert.equal(back.restoredConstraintReport.state,'BLOCKED');});
test('repair does not waive target violations or accept undeclared defects',async()=>{for(const mode of ['badtarget','missing','extra']){const f=fixture(),p=repairPlan(await f.plan());if(mode==='badtarget')p.moves[0].x=0;if(mode==='missing')p.repair.allow.pop();if(mode==='extra')p.repair.allow.push({code:'KEEPOUT',id:'a'});assert.equal((await f.run('apply',p)).state,'REJECTED');assert.equal(f.count(),0);}});
test('repair failure restores original defective baseline without claiming valid design',async()=>{const f=fixture(),p=repairPlan(await f.plan());f.hooks.modify=n=>{if(n===2)throw Error('native failure');};const r=await f.run('apply',p);assert.equal(r.state,'ROLLED_BACK');assert.equal(r.restoredConstraintReport.state,'BLOCKED');assert.deepEqual((await f.run('capture')).snapshot,p.source);});

test('native null style plus null color is unfilled, colored null remains blocked',async()=>{for(const color of [null,'#ff0000']){const f=fixture();frame(f,{FillStyle:null,FillColor:color});assert.equal((await f.run('apply',await f.plan())).state,color===null?'APPLIED':'REJECTED');}});

test('swap path is rejected before first write',async()=>{const f=fixture(),p=await f.plan();p.moves=[{id:'a',x:100,y:0},{id:'b',x:0,y:0}];const out=await f.run('apply',p);assert.equal(out.state,'REJECTED');assert.match(out.error,/COLLISION/);assert.equal(f.count(),0);});
test('scoped repair cannot introduce an intermediate collision',async()=>{const f=fixture();f.parts.forEach(p=>p.Y=40);const p=await f.plan();p.constraints.bounds=[0,0,150,100];p.bounds=[0,0,150,100];p.moves=[{id:'a',x:100,y:40},{id:'b',x:20,y:40}];p.repair={reason:'fix a',allow:[{code:'BOARD_OR_PAGE_BOUNDS',id:'a'}]};assert.equal((await f.run('apply',p)).state,'REJECTED');assert.equal(f.count(),0);});
test('actual clearance is enforced below readback equivalence tolerance',async()=>{const f=fixture(),p=await f.plan(),old=f.eda.sch_Primitive.getPrimitivesBBox;p.moves=[{id:'a',x:85,y:0}];f.eda.sch_Primitive.getPrimitivesBBox=async ids=>{const b=await old(ids);if(ids[0]==='a'&&f.parts[0].X===85)b.maxX+=0.0005;return b;};const out=await f.run('apply',p);assert.equal(out.state,'ROLLED_BACK');assert.match(out.error,/COLLISION/);});
test('operation replay detects external edits without writing',async()=>{const f=fixture(),p=await f.plan();await f.run('apply',p);f.parts[0].X=1000;assert.equal((await f.run('apply',p)).state,'RECONCILIATION_REQUIRED');assert.equal(f.count(),2);});
test('operation replay checks current document',async()=>{const f=fixture(),p=await f.plan();await f.run('apply',p);f.eda.dmt_SelectControl.getCurrentDocumentInfo=async()=>({documentType:1,uuid:'other',parentProjectUuid:'project'});await assert.rejects(()=>f.run('apply',p),/TARGET_CHANGED/);assert.equal(f.count(),2);});

// Bbox changes below equivalent() tolerance must still pass both independent checks.
for(const action of ['apply','replay','resume','reopen'])for(const defect of ['clearance','contract'])test(action+' rejects actual '+defect+' drift within bbox tolerance',async()=>{
 const f=fixture(),p=await f.plan();p.moves=[{id:'a',x:85,y:0}];
 if(defect==='contract')p.constraints.rules=[{type:'region',ids:['a'],source:'exact region edge',box:[-20,-20,150,5]}];
 const bbox=f.eda.sch_Primitive.getPrimitivesBBox;let drift=false;
 f.eda.sch_Primitive.getPrimitivesBBox=async ids=>{const b=await bbox(ids);if(drift&&ids[0]==='a')b[defect==='clearance'?'maxX':'maxY']+=0.0005;return b;};
 if(action==='apply'){
  const all=f.eda.sch_PrimitiveComponent.getAll;let captures=0;
  f.eda.sch_PrimitiveComponent.getAll=async()=>{if(++captures===4)drift=true;return all();};
  const out=await f.run('apply',p);assert.equal(out.state,'ROLLED_BACK');assert.match(out.error,defect==='clearance'?/COLLISION/:/FINAL_CONSTRAINTS/);
 }else{
  assert.equal((await f.run('apply',p)).state,'APPLIED');const writes=f.count();
  if(action==='reopen')f.hooks.reopen=()=>{drift=true;};else drift=true;
  const out=await f.run(action==='replay'?'apply':action,action==='replay'?p:{});
  assert.equal(out.state,action==='reopen'?'RELOAD_MISMATCH':'RECONCILIATION_REQUIRED');
  assert.match(out.error??out.reloadError,defect==='clearance'?/COLLISION/:/CONSTRAINTS/);
  if(action==='resume')assert.equal(out.constraintReport.state,defect==='clearance'?'PASS':'BLOCKED');
  assert.equal(f.count(),writes);
 }
});

test('reopen validates actual geometry before saving or closing',async()=>{
 const f=fixture(),p=await f.plan();p.moves=[{id:'a',x:85,y:0}];await f.run('apply',p);
 const bbox=f.eda.sch_Primitive.getPrimitivesBBox;f.eda.sch_Primitive.getPrimitivesBBox=async ids=>{const b=await bbox(ids);if(ids[0]==='a')b.maxX+=0.0005;return b;};
 let saves=0,closes=0;f.eda.sch_Document.save=async()=>{saves++;return true;};f.eda.dmt_EditorControl.closeDocument=async()=>{closes++;return true;};
 await assert.rejects(()=>f.run('reopen'),/COLLISION/);assert.equal(saves,0);assert.equal(closes,0);assert.equal(f.count(),1);
});

test('repair restoration stays inspectable without claiming the defective source is valid',async()=>{
 const f=fixture(),p=repairPlan(await f.plan());await f.run('apply',p);
 assert.equal((await f.run('resume')).state,'RESUME_INSPECTED');assert.equal((await f.run('reopen')).state,'RELOADED_MATCH');
 const back=await f.run('rollback');assert.equal(back.state,'ROLLED_BACK');assert.equal(back.restoredConstraintReport.state,'BLOCKED');
 const writes=f.count(),resumed=await f.run('resume');assert.equal(resumed.state,'RECONCILIATION_REQUIRED');assert.equal(resumed.constraintReport.state,'BLOCKED');
 assert.equal((await f.run('apply',p)).state,'ROLLED_BACK');assert.equal(f.count(),writes);
});

test('bridge diagnostic reports vendor package version without contacting EDA',async()=>{
 const {readFile}=await import('node:fs/promises'),{spawnSync}=await import('node:child_process');
 const expected=JSON.parse(await readFile(new URL('../vendor/easyeda-api/package.json',import.meta.url),'utf8')).version;
 const bridge=new URL('./easyeda_bridge.mjs',import.meta.url).href;
 const script=`import http from 'node:http';import {EventEmitter} from 'node:events';import {syncBuiltinESMExports} from 'node:module';
 http.get=()=>{const req=new EventEmitter();req.setTimeout=()=>req;req.destroy=()=>req;queueMicrotask(()=>req.emit('error',Error('mock offline')));return req;};syncBuiltinESMExports();
 process.argv[2]='doctor';await import(${JSON.stringify(bridge)});`;
 const result=spawnSync(process.execPath,['--input-type=module','--eval',script],{encoding:'utf8',windowsHide:true});
 assert.equal(result.status,2,result.stderr);const diagnostic=JSON.parse(result.stdout);
 assert.equal(diagnostic.status,'BRIDGE_NOT_FOUND');assert.equal(diagnostic.bundledApiVersion,expected);
});
