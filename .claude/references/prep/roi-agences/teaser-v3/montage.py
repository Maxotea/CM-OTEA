# Monte le teaser R.O.I. v3 à partir de plan.py :
#  - plans vidéo tirés des rushs OTEA (dossier RUSHS : extraits 1080p, LUT S-Log3 déjà
#    appliquée), exposition corrigée plan par plan (expo.json), rampes de vitesse avec
#    images intermédiaires par flux optique, coups de zoom aux coupes ;
#  - segments « masque » : la vidéo n'apparaît qu'à travers le texte ;
#  - couche motion design (PNG transparents de titres.html) par-dessus, flashs rouges.
# Usage : python3 montage.py <rushs> <expo.json> <titres> <masques> <master.mov>
import os, sys, json, math, subprocess
import numpy as np, cv2
from plan import SEGMENTS, FLASHS, T, FPS, K_FIN

RUSHS, EXPO, TITRES, MASQUES, SORTIE = sys.argv[1:6]
EXPO = json.load(open(EXPO))
W, H = 1920, 1080
NOIR = np.array([10, 10, 10], np.float32) / 255.0
ROUGE = np.array([38, 38, 220], np.float32) / 255.0   # #DC2626 en BGR

dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
_cache = {}

def images(clip, i0, i1):
    """Images i0..i1 du rush (on ne garde en mémoire que la fenêtre utile)."""
    cle = (clip, i0, i1)
    if cle not in _cache:
        _cache.clear()
        cap = cv2.VideoCapture(os.path.join(RUSHS, clip + '.mov'))
        cap.set(cv2.CAP_PROP_POS_FRAMES, i0)
        fr = []
        for _ in range(i1 - i0 + 1):
            ok, f = cap.read()
            if not ok: break
            fr.append(f)
        _cache[cle] = fr
    return _cache[cle]

_flux = {}
def intermediaire(fr, i, f):
    a, b = fr[i], fr[min(i + 1, len(fr) - 1)]
    if f < 0.04 or a is b: return a.astype(np.float32)
    if f > 0.96: return b.astype(np.float32)
    cle = (id(fr), i)
    if cle not in _flux:
        _flux.clear()
        ga, gb = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
        _flux[cle] = (dis.calc(ga, gb, None), dis.calc(gb, ga, None))
    fab, fba = _flux[cle]
    h, w = a.shape[:2]
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    aw = cv2.remap(a, gx - f * fab[..., 0], gy - f * fab[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    bw = cv2.remap(b, gx - (1 - f) * fba[..., 0], gy - (1 - f) * fba[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return (1 - f) * aw.astype(np.float32) + f * bw.astype(np.float32)

def lisse(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)

def position_source(entree, vitesse, u, duree):
    if not isinstance(vitesse, tuple): return entree + vitesse * u, vitesse
    v1, v2 = vitesse
    n = 200; pas = u / n if u > 0 else 0
    acc = sum((v1 + (v2 - v1) * lisse((j + 0.5) * pas / duree)) * pas for j in range(n))
    return entree + acc, v1 + (v2 - v1) * lisse(u / duree)

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIGNETTE = (1 - 0.25 * np.clip(r - 0.45, 0, 1) ** 1.6)[..., None]
def etalonne(img, gamma):
    x = np.clip(img, 0, 1) ** gamma                               # exposition du plan
    x = x + 0.16 * (x - 0.5) * (1 - np.abs(2 * x - 1))            # contraste en S
    l = x.mean(axis=2, keepdims=True)
    x = l + 0.88 * (x - l)                                         # saturation un peu tenue
    x = np.where(x < 0.04, x * 0.85, x)                            # noirs profonds
    return np.clip(x * VIGNETTE, 0, 1)

def cadre(src, zoom, dx=0.0, dy=0.0):
    h, w = src.shape[:2]
    s = (W / w) * zoom
    M = np.float32([[s, 0, W / 2 - s * w / 2 + dx], [0, s, H / 2 - s * h / 2 + dy]])
    return cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def segment(t):
    k = t / T
    for s in SEGMENTS:
        if s[0] <= k < s[1]: return s
    return SEGMENTS[-1]

def image_video(s, t):
    ka, kb, typ, clip, entree, vitesse, opt = s
    u, duree = t - ka * T, (kb - ka) * T
    e = EXPO[clip]; sfps = e['fps']
    ts, v = position_source(entree, vitesse, u, duree)
    # fenêtre d'images utile pour tout le segment
    fin, _ = position_source(entree, vitesse, duree, duree)
    i0 = max(0, int(min(entree, fin) * sfps) - 2); i1 = min(e['n'] - 1, int(max(entree, fin) * sfps) + 4)
    fr = images(clip, i0, i1)
    n = 1 if abs(v) * sfps / FPS < 1.6 else 3                     # flou de bouger si ça va vite
    acc = None
    for j in range(n):
        tj = ts + (j - (n - 1) / 2) * (v / FPS) / n
        p = min(max(tj * sfps - i0, 0), len(fr) - 1.001)
        i = int(p)
        img = intermediaire(fr, i, p - i)
        acc = img if acc is None else acc + img
    src = acc / n
    zoom, dx, dy = opt.get('zoom', 1.0), opt.get('dx', 0.0), opt.get('dy', 0.0)
    if 'push' in opt: zoom *= 1 + opt['push'] * lisse(u / duree)
    if 'punch' in opt: zoom *= 1 + 0.10 * (1 - lisse(u / 0.2))
    if 'shake' in opt:
        amp = 18 * math.exp(-u * 5)
        dx, dy = dx + amp * math.sin(u * 63), dy + amp * math.cos(u * 51)
    img = etalonne(cadre(src, zoom, dx, dy).astype(np.float32) / 255.0, e['gamma'])
    if 'gain' in opt: img = 1 - (1 - img) ** opt['gain']             # plus lumineux (vidéo dans les lettres)
    return img

def flash(img, t):
    for kf in FLASHS:
        lt = t - kf * T
        if 0 <= lt < 0.4:
            a = 0.85 * math.exp(-lt / 0.09)
            img = img * (1 - a) + ROUGE * a + 0.25 * a * img
    return np.clip(img, 0, 1)

def lire_png(dossier, i):
    p = os.path.join(dossier, f'f{i:05d}.png')
    if not os.path.exists(p): return None
    o = cv2.imread(p, cv2.IMREAD_UNCHANGED).astype(np.float32) / 255.0
    if o.shape[2] == 3: o = np.dstack([o, np.ones(o.shape[:2], np.float32)])
    return o

n_total = int(round(K_FIN * T * FPS))
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS),
                       '-i', '-', '-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le', '-vendor', 'apl0',
                       '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', SORTIE], stdin=subprocess.PIPE)
for i in range(n_total):
    t = i / FPS
    s = segment(t)
    if s[2] == 'm':
        img = np.broadcast_to(NOIR, (H, W, 3)).copy()
    else:
        img = image_video(s, t)
        if s[2] == 'k':
            m = lire_png(MASQUES, i)
            a = m[..., 3:4] if m is not None else 0
            img = np.broadcast_to(NOIR, (H, W, 3)) * (1 - a) + img * a
    o = lire_png(TITRES, i)
    if o is not None:
        a = o[..., 3:4]
        img = img * (1 - a) + o[..., :3] * a
    img = flash(img, t)
    ff.stdin.write((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
    if i % 100 == 0: print(f'{i}/{n_total}', flush=True)
ff.stdin.close(); ff.wait()
print('fini', SORTIE)
