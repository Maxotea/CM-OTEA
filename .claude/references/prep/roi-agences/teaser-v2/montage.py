# Monte le teaser R.O.I. v2 à partir de plan.py : plans broll/ remappés dans le
# temps (rampes de vitesse avec images intermédiaires par flux optique), coups de
# zoom aux coupes, flashs rouges, couche titres (PNG transparents) par-dessus.
# Sortie : flux d'images brutes vers ffmpeg (master ProRes 422 HQ).
# Usage : python3 montage.py <dossier_titres> <master.mov> [debut_s fin_s]
import os, sys, subprocess, math
import numpy as np, cv2
from plan import PLANS, FLASHS, T, FPS, K_FIN

ICI = os.path.dirname(os.path.abspath(__file__))
BROLL = os.path.join(ICI, '..', 'broll')
W, H = 1920, 1080
NOIR = np.array([10, 10, 10], np.float32) / 255.0
ROUGE = np.array([38, 38, 220], np.float32) / 255.0   # #DC2626 en BGR

titres, sortie = sys.argv[1], sys.argv[2]
borne = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else None

dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
_cache = {}

def images(clip):
    if clip not in _cache:
        _cache.clear()
        cap = cv2.VideoCapture(os.path.join(BROLL, clip + '.mp4'))
        fr = []
        while True:
            ok, f = cap.read()
            if not ok: break
            fr.append(f)
        _cache[clip] = (fr, cap.get(cv2.CAP_PROP_FPS) or 24.0)
    return _cache[clip]

_flux = {}
def intermediaire(fr, i, f):
    """Image source à la position fractionnaire i+f, par flux optique."""
    a, b = fr[i], fr[min(i + 1, len(fr) - 1)]
    if f < 0.04 or a is b: return a.astype(np.float32)
    if f > 0.96: return b.astype(np.float32)
    cle = (id(fr), i)
    if cle not in _flux:
        ga, gb = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
        _flux.clear()
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
    """Temps source (s) à l'instant u du plan, rampe intégrée numériquement."""
    if not isinstance(vitesse, tuple): return entree + vitesse * u, vitesse
    v1, v2 = vitesse
    n = 200; pas = u / n if u > 0 else 0
    acc = sum((v1 + (v2 - v1) * lisse((j + 0.5) * pas / duree)) * pas for j in range(n))
    return entree + acc, v1 + (v2 - v1) * lisse(u / duree)

# Étalonnage commun : contraste doux, saturation un peu tenue, vignette
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIGNETTE = (1 - 0.22 * np.clip(r - 0.45, 0, 1) ** 1.6)[..., None]
def etalonne(img):
    x = np.clip(img, 0, 1)
    x = x + 0.10 * (x - 0.5) * (1 - np.abs(2 * x - 1))          # courbe en S
    l = x.mean(axis=2, keepdims=True)
    x = l + 0.9 * (x - l)
    return np.clip(x * VIGNETTE, 0, 1)

def cadre(src, zoom, dx=0.0, dy=0.0):
    h, w = src.shape[:2]
    s = (W / w) * zoom
    M = np.float32([[s, 0, W / 2 - s * w / 2 + dx], [0, s, H / 2 - s * h / 2 + dy]])
    return cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)

def image_video(t):
    k = t / T
    for (ka, kb, clip, entree, vitesse, opt) in PLANS:
        if ka <= k < kb: break
    else:
        ka, kb, clip, opt = PLANS[-1][0], PLANS[-1][1], None, {'noir': 1}
    if clip is None:
        return np.broadcast_to(NOIR, (H, W, 3)).copy()
    u, duree = t - ka * T, (kb - ka) * T
    fr, sfps = images(clip)
    ts, v = position_source(entree, vitesse, u, duree)
    # flou de bouger quand ça va vite : on moyenne quelques sous-images
    n = 1 if abs(v) < 1.3 else 3
    acc = None
    for j in range(n):
        tj = ts + (j - (n - 1) / 2) * (v / FPS) / n
        p = min(max(tj * sfps, 0), len(fr) - 1.001)
        i = int(p)
        img = intermediaire(fr, i, p - i)
        acc = img if acc is None else acc + img
    src = acc / n
    zoom, dx, dy = 1.0, 0.0, 0.0
    if 'push' in opt: zoom *= 1 + opt['push'] * lisse(u / duree)
    if 'punch' in opt: zoom *= 1 + 0.09 * (1 - lisse(u / 0.22))
    if 'shake' in opt:
        amp = 16 * math.exp(-u * 5)
        dx, dy = amp * math.sin(u * 63), amp * math.cos(u * 51)
    return etalonne(cadre(src, zoom, dx, dy).astype(np.float32) / 255.0)

def flash(img, t):
    for kf in FLASHS:
        lt = t - kf * T
        if 0 <= lt < 0.4:
            a = 0.85 * math.exp(-lt / 0.09)
            img = img * (1 - a) + ROUGE * a + 0.25 * a * img
    return np.clip(img, 0, 1)

n_total = int(round(K_FIN * T * FPS))
i0, i1 = (0, n_total) if not borne else (int(borne[0] * FPS), int(borne[1] * FPS))
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS),
                       '-i', '-', '-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le', '-vendor', 'apl0',
                       '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', sortie], stdin=subprocess.PIPE)
for i in range(i0, i1):
    t = i / FPS
    img = flash(image_video(t), t)
    p = os.path.join(titres, f'f{i:05d}.png')
    if os.path.exists(p):
        o = cv2.imread(p, cv2.IMREAD_UNCHANGED).astype(np.float32) / 255.0
        if o.ndim == 3 and o.shape[2] == 4:
            a = o[..., 3:4]
            img = img * (1 - a) + o[..., :3] * a
        else:   # image opaque (la signature sur fond noir)
            img = o[..., :3] if o.ndim == 3 else np.repeat(o[..., None], 3, 2)
    ff.stdin.write((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
    if i % 100 == 0: print(f'{i}/{i1}', flush=True)
ff.stdin.close(); ff.wait()
print('fini', sortie)
