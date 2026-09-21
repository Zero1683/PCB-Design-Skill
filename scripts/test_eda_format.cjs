'use strict';
const assert = require('node:assert/strict');
const {test} = require('node:test');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const {validate} = require('./validate_eda_primitive.cjs');
const canvas = () => ({docType:'SCH_PAGE', primitiveType:'CANVAS',
  outer:{type:'CANVAS',id:'CANVAS',ticket:1},data:{originX:0,originY:0}});
const line = () => ({docType:'PCB',primitiveType:'LINE',data:{groupId:'g1',layerId:1,
  locked:false,zIndex:-1,netName:'GND',startX:0,startY:0,endX:10,endY:0,width:1}});
test('valid typed primitive has bounded coverage',()=>{
  const r=validate(canvas());assert.equal(r.valid,true);assert.equal(r.schema,'t-sch-canvas');
  assert.equal(r.outer_checked,true);assert.ok(r.not_checked.includes('connectivity'));
});
test('payload cannot use another document schema',()=>{
  const v=canvas();v.docType='PCB';assert.equal(validate(v).valid,false);
  const r=validate(line());assert.equal(r.valid,true);assert.equal(r.schema,'t-pcb-line');
});
test('unknown pair cannot fall back to global alias',()=>{
  const v=line();v.docType='BOARD';assert.equal(validate(v).valid,false);
  for(const doc of ['NOT_REAL','toString','pcb']) {v.docType=doc;assert.equal(validate(v).valid,false);}
});
test('invalid envelope fails even with valid payload',()=>{
  const v=canvas();v.outer.type='LINE';assert.equal(validate(v).valid,false);
  v.outer.type='CANVAS';v.outer.ticket=-1;assert.equal(validate(v).valid,false);
  delete v.outer.id;assert.equal(validate(v).valid,false);
});
test('DOCHEAD must match requested domain',()=>{
  const v={docType:'PCB',primitiveType:'DOCHEAD',outer:{type:'DOCHEAD',ticket:1},
    data:{docType:'PCB',client:'0123456789abcdef',uuid:'1123456789abcdef'}};
  assert.equal(validate(v).valid,true);v.data.docType='SCH_PAGE';assert.equal(validate(v).valid,false);
});
test('input contract and field types rejected',()=>{
  for(const v of [null,[],{}, {...canvas(),typo:1},{...canvas(),data:[]},
    {...canvas(),data:{originX:'0',originY:0}}, {...canvas(),primitiveType:'PCB_LINE'}])
    assert.equal(validate(v).valid,false);
});
test('native/schema discrepancy is exposed without coercion',()=>{
  const v=line();v.data.groupId=0;assert.equal(validate(v).valid,false);assert.equal(v.data.groupId,0);
});
test('file CLI status and malformed input',()=>{
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'eda-format-'));
  try {
    const input=path.join(tmp,'primitive.json');
    for(const [text,status] of [[JSON.stringify(canvas()),0],['{',1],[JSON.stringify({...canvas(),docType:'PCB'}),1]]) {
      fs.writeFileSync(input,text);
      const r=spawnSync(process.execPath,[path.join(__dirname,'validate_eda_primitive.cjs'),input],{encoding:'utf8',windowsHide:true});
      assert.equal(r.status,status,r.stderr);assert.equal(JSON.parse(r.stdout).valid,status===0);
    }
  } finally {fs.rmSync(tmp,{recursive:true,force:true});}
});
