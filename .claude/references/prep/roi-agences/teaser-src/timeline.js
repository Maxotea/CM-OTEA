// R.O.I. teaser agences : timeline déterministe pilotée par seek(t), t en secondes.
// Aucune animation temps réel : chaque image est une fonction pure du temps.
(function () {
  'use strict';
  const DURATION = 43;
  const NS = 'http://www.w3.org/2000/svg';
  const $ = (id) => document.getElementById(id);

  // Easings
  const E = {
    lin: (x) => x,
    outCubic: (x) => 1 - Math.pow(1 - x, 3),
    outQuart: (x) => 1 - Math.pow(1 - x, 4),
    outExpo: (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),
    inCubic: (x) => x * x * x,
    inOutCubic: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
    inOutQuint: (x) => (x < 0.5 ? 16 * x * x * x * x * x : 1 - Math.pow(-2 * x + 2, 5) / 2),
    outBack: (x) => { const c1 = 1.4, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
  };
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const P = (t, a, b, e = E.outCubic) => e(clamp((t - a) / (b - a)));
  const lerp = (a, b, k) => a + (b - a) * k;
  // fenêtre d'opacité : entre a et b en fondu, puis sortie entre c et d
  const win = (t, a, b, c, d) => P(t, a, b, E.outCubic) * (1 - P(t, c, d, E.inCubic));

  // Générateur pseudo-aléatoire à graine fixe
  function rng(seed) {
    return function () {
      seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
      let r = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      r = (r + Math.imul(r ^ (r >>> 7), 61 | r)) ^ r;
      return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
    };
  }
  function el(tag, attrs, parent) {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }

  const GROUND = 820;
  const S = {}; // état construit à l'init

  // ---------- Textes ----------
  function splitWords(root) {
    const words = [];
    const walk = (node) => {
      for (const child of Array.from(node.childNodes)) {
        if (child.nodeType === 3) {
          const parts = child.textContent.split(/( +)/);
          const frag = document.createDocumentFragment();
          for (const p of parts) {
            if (!p) continue;
            if (/^ +$/.test(p)) { frag.appendChild(document.createTextNode(p)); continue; }
            const w = document.createElement('span'); w.className = 'w';
            const wi = document.createElement('span'); wi.className = 'wi'; wi.textContent = p;
            w.appendChild(wi); frag.appendChild(w); words.push(wi);
          }
          node.replaceChild(frag, child);
        } else if (child.nodeType === 1) walk(child);
      }
    };
    walk(root);
    return words;
  }
  function splitChars(root) {
    const chars = [];
    const txt = root.textContent; root.textContent = '';
    for (const c of txt) {
      const s = document.createElement('span'); s.className = 'ch'; s.textContent = c;
      root.appendChild(s); chars.push(s);
    }
    return chars;
  }
  function initTexts() {
    S.texts = [];
    document.querySelectorAll('.tx').forEach((node) => {
      const k = node.dataset.k || 'up';
      const item = { node, k, tin: +node.dataset.in, tout: +node.dataset.out, st: +(node.dataset.st || 0.06) };
      item.parts = k === 'chars' ? splitChars(node) : splitWords(node);
      S.texts.push(item);
    });
  }
  function animTexts(t) {
    for (const it of S.texts) {
      const n = it.parts.length;
      const end = it.tout + 0.5 + n * it.st * 0.4;
      if (t < it.tin - 0.01 || t > end) { it.node.style.visibility = 'hidden'; continue; }
      it.node.style.visibility = 'visible';
      it.parts.forEach((p, i) => {
        if (it.k === 'chars') {
          const a = P(t, it.tin + i * it.st, it.tin + i * it.st + 0.7, E.outExpo);
          const o = P(t, it.tout, it.tout + 0.45, E.inCubic);
          p.style.opacity = (a * (1 - o)).toFixed(3);
          p.style.transform = `translateY(${((1 - a) * 46 - o * 30).toFixed(2)}px)`;
          p.style.filter = a < 1 || o > 0 ? `blur(${((1 - a) * 14 + o * 10).toFixed(2)}px)` : 'none';
        } else {
          const a = P(t, it.tin + i * it.st, it.tin + i * it.st + 0.85, E.outExpo);
          const o = P(t, it.tout + i * it.st * 0.4, it.tout + i * it.st * 0.4 + 0.45, E.inCubic);
          p.style.transform = `translateY(${((1 - a) * 108 - o * 108).toFixed(2)}%)`;
        }
      });
    }
  }

  // ---------- Monde : tours, arche, arena, parcours ----------
  function buildTowers() {
    const r = rng(11);
    const back = $('towersBack'), front = $('towersFront');
    S.towers = [];
    // rangée arrière (parallaxe), plus sombre
    let x = -300;
    while (x < 4600) {
      const w = 70 + r() * 90;
      const inArena = x + w > 2150 + 600 && x < 3600 + 600; // décalée par la parallaxe
      let h = 220 + r() * 330;
      if (x < 1150) h = Math.min(h, 200 + r() * 40);
      if (!inArena) S.towers.push(mkTower(back, x, w, h, 'url(#winA)', '#1a1a1a', r));
      x += w + 8 + r() * 26;
    }
    // rangée avant
    x = -200;
    while (x < 4400) {
      const w = 90 + r() * 110;
      let h = 170 + r() * 430;
      const skip = (x + w > 1230 && x < 1630) || (x + w > 2180 && x < 3580);
      if (x < 1150) h = Math.min(h, 150 + r() * 110);
      if (!skip) S.towers.push(mkTower(front, x, w, h, 'url(#winB)', '#2a2a2a', r));
      x += w + 22 + r() * 70;
    }
    // feux d'obstacle rouges sur les plus hautes tours visibles
    const tall = S.towers.filter((tw) => tw.x > 1000 && tw.x < 2100).sort((a, b) => b.h - a.h).slice(0, 4);
    S.beacons = tall.map((tw, i) => ({ tw, c: el('circle', { r: 4.5, fill: '#DC2626' }, tw.g), ph: i * 1.7 }));
  }
  function mkTower(parent, x, w, h, fill, edge, r) {
    const g = el('g', {}, parent);
    const body = el('rect', { x, width: w, fill }, g);
    const hi = el('rect', { x: x + w - 3, width: 3, fill: edge }, g);
    const sx = (x % 1920 + 1920) % 1920;
    return { g, body, hi, x, w, h, delay: 4.35 + (sx / 1920) * 0.85 + r() * 0.25 };
  }
  function buildArche() {
    const g = $('arche');
    const x = 1300, w = 260, h = 250, th = 34, top = GROUND - h;
    S.arche = { g, x, w, h };
    el('path', { d: `M${x + w} ${top} l38 -22 v${h} l-38 22 z`, fill: '#121212' }, g);
    el('path', { d: `M${x} ${top} l38 -22 h${w} l-38 22 z`, fill: '#1f1f1f' }, g);
    el('path', {
      d: `M${x} ${top} h${w} v${h} h-${w} z M${x + th} ${top + th} v${h - th} h${w - 2 * th} v-${h - th} z`,
      fill: '#1c1c1c', 'fill-rule': 'evenodd',
    }, g);
  }
  function buildArena() {
    const g = $('arena');
    const cx = 2880, rx = 560, ry = 360, base = GROUND - 14;
    S.arena = { cx, rx, ry, base };
    S.glow = el('ellipse', { cx, cy: GROUND + 10, rx: 820, ry: 170, fill: 'url(#glow)', opacity: 0 }, g);
    S.dome = el('path', { d: `M${cx - rx} ${base} A${rx} ${ry} 0 0 1 ${cx + rx} ${base} Z`, fill: 'url(#domeFill)', opacity: 0 }, g);
    S.ribs = [];
    for (let k = 1; k <= 6; k++) {
      const rr = rx * (k / 7);
      S.ribs.push(el('path', { d: `M${cx - rr} ${base} A${rr} ${ry} 0 0 1 ${cx + rr} ${base}`, fill: 'none', stroke: '#2f2f2f', 'stroke-width': 2 }, g));
    }
    for (let k = 1; k <= 3; k++) {
      const yy = base - ry * (k / 4);
      const hw = rx * Math.sqrt(1 - Math.pow((base - yy) / ry, 2));
      S.ribs.push(el('path', { d: `M${cx - hw} ${yy} L${cx + hw} ${yy}`, fill: 'none', stroke: '#2f2f2f', 'stroke-width': 2 }, g));
    }
    S.rim = el('path', { d: `M${cx - rx} ${base} A${rx} ${ry} 0 0 1 ${cx + rx} ${base}`, fill: 'none', stroke: '#E5E5E5', 'stroke-width': 3 }, g);
    S.plinth = el('rect', { x: cx - rx - 60, y: base - 4, width: 2 * rx + 120, height: GROUND - base + 4, fill: '#161616' }, g);
    S.strip = el('rect', { x: cx - rx - 60, y: base + 3, width: 2 * rx + 120, height: 4, fill: '#DC2626', opacity: 0 }, g);
    [S.rim, ...S.ribs].forEach((p) => { p._len = p.getTotalLength(); p.setAttribute('stroke-dasharray', p._len); });

    // portique d'arrivée
    const f = $('arenaFront');
    S.gantry = el('g', {}, f);
    el('rect', { x: 2786, y: 790, width: 8, height: 140, fill: '#E5E5E5' }, S.gantry);
    el('rect', { x: 2966, y: 790, width: 8, height: 140, fill: '#E5E5E5' }, S.gantry);
    el('rect', { x: 2780, y: 772, width: 200, height: 32, fill: 'url(#checker)' }, S.gantry);
    el('rect', { x: 2780, y: 772, width: 200, height: 32, fill: 'none', stroke: '#E5E5E5', 'stroke-width': 3 }, S.gantry);
    S.burst = [0, 1].map(() => el('circle', { cx: 2880, cy: 905, r: 10, fill: 'none', stroke: '#DC2626', 'stroke-width': 3, opacity: 0 }, f));
  }
  function buildRoutes() {
    const g = $('routes');
    const d5 = 'M160 948 C 420 950, 560 928, 800 934 S 1200 966, 1450 956 S 1900 928, 2150 938 S 2600 952, 2880 910';
    const d10 = 'M160 874 C 380 874, 470 846, 640 852 S 860 892, 1000 870 S 1180 836, 1330 852 S 1560 900, 1720 874 S 1960 840, 2120 860 S 2420 896, 2600 878 S 2800 902, 2880 902';
    S.startDot = el('g', {}, g);
    el('rect', { x: 150, y: 846, width: 6, height: 124, fill: '#E5E5E5' }, S.startDot);
    const mk = (d, color, w) => {
      const p = el('path', { d, fill: 'none', stroke: color, 'stroke-width': w, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
      p._len = p.getTotalLength();
      p.setAttribute('stroke-dasharray', `${p._len} ${p._len + 10}`);
      // longueur atteinte au bord droit du premier écran
      let lo = 0, hi = p._len;
      for (let i = 0; i < 40; i++) { const m = (lo + hi) / 2; if (p.getPointAtLength(m).x < 1830) lo = m; else hi = m; }
      p._mid = lo;
      const halo = el('circle', { r: 20, fill: 'none', stroke: color, 'stroke-width': 2, opacity: 0.45 }, g);
      const head = el('circle', { r: 10, fill: color }, g);
      return { p, head, halo };
    };
    S.r5 = mk(d5, '#FFFFFF', 6);
    S.r10 = mk(d10, '#DC2626', 7);
  }
  function buildNet() {
    const g = $('net');
    const r = rng(5);
    const { cx, rx, ry, base } = S.arena;
    const nodes = [];
    let guard = 0;
    while (nodes.length < 36 && guard++ < 5000) {
      const x = cx + (r() * 2 - 1) * rx * 0.88;
      const y = base - r() * ry * 0.86;
      if (Math.pow((x - cx) / (rx * 0.9), 2) + Math.pow((base - y) / (ry * 0.88), 2) > 1) continue;
      if (base - y < 26) continue;
      if (nodes.some((n) => Math.hypot(n.x - x, n.y - y) < 70)) continue;
      nodes.push({ x, y });
    }
    nodes.sort((a, b) => Math.hypot(a.x - 2880, a.y - 905) - Math.hypot(b.x - 2880, b.y - 905));
    const edges = [];
    const key = new Set();
    nodes.forEach((n, i) => {
      const near = nodes.map((m, j) => ({ j, d: Math.hypot(m.x - n.x, m.y - n.y) })).filter((o) => o.j !== i).sort((a, b) => a.d - b.d).slice(0, 2);
      near.forEach((o) => {
        const k = Math.min(i, o.j) + '-' + Math.max(i, o.j);
        if (!key.has(k)) { key.add(k); edges.push({ a: i, b: o.j }); }
      });
    });
    S.edges = edges.map((e) => ({ ...e, ln: el('line', { stroke: '#E5E5E5', 'stroke-width': 1.6, opacity: 0 }, g) }));
    S.nodes = nodes.map((n, i) => ({
      ...n, delay: 15.85 + i * 0.05,
      c: el('circle', { r: i % 4 === 0 ? 8 : 6, fill: i % 4 === 0 ? '#DC2626' : '#FFFFFF', opacity: 0 }, g),
    }));
  }
  function buildDots() {
    const g = $('dots');
    const r = rng(23);
    S.dots = [];
    const cols = 46, rows = 24, sp = 40, ox = (1920 - (cols - 1) * sp) / 2, oy = (1080 - (rows - 1) * sp) / 2;
    for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
      const x = ox + i * sp, y = oy + j * sp;
      // on laisse respirer le texte central et le bandeau du haut
      if (Math.pow((x - 960) / 640, 2) + Math.pow((y - 545) / 330, 2) < 1) continue;
      if (y < 110 || y > 1000) continue;
      S.dots.push({ c: el('circle', { cx: ox + i * sp, cy: oy + j * sp, r: 3, fill: '#1e1e1e' }, g), k: r(), lit: false });
    }
    S.dots.sort((a, b) => a.k - b.k);
  }

  // ---------- Animation du monde ----------
  function animWorld(t) {
    const world = $('world');
    const vis = t > 4.0 && t < 20.7;
    world.style.visibility = vis ? 'visible' : 'hidden';
    if (!vis) { $('pill5').style.opacity = 0; $('pill10').style.opacity = 0; return; }

    // caméra : légère poussée, panoramique vers l'arena, plongée finale
    const push = 1 + 0.035 * P(t, 4.3, 12, E.lin);
    const pan = 1920 * P(t, 11.9, 14.1, E.inOutCubic);
    const dive = P(t, 19.55, 20.55, E.inCubic);
    const sc = push * (1 + 0.7 * dive);
    const ox = 960, oy = 640;
    $('cam').setAttribute('transform', `translate(${ox} ${oy}) scale(${sc}) translate(${-ox - pan} ${-oy})`);
    $('par').setAttribute('transform', `translate(${pan * 0.38} 0)`);
    world.style.opacity = (1 - dive).toFixed(3);

    // tours qui montent
    for (const tw of S.towers) {
      const k = P(t, tw.delay, tw.delay + 1.0, E.outExpo);
      const h = tw.h * k;
      tw.body.setAttribute('y', GROUND - h); tw.body.setAttribute('height', Math.max(0, h));
      tw.hi.setAttribute('y', GROUND - h); tw.hi.setAttribute('height', Math.max(0, h));
    }
    for (const b of S.beacons) {
      const k = P(t, b.tw.delay + 0.9, b.tw.delay + 1.2);
      b.c.setAttribute('cx', b.tw.x + b.tw.w / 2); b.c.setAttribute('cy', GROUND - b.tw.h - 7);
      const blink = 0.35 + 0.65 * Math.pow(0.5 + 0.5 * Math.sin(t * 3.2 + b.ph), 3);
      b.c.setAttribute('opacity', (k * blink).toFixed(3));
    }
    const ka = P(t, 4.9, 6.0, E.outExpo);
    $('arche').setAttribute('transform', `translate(0 ${(1 - ka) * 300})`);
    $('arche').setAttribute('opacity', ka.toFixed(3));
    $('groundLine').setAttribute('opacity', P(t, 4.2, 4.8).toFixed(3));

    // parcours 5 km et 10 km
    const startK = P(t, 5.6, 6.0);
    S.startDot.setAttribute('opacity', startK.toFixed(3));
    const prog = (rt) => {
      const a = P(t, 6.0, 11.2, E.inOutCubic) * rt.p._mid;
      const b = P(t, 11.95, 14.05, E.inOutCubic) * (rt.p._len - rt.p._mid);
      return a + b;
    };
    for (const [rt, pill, below] of [[S.r5, $('pill5'), true], [S.r10, $('pill10'), false]]) {
      const L = prog(rt);
      rt.p.setAttribute('stroke-dashoffset', (rt.p._len - L).toFixed(2));
      const pt = rt.p.getPointAtLength(Math.max(0.01, L));
      const on = t > 6.0 ? 1 : 0;
      const doneFade = 1 - P(t, 14.3, 14.8);
      rt.head.setAttribute('cx', pt.x); rt.head.setAttribute('cy', pt.y);
      rt.halo.setAttribute('cx', pt.x); rt.halo.setAttribute('cy', pt.y);
      rt.head.setAttribute('opacity', on * doneFade);
      const pulse = (t * 1.6) % 1;
      rt.halo.setAttribute('r', 12 + pulse * 22);
      rt.halo.setAttribute('opacity', (on * doneFade * 0.6 * (1 - pulse)).toFixed(3));
      // pastille qui suit la tête du tracé (coordonnées écran)
      const scx = (pt.x - pan - ox) * sc + ox, scy = (pt.y - oy) * sc + oy;
      const pk = P(t, 6.5, 7.1, E.outBack) * (1 - P(t, 13.6, 14.0, E.inCubic));
      pill.style.left = (scx - 70) + 'px';
      pill.style.top = (scy + (below ? 46 : -50)) + 'px';
      pill.style.opacity = pk.toFixed(3);
      pill.style.transform = `translate(-50%,-50%) scale(${(0.6 + 0.4 * pk).toFixed(3)})`;
    }

    // arena
    const kd = P(t, 12.3, 13.6);
    S.dome.setAttribute('opacity', kd.toFixed(3));
    S.ribs.forEach((p, i) => {
      const k = P(t, 12.5 + i * 0.08, 13.9 + i * 0.08, E.inOutCubic);
      p.setAttribute('stroke-dashoffset', (p._len * (1 - k)).toFixed(2));
    });
    const kr = P(t, 12.4, 14.0, E.inOutCubic);
    S.rim.setAttribute('stroke-dashoffset', (S.rim._len * (1 - kr)).toFixed(2));
    const hit = P(t, 14.0, 14.5);
    S.strip.setAttribute('opacity', (P(t, 13.4, 14.0) * 0.6 + hit * 0.4).toFixed(3));
    S.glow.setAttribute('opacity', (P(t, 13.0, 14.0) * 0.45 + hit * 0.55 - 0.25 * P(t, 15.2, 16.5)).toFixed(3));
    const kg = P(t, 13.2, 13.9, E.outBack);
    S.gantry.setAttribute('transform', `translate(0 ${930 * (1 - kg)}) scale(1 ${kg.toFixed(4)})`);
    S.gantry.setAttribute('opacity', P(t, 13.2, 13.5).toFixed(3));
    S.burst.forEach((c, i) => {
      const k = P(t, 14.0 + i * 0.18, 15.1 + i * 0.18, E.outCubic);
      c.setAttribute('r', 10 + k * (180 + i * 90));
      c.setAttribute('opacity', (k > 0 ? (1 - k) * 0.9 : 0).toFixed(3));
    });

    // réseau : les participants se connectent après l'arrivée
    for (const n of S.nodes) {
      const k = P(t, n.delay, n.delay + 0.9, E.outExpo);
      n.cx = lerp(2880, n.x, k); n.cy = lerp(905, n.y, k);
      n.c.setAttribute('cx', n.cx.toFixed(1)); n.c.setAttribute('cy', n.cy.toFixed(1));
      n.c.setAttribute('opacity', (P(t, n.delay, n.delay + 0.2)).toFixed(3));
      n.k = k;
    }
    for (const e of S.edges) {
      const a = S.nodes[e.a], b = S.nodes[e.b];
      const st = Math.max(a.delay, b.delay) + 0.6;
      const k = P(t, st, st + 0.6, E.outCubic);
      e.ln.setAttribute('x1', a.cx); e.ln.setAttribute('y1', a.cy);
      e.ln.setAttribute('x2', lerp(a.cx, b.cx, k)); e.ln.setAttribute('y2', lerp(a.cy, b.cy, k));
      e.ln.setAttribute('opacity', (k > 0 ? 0.42 : 0).toFixed(3));
    }
  }

  // ---------- Scènes à plat ----------
  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }

  function animFlat(t) {
    // Scène 1 : ligne de départ
    const s1 = $('s1svg');
    s1.style.visibility = t < 4.4 ? 'visible' : 'hidden';
    const kl = P(t, 0.05, 1.0, E.outExpo);
    const ko = P(t, 3.7, 4.2, E.inCubic);
    const ln = $('startLine');
    ln.setAttribute('x1', lerp(960, 160, kl) + ko * 1600);
    ln.setAttribute('x2', lerp(960, 1760, kl) + ko * 400);
    ln.setAttribute('opacity', (1 - P(t, 4.0, 4.25)).toFixed(3));
    $('startCheck').setAttribute('width', 0);
    const z1 = 1 + 0.05 * P(t, 0, 4.2, E.lin);
    ['t1a', 't1b'].forEach((id) => { $(id).style.transform = `scale(${z1.toFixed(4)})`; });

    // transition rouge en biais
    const slash = $('slash');
    const k1 = P(t, 3.95, 4.6, E.inOutQuint);
    const k2 = P(t, 37.35, 38.0, E.inOutQuint);
    if (k1 > 0 && k1 < 1) {
      slash.style.visibility = 'visible';
      slash.style.transform = `translateX(${lerp(-1300, 2400, k1)}px) skewX(-18deg)`;
    } else if (k2 > 0 && k2 < 1) {
      slash.style.visibility = 'visible';
      slash.style.transform = `translateX(${lerp(2400, -1300, k2)}px) skewX(-18deg)`;
    } else slash.style.visibility = 'hidden';

    // barre rouge verticale (signature du deck) et HUD
    $('bar').style.transform = `scaleY(${P(t, 4.3, 5.1, E.outExpo).toFixed(4)})`;
    const hud = $('hud');
    const kh = win(t, 4.6, 5.3, 37.0, 37.4);
    hud.style.opacity = kh.toFixed(3);
    const pr = P(t, 4.6, 37.2, E.lin);
    $('progFill').style.width = (pr * 100).toFixed(3) + '%';
    $('progDot').style.left = (pr * 100).toFixed(3) + '%';

    // Scène 4 : compteur et points
    const dotsVis = t > 19.9 && t < 27.4;
    $('dots').style.visibility = dotsVis ? 'visible' : 'hidden';
    const kdots = win(t, 20.0, 20.7, 26.7, 27.25);
    $('dots').style.opacity = kdots.toFixed(3);
    $('center4').style.opacity = kdots.toFixed(3);
    const val = Math.round(10000 * P(t, 20.55, 23.7, E.outQuart));
    const shown = val >= 10000 ? 10000 : Math.round(val / 10) * 10;
    S.num.textContent = fmt(shown);
    const lit = Math.floor(S.dots.length * (shown / 10000));
    if (dotsVis) S.dots.forEach((d, i) => {
      const on = i < lit;
      if (on !== d.lit) { d.lit = on; d.c.setAttribute('fill', on ? '#DC2626' : '#1e1e1e'); d.c.setAttribute('r', on ? 3.6 : 3); }
    });
    const pop = P(t, 23.7, 24.2, E.outCubic) * (1 - P(t, 24.2, 24.9, E.inOutCubic));
    $('t4num').style.transform = `scale(${(1 + 0.04 * pop).toFixed(4)})`;
    $('t4num').style.color = pop > 0.02 ? '#FFFFFF' : '';

    // Scène 5 : surlignage et trait de parcours
    const hl = $('hl');
    const kh5 = P(t, 28.25, 28.85, E.outExpo);
    const ko5 = P(t, 32.7, 33.05, E.inCubic);
    hl.style.visibility = t > 28.2 && t < 33.1 ? 'visible' : 'hidden';
    hl.style.transform = `scaleX(${kh5.toFixed(4)}) scaleY(${(1 - ko5).toFixed(4)})`;
    const s5 = $('s5svg');
    s5.style.visibility = t > 28.6 && t < 33.2 ? 'visible' : 'hidden';
    const pen = $('pen');
    const kp = P(t, 28.75, 29.9, E.inOutCubic);
    pen.setAttribute('stroke-dashoffset', (pen._len * (1 - kp)).toFixed(2));
    const pp = pen.getPointAtLength(Math.max(0.01, pen._len * kp));
    $('penDot').setAttribute('cx', pp.x); $('penDot').setAttribute('cy', pp.y);
    s5.style.opacity = (1 - ko5).toFixed(3);

    // Scène 6 : lignes masquées
    const rdVis = t > 34.1 && t < 37.6;
    $('redacts').style.visibility = rdVis ? 'visible' : 'hidden';
    ['rd1', 'rd2', 'rd3'].forEach((id, i) => {
      const n = $(id);
      const k = P(t, 34.3 + i * 0.12, 34.95 + i * 0.12, E.outExpo);
      const o = P(t, 37.2, 37.5, E.inCubic);
      n.style.transformOrigin = '0 50%';
      n.style.transform = `scaleX(${k.toFixed(4)})`;
      n.style.opacity = (1 - o).toFixed(3);
      const w = n.offsetWidth;
      const ph = ((t - 34.3 + i * 0.25) / 1.7) % 1;
      n.firstElementChild.style.transform = `translateX(${(-260 + ph * (w + 520)).toFixed(1)}px)`;
    });

    // Scène 7 : séparateur et légère respiration du logo
    const ks = P(t, 39.3, 40.0, E.outExpo);
    $('sep7').setAttribute('x1', 960 - 180 * ks); $('sep7').setAttribute('x2', 960 + 180 * ks);
    $('s7svg').style.visibility = t > 39.2 ? 'visible' : 'hidden';
    const z7 = 1.06 - 0.06 * P(t, 37.85, 39.2, E.outCubic) - 0.015 * P(t, 39.2, 43, E.lin);
    $('t7a').style.transform = `scale(${z7.toFixed(4)})`;
  }

  function init() {
    // compteur : un seul masque dont le texte change
    const num = $('t4num');
    num.textContent = '';
    const w = document.createElement('span'); w.className = 'w';
    const wi = document.createElement('span'); wi.className = 'wi'; wi.textContent = '10 000';
    w.appendChild(wi); num.appendChild(w);
    S.num = wi;
    num.dataset.k = 'num';
    initTexts();
    const numItem = S.texts.find((x) => x.node === num);
    numItem.k = 'up'; numItem.parts = [wi];

    buildTowers(); buildArche(); buildArena(); buildRoutes(); buildNet(); buildDots();

    // surlignage calé sur le mot « l'agence »
    const ag = $('agence').getBoundingClientRect();
    const hl = $('hl');
    hl.style.left = (ag.left - 14) + 'px';
    hl.style.top = (ag.top + ag.height * 0.12) + 'px';
    hl.style.width = (ag.width + 28) + 'px';
    hl.style.height = (ag.height * 0.86) + 'px';
    // trait de parcours sous « l'écrire avec nous. »
    const l3 = $('t5c').getBoundingClientRect();
    const x0 = l3.left + 4, x1 = l3.right - 6, y = l3.bottom + 14;
    const pen = $('pen');
    const wdt = x1 - x0;
    pen.setAttribute('d', `M${x0} ${y} C ${x0 + wdt * 0.19} ${y - 18}, ${x0 + wdt * 0.34} ${y + 26}, ${x0 + wdt * 0.58} ${y + 4} S ${x0 + wdt * 0.87} ${y - 20}, ${x1} ${y - 4}`);
    pen._len = pen.getTotalLength();
    pen.setAttribute('stroke-dasharray', `${pen._len} ${pen._len + 10}`);
  }

  let ready = false;
  window.DURATION = DURATION;
  window.seek = function (t) {
    if (!ready) return false;
    animTexts(t);
    animWorld(t);
    animFlat(t);
    return true;
  };
  window.ready = document.fonts.ready.then(() => {
    init(); ready = true; window.seek(0); return true;
  });

  // aperçu dans un navigateur : ?t=12.5 fige une image, ?play lance la lecture
  const q = new URLSearchParams(location.search);
  window.ready.then(() => {
    if (q.has('t')) window.seek(+q.get('t'));
    else if (q.has('play')) {
      const t0 = performance.now();
      const loop = () => { const t = ((performance.now() - t0) / 1000) % DURATION; window.seek(t); requestAnimationFrame(loop); };
      loop();
    }
  });
})();
