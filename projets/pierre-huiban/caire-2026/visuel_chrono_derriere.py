# Visuel Cairo 15/11/2026 : photo N&B + masque + glow, chrono géant DERRIÈRE Pierre (son détourage repasse devant), rang en bas. Usage : python3 visuel_chrono_derriere.py DOSSIER(cairo-arrivee.jpg, cut-cairo.png) SORTIE.jpg
import sys
sys.path.insert(0, 'scripts')
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import hyrox_visuel as hv
S = sys.argv[1]; sortie = sys.argv[2]
src = Image.open(f'{S}/cairo-arrivee.jpg').convert('RGB')
m = Image.open(f'{S}/cut-cairo.png').getchannel('A').resize(src.size)
box = (8, 330, 1128, 1730)
W, H = 1080, 1350
img = src.crop(box).resize((W, H), Image.LANCZOS)
mm = m.crop(box).resize((W, H))
fond = hv.etalonner(img, mm)

DAWN, BLANC, PALE = (232, 99, 43), (246, 243, 237), (210, 205, 197)
# Calque DERRIÈRE Pierre : le chrono géant et le label
der = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(der)
f = hv.police('titre', 330)
txt = '1:06:12'
while d.textlength(txt, font=f) > W - 70: f = hv.police('titre', f.size - 6)
bb = d.textbbox((0, 0), txt, font=f)
x = (W - (bb[2] - bb[0])) // 2 - bb[0]; y = 168 - bb[1]
d.text((x, y), txt, font=f, fill=BLANC + (255,))
hv._espace(d, (60, 96), 'HYROX CAIRO · PRO MEN', hv.police('label', 30), DAWN + (255,), 4)
# Pierre repasse devant : alpha du texte coupé par son masque (léger flou du bord)
pm = np.asarray(mm.filter(ImageFilter.GaussianBlur(1.5)), np.float32) / 255
a = np.asarray(der.getchannel('A'), np.float32) * (1 - pm)
der.putalpha(Image.fromarray(a.astype(np.uint8)))
out = fond.convert('RGBA'); out.alpha_composite(der)

# Calque DEVANT, en bas sur le sol sombre : rang et catégorie, pied
dv = ImageDraw.Draw(out)
fs, fsm = hv.police('mono', 46), hv.police('mono_m', 36)
yb = H - 112
dv.line([(60, yb), (W - 60, yb)], fill=(110, 110, 110), width=2)
hv._espace(dv, (60, yb + 30), 'ROAD TO HONG KONG · JUNE 2027', hv.police('label', 22), PALE, 2.8)
x = 60; ys = yb - 84
for i, (fort, reste) in enumerate([('30th', ' / 176'), ('4th', ' AG 35-39')]):
    dv.text((x, ys), fort, font=fs, fill=DAWN); x += dv.textlength(fort, font=fs)
    dv.text((x, ys + 8), reste, font=fsm, fill=BLANC); x += dv.textlength(reste, font=fsm)
    if i == 0:
        x += 26; dv.text((x, ys + 4), '·', font=fsm, fill=PALE); x += dv.textlength('·', font=fsm) + 26
out.convert('RGB').save(sortie, quality=94, subsampling=0)
print(sortie)
