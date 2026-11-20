# Exporte le montage pour DaVinci Resolve :
#  1. titres-flashs.mov : couche titres + flashs rouges, QuickTime Animation avec
#     transparence (Resolve ignore la transparence des ProRes 4444 générés par ffmpeg) ;
#  2. ROI_teaser_v2.fcpxml : plans broll/ sur la piste 1 avec leurs rampes de
#     vitesse, titres sur la piste 2, musique calée sur le drop.
# Les coups de zoom, la secousse et l'étalonnage restent à refaire dans Resolve.
# Usage : python3 export_davinci.py <dossier_titres> <dossier_sortie> <musique>
import os, sys, math, subprocess
from fractions import Fraction
from xml.sax.saxutils import quoteattr
import numpy as np, cv2
from plan import PLANS, FLASHS, T, FPS, K_FIN, MUSIQUE_DEBUT

ICI = os.path.dirname(os.path.abspath(__file__))
BROLL = os.path.abspath(os.environ.get('BROLL', os.path.join(ICI, '..', 'broll')))
titres, sortie, musique = sys.argv[1], os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3])
os.makedirs(sortie, exist_ok=True)
N = int(round(K_FIN * T * FPS))

# 1. couche titres + flashs
mov = os.path.join(sortie, 'titres-flashs.mov')
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', '1920x1080', '-r', str(FPS),
                       '-i', '-', '-c:v', 'qtrle', '-pix_fmt', 'argb', mov], stdin=subprocess.PIPE)
for i in range(N):
    t = i / FPS
    o = cv2.imread(os.path.join(titres, f'f{i:05d}.png'), cv2.IMREAD_UNCHANGED)
    if o.shape[2] == 3: o = np.dstack([o, np.full(o.shape[:2], 255, np.uint8)])
    o = o.astype(np.float32) / 255.0
    for kf in FLASHS:
        lt = t - kf * T
        if 0 <= lt < 0.4:
            a = 0.85 * math.exp(-lt / 0.09)
            rgb, al = o[..., :3], o[..., 3:4]
            na = al + a * (1 - al)
            o = np.dstack([(rgb * al + np.array([38, 38, 220], np.float32) / 255 * a * (1 - al)) / np.maximum(na, 1e-6), na])
    ff.stdin.write((np.clip(o, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()

# 2. FCPXML
def lisse(x): x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def src(entree, v, u, d):
    if not isinstance(v, tuple): return entree + v * u
    n = 200; p = u / n
    return entree + sum((v[0] + (v[1] - v[0]) * lisse((j + .5) * p / d)) * p for j in range(n))
def sec(x, base=FPS): return f'{Fraction(round(x * base), base)}s'.replace('/1s', 's') if round(x * base) % base else f'{round(x * base) // base}s'
def fr(f): return f'{f}/{FPS}s' if f % FPS else f'{f // FPS}s'

clips = sorted({p[2] for p in PLANS if p[2]})
res = ['<format id="r0" name="FFVideoFormat1080p25" frameDuration="1/25s" width="1920" height="1080"/>',
       '<format id="r1" frameDuration="1/24s" width="1280" height="720"/>']
for c in clips:
    res.append(f'<asset id="a_{c}" name="{c}" src={quoteattr("file://" + os.path.join(BROLL, c + ".mp4"))} start="0s" duration="5088/1000s" hasVideo="1" hasAudio="0" format="r1"/>')
res.append(f'<asset id="a_titres" name="titres-flashs" src={quoteattr("file://" + mov)} start="0s" duration="{fr(N)}" hasVideo="1" hasAudio="0" format="r0"/>')
res.append(f'<asset id="a_musique" name="Runaway" src={quoteattr("file://" + musique)} start="0s" duration="147s" hasVideo="0" hasAudio="1" audioSources="1" audioChannels="2" audioRate="44100"/>')

spine = []
for n, (ka, kb, c, e, v, opt) in enumerate(PLANS):
    f0, f1 = round(ka * T * FPS), round(kb * T * FPS)
    d = (f1 - f0) / FPS
    if c is None:
        spine.append(f'<gap name="Noir" offset="{fr(f0)}" duration="{fr(f1 - f0)}" start="0s"/>')
        continue
    pts = ''.join(f'<timept time="{fr(j)}" value="{src(e, v, j / FPS, d):.4f}s" interp="linear"/>'
                  for j in range(0, f1 - f0 + 1, 1 if isinstance(v, tuple) else f1 - f0))
    extra = ''
    if n == 0:
        extra = (f'<asset-clip ref="a_titres" lane="1" offset="0s" start="0s" duration="{fr(N)}" name="titres-flashs"/>'
                 f'<asset-clip ref="a_musique" lane="-1" offset="0s" start="{MUSIQUE_DEBUT:.4f}s" duration="{fr(N)}" name="Runaway"/>')
    spine.append(f'<asset-clip ref="a_{c}" name="{c}" offset="{fr(f0)}" start="0s" duration="{fr(f1 - f0)}"><timeMap>{pts}</timeMap>{extra}</asset-clip>')

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.9">
<resources>
{chr(10).join(res)}
</resources>
<library><event name="ROI teaser"><project name="ROI teaser v2">
<sequence format="r0" duration="{fr(N)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k"><spine>
{chr(10).join(spine)}
</spine></sequence></project></event></library>
</fcpxml>
'''
open(os.path.join(sortie, 'ROI_teaser_v2.fcpxml'), 'w').write(xml)
print('ok', mov)
