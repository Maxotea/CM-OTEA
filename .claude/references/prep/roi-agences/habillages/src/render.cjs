// Rendu des habillages R.O.I. : PNG à fond transparent (Playwright), puis ProRes 4444 avec alpha ou version légère.
// Usage :
//   node render.cjs mov <dossier_sortie> all|<id> [<id> ...]     ProRes 4444 avec alpha (qualité master)
//   node render.cjs leger <dossier_sortie> all|<id> [<id> ...]   version légère : .mov codec PNG avec alpha
//   node render.cjs stills <dossier_sortie> <id> <image> [<image> ...] [--review]
// Variables : FFMPEG (chemin du ffmpeg complet), TMPDIR_FRAMES (dossier temporaire des PNG).
process.env.PLAYWRIGHT_BROWSERS_PATH = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
let pw;
try { pw = require('playwright'); } catch (e) { pw = require('/opt/node22/lib/node_modules/playwright'); }

const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const PAGE = 'file://' + path.join(__dirname, 'index.html');

async function open(browser, id, review, lite) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => console.log('[erreur page]', e.message));
  await page.goto(`${PAGE}?h=${id}${review ? '&review=1' : ''}${lite ? '&lite=1' : ''}`);
  await page.evaluate(() => window.ready);
  return page;
}

(async () => {
  const [mode, out, ...rest] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const browser = await pw.chromium.launch({ args: ['--font-render-hinting=none', '--disable-lcd-text'] });

  if (mode === 'stills') {
    const review = rest.includes('--review');
    const [id, ...frames] = rest.filter((a) => a !== '--review');
    const page = await open(browser, id, review);
    for (const f of frames) {
      await page.evaluate((ff) => window.seekFrame(ff), +f);
      await page.screenshot({ path: path.join(out, `${id}_f${String(f).padStart(3, '0')}.png`), omitBackground: !review });
    }
  } else if (mode === 'mov' || mode === 'leger') {
    const lite = mode === 'leger';
    const probe = await open(browser, '01_10000', false);
    const list = await probe.evaluate(() => window.HAB_LIST);
    await probe.close();
    const ids = rest[0] === 'all' ? list.map((h) => h.id) : rest;
    const tmpRoot = process.env.TMPDIR_FRAMES || path.join(__dirname, '..', 'frames');
    for (const id of ids) {
      const h = list.find((x) => x.id === id);
      const dir = path.join(tmpRoot, id);
      fs.rmSync(dir, { recursive: true, force: true });
      fs.mkdirSync(dir, { recursive: true });
      const page = await open(browser, id, false, lite);
      const t0 = Date.now();
      for (let f = 0; f < h.frames; f++) {
        await page.evaluate((ff) => window.seekFrame(ff), f);
        await page.screenshot({ path: path.join(dir, `f${String(f).padStart(4, '0')}.png`), omitBackground: true });
      }
      await page.close();
      const mov = path.join(out, `${id}.mov`);
      const input = ['-y', '-loglevel', 'error', '-framerate', '25', '-i', path.join(dir, 'f%04d.png')];
      if (lite) {
        // PNG sans perte des couleurs ; alpha arrondi au pas de 4 (invisible) pour alléger
        execFileSync(FFMPEG, [...input,
          '-vf', "format=rgba,lutrgb=a='if(gte(val\\,252)\\,255\\,floor(val/4+0.5)*4)'",
          '-c:v', 'png', '-pred', 'mixed', '-pix_fmt', 'rgba', '-r', '25', mov]);
      } else execFileSync(FFMPEG, [...input,
        '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuva444p10le',
        '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-alpha_bits', '16',
        '-vendor', 'apl0', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
        '-r', '25', mov,
      ]);
      fs.rmSync(dir, { recursive: true, force: true });
      const mb = (fs.statSync(mov).size / 1e6).toFixed(1);
      console.log(`${id}.mov  ${h.frames} images  ${(h.frames / 25).toFixed(2)} s  ${mb} Mo  (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
    }
  }
  await browser.close();
})();
