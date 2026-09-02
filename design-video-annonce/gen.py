# -*- coding: utf-8 -*-
"""Génère les 7 planches .dc.html de la présentation « vidéo d'annonce »
pour La Galerie Immobilière, dans LEUR charte (relevée le 19/08/2026 sur
leurs publications) : sable #D4BBA5, encre #292527, Playfair Display en
bas-de-casse, filet tracé à main levée, doodles au trait, pied
« puteaux · paris ouest ».

    python3 gen.py        # écrit Main.dc.html, Constat.dc.html, ... et canvas.json
"""
import json

SABLE  = "#D4BBA5"
CLAIR  = "#DCC8B4"
SOMBRE = "#B2997C"   # filets et bordures, jamais du texte
LABEL  = "#7A664E"   # libellés mono, lisibles sur le sable
ENCRE  = "#292527"
ENCRE2 = "#4A4340"   # texte courant, un cran plus doux que le titre
NOIR   = "#151313"   # le disque du logo

SERIF = "'Playfair Display', Georgia, 'Times New Roman', serif"
SANS  = "'Nunito Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO  = "'Space Mono', 'SFMono-Regular', Consolas, monospace"
FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400"
         "&family=Nunito+Sans:wght@300;400;600"
         "&family=Space+Mono:wght@400&display=swap")

W, H = 1440, 810
N = 7

FILET = ("""<svg width="190" height="12" viewBox="0 0 190 12" fill="none" style="display: block; margin: 18px 0 0;">"""
         """<path d="M2 7 C 30 3, 55 10, 85 6 S 140 4, 188 7" stroke="%s" stroke-width="2.6" stroke-linecap="round"></path></svg>""" % ENCRE)

def doodle(nom, taille=44):
    """Doodles au trait, leur signature graphique. Trait fin, un peu tremblé."""
    s = 'width="%d" height="%d" viewBox="0 0 48 48" fill="none" stroke="%s" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"' % (taille, taille, ENCRE)
    d = {
        "maison":  '<path d="M9 24 L24 10 L39 24"></path><path d="M13 21 V39 H35 V21"></path><path d="M21 39 V29 H27 V39"></path>',
        "cle":     '<circle cx="16" cy="18" r="7"></circle><path d="M21 23 L38 40"></path><path d="M31 33 L35 29"></path><path d="M35 37 L39 33"></path>',
        "loupe":   '<circle cx="20" cy="20" r="11"></circle><path d="M28 28 L40 40"></path>',
        "camera":  '<rect x="8" y="16" width="26" height="18" rx="3"></rect><path d="M34 22 L41 18 V32 L34 28"></path>',
        "horloge": '<circle cx="24" cy="24" r="14"></circle><path d="M24 14 V24 L31 28"></path>',
        "personne":'<circle cx="24" cy="16" r="7"></circle><path d="M10 40 C 12 30, 36 30, 38 40"></path>',
        "lien":    '<path d="M20 28 L28 20"></path><path d="M17 23 L13 27 A 6 6 0 0 0 21 35 L25 31"></path><path d="M31 25 L35 21 A 6 6 0 0 0 27 13 L23 17"></path>',
        "plume":   '<path d="M12 36 C 14 22, 26 12, 40 10 C 38 24, 28 34, 14 36"></path><path d="M12 36 L26 22"></path>',
        "coche":   '<path d="M10 25 L20 35 L38 14"></path>',
        "envoi":   '<path d="M8 24 L40 10 L30 40 L24 28 Z"></path><path d="M24 28 L40 10"></path>',
    }[nom]
    return "<svg %s>%s</svg>" % (s, d)

def page(corps, pad=96):
    return ("""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="%s">
  <style>
    body { margin: 0; }
    a { color: %s; text-decoration: none; border-bottom: 1px solid %s; }
    a:hover { color: %s; }
  </style>
</helmet>
<div style="width: %dpx; height: %dpx; box-sizing: border-box; padding: %dpx; background: %s; color: %s; font-family: %s; font-weight: 400; position: relative; overflow: hidden; display: flex; flex-direction: column;">
%s
</div>
</x-dc>
</body>
</html>
""" % (FONTS, ENCRE, SOMBRE, SOMBRE, W, H, pad, SABLE, ENCRE, SANS, corps))

def eyebrow(num, texte):
    return ("""  <div style="display: flex; align-items: center; gap: 14px; font-family: %s; font-size: 13px; letter-spacing: 0.16em; color: %s;">
    <span style="color: %s;">%s</span>
    <span style="width: 40px; height: 1px; background: %s;"></span>
    <span>%s</span>
  </div>""" % (MONO, LABEL, ENCRE, num, SOMBRE, texte))

def pied(n, pad=96):
    return ("""  <div style="position: absolute; left: %dpx; bottom: 56px; font-family: %s; font-size: 13px; letter-spacing: 0.22em; color: %s;">puteaux · paris ouest</div>
  <div style="position: absolute; right: %dpx; bottom: 56px; font-family: %s; font-size: 13px; letter-spacing: 0.14em; color: %s;">%d / %d</div>""" % (pad, MONO, LABEL, pad, MONO, LABEL, n, N))

def titre(t, taille=56, mb=36):
    return ("""  <div style="margin: 0 0 %dpx;">
    <h1 style="margin: 0; font-family: %s; font-weight: 500; font-size: %dpx; line-height: 1.12; letter-spacing: -0.005em; color: %s; text-wrap: pretty;">%s</h1>
    %s
  </div>""" % (mb, SERIF, taille, ENCRE, t, FILET))

def para(t, taille=20, couleur=ENCRE2, maxw=560, mb=0):
    return """<p style="margin: 0 0 %dpx; font-size: %dpx; font-weight: 400; line-height: 1.6; color: %s; max-width: %dpx; text-wrap: pretty;">%s</p>""" % (mb, taille, couleur, maxw, t)

P = {}

# ------------------------------------------------------------ 01 couverture
P["Main"] = page("""%s
  <div style="flex-grow: 1;"></div>
  <div style="display: flex; align-items: flex-end; gap: 72px;">
    <div style="flex-grow: 1;">
      <h1 style="margin: 0; font-family: %s; font-weight: 500; font-size: 84px; line-height: 1.08; letter-spacing: -0.01em; color: %s; max-width: 980px;">une vidéo par bien.<br>rien à filmer.</h1>
      %s
      <p style="margin: 34px 0 0; font-size: 22px; font-weight: 400; line-height: 1.5; color: %s; max-width: 640px;">Vos annonces en vidéo, à partir des photos que vous avez déjà.</p>
    </div>
    <div style="flex-shrink: 0; padding-bottom: 8px;">%s</div>
  </div>
  <div style="height: 88px;"></div>
%s""" % (eyebrow("La Galerie Immobilière", "OTEA Production"), SERIF, ENCRE, FILET, ENCRE2, doodle("maison", 120), pied(1)))

# ------------------------------------------------------------ 02 le constat
def ligne_doodle(nom, texte):
    return """      <div style="display: flex; align-items: center; gap: 22px;">
        <div style="flex-shrink: 0; width: 64px; height: 64px; display: flex; align-items: center; justify-content: center; border: 1px solid %s; border-radius: 50%%;">%s</div>
        <div style="font-family: %s; font-size: 24px; font-weight: 400; color: %s; line-height: 1.3;">%s</div>
      </div>""" % (SOMBRE, doodle(nom, 34), SERIF, ENCRE, texte)

P["Constat"] = page("""%s
  <div style="height: 28px;"></div>
  <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 88px; flex-grow: 1; align-items: center;">
    <div>
      %s
      %s
      %s
    </div>
    <div style="display: flex; flex-direction: column; gap: 26px; padding-left: 24px; border-left: 1px solid %s;">
%s
%s
%s
      <div style="margin-top: 10px; font-family: %s; font-size: 13px; letter-spacing: 0.16em; color: %s;">résultat : le reel attend. le mandat, non.</div>
    </div>
  </div>
%s""" % (eyebrow("02", "Le constat"),
         titre("vos biens se vendent en photos.", 52, 28),
         para("Une vidéo d'annonce demande une demi-journée, un tournage et quelqu'un devant la caméra.", 21, ENCRE, 520, 18),
         para("Alors elle ne se fait pas. Le bien sort en photos, comme tous les autres, et il ne se distingue de rien.", 19, ENCRE2, 520),
         SOMBRE,
         ligne_doodle("horloge", "une demi-journée à trouver"),
         ligne_doodle("personne", "quelqu'un devant la caméra"),
         ligne_doodle("camera", "un tournage à caler, un montage à attendre"),
         MONO, LABEL, pied(2)))

# ------------------------------------------------------------ 03 ce qu'on propose
def bloc(nom, t, texte):
    return """    <div style="display: flex; flex-direction: column; gap: 14px; padding: 28px 26px 26px; border: 1px solid %s; background: %s; box-sizing: border-box;">
      <div>%s</div>
      <div style="font-family: %s; font-size: 26px; font-weight: 500; color: %s; line-height: 1.2;">%s</div>
      <div style="font-size: 16px; line-height: 1.55; color: %s;">%s</div>
    </div>""" % (SOMBRE, CLAIR, doodle(nom, 36), SERIF, ENCRE, t, ENCRE2, texte)

P["Proposition"] = page("""%s
  <div style="height: 22px;"></div>
  %s
  <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 22px; flex-grow: 1; align-content: center; padding-bottom: 60px;">
%s
%s
%s
%s
  </div>
%s""" % (eyebrow("03", "Ce qu'on vous propose"),
         titre("trente secondes. vos photos. votre charte.", 50, 34),
         bloc("camera", "vos photos, animées", "Les photos de l'annonce prennent vie : un mouvement subtil, la lumière, les rideaux. La caméra reste fixe."),
         bloc("maison", "votre charte", "Le sable, votre typographie, votre logo. On reconnaît La Galerie dès la première seconde."),
         bloc("plume", "le texte à l'écran", "Une phrase par pièce, lisible sans le son. La plupart des reels se regardent en silence."),
         bloc("lien", "deux formats", "Vertical pour Instagram, Facebook et TikTok. Horizontal pour votre site et les portails."),
         pied(3, 72)), pad=72)

# ------------------------------------------------------------ 04 storyboard
def vignette(titre_v, texte_v, carte=False, photo="linear-gradient(160deg, #6E5A4A 0%, #3E332C 55%, #2A2320 100%)"):
    if carte:
        haut = """<div style="height: 100%%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; padding: 0 14px; box-sizing: border-box;">
          <div style="width: 40px; height: 40px; border-radius: 50%%; background: %s; border: 2px solid %s;"></div>
          <div style="font-family: %s; font-size: 8px; letter-spacing: 0.14em; color: %s; text-align: center;">%s</div>
          <div style="font-family: %s; font-size: 15px; font-weight: 500; color: %s; text-align: center; line-height: 1.2;">%s</div>
        </div>""" % (NOIR, SOMBRE, MONO, LABEL, titre_v, SERIF, ENCRE, texte_v)
        return """      <div style="width: 156px; height: 277px; background: %s; border: 1px solid %s; box-sizing: border-box; overflow: hidden; position: relative;">%s</div>""" % (SABLE, SOMBRE, haut)
    return """      <div style="width: 156px; height: 277px; background: %s; border: 1px solid %s; box-sizing: border-box; overflow: hidden; position: relative; display: flex; flex-direction: column;">
        <div style="height: 152px; background: %s; position: relative;">
          <div style="position: absolute; right: 12px; top: 22px; width: 26px; height: 26px; border-radius: 50%%; background: %s; border: 2px solid %s;"></div>
          <div style="position: absolute; left: 12px; bottom: 10px; font-family: %s; font-size: 8px; letter-spacing: 0.12em; color: %s;">votre photo, animée</div>
        </div>
        <div style="flex-grow: 1; padding: 14px 12px 10px; box-sizing: border-box; display: flex; flex-direction: column;">
          <div style="font-family: %s; font-size: 15px; font-weight: 500; color: %s; line-height: 1.15;">%s</div>
          <svg width="44" height="6" viewBox="0 0 44 6" fill="none" style="display: block; margin: 6px 0 6px;"><path d="M1 3 C 10 1, 20 5, 43 3" stroke="%s" stroke-width="1.4" stroke-linecap="round"></path></svg>
          <div style="font-size: 9.5px; line-height: 1.4; color: %s;">%s</div>
          <div style="margin-top: auto; font-family: %s; font-size: 6.5px; letter-spacing: 0.16em; color: %s;">puteaux · paris ouest</div>
        </div>
      </div>""" % (SABLE, SOMBRE, photo, NOIR, SABLE, MONO, CLAIR, SERIF, ENCRE, titre_v, ENCRE, ENCRE2, texte_v, MONO, LABEL)

P["Storyboard"] = page("""%s
  <div style="height: 22px;"></div>
  %s
  <div style="display: flex; gap: 20px; align-items: flex-start;">
%s
%s
%s
%s
%s
%s
  </div>
  <div style="margin-top: 34px; display: flex; gap: 40px; font-family: %s; font-size: 13px; letter-spacing: 0.14em; color: %s;">
    <span>intro 2,5 s</span><span>six plans de 5 s, en fondu</span><span>fin 3,5 s</span><span style="color: %s;">32 secondes en tout</span>
  </div>
%s""" % (eyebrow("04", "À quoi ça ressemble"),
         titre("un bien, six plans, trente-deux secondes.", 46, 30),
         vignette("à vendre · [ville]", "[type de bien]", carte=True),
         vignette("le salon", "La lumière, le critère qu'on sous-estime le plus."),
         vignette("la cuisine", "Là où tout se passe.", photo="linear-gradient(160deg, #8A7663 0%, #4B3F36 60%, #2A2320 100%)"),
         vignette("la terrasse", "Un extérieur, à quelques minutes de Paris.", photo="linear-gradient(160deg, #9C8B76 0%, #5A4C40 55%, #2A2320 100%)"),
         vignette("la chambre", "Le calme, sans renoncer à la ville.", photo="linear-gradient(160deg, #7A6656 0%, #3E332C 60%, #2A2320 100%)"),
         vignette("la galerie immobilière", "visite sur rendez-vous", carte=True),
         MONO, LABEL, ENCRE, pied(4, 72)), pad=72)

# ------------------------------------------------------------ 05 rien d'inventé
def regle(t, texte):
    return """    <div style="display: flex; gap: 20px; align-items: flex-start;">
      <div style="flex-shrink: 0; margin-top: 4px;">%s</div>
      <div>
        <div style="font-family: %s; font-size: 24px; font-weight: 500; color: %s; line-height: 1.25; margin-bottom: 6px;">%s</div>
        <div style="font-size: 16.5px; line-height: 1.55; color: %s; max-width: 480px;">%s</div>
      </div>
    </div>""" % (doodle("coche", 30), SERIF, ENCRE, t, ENCRE2, texte)

P["Honnete"] = page("""%s
  <div style="height: 24px;"></div>
  <div style="display: grid; grid-template-columns: 5fr 7fr; gap: 80px; flex-grow: 1; align-items: center; padding-bottom: 70px;">
    <div>
      %s
      %s
    </div>
    <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 34px 36px;">
%s
%s
%s
%s
    </div>
  </div>
%s""" % (eyebrow("05", "Ce qu'on s'interdit"),
         titre("rien d'inventé.", 60, 30),
         para("Un acquéreur qui visite doit retrouver exactement ce qu'il a vu. C'est la seule façon de faire de la vidéo qui serve le mandat.", 19, ENCRE2, 440),
         regle("vos vraies photos", "Jamais une image de banque, jamais une image générée. Les photos de l'annonce, rien d'autre."),
         regle("la caméra reste fixe", "Aucune pièce réinventée, aucun angle que la photo ne montre pas. Le mouvement est dans l'image, pas autour."),
         regle("aucun visage créé", "On ne fabrique jamais une personne. Le jour où vous voulez apparaître, on vous filme pour de vrai."),
         regle("aucun chiffre qui ne soit sur l'annonce", "Vous choisissez ce qui s'affiche : le prix, la surface, ou rien du tout."),
         pied(5)))

# ------------------------------------------------------------ 06 le déroulé
def etape(num, nom, t, texte):
    return """    <div style="display: flex; flex-direction: column; gap: 12px; padding-top: 22px; border-top: 1px solid %s;">
      <div style="display: flex; align-items: center; justify-content: space-between;">
        <span style="font-family: %s; font-size: 13px; letter-spacing: 0.18em; color: %s;">%s</span>
        %s
      </div>
      <div style="font-family: %s; font-size: 24px; font-weight: 500; color: %s; line-height: 1.2;">%s</div>
      <div style="font-size: 16px; line-height: 1.55; color: %s;">%s</div>
    </div>""" % (SOMBRE, MONO, ENCRE, num, doodle(nom, 30), SERIF, ENCRE, t, ENCRE2, texte)

P["Deroule"] = page("""%s
  <div style="height: 22px;"></div>
  %s
  <div style="flex-grow: 1;"></div>
  <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 30px;">
%s
%s
%s
%s
  </div>
  <div style="flex-grow: 1;"></div>
  <div style="padding-top: 30px; font-family: %s; font-size: 22px; font-weight: 400; font-style: italic; color: %s;">Chaque nouveau mandat peut avoir sa vidéo la semaine de sa mise en ligne.</div>
  <div style="height: 34px;"></div>
%s""" % (eyebrow("06", "Comment ça se passe"),
         titre("quatre étapes, aucune de votre côté sauf la première.", 44, 34),
         etape("01", "envoi", "vous envoyez le lien", "Le lien de l'annonce en ligne, et ce que vous souhaitez voir affiché."),
         etape("02", "plume", "on relève et on écrit", "Vos photos, une phrase par pièce, relue avant tout montage."),
         etape("03", "horloge", "la vidéo arrive en brouillon", "Sous cinq jours ouvrés, dans votre espace de validation. Rien ne part sans votre accord."),
         etape("04", "coche", "vous validez, elle sort", "Et la version horizontale vous est livrée pour votre site."),
         SERIF, ENCRE, pied(6, 72)), pad=72)

# ------------------------------------------------------------ 07 essayez
P["Essai"] = page("""%s
  <div style="height: 24px;"></div>
  <div style="display: grid; grid-template-columns: 7fr 5fr; gap: 80px; flex-grow: 1; align-items: start;">
    <div>
      %s
      %s
      %s
      <div style="margin-top: 34px; display: flex; flex-direction: column; gap: 10px;">
        <div style="font-family: %s; font-size: 13px; letter-spacing: 0.18em; color: %s;">pour essayer</div>
        <div style="font-family: %s; font-size: 24px; font-weight: 500; color: %s; line-height: 1.3;">Envoyez le lien d'une annonce à Maxime, par WhatsApp ou à <a href="mailto:contact@oteaproduction.com">contact@oteaproduction.com</a>.</div>
      </div>
    </div>
    <div style="display: flex; flex-direction: column; gap: 18px; padding: 30px 30px 28px; border: 1px solid %s; background: %s; box-sizing: border-box; margin-top: 8px;">
      <div style="font-family: %s; font-size: 13px; letter-spacing: 0.18em; color: %s;">ensuite</div>
      <div style="font-family: %s; font-size: 22px; font-weight: 500; color: %s; line-height: 1.3;">deux vidéos par mois, incluses</div>
      <div style="font-size: 16px; line-height: 1.55; color: %s;">Sur les créneaux reel déjà prévus dans votre accompagnement. Sans supplément.</div>
      <div style="height: 1px; background: %s; margin: 4px 0;"></div>
      <div style="font-family: %s; font-size: 22px; font-weight: 500; color: %s; line-height: 1.3;">au-delà</div>
      <div style="display: flex; gap: 28px; align-items: baseline;">
        <div><span style="font-family: %s; font-size: 34px; color: %s;">149 €</span><span style="font-size: 14px; color: %s;"> la vidéo</span></div>
        <div><span style="font-family: %s; font-size: 34px; color: %s;">490 €</span><span style="font-size: 14px; color: %s;"> les quatre</span></div>
      </div>
      <div style="font-family: %s; font-size: 11px; letter-spacing: 0.1em; color: %s;">tarifs hors taxes</div>
    </div>
  </div>
%s""" % (eyebrow("07", "Essayez"),
         titre("essayez sur un de vos biens.", 58, 30),
         para("Le premier est offert. Vous choisissez le bien, on fait la vidéo, et vous jugez sur pièce.", 21, ENCRE, 560, 16),
         para("Elle arrive dans la semaine, en brouillon, à votre charte, avec la version horizontale pour votre site.", 18, ENCRE2, 560),
         MONO, LABEL, SERIF, ENCRE,
         SOMBRE, CLAIR, MONO, LABEL, SERIF, ENCRE, ENCRE2, SOMBRE, SERIF, ENCRE,
         SERIF, ENCRE, ENCRE2, SERIF, ENCRE, ENCRE2, MONO, LABEL,
         pied(7)))

ORDRE = ["Main", "Constat", "Proposition", "Storyboard", "Honnete", "Deroule", "Essai"]
for nom in ORDRE:
    with open(nom + ".dc.html", "w", encoding="utf-8") as f:
        f.write(P[nom])

canvas = {"artboards": [], "launch": {"view": "canvas"}}
for i, nom in enumerate(ORDRE):
    canvas["artboards"].append({"file": nom + ".dc.html", "x": (i % 4) * 1560, "y": (i // 4) * 970, "w": W, "h": H})
with open("canvas.json", "w", encoding="utf-8") as f:
    json.dump(canvas, f, indent=2, ensure_ascii=False)
print("ok", len(ORDRE), "planches")
