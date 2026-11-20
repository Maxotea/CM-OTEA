// Rendu image par image du teaser avec Playwright (Chromium de /opt/pw-browsers).
// Usage :
//   node render.cjs frames <dossier_sortie> [fps=30]        toutes les images
//   node render.cjs stills <dossier_sortie> t1 t2 ...       quelques instants (secondes)
process.env.PLAYWRIGHT_BROWSERS_PATH = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
const path = require('path');
const fs = require('fs');
let pw;
try { pw = require('playwright'); } catch (e) { pw = require('/opt/node22/lib/node_modules/playwright'); }

(async () => {
  const [mode, out, ...rest] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const browser = await pw.chromium.launch({ args: ['--font-render-hinting=none', '--disable-lcd-text'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('console', (m) => console.log('[page]', m.text()));
  page.on('pageerror', (e) => console.log('[erreur page]', e.message));
  await page.goto('file://' + path.join(__dirname, 'index.html'));
  await page.evaluate(() => window.ready);
  const shot = async (t, file) => {
    await page.evaluate((tt) => window.seek(tt), t);
    await page.screenshot({ path: file, type: 'png' });
  };
  if (mode === 'stills') {
    for (const s of rest) await shot(+s, path.join(out, `t${(+s).toFixed(2).padStart(5, '0')}.png`));
  } else {
    const fps = +(rest[0] || 30);
    const dur = await page.evaluate(() => window.DURATION);
    const n = Math.round(dur * fps);
    const t0 = Date.now();
    for (let i = 0; i < n; i++) {
      await shot(i / fps, path.join(out, `f${String(i).padStart(5, '0')}.png`));
      if (i % 150 === 0) console.log(`${i}/${n} images, ${((Date.now() - t0) / 1000).toFixed(0)} s`);
    }
    console.log('fini', n, 'images');
  }
  await browser.close();
})();
