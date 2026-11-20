// Habillages R.O.I. : timeline déterministe, image par image (25 i/s).
// Chaque habillage est une fonction pure du numéro d'image : seekFrame(f).
// Page : index.html?h=01_10000   (ajouter &review=1 pour un fond de contrôle)
(function () {
  'use strict';
  const FPS = 25;

  // ---------- Outils ----------
  const E = {
    lin: (x) => x,
    outCubic: (x) => 1 - Math.pow(1 - x, 3),
    outQuart: (x) => 1 - Math.pow(1 - x, 4),
    outExpo: (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),
    inCubic: (x) => x * x * x,
    inQuad: (x) => x * x,
  };
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  // progression sur d images à partir de l'image a (atteint 1 à l'image a+d-1)
  const pr = (f, a, d, e = E.outExpo) => e(clamp((f - a + 1) / d));
  const fx = (n) => n.toFixed(3);

  // Masque : le mot glisse dans sa fenêtre. Sortie nette en od images.
  function rv(m, f, a, d = 3, oa = 1e6, od = 3, o = {}) {
    const mi = m.firstElementChild;
    const p = (o.eIn || E.outExpo)(clamp((f - a + 1) / d));
    const q = (o.eOut || E.inCubic)(clamp((f - oa + 1) / od));
    if (f < a || q >= 1) { m.style.visibility = 'hidden'; return; }
    m.style.visibility = 'visible';
    const y = (1 - p) * (o.inDir ?? 1) * 150 + q * (o.outDir ?? -1) * 150;
    mi.style.transform = `translateY(${y.toFixed(2)}%)`;
    m.classList.toggle('clip', p < 1 || q > 0);
  }
  // Fondu simple (voile sombre, libellés)
  function fade(el, f, a, d, oa, od, max = 1) {
    const v = pr(f, a, d, E.outCubic) * (1 - pr(f, oa, od, E.lin));
    el.style.opacity = fx(v * max);
    el.style.visibility = v > 0 ? 'visible' : 'hidden';
  }
  // Échelle 0..1 d'un aplat ou d'un filet, avec point d'ancrage
  function sc(el, axis, k, origin, extra = '') {
    el.style.visibility = k > 0.001 ? 'visible' : 'hidden';
    el.style.transformOrigin = origin;
    el.style.transform = `${extra} scale${axis}(${fx(Math.max(k, 0))})`;
  }
  // Grow puis retrait : entre en [a, a+d), ressort en [oa, oa+od)
  function grow(f, a, d, oa, od, eIn = E.outExpo, eOut = E.inCubic) {
    return pr(f, a, d, eIn) * (1 - pr(f, oa, od, eOut));
  }
  // Secousse courte, déterministe, qui s'amortit
  const SHK = [[0, 0], [1, -0.6], [-0.8, 0.5], [0.55, 0.35], [-0.3, -0.25], [0.15, 0.1]];
  function shake(f, a, amp) {
    const i = f - a;
    if (i < 0 || i >= SHK.length) return [0, 0];
    return [SHK[i][0] * amp, SHK[i][1] * amp];
  }
  // Mot masqué
  const W = (txt, k, cls = '', style = '') =>
    `<span class="m" data-k="${k}"><span class="mi ${cls}" style="${style}">${txt}</span></span>`;

  // Mesure de l'encre (haut des capitales, ligne de base) d'un élément sur une ligne, interligne 1
  const cv = document.createElement('canvas').getContext('2d');
  function ink(el) {
    const cs = getComputedStyle(el);
    const fs = parseFloat(cs.fontSize);
    cv.font = `${cs.fontStyle} ${cs.fontWeight} ${fs}px ${cs.fontFamily}`;
    let txt = el.textContent;
    if (cs.textTransform === 'uppercase') txt = txt.toUpperCase();
    const m = cv.measureText(txt);
    const r = el.getBoundingClientRect();
    const lh = parseFloat(cs.lineHeight) || fs;
    const base = r.top + (lh - (m.fontBoundingBoxAscent + m.fontBoundingBoxDescent)) / 2 + m.fontBoundingBoxAscent;
    return { left: r.left, right: r.right, width: r.width, top: base - m.actualBoundingBoxAscent, base, bottom: base + m.actualBoundingBoxDescent };
  }
  function place(el, x, y, w, h) {
    Object.assign(el.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' });
  }
  const shade = (k, x, y, w, h) => `<div class="shade" data-k="${k}" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px"></div>`;

  // ---------- Les habillages ----------
  const HABS = [];

  // 00 : flash rouge réutilisable (0,52 s)
  HABS.push({
    id: '00_flash-rouge', frames: 13,
    html: `
      <div data-k="fl" style="position:absolute;inset:0;background:radial-gradient(ellipse 75% 75% at 50% 50%,#DC2626 0%,#C41E1E 60%,#9F1414 100%)"></div>
      <div class="slab" data-k="b1" style="left:0;top:-300px;width:560px;height:1680px"></div>
      <div class="slab" data-k="b2" style="left:0;top:-300px;width:150px;height:1680px"></div>`,
    run(f, M) {
      const OP = [1, 0.9, 0.72, 0.55, 0.41, 0.3, 0.21, 0.14, 0.09, 0.05, 0.025, 0.01, 0];
      M.fl.style.opacity = OP[clamp(f, 0, 12)] ?? 0;
      const k1 = clamp(f / 5), k2 = clamp((f - 1) / 5);
      M.b1.style.transform = `translateX(${(-700 + k1 * 3100).toFixed(1)}px) skewX(-18deg)`;
      M.b1.style.opacity = f <= 5 ? 1 : 0;
      M.b2.style.transform = `translateX(${(-500 + k2 * 2900).toFixed(1)}px) skewX(-18deg)`;
      M.b2.style.opacity = f >= 1 && f <= 6 ? 0.85 : 0;
    },
  });

  // 01 : « 10 000 » qui claque, puis « ENTREPRENEURS. » (2 s)
  HABS.push({
    id: '01_10000', frames: 50,
    html: `
      ${shade('sh', 160, 110, 1600, 860)}
      <div class="blk cx" data-k="nw" style="top:215px">${W('10<span class="g"></span>000', 'num', 'sp sh', 'font-size:470px')}</div>
      <div class="slab" data-k="slab"></div>
      <div class="blk cx" style="top:690px">${W('Entrepreneurs<span class="red">.</span>', 'ent', 'sp sh', 'font-size:230px')}</div>`,
    init(M) {
      const r = ink(M.num.firstElementChild);
      place(M.slab, r.left - 70, r.top - 50, r.width + 140, r.bottom - r.top + 100);
    },
    run(f, M) {
      fade(M.sh, f, 0, 3, 45, 4);
      const k = f < 3 ? pr(f, 0, 3) : 1 - pr(f, 3, 3, E.inQuad);
      sc(M.slab, 'X', f > 5 ? 0 : k, f < 3 ? '0 50%' : '100% 50%', 'skewX(-12deg)');
      rv(M.num, f, 2, 1, 46, 3);
      const [sx, sy] = shake(f, 3, 12);
      const punch = 1 + 0.12 * (1 - pr(f, 2, 5, E.outCubic));
      const up = pr(f, 20, 5, E.outExpo);
      M.nw.style.transform = `translate(${sx}px,${(sy - 110 * up).toFixed(1)}px) scale(${fx(punch * (1 - 0.2 * up))})`;
      M.nw.style.transformOrigin = '50% 50%';
      rv(M.ent, f, 21, 4, 47, 3, { outDir: 1 });
    },
  });

  // 02 : « UNE LIGNE DE DÉPART. » (1,52 s)
  HABS.push({
    id: '02_ligne-depart', frames: 38,
    html: `
      ${shade('sh', -60, 200, 1560, 800)}
      <div class="blk" style="left:170px;top:315px">
        <div class="sp sh" style="font-size:240px;line-height:1">
          <div>${W('Une', 'w1')} ${W('ligne', 'w2')}</div>
          <div data-k="l2">${W('de', 'w3')} ${W('départ<span class="red">.</span>', 'w4')}</div>
        </div>
      </div>
      <div class="rule" data-k="bar" style="background:var(--red)"></div>`,
    init(M) {
      const r = ink(M.w4.firstElementChild);
      place(M.bar, 0, r.base + 38, 1920, 9);
    },
    run(f, M) {
      fade(M.sh, f, 0, 3, 32, 5);
      rv(M.w1, f, 0, 3, 32, 3);
      rv(M.w2, f, 2, 3, 33, 3);
      rv(M.w3, f, 5, 3, 33, 3);
      rv(M.w4, f, 7, 3, 34, 3);
      const k = f < 20 ? pr(f, 8, 4) : 1 - pr(f, 32, 4, E.inCubic);
      sc(M.bar, 'X', k, f < 20 ? '0 50%' : '100% 50%');
    },
  });

  // 03 : cartouche corporate « COURSE PROFESSIONNELLE » / « LA DÉFENSE · PARIS » (2 s)
  HABS.push({
    id: '03_la-defense', frames: 50,
    html: `
      ${shade('sh', -200, 560, 1700, 600)}
      <div class="blk" style="left:150px;top:690px">
        <div data-k="bar" style="position:absolute;left:0;top:0;bottom:0;width:12px;background:var(--red)"></div>
        <div data-k="box" style="margin-left:12px;background:rgba(10,10,10,.82);padding:34px 64px 36px 46px">
          <div class="sp" style="font-size:100px;line-height:1">${W('Course professionnelle', 't1')}</div>
          <div data-k="rule" style="height:2px;background:rgba(255,255,255,.24);margin:24px 0 22px"></div>
          <div class="lb" style="font-size:34px;color:#D1D5DB">${W('La Défense <span class="red">·</span> Paris', 't2')}</div>
        </div>
      </div>`,
    run(f, M) {
      fade(M.sh, f, 0, 4, 44, 5, 0.8);
      sc(M.bar, 'Y', f < 30 ? pr(f, 0, 3) : 1 - pr(f, 46, 3, E.inCubic), f < 30 ? '50% 100%' : '50% 0');
      const kb = f < 30 ? pr(f, 1, 6) : 1 - pr(f, 44, 4, E.inCubic);
      M.box.style.visibility = kb > 0.001 ? 'visible' : 'hidden';
      M.box.style.clipPath = `inset(0 ${((1 - kb) * 100).toFixed(2)}% 0 0)`;
      rv(M.t1, f, 3, 4, 43, 3, { outDir: 1 });
      sc(M.rule, 'X', f < 30 ? pr(f, 5, 6) : 1 - pr(f, 42, 3, E.inCubic), f < 30 ? '0 50%' : '100% 50%');
      rv(M.t2, f, 6, 4, 42, 3, { inDir: -1, outDir: -1 });
    },
  });

  // 04 et 05 : « 5 KM » et « 10 KM » en coup de poing (1 s)
  function km(id, num, origin) {
    return {
      id, frames: 25,
      html: `
        ${shade('sh', 210, 60, 1500, 960)}
        <div class="slab" data-k="slab"></div>
        <div class="blk cx" data-k="nw" style="top:205px">${W(`${num}<span class="g"></span><span style="font-size:.4em">Km</span>`, 'n', 'sp sh', 'font-size:640px')}</div>`,
      init(M) {
        const r = ink(M.n.firstElementChild);
        place(M.slab, r.left - 80, r.top - 46, r.width + 160, r.bottom - r.top + 46 + 48);
        M.slabH = r.bottom - r.top + 94;
      },
      run(f, M) {
        fade(M.sh, f, 0, 2, 21, 4);
        const SC = [1.34, 1.1, 0.965, 0.985, 1];
        const s = SC[clamp(f, 0, 4)];
        const [sx, sy] = shake(f, 1, 14);
        rv(M.n, f, 0, 1, 22, 3);
        M.nw.style.transformOrigin = '50% 55%';
        M.nw.style.transform = `translate(${sx}px,${sy}px) scale(${s})`;
        // aplat plein qui se replie en barre épaisse sous le chiffre, puis file
        const ky = 1 - pr(f, 1, 5, E.outExpo) * (1 - 16 / M.slabH);
        const kx = 1 - pr(f, 21, 3, E.inCubic);
        M.slab.style.visibility = kx > 0.001 ? 'visible' : 'hidden';
        M.slab.style.transformOrigin = `${origin} 100%`;
        M.slab.style.transform = `skewX(-12deg) scale(${fx(kx)},${fx(ky)})`;
      },
    };
  }
  HABS.push(km('04_5km', '5', '100%'));
  HABS.push(km('05_10km', '10', '0%'));

  // 06 : « ARRIVÉE » puis « PLÉNITUDE ARENA » (2 s)
  HABS.push({
    id: '06_arena', frames: 50,
    html: `
      ${shade('sh', 160, 170, 1600, 740)}
      <div class="blk cx" data-k="aw" style="top:330px">${W('Arrivée', 'a', 'sp sh', 'font-size:400px')}</div>
      <div class="blk cx" style="top:358px">
        <span class="rule" data-k="rl" style="position:relative;display:inline-block;width:150px;height:2px;vertical-align:middle;margin-right:34px;opacity:.8"></span>${W('Arrivée', 'lab', 'lb red sh', 'font-size:48px;margin-right:-.34em')}<span class="rule" data-k="rr" style="position:relative;display:inline-block;width:150px;height:2px;vertical-align:middle;margin-left:34px;opacity:.8"></span>
      </div>
      <div class="blk cx" style="top:450px">${W('Plénitude Arena', 'b', 'sp sh', 'font-size:240px')}</div>`,
    run(f, M) {
      fade(M.sh, f, 0, 3, 45, 4);
      rv(M.a, f, 0, 3, 21, 1);
      const [sx, sy] = shake(f, 1, 9);
      M.aw.style.transform = `translate(${sx}px,${sy}px) scale(${fx(1 + 0.08 * (1 - pr(f, 0, 4, E.outCubic)))})`;
      rv(M.b, f, 21, 3, 46, 3, { outDir: 1 });
      rv(M.lab, f, 22, 4, 45, 3, { inDir: -1, outDir: -1 });
      const kr = f < 30 ? pr(f, 22, 6) : 1 - pr(f, 44, 3, E.inCubic);
      sc(M.rl, 'X', kr, '100% 50%');
      sc(M.rr, 'X', kr, '0 50%');
    },
  });

  // 07 : « LE NETWORKING COMMENCE À LA LIGNE D'ARRIVÉE. » (2,52 s)
  HABS.push({
    id: '07_networking', frames: 63,
    html: `
      ${shade('sh', -120, 110, 1720, 860)}
      <div class="rule" data-k="vr" style="opacity:.85"></div>
      <div class="blk" style="left:180px;top:215px">
        <div class="sp sh" style="font-size:172px;line-height:1.03">
          <div>${W('Le', 'a1')} ${W('networking', 'a2', 'red')}</div>
          <div>${W('commence', 'b1')} ${W('à', 'b2')} ${W('la', 'b3')}</div>
          <div>${W('ligne', 'c1')} ${W('d’arrivée.', 'c2')}</div>
        </div>
      </div>`,
    init(M) {
      const t = ink(M.a1.firstElementChild), b = ink(M.c2.firstElementChild);
      place(M.vr, 136, t.top, 3, b.base - t.top);
    },
    run(f, M) {
      fade(M.sh, f, 0, 3, 57, 5);
      sc(M.vr, 'Y', f < 30 ? pr(f, 0, 8) : 1 - pr(f, 57, 3, E.inCubic), f < 30 ? '50% 0' : '50% 100%');
      rv(M.a1, f, 0, 3, 57, 3);
      rv(M.a2, f, 2, 3, 57, 3);
      rv(M.b1, f, 9, 3, 58, 3);
      rv(M.b2, f, 11, 3, 58, 3);
      rv(M.b3, f, 12, 3, 58, 3);
      rv(M.c1, f, 19, 3, 59, 3);
      rv(M.c2, f, 21, 3, 59, 3);
    },
  });

  // 08 : compteur 0 → 10 000, « PARTICIPANTS VISÉS » (2,52 s)
  const col = (i) => `<span class="col" data-k="c${i}" style="display:inline-block;width:.71em;height:1em;padding:0 .12em;margin:0 -.12em;overflow:hidden;vertical-align:top"><span class="strip" style="display:block;text-align:center;line-height:1">0<br>1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>0</span></span>`;
  HABS.push({
    id: '08_compteur', frames: 63,
    html: `
      ${shade('sh', 210, 90, 1500, 920)}
      <div class="blk cx" data-k="nw" style="top:215px">${W(`${col(4)}${col(3)}<span class="g"></span>${col(2)}${col(1)}${col(0)}`, 'cnt', 'sp sh', 'font-size:410px')}</div>
      <div class="rule" data-k="ul" style="background:var(--red)"></div>
      <div class="blk cx" style="top:775px">
        <span class="rule" data-k="rl" style="position:relative;display:inline-block;width:110px;height:2px;vertical-align:middle;margin-right:30px;opacity:.8"></span>${W('Participants visés', 'lab', 'lb white sh', 'font-size:46px;margin-right:-.34em')}<span class="rule" data-k="rr" style="position:relative;display:inline-block;width:110px;height:2px;vertical-align:middle;margin-left:30px;opacity:.8"></span>
      </div>`,
    init(M) {
      const strip = M.c0.firstElementChild;
      const cs = getComputedStyle(strip);
      cv.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
      const m = cv.measureText('0');
      const fs = parseFloat(cs.fontSize);
      const r = M.cnt.firstElementChild.getBoundingClientRect();
      const base = r.top + (fs - (m.fontBoundingBoxAscent + m.fontBoundingBoxDescent)) / 2 + m.fontBoundingBoxAscent;
      place(M.ul, r.left + 10, base + 34, r.width - 20, 14);
      M.prev = null;
    },
    run(f, M) {
      fade(M.sh, f, 0, 3, 57, 5);
      rv(M.cnt, f, 0, 3, 57, 3);
      const v = 10000 * pr(f, 2, 40, E.outCubic) * (f >= 2 ? 1 : 0);
      const vp = 10000 * pr(f - 1, 2, 40, E.outCubic) * (f - 1 >= 2 ? 1 : 0);
      const pos = (val, i) => {
        if (i === 0) return val % 10;
        const p = Math.pow(10, i);
        return (Math.floor(val / p) % 10) + clamp((val % p) - (p - 1), 0, 1);
      };
      for (let i = 0; i < 5; i++) {
        const c = M['c' + i], s = c.firstElementChild;
        const ps0 = pos(v, i);
        const speed = Math.min(10, (v - vp) / Math.pow(10, i)); // chiffres par image
        // colonne rapide : le chiffre change sur place (flou), colonne lente : vrai roulement
        const ps = speed > 0.8 && v < 9990 ? Math.round(ps0) % 10 : ps0;
        s.style.transform = `translateY(${(-ps).toFixed(4)}em)`;
        s.style.filter = speed > 0.25 ? `blur(${Math.min(7, speed * 2.2).toFixed(2)}px)` : 'none';
        const on = i === 0 || v >= Math.pow(10, i) - 0.5;
        c.style.opacity = on ? 1 : 0.22;
      }
      const land = pr(f, 42, 4, E.outCubic);
      const [sx, sy] = shake(f, 42, 6);
      M.nw.style.transform = `translate(${sx}px,${sy}px) scale(${fx(f >= 42 ? 1 + 0.05 * (1 - land) : 1)})`;
      sc(M.ul, 'X', f < 50 ? pr(f, 42, 4) : 1 - pr(f, 56, 3, E.inCubic), f < 50 ? '0 50%' : '100% 50%', 'skewX(-12deg)');
      rv(M.lab, f, 4, 5, 56, 3, { inDir: -1, outDir: 1 });
      const kr = f < 30 ? pr(f, 5, 6) : 1 - pr(f, 56, 3, E.inCubic);
      sc(M.rl, 'X', kr, '100% 50%');
      sc(M.rr, 'X', kr, '0 50%');
    },
  });

  // 09 : « ENTREPRENEURS · DIRIGEANTS · CADRES · INDÉPENDANTS » sur le rythme (2 s)
  const PUB = ['Entrepreneurs', 'Dirigeants', 'Cadres', 'Indépendants'];
  HABS.push({
    id: '09_public', frames: 50,
    html: `
      ${shade('sh', 160, 160, 1600, 800)}
      ${PUB.map((w, i) => `<div class="blk cx" data-k="ww${i}" style="top:300px">${W(w, 'w' + i, 'sp sh', 'font-size:280px')}</div>`).join('')}
      <div class="blk cx" style="top:700px">${W(PUB.map((w, i) => `<span data-k="l${i}">${w}</span>`).join(' <span class="red">·</span> '), 'list', 'lb sh', 'font-size:36px;margin-right:-.34em')}</div>`,
    run(f, M) {
      fade(M.sh, f, 0, 3, 45, 4);
      const A = [0, 10, 20, 30];
      for (let i = 0; i < 4; i++) {
        const last = i === 3;
        rv(M['w' + i], f, A[i], 3, last ? 45 : A[i + 1], last ? 3 : 1);
        const [sx, sy] = shake(f, A[i], 6);
        M['ww' + i].style.transform = `translate(${sx}px,${sy}px) scale(${fx(1 + 0.07 * (1 - pr(f, A[i], 4, E.outCubic)))})`;
        const cur = f >= A[i] && (last || f < A[i + 1]);
        M['l' + i].style.color = cur ? '#FFFFFF' : '#C4C8CE';
        M['l' + i].style.opacity = cur ? 1 : 0.8;
      }
      rv(M.list, f, 1, 5, 45, 3, { inDir: -1, outDir: 1 });
    },
  });

  // 10 : « AUTOMNE 2027 » / « ÉDITION 1 » (1,52 s)
  HABS.push({
    id: '10_2027', frames: 38,
    html: `
      ${shade('sh', 210, 170, 1500, 760)}
      <div class="blk cx sp" data-k="aw" style="top:290px;font-size:260px">${W('Automne', 'a1', 'sh')} ${W('2027', 'a2', 'sh red')}</div>
      <div class="blk cx" style="top:635px"><span data-k="ed" style="display:inline-block;background:#FFFFFF;padding:18px 30px 16px 42px;box-shadow:0 6px 24px rgba(0,0,0,.25)"><span class="lb" style="color:#0A0A0A;font-size:52px;display:inline-block;transform:translateY(2px)">Édition 1</span></span></div>`,
    run(f, M) {
      fade(M.sh, f, 0, 3, 32, 5);
      rv(M.a1, f, 0, 3, 32, 3);
      rv(M.a2, f, 2, 3, 33, 3);
      const [sx, sy] = shake(f, 2, 7);
      M.aw.style.transform = `translate(${sx}px,${sy}px)`;
      const k = f < 20 ? pr(f, 5, 5) : 1 - pr(f, 32, 4, E.inCubic);
      M.ed.style.visibility = k > 0.001 ? 'visible' : 'hidden';
      M.ed.style.clipPath = f < 20 ? `inset(-30px ${((1 - k) * 100).toFixed(2)}% -30px 0)` : `inset(-30px 0 -30px ${((1 - k) * 100).toFixed(2)}%)`;
    },
  });

  // 11 : « NOUS CHERCHONS L'AGENCE QUI VA L'ÉCRIRE AVEC NOUS. », « L'AGENCE » sur aplat rouge (3 s)
  HABS.push({
    id: '11_agence', frames: 75,
    html: `
      ${shade('sh', 60, 80, 1800, 920)}
      <div class="blk cx" style="top:190px"><div class="sp sh" style="font-size:136px">${W('Nous', 'n1')} ${W('cherchons', 'n2')}</div></div>
      <div class="slab" data-k="slab"></div>
      <div class="blk cx" style="top:345px">${W('L’agence', 'ag', 'sp', 'font-size:290px')}</div>
      <div class="blk cx" style="top:700px"><div class="sp sh" style="font-size:136px">${W('Qui', 'q1')} ${W('va', 'q2')} ${W('l’écrire', 'q3')} ${W('avec', 'q4')} ${W('nous<span class="red">.</span>', 'q5')}</div></div>`,
    init(M) {
      const r = ink(M.ag.firstElementChild);
      place(M.slab, r.left - 60, r.top - 40, r.width + 120, r.bottom - r.top + 80);
    },
    run(f, M) {
      fade(M.sh, f, 0, 3, 68, 5);
      rv(M.n1, f, 0, 3, 68, 3);
      rv(M.n2, f, 2, 3, 68, 3);
      const k = f < 40 ? pr(f, 7, 4) : 1 - pr(f, 69, 3, E.inCubic);
      sc(M.slab, 'X', k, f < 40 ? '0 50%' : '100% 50%', 'skewX(-10deg)');
      rv(M.ag, f, 9, 4, 69, 2);
      rv(M.q1, f, 17, 3, 69, 3, { outDir: 1 });
      rv(M.q2, f, 18, 3, 69, 3, { outDir: 1 });
      rv(M.q3, f, 20, 3, 70, 3, { outDir: 1 });
      rv(M.q4, f, 22, 3, 70, 3, { outDir: 1 });
      rv(M.q5, f, 23, 3, 70, 3, { outDir: 1 });
    },
  });

  // 12 : « ET CE N'EST PAS TOUT. » puis « LA SUITE, EN VISIO. » (2,52 s)
  HABS.push({
    id: '12_pas-tout', frames: 63,
    html: `
      ${shade('sh', 160, 140, 1600, 820)}
      <div class="blk cx" style="top:255px"><div class="sp sh" style="font-size:230px;line-height:1">
        <div>${W('Et', 'a1')} ${W('ce', 'a2')} ${W('n’est', 'a3')}</div>
        <div>${W('pas', 'a4')} ${W('tout<span class="red">.</span>', 'a5')}</div>
      </div></div>
      <div class="blk cx" style="top:255px"><div class="sp sh" style="font-size:230px;line-height:1">
        <div>${W('La', 'b1')} ${W('suite,', 'b2')}</div>
        <div>${W('en', 'b3', 'red')} ${W('visio.', 'b4', 'red')}</div>
      </div></div>`,
    run(f, M) {
      fade(M.sh, f, 0, 3, 57, 5);
      rv(M.a1, f, 0, 3, 28, 2);
      rv(M.a2, f, 2, 3, 28, 2);
      rv(M.a3, f, 4, 3, 28, 2);
      rv(M.a4, f, 8, 3, 28, 2);
      rv(M.a5, f, 10, 3, 28, 2);
      rv(M.b1, f, 30, 3, 57, 3);
      rv(M.b2, f, 31, 3, 57, 3);
      rv(M.b3, f, 35, 3, 58, 3, { outDir: 1 });
      rv(M.b4, f, 36, 3, 58, 3, { outDir: 1 });
    },
  });

  // 13 : signature, fond noir plein (4 s)
  HABS.push({
    id: '13_signature', frames: 100, opaque: true,
    html: `
      <div style="position:absolute;inset:0;background:#0A0A0A"></div>
      <div data-k="bar" style="position:absolute;left:0;top:0;width:14px;height:1080px;background:var(--red)"></div>
      <div class="blk cx" style="top:150px">${W('R.O.I.', 'logo', '', 'font-family:var(--serif);font-weight:700;font-size:230px;line-height:1;letter-spacing:.01em')}</div>
      <div class="blk cx" style="top:408px">${W('Run on Investment', 'sub', 'lb red', 'font-size:38px;letter-spacing:.42em;margin-right:-.42em')}</div>
      <div class="rule" data-k="rule" style="left:880px;top:492px;width:160px;height:2px;background:#6B7280"></div>
      <div class="blk cx" style="top:528px">${W('La course qui connecte les entrepreneurs', 'tag', '', 'font-family:var(--serif);font-style:italic;font-weight:400;font-size:54px;line-height:1;color:var(--soft)')}</div>
      <div class="blk cx" style="top:715px">${W('On en parle 30 minutes&nbsp;?', 'cta', '', 'font-family:var(--sport);font-weight:800;font-style:italic;font-size:92px;line-height:1')}</div>
      <div class="blk cx" style="top:850px">${W('Maxime Dietrich <span class="red">·</span> 07 79 97 19 61', 'ct', '', 'font-family:var(--sans);font-weight:700;font-size:32px;line-height:1;letter-spacing:.14em;margin-right:-.14em;color:var(--grey)')}</div>`,
    run(f, M) {
      sc(M.bar, 'Y', pr(f, 0, 7), '50% 0');
      rv(M.logo, f, 3, 9);
      rv(M.sub, f, 8, 8, 1e6, 3, { inDir: -1 });
      sc(M.rule, 'X', pr(f, 12, 9), '50% 50%');
      rv(M.tag, f, 14, 9);
      rv(M.cta, f, 34, 6);
      rv(M.ct, f, 40, 8);
    },
  });

  // ---------- Moteur ----------
  const qs = new URLSearchParams(location.search);
  const id = qs.get('h') || '01_10000';
  if (qs.get('review')) document.body.classList.add('review');
  if (qs.get('lite')) document.body.classList.add('lite');
  const stage = document.getElementById('stage');
  const H = HABS.find((h) => h.id === id);
  const M = {};
  window.HAB_LIST = HABS.map((h) => ({ id: h.id, frames: h.frames, opaque: !!h.opaque }));
  window.FPS = FPS;
  window.ready = (async () => {
    await Promise.all([
      '900 italic 100px "Barlow Condensed"', '800 italic 100px "Barlow Condensed"',
      '700 100px Caladea', 'italic 400 100px Caladea', '700 100px Carlito', '400 100px Carlito',
    ].map((s) => document.fonts.load(s)));
    await document.fonts.ready;
    stage.innerHTML = `<div class="hab on">${H.html}</div>`;
    stage.querySelectorAll('[data-k]').forEach((e) => { M[e.dataset.k] = e; });
    if (H.init) H.init(M);
    window.FRAMES = H.frames;
    window.seekFrame = (f) => H.run(f, M);
    window.seekFrame(0);
    return true;
  })();
})();
