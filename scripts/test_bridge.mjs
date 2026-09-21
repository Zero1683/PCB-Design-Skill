// Exercise the bundled bridge with simulated EDA windows on an isolated ephemeral port.
import assert from 'node:assert/strict';
import {readFile, writeFile, mkdtemp, rm} from 'node:fs/promises';
import {createServer} from 'node:net';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {fileURLToPath, pathToFileURL} from 'node:url';
import path from 'node:path';
import WebSocket from '../vendor/easyeda-api/node_modules/ws/wrapper.mjs';

const args=process.argv.slice(2);
if (args.length!==2 || args[0]!=='--workdir') throw new Error('Use --workdir <existing temporary-work directory>');
const root=fileURLToPath(new URL('../',import.meta.url));
const temp=await mkdtemp(path.join(path.resolve(args[1]),'pcb-bridge-test-'));
const sockets=[];let child;let childExit;let stderr='';
const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));
try {
  const reservation=createServer();reservation.listen(0,'127.0.0.1');await once(reservation,'listening');
  const port=reservation.address().port;await new Promise(resolve=>reservation.close(resolve));
  let source=await readFile(path.join(root,'vendor/easyeda-api/scripts/bridge-server.mjs'),'utf8');
  // Only relocate ports and ws resolution; request handlers are tested unchanged.
  source=source.replace('const PORT_START = 49620;',`const PORT_START = ${port};`)
    .replace('const PORT_END = 49629;',`const PORT_END = ${port};`)
    .replace("from 'ws'",`from ${JSON.stringify(pathToFileURL(path.join(root,'vendor/easyeda-api/node_modules/ws/wrapper.mjs')).href)}`);
  const file=path.join(temp,'bridge.mjs');await writeFile(file,source);
  child=spawn(process.execPath,[file],{windowsHide:true,stdio:['ignore','ignore','pipe']});
  childExit=once(child,'exit');child.stderr.on('data',chunk=>{stderr+=chunk;});
  const call=async(route,body)=>{
    const res=await fetch(`http://127.0.0.1:${port}${route}`,{method:body?'POST':'GET',
      headers:body?{'Content-Type':'application/json'}:{},body:body?JSON.stringify(body):undefined,
      signal:AbortSignal.timeout(4000)});
    return {status:res.status,data:await res.json()};
  };
  let ready=false;
  for(let i=0;i<30;i++) {
    try {if((await call('/health')).data.service==='easyeda-bridge'){ready=true;break;}}catch{}
    await wait(100);
  }
  assert(ready,stderr || 'Bridge did not start');
  assert.equal((await call('/health')).data.integrationRevision,'pcb-design-skill-1.2.0');
  for(const id of ['test-a','test-b']) {
    const ws=new WebSocket(`ws://127.0.0.1:${port}/eda`);sockets.push(ws);
    ws.on('message',raw=>{const msg=JSON.parse(raw);if(msg.type==='execute')ws.send(JSON.stringify({type:'result',id:msg.id,result:{window:id}}));});
    await once(ws,'open');ws.send(JSON.stringify({type:'register',windowId:id}));
  }
  let count=0;for(let i=0;i<20;i++){count=(await call('/eda-windows')).data.count;if(count===2)break;await wait(50);}
  assert.equal(count,2);
  const selected=await call('/eda-windows/select',{windowId:'test-b'});
  assert.equal(selected.status,200);assert.equal(selected.data.success,true);assert.equal(selected.data.activeWindowId,'test-b');
  assert.equal((await call('/health')).data.activeWindowId,'test-b');
  const invalid=await call('/eda-windows/select',{windowId:'absent'});assert.equal(invalid.status,404);
  assert.equal((await call('/health')).data.activeWindowId,'test-b');
  const response=await call('/execute',{windowId:'test-a',code:'return null;'});
  assert.equal(response.data.success,true);assert.equal(response.data.result.window,'test-a');
  console.log('PASS: window selection, missing-window isolation, and explicit-window request routing (simulated EDA clients).');
} finally {
  for(const ws of sockets)ws.terminate();
  if(child && child.exitCode===null){child.kill();await childExit;}
  await rm(temp,{recursive:true,force:true});
}
