# Cairo 15/11/2026 : trois pistes typo (A dossard, B tableau de stade, C chrono officiel). Maxime a retenu la B.
# Usage, depuis la racine : python3 projets/pierre-huiban/caire-2026/visuel_pistes.py DOSSIER (cairo-arrivee.jpg, cut-cairo.png)
# Photo du sled (retenue le 15/11) : --photo cairo-sled --box 0,200,1336,1870 --nettoyage "" --base 530 --bas-etroit 430 [--couleur]
import sys
sys.path.insert(0, 'scripts')
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import hyrox_visuel as hv
S = sys.argv[1]
CF = 'fonts/big-shoulders/'  # piste B ; Boldonse, Tektur, Geist (pistes A et C) ne sont pas dans le dépôt
F = {'expanded': 'fonts/archivo/Archivo_Expanded-Black.ttf', 'archivo': 'fonts/archivo/Archivo-Regular.ttf',
     'shoulders': CF + 'BigShoulders-Bold.ttf', 'shoulders_r': CF + 'BigShoulders-Regular.ttf',
     'boldonse': CF + 'Boldonse-Regular.ttf', 'tektur': CF + 'Tektur-Medium.ttf', 'geist': CF + 'GeistMono-Bold.ttf'}
W, H = 1080, 1350
BL, GR = (245, 245, 243), (175, 175, 172)
def _opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut
# --photo NOM : NOM.jpg et son détourage cut-NOM.png dans DOSSIER ; --box x0,y0,x1,y1 (4:5) ;
# --nettoyage "y0:y1,x0:x1;..." zones du détourage à effacer ; --base Y bas du mot CAIRO.
PHOTO = _opt('--photo', 'cairo-arrivee')
src = Image.open(f'{S}/{PHOTO}.jpg').convert('RGB')
m = Image.open(f'{S}/cut-{PHOTO}.png' if PHOTO != 'cairo-arrivee' else f'{S}/cut-cairo.png').getchannel('A').resize(src.size)
box = tuple(int(v) for v in _opt('--box', '8,330,1128,1730').split(','))
NETTOYAGE = _opt('--nettoyage', ':352,:;522:550,926:962')
BASE = int(_opt('--base', '560'))
COULEUR = '--couleur' in sys.argv
if COULEUR:
    # Version couleur : la photo d'origine, contraste un peu relevé et glow léger, sans désaturer
    from PIL import ImageEnhance
    _c = ImageEnhance.Contrast(src.crop(box).resize((W, H), Image.LANCZOS)).enhance(1.12)
    _a = np.asarray(_c, np.float32) / 255
    _y = _a.mean(-1)
    _hl = np.clip((_y - 0.6) / 0.4, 0, 1) ** 1.4
    _g = np.asarray(Image.fromarray((_hl * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(28)), np.float32) / 255
    _a = 1 - (1 - _a) * (1 - np.clip(_g * 0.35, 0, 1)[..., None])
    fond = Image.fromarray((np.clip(_a, 0, 1) * 255).astype(np.uint8))
else:
    fond = hv.etalonner(src.crop(box).resize((W, H), Image.LANCZOS), m.crop(box).resize((W, H)))
mm = m.crop(box).resize((W, H))
# Nettoyage du détourage : un spot au-dessus de la tête et un reflet près du O avaient été pris pour Pierre
_a = np.asarray(mm, np.float32).copy()
# Arrivée : rien au-dessus de y=352 (spot pris pour Pierre) ; reflet à droite du coude (le coude finit à x=923)
def _sl(t):
    a, b = t.split(':')
    return slice(int(a) if a else None, int(b) if b else None)
for zone in filter(None, NETTOYAGE.split(';')):
    ys, xs = zone.split(',')
    _a[_sl(ys), _sl(xs)] = 0
mm = Image.fromarray(_a.astype(np.uint8))
# Bord du détourage durci (seuil) : un bord trop doux laissait un liseré de lettre autour de Pierre ; l'élargir faisait un contour sombre
_pm = np.clip((np.asarray(mm, np.float32) / 255 - 0.3) / 0.3, 0, 1)
pm = np.asarray(Image.fromarray((_pm * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255

def font(k, s): return ImageFont.truetype(F[k], s)

def fit(d, t, k, largeur, start=600, track=0):
    s = start
    while True:
        f = font(k, s)
        w = sum(d.textlength(c, font=f) + track for c in t) - track
        if w <= largeur or s < 40: return f, w
        s -= 4

def spaced(d, xy, t, f, fill, track, **kw):
    x, y = xy
    for c in t:
        d.text((x, y), c, font=f, fill=fill, **kw); x += d.textlength(c, font=f) + track
    return x

def derriere(layer):
    a = np.asarray(layer.getchannel('A'), np.float32) * (1 - pm)
    layer.putalpha(Image.fromarray(a.astype(np.uint8))); return layer

def italique(layer, k=0.18, yc=300):
    return layer.transform(layer.size, Image.AFFINE, (1, k, -k * yc, 0, 1, 0), Image.BICUBIC)

def piste(n):
    out = fond.convert('RGBA')
    der = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(der)
    dev = Image.new('RGBA', (W, H)); v = ImageDraw.Draw(dev)
    if n == 'A':   # dossard : Archivo Expanded Black, très large et lourd
        f, w = fit(d, 'CAIRO', 'expanded', W - 90)
        bb = d.textbbox((0, 0), 'CAIRO', font=f)
        d.text(((W - w) / 2 - bb[0], 500 - bb[3]), 'CAIRO', font=f, fill=BL)
        spaced(d, (48, 120), 'HYROX  ·  PRO MEN  ·  14.11.2026', font('archivo', 26), BL, 6)
        fc, wc = fit(v, '1:06:12', 'expanded', 640, 200)
        v.text((48, H - 300), '1:06:12', font=fc, fill=BL)
        spaced(v, (52, H - 150), '30TH / 176    4TH AG 35-39', font('archivo', 30), GR, 5)
        spaced(v, (52, H - 92), 'ROAD TO HONG KONG', font('archivo', 22), GR, 8)
    elif n == 'B':  # tableau de stade : Big Shoulders condensé, italique de vitesse
        f, w = fit(d, 'CAIRO', 'shoulders', W - 60, 900, 6)
        bb = d.textbbox((0, 0), 'CAIRO', font=f)
        spaced(d, ((W - w) / 2, BASE - bb[3]), 'CAIRO', f, BL, 6)
        der = italique(der, 0.18, 330)
        dd = ImageDraw.Draw(der)
        spaced(dd, (44, 70), 'HYROX PRO MEN · EGYPT', font('shoulders_r', 40), BL, 8)
        etroit = int(_opt('--bas-etroit', '0'))   # largeur max du bloc du bas, quand Pierre est en pied au centre
        if etroit:
            fc, wc = fit(v, '1:06:12', 'shoulders', etroit, 230)
            bbc = v.textbbox((0, 0), '1:06:12', font=fc)
            yb = H - 150 - bbc[3]
            v.text((40, yb), '1:06:12', font=fc, fill=BL)
            spaced(v, (46, H - 140), '30TH OF 176  ·  4TH AG 35-39', font('shoulders_r', 34), GR, 3)
            spaced(v, (46, H - 92), 'ROAD TO HONG KONG', font('shoulders_r', 34), GR, 3)
        else:
            fc = font('shoulders', 230)
            v.text((40, H - 345), '1:06:12', font=fc, fill=None, stroke_width=3, stroke_fill=BL)
            spaced(v, (46, H - 110), '30TH OF 176   ·   4TH AG 35-39   ·   ROAD TO HONG KONG', font('shoulders_r', 36), GR, 3)
        dev = italique(dev, 0.12, H - 230)
    else:          # chrono officiel : Boldonse + Geist Mono
        f, w = fit(d, 'CAIRO', 'boldonse', W - 80)
        bb = d.textbbox((0, 0), 'CAIRO', font=f)
        d.text(((W - w) / 2 - bb[0], 510 - bb[3]), 'CAIRO', font=f, fill=BL)
        spaced(d, (48, 120), 'HYROX / PRO MEN', font('geist', 28), BL, 4)
        v.rectangle([40, H - 260, W - 40, H - 258], fill=GR)
        spaced(v, (44, H - 240), 'TIME', font('geist', 24), GR, 4)
        spaced(v, (44, H - 205), '1:06:12', font('geist', 96), BL, 2)
        spaced(v, (560, H - 240), 'RANK', font('geist', 24), GR, 4)
        spaced(v, (560, H - 205), '30/176', font('geist', 64), BL, 1)
        spaced(v, (560, H - 130), 'AG 35-39  4TH', font('geist', 30), BL, 2)
        spaced(v, (44, H - 70), 'ROAD TO HONG KONG · 06.2027', font('geist', 22), GR, 3)
    out.alpha_composite(derriere(der))
    # --tout-derriere : chrono et stats passent aussi derrière Pierre (photo en pied, jambes au premier plan)
    out.alpha_composite(derriere(dev) if '--tout-derriere' in sys.argv else dev)
    return out.convert('RGB')

PISTES = 'ABC' if '--toutes' in sys.argv else 'B'   # A et C demandent des polices hors dépôt
ims = {n: piste(n) for n in PISTES}
for n, im in ims.items(): im.save(f'{S}/piste-{n}-{PHOTO}{"-couleur" if COULEUR else ""}.jpg', quality=93)
if len(ims) < 3: sys.exit(0)
pl = Image.new('RGB', (3 * 540 + 40, 675 + 70), (20, 20, 20)); dp = ImageDraw.Draw(pl)
for i, n in enumerate('ABC'):
    pl.paste(ims[n].resize((540, 675), Image.LANCZOS), (10 + i * 550, 60))
    dp.text((10 + i * 550, 14), n, font=font('expanded', 34), fill=BL)
pl.save(f'{S}/pistes.jpg', quality=92)
