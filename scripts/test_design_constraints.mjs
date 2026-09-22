import assert from 'node:assert/strict';
import test from 'node:test';
import {checkConstraints} from './design_constraints.mjs';
const fixture=()=>({snapshot:{schema:1,domain:'pcb',coverage:'complete',projectId:'p',documentId:'d',units:'mm',axis:'y-up',objects:[{id:'J1',anchor:[5,5],rotation:0,side:'top',bbox:[4,4,6,6],height:3}]},contract:{schema:1,revision:'mech-A',domain:'pcb',projectId:'p',documentId:'d',units:'mm',axis:'y-up',source:'drawing A',bounds:[0,0,20,20],rules:[]}});
test('geometry accepted without changing inputs',()=>{const f=fixture(),before=JSON.stringify(f);assert.equal(checkConstraints(f.snapshot,f.contract).state,'PASS');assert.equal(JSON.stringify(f),before);});
for(const [name,rule,code] of [
 ['fixed connector',{type:'lock',anchor:[6,5],rotation:0,side:'top'},'LOCKED_PLACEMENT'],
 ['connector mating region',{type:'region',box:[10,10,20,20]},'ALLOWED_REGION'],
 ['antenna clearance',{type:'keepout',box:[7,4,10,6],gap:2},'KEEPOUT'],
 ['enclosure height',{type:'height',max:2},'HEIGHT_LIMIT']])test(name,()=>{const f=fixture();f.contract.rules=[{...rule,source:'drawing',ids:['J1']}];assert.equal(checkConstraints(f.snapshot,f.contract).violations[0].code,code);});
test('missing height is not zero',()=>{const f=fixture();delete f.snapshot.objects[0].height;f.contract.rules=[{type:'height',max:5,ids:'*',source:'housing'}];assert.equal(checkConstraints(f.snapshot,f.contract).violations[0].code,'HEIGHT_UNKNOWN');});
test('boundary clearance equality allowed',()=>{const f=fixture();f.contract.rules=[{type:'keepout',box:[7,4,10,6],gap:1,ids:'*',source:'drawing'}];assert.equal(checkConstraints(f.snapshot,f.contract).state,'PASS');});
test('wrong units, project and incomplete inventory rejected',()=>{for(const [key,v]of [['units','mil'],['projectId','other'],['coverage','partial']]){const f=fixture();f.snapshot[key]=v;assert.throws(()=>checkConstraints(f.snapshot,f.contract));}});
test('unsupported rule, stale ID, and malformed constraints rejected',()=>{for(const patch of [{type:'polygon'},{ids:['missing']},{box:[NaN,0,1,1]},{gap:2}]){const f=fixture();f.contract.rules=[{type:'region',box:[0,0,20,20],ids:['J1'],source:'drawing',...patch}];assert.throws(()=>checkConstraints(f.snapshot,f.contract));}});
test('serialized evaluator keeps standalone semantics',()=>{const f=fixture();const remote=new Function('return ('+checkConstraints.toString()+')')();assert.deepEqual(remote(f.snapshot,f.contract),checkConstraints(f.snapshot,f.contract));});
