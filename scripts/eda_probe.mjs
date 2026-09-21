// Read-only identity/capability probe. Never creates a project or starts routing.
import { request } from 'node:http';
const args = process.argv.slice(2);
if (args.length !== 2 || !/^4962[0-9]$/.test(args[0]) || !args[1].trim()) {
  console.error('Usage: node scripts/eda_probe.mjs <actual-port-49620..49629> <windowId>');
  process.exit(2);
}
const [port, windowId] = args;
function call(route, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const req = request({host: '127.0.0.1', port, path: route, method: data ? 'POST' : 'GET',
      headers: data ? {'Content-Type':'application/json', 'Content-Length':Buffer.byteLength(data)} : {}}, res => {
      let text = '';
      res.on('data', chunk => { text += chunk; if (text.length > 1000000) req.destroy(new Error('Response too large')); });
      res.on('error', reject);
      res.on('end', () => {
        try { if (res.statusCode !== 200) throw new Error(`HTTP ${res.statusCode}: ${text}`); resolve(JSON.parse(text)); }
        catch (error) { reject(error); }
      });
    });
    req.setTimeout(10000, () => req.destroy(new Error('Probe timeout; no mutation was requested')));
    req.on('error', reject); req.end(data);
  });
}
try {
  const health = await call('/health');
  if (health.service !== 'easyeda-bridge' || !health.edaConnected) throw new Error('No connected EasyEDA bridge at selected port');
  const reply = await call('/execute', {windowId, code: `
    const project = await eda.dmt_Project.getCurrentProjectInfo();
    const document = await eda.dmt_SelectControl.getCurrentDocumentInfo();
    return { probe: 'pcb-skill-readonly-v1', project: project ?? null, document: document ?? null,
      capabilities: {
        createProject: typeof eda.dmt_Project?.createProject === 'function',
        openProject: typeof eda.dmt_Project?.openProject === 'function',
        autoRouting: typeof eda.pcb_Document?.autoRouting === 'function',
        drc: typeof eda.pcb_Drc?.check === 'function'
      }};`});
  if (reply.success !== true || reply.result?.probe !== 'pcb-skill-readonly-v1') throw new Error(`Unexpected API payload: ${JSON.stringify(reply)}`);
  console.log(JSON.stringify({status: 'API_RESPONDED', windowId, ...reply.result,
    scope: 'identity-and-method-presence-only', note: 'No active project is valid before project creation; method presence is not operation validation.'}, null, 2));
} catch (error) { console.error(JSON.stringify({status: 'API_PROBE_FAILED', error: error.message})); process.exitCode = 1; }
