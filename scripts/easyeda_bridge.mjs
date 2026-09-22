import { get } from 'node:http';
import { spawn } from 'node:child_process';
import { mkdirSync, openSync, closeSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const vendor = path.join(root, 'vendor', 'easyeda-api');
const bundledApiVersion = JSON.parse(readFileSync(path.join(vendor, 'package.json'), 'utf8')).version;
const mode = process.argv[2] || 'start';
if (!['start', 'status', 'doctor'].includes(mode)) {
  console.error('Usage: node scripts/easyeda_bridge.mjs [start|status|doctor]');
  process.exit(1);
}
if (Number(process.versions.node.split('.')[0]) < 18) {
  console.error('Node.js 18+ is required.'); process.exit(1);
}
function request(port, route) {
  return new Promise(resolve => {
    const req = get(`http://127.0.0.1:${port}${route}`, res => {
      let data = '';
      res.on('data', part => { data += part; if (data.length > 100000) req.destroy(); });
      res.on('end', () => {
        try { resolve(res.statusCode === 200 ? JSON.parse(data) : null); }
        catch { resolve(null); }
      });
      res.on('error', () => resolve(null));
    });
    req.setTimeout(900, () => req.destroy());
    req.on('error', () => resolve(null));
  });
}
async function discover() {
  const results = await Promise.all(Array.from({ length: 10 }, async (_, i) => {
    const port = 49620 + i;
    const health = await request(port, '/health');
    return health?.service === 'easyeda-bridge' ? { port, health } : null;
  }));
  return results.filter(Boolean);
}
let bridges = await discover();
let startedPid = null;
let logPath = null;
if (!bridges.length && mode === 'start') {
  // Resolve from the bundled dependency, never from a user's global npm install.
  await import(new URL('../vendor/easyeda-api/node_modules/ws/wrapper.mjs', import.meta.url));
  const state = process.env.PCB_SKILL_STATE_DIR || path.join(root, '.runtime');
  mkdirSync(state, { recursive: true });
  logPath = path.join(state, 'easyeda-bridge.log');
  const fd = openSync(logPath, 'a');
  let child;
  try {
    child = spawn(process.execPath, [path.join(vendor, 'scripts', 'bridge-server.mjs')], {
      cwd: vendor, detached: true, windowsHide: true, stdio: ['ignore', fd, fd],
    });
    await new Promise((resolve, reject) => { child.once('spawn', resolve); child.once('error', reject); });
    startedPid = child.pid;
    child.unref();
  } finally { closeSync(fd); }
  for (let i = 0; i < 20 && !bridges.length; i++) {
    await new Promise(resolve => setTimeout(resolve, 250));
    bridges = await discover();
  }
}
for (const bridge of bridges) bridge.windows = await request(bridge.port, '/eda-windows');
const connected = bridges.some(b => b.health.edaConnected);
const expectedBridgeRevision = 'pcb-design-skill-1.2.0';
const bridgeUpdateRecommended = bridges.some(b => b.health.integrationRevision !== expectedBridgeRevision);
const status = !bridges.length ? 'BRIDGE_NOT_FOUND' : connected ? 'EDA_CONNECTED' : 'WAITING_FOR_EDA';
console.log(JSON.stringify({ status, node: process.versions.node, bundledApiVersion,
  expectedBridgeRevision, bridgeUpdateRecommended,
  upgradeNote: bridgeUpdateRecommended ? 'An existing bridge predates this integration patch. It was not terminated. After saving work and finishing active operations, restart that bridge from this package to load the update; do not terminate unrelated services.' : null,
  startedPid, logPath, bridges,
  next: !bridges.length ? 'Run start; inspect the log if startup fails. Ports 49620-49629 must have one free slot.'
    : !connected ? 'Open EasyEDA desktop; install/enable Run API Gateway; then run status.'
    : 'Read /eda-windows and verify target project/document before executing changes.',
}, null, 2));
// No bridge is a failure; waiting for the desktop is a distinct, successful service startup.
process.exitCode = bridges.length ? 0 : 2;
