// Rend titres.html image par image en PNG transparents, avec le Chrome du Mac
// piloté en direct (aucun paquet npm).
// MASQUE=1 pour la passe masque. Usage : node rendu-titres.mjs <dossier_sortie> [fps=25] [t1 t2 ... pour quelques instants seulement]
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const [out, fpsArg, ...instants] = process.argv.slice(2);
const fps = +(fpsArg || 25);
fs.mkdirSync(out, { recursive: true });
const port = 9300 + Math.floor(Math.random() * 500);
const profil = fs.mkdtempSync(path.join(os.tmpdir(), 'roi-chrome-'));
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profil}`,
  '--hide-scrollbars', '--force-device-scale-factor=1', '--font-render-hinting=none', '--disable-lcd-text', 'about:blank'], { stdio: 'ignore' });

const attendre = (ms) => new Promise((r) => setTimeout(r, ms));
let cible;
for (let i = 0; i < 50 && !cible; i++) {
  await attendre(200);
  try { cible = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((x) => x.type === 'page'); } catch {}
}
const ws = new WebSocket(cible.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r, { once: true }));
let id = 0; const enAttente = new Map();
ws.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.id && enAttente.has(m.id)) { enAttente.get(m.id)(m); enAttente.delete(m.id); } });
const cmd = (method, params = {}) => new Promise((r) => { const i = ++id; enAttente.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evalue = async (expression) => {
  const r = await cmd('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (r.result?.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails));
  return r.result?.result?.value;
};

await cmd('Page.enable');
await cmd('Emulation.setDeviceMetricsOverride', { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false });
await cmd('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });
await cmd('Page.navigate', { url: 'file://' + path.resolve(path.dirname(new URL(import.meta.url).pathname), 'titres.html') + (process.env.MASQUE ? '?masque' : '') });
await attendre(800);
await evalue('window.ready');
const duree = await evalue('window.DURATION');

const temps = instants.length ? instants.map(Number) : Array.from({ length: Math.round(duree * fps) }, (_, i) => i / fps);
const t0 = Date.now();
for (let i = 0; i < temps.length; i++) {
  await evalue(`window.seek(${temps[i]})`);
  const shot = await cmd('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
  const nom = instants.length ? `t${temps[i].toFixed(2)}.png` : `f${String(i).padStart(5, '0')}.png`;
  fs.writeFileSync(path.join(out, nom), Buffer.from(shot.result.data, 'base64'));
  if (i % 200 === 0) console.log(`${i}/${temps.length} images, ${((Date.now() - t0) / 1000).toFixed(0)} s`);
}
console.log('fini', temps.length, 'images');
ws.close(); chrome.kill();
