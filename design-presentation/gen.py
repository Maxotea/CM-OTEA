# -*- coding: utf-8 -*-
"""Génère les 10 planches .dc.html de la présentation OTEA Production."""
import io, json, os

INK      = "#12100E"   # fond, noir chaud
INK2     = "#1B1815"   # panneaux
CREME    = "#F0E9DE"
DIM      = "#9E9488"
ACCENT   = "#C88B52"   # oklch(~0.68 0.13 55), laiton
LINE     = "#2E2823"

SERIF = "'Bodoni Moda', Georgia, 'Times New Roman', serif"
SANS  = "'IBM Plex Sans', 'Helvetica Neue', Helvetica, sans-serif"
MONO  = "'IBM Plex Mono', 'SFMono-Regular', Consolas, monospace"

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500;6..96,600"
         "&family=IBM+Plex+Sans:wght@300;400;500"
         "&family=IBM+Plex+Mono:wght@400;500&display=swap")

W, H = 1440, 810

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
    a { color: %s; text-decoration: none; }
    a:hover { color: #E5AB6E; }
  </style>
</helmet>
<div style="width: %dpx; height: %dpx; box-sizing: border-box; padding: %dpx; background: %s; color: %s; font-family: %s; font-weight: 300; position: relative; overflow: hidden; display: flex; flex-direction: column;">
%s
</div>
</x-dc>
</body>
</html>
""" % (FONTS, ACCENT, W, H, pad, INK, CREME, SANS, corps))

def eyebrow(num, texte):
    return ("""  <div style="display: flex; align-items: center; gap: 16px; font-family: %s; font-size: 13px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: %s;">
    <span style="color: %s;">%s</span>
    <span style="width: 48px; height: 1px; background: %s;"></span>
    <span>%s</span>
  </div>""" % (MONO, DIM, ACCENT, num, LINE, texte))

def folio(n):
    return ("""  <div style="position: absolute; right: 96px; bottom: 76px; font-family: %s; font-size: 12px; letter-spacing: 0.14em; color: %s;">%s <span style="color: %s;">/ 10</span></div>""" % (MONO, LINE, n, LINE))

def titre(t, taille=58, mb=40):
    return ("""  <h1 style="margin: 0 0 %dpx; font-family: %s; font-weight: 500; font-size: %dpx; line-height: 1.08; letter-spacing: -0.01em; color: %s; text-wrap: pretty;">%s</h1>""" % (mb, SERIF, taille, CREME, t))

P = {}

# ------------------------------------------------------------ 01 couverture
P["Main"] = page("""  <div style="font-family: %s; font-size: 14px; font-weight: 500; letter-spacing: 0.32em; text-transform: uppercase; color: %s;">OTEA Production</div>
  <div style="flex-grow: 1;"></div>
  <div style="width: 92px; height: 2px; background: %s; margin-bottom: 44px;"></div>
  <h1 style="margin: 0 0 36px; font-family: %s; font-weight: 400; font-size: 78px; line-height: 1.1; letter-spacing: -0.015em; color: %s; max-width: 1100px;">Je m%sccupe de vos r%sseaux sociaux.<br>Vous vous occupez de votre m%stier.</h1>
  <div style="font-size: 21px; font-weight: 300; letter-spacing: 0.01em; color: %s;">Community management pour commerces et ind%spendants</div>
""" % (MONO, CREME, ACCENT, SERIF, CREME, "’", "é", "é", DIM, "é"))

# ------------------------------------------------------------ 02 le constat
P["Constat"] = page("""%s
  <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 80px; flex-grow: 1; align-items: center;">
    <div>
      %s
      <p style="margin: 0 0 32px; font-size: 25px; font-weight: 300; line-height: 1.5; color: %s;">Vous savez aussi que vous ne le ferez pas cette semaine.<br>Ni la semaine prochaine.</p>
      <p style="margin: 0; font-size: 19px; font-weight: 300; line-height: 1.65; color: %s; max-width: 520px; text-wrap: pretty;">Ce n%sest pas un manque de volont%s. C%sest qu%sun compte qui tient demande une heure par jour, tous les jours, et que cette heure vous ne l%savez pas.</p>
    </div>
    <div style="height: 100%%; display: flex; align-items: center; justify-content: center;">
      <div style="width: 1px; height: 64%%; background: linear-gradient(to bottom, %s 0%%, %s 50%%, %s 100%%);"></div>
    </div>
  </div>
%s""" % (eyebrow("01", "Le constat"),
         titre("Vous savez qu’il faut poster.", 58, 34),
         CREME, DIM, "’", "é", "’", "’", "’",
         INK, LINE, INK, folio("02")))

# ------------------------------------------------------------ 03 ce que je fais
BLOCS = [
    ("01", "Je construis le calendrier.", "Un mois à l’avance, calé sur ce qui se passe vraiment dans votre métier : la rentrée, les fêtes, votre saison forte."),
    ("02", "J’écris et je fabrique.", "Les textes, les visuels, les carrousels, les stories vidéo. À partir de vos photos, pas de photos achetées."),
    ("03", "Vous validez.", "Tout arrive en brouillon dans votre outil. Rien ne part sans votre accord."),
    ("04", "Je programme et je vous rends compte.", "Chaque mois, les chiffres et ce qu’ils veulent dire."),
]
lignes = "".join("""
    <div style="display: grid; grid-template-columns: 88px minmax(0, 1fr); gap: 32px; align-items: baseline; padding: 26px 0; border-top: 1px solid %s;">
      <div style="font-family: %s; font-size: 15px; font-weight: 500; letter-spacing: 0.14em; color: %s;">%s</div>
      <div>
        <span style="font-size: 24px; font-weight: 500; color: %s;">%s</span>
        <span style="font-size: 20px; font-weight: 300; color: %s;"> %s</span>
      </div>
    </div>""" % (LINE, MONO, ACCENT, n, CREME, t, DIM, c) for n, t, c in BLOCS)
P["Services"] = page("""%s
  <div style="height: 34px;"></div>
  %s
  <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center;">%s
    <div style="border-top: 1px solid %s;"></div>
  </div>
%s""" % (eyebrow("02", "Ce que je fais"), titre("Concrètement", 58, 8), lignes, LINE, folio("03")))

# ------------------------------------------------------------ 04 la méthode
ETAPES = [
    ("01", "On regarde votre mois.", "Ce qui arrive chez vous, ce qui bouge dans votre secteur."),
    ("02", "Je produis.", "Vous ne touchez à rien."),
    ("03", "Vous validez.", "Dix minutes, sur votre téléphone."),
    ("04", "Ça part.", "Aux bonnes heures, sur les bons réseaux."),
]
cols = "".join("""
    <div style="display: flex; flex-direction: column; gap: 18px;">
      <div style="display: flex; align-items: center; gap: 14px;">
        <span style="width: 9px; height: 9px; border-radius: 50%%; background: %s; flex-shrink: 0;"></span>
        <span style="font-family: %s; font-size: 34px; font-weight: 500; color: %s; line-height: 1;">%s</span>
      </div>
      <div style="font-size: 23px; font-weight: 500; color: %s; line-height: 1.25;">%s</div>
      <div style="font-size: 17px; font-weight: 300; color: %s; line-height: 1.55;">%s</div>
    </div>""" % (ACCENT, SERIF, ACCENT, n, CREME, t, DIM, c) for n, t, c in ETAPES)
P["Methode"] = page("""%s
  <div style="height: 34px;"></div>
  %s
  <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center;">
    <div style="height: 1px; background: %s; margin-bottom: -5px; margin-left: 4px;"></div>
    <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 48px;">%s
    </div>
  </div>
%s""" % (eyebrow("03", "La méthode"), titre("Quatre temps, tous les mois", 54, 10),
         LINE, cols, folio("04")))

# ------------------------------------------------------------ 05 ce qui me distingue
P["Distinction"] = page("""%s
  <div style="height: 30px;"></div>
  %s
  <div style="flex-grow: 1; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 56px; align-content: start;">

    <div style="display: flex; flex-direction: column; gap: 16px;">
      <div style="font-family: %s; font-size: 24px; font-weight: 500; color: %s; line-height: 1.2;">Vos vraies photos, anim%ses.</div>
      <div style="width: 40px; height: 1px; background: %s;"></div>
      <div style="font-size: 16px; font-weight: 300; line-height: 1.6; color: %s;">Je pars de vos propres photos et je leur donne du mouvement. Votre client reconna%st votre salle, votre vitrine, votre %squipe. Pas un d%scor achet%s sur une banque d%simages.</div>
      <div style="height: 1px; background: %s; margin: 6px 0;"></div>
      <div style="font-family: %s; font-style: italic; font-size: 16px; font-weight: 400; line-height: 1.55; color: %s;">En %schange, une seule chose vous est demand%se : alimenter un album partag%s. Dix photos par mois, prises au t%sl%sphone, sans mise en sc%sne. C%sest le seul effort qui reste de votre c%st%s, et c%sest lui qui fait toute la diff%srence entre un compte qui vous ressemble et un compte interchangeable.</div>
    </div>

    <div style="display: flex; flex-direction: column; gap: 16px;">
      <div style="font-family: %s; font-size: 24px; font-weight: 500; color: %s; line-height: 1.2;">Un calendrier cal%s sur votre m%stier.</div>
      <div style="width: 40px; height: 1px; background: %s;"></div>
      <div style="font-size: 16px; font-weight: 300; line-height: 1.6; color: %s;">Pas un planning g%sn%srique. Ce qui se passe chez vous, quand %sa se passe.</div>
    </div>

    <div style="display: flex; flex-direction: column; gap: 16px;">
      <div style="font-family: %s; font-size: 24px; font-weight: 500; color: %s; line-height: 1.2;">Vous gardez la main.</div>
      <div style="width: 40px; height: 1px; background: %s;"></div>
      <div style="font-size: 16px; font-weight: 300; line-height: 1.6; color: %s;">Tout est en brouillon. Vous validez. Rien ne sort de votre compte sans que vous l%sayez vu.</div>
    </div>

  </div>
%s""" % (eyebrow("04", "Ce qui me distingue"),
         titre("Trois choses que les autres ne font pas", 50, 44),
         SERIF, ACCENT, "é", LINE, CREME,
         "î", "é", "é", "é", "’",
         LINE, SERIF, DIM,
         "é", "é", "é", "é", "é", "è", "’", "ô", "é", "’", "é",
         SERIF, ACCENT, "é", "é", LINE, CREME, "é", "é", "ç",
         SERIF, ACCENT, LINE, CREME, "’",
         folio("05")))

# ------------------------------------------------------------ 06 la preuve
CHIFFRES = [
    ("14", "contenus publiés par mois sur la formule Signature."),
    ("5",  "stories vidéo fabriquées depuis vos propres photos."),
    ("1",  "compte rendu chiffré, le premier lundi du mois."),
    ("0",  "publication partie sans votre validation."),
]
cases = "".join("""
      <div style="display: flex; flex-direction: column; gap: 20px;">
        <div style="font-family: %s; font-size: 132px; font-weight: 400; line-height: 0.86; color: %s; letter-spacing: -0.02em;">%s</div>
        <div style="height: 1px; background: %s;"></div>
        <div style="font-size: 16px; font-weight: 300; line-height: 1.55; color: %s;">%s</div>
      </div>""" % (SERIF, ACCENT, n, LINE, DIM, c) for n, c in CHIFFRES)
P["Preuve"] = page("""%s
  <div style="height: 34px;"></div>
  %s
  <div style="flex-grow: 1; display: flex; align-items: center;">
    <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 44px; width: 100%%;">%s
    </div>
  </div>
%s""" % (eyebrow("05", "La preuve"), titre("Ce qui sort réellement", 54, 10), cases, folio("06")))

# ------------------------------------------------------------ 07 les formules
FORMULES = [
    ("Entretien", "290 €", ["1 réseau", "8 contenus publiés par mois",
      "4 stories vidéo animées depuis vos photos", "calendrier saisonnier",
      "compte rendu mensuel"], "Sans reel.", False),
    ("Signature", "690 €", ["2 réseaux", "14 contenus publiés par mois",
      "5 stories vidéo", "1 reel", "calendrier calé sur votre actualité",
      "compte rendu mensuel chiffré"], None, True),
    ("Croissance", "1 190 €", ["2 à 3 réseaux", "20 contenus publiés par mois",
      "8 stories vidéo", "2 reels", "une demi-journée de tournage par trimestre",
      "compte rendu chiffré et point trimestriel"], None, False),
]
def colonne(nom, prix, points, note, star):
    bord = ACCENT if star else LINE
    fond = INK2 if star else "transparent"
    badge = ("""
        <div style="position: absolute; top: -9px; left: 24px; background: %s; padding: 0 10px; font-family: %s; font-size: 10px; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: %s;">Le plus choisi</div>""" % (INK, MONO, ACCENT)) if star else ""
    lst = "".join("""
          <li style="display: flex; gap: 10px; align-items: baseline;"><span style="color: %s; flex-shrink: 0;">&middot;</span><span>%s</span></li>""" % (ACCENT, p) for p in points)
    fin = ("""
        <div style="margin-top: auto; padding-top: 14px; font-size: 14px; font-weight: 500; color: %s;">%s</div>""" % (ACCENT, note)) if note else ""
    return """
      <div style="position: relative; display: flex; flex-direction: column; border: 1px solid %s; background: %s; padding: 26px 24px 22px; box-sizing: border-box;">%s
        <div style="font-family: %s; font-size: 12px; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; color: %s;">%s</div>
        <div style="font-family: %s; font-size: 42px; font-weight: 400; color: %s; line-height: 1.1; margin: 10px 0 2px;">%s</div>
        <div style="font-family: %s; font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase; color: %s; margin-bottom: 20px;">par mois</div>
        <ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 9px; font-size: 15px; font-weight: 300; line-height: 1.4; color: %s;">%s
        </ul>%s
      </div>""" % (bord, fond, badge, MONO, DIM, nom, SERIF, CREME, prix,
                   MONO, DIM, CREME, lst, fin)
P["Formules"] = page("""%s
  <div style="height: 22px;"></div>
  %s
  <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 26px;">%s
  </div>
  <div style="display: flex; gap: 22px; align-items: baseline; margin-top: 24px; padding-top: 18px; border-top: 1px solid %s;">
    <div style="font-size: 16px; font-weight: 500; color: %s; white-space: nowrap;">Reel suppl%smentaire : 190 %s l%sunit%s.</div>
    <div style="font-size: 15px; font-weight: 300; color: %s; line-height: 1.5;">Le tournage se fait chez vous, avec vous. Je ne vends un reel que le jour o%s vous %stes pr%st %s passer devant la cam%sra, jamais %s l%savance.</div>
  </div>
  <div style="margin-top: 16px; font-size: 12px; font-weight: 300; line-height: 1.6; color: %s;">
    Tarifs hors taxes. Engagement de trois mois. En dessous de trois mois, aucun compte ne bouge assez pour qu%son puisse en tirer quoi que ce soit.<br>
    Toutes les formules supposent un album partag%s aliment%s de dix photos par mois. Album vide, mois non produit et non factur%s.
  </div>
%s""" % (eyebrow("06", "Les formules"), titre("Trois façons de travailler ensemble", 40, 24),
         "".join(colonne(*f) for f in FORMULES), LINE,
         ACCENT, "é", "€", "’", "é", DIM,
         "ù", "ê", "ê", "à", "é", "à", "’",
         LINE, "’", "é", "é", "é", folio("07")), pad=72)

# ------------------------------------------------------------ 08 le calcul
CALCULS = [
    ("Un salon, un institut.", "Un client qui revient toutes les cinq semaines vaut douze passages par an. Quelques nouveaux clients fidélisés couvrent l’année."),
    ("Une prestation à forte valeur.", "Un fitting de golf à 160 €. Deux rendez-vous remboursent la formule Entretien, cinq remboursent Signature."),
    ("Une agence immobilière.", "Un seul mandat rentré par les réseaux couvre largement plusieurs mois."),
]
rows = "".join("""
    <div style="display: grid; grid-template-columns: 300px minmax(0, 1fr); gap: 40px; align-items: baseline; padding: 24px 0; border-top: 1px solid %s;">
      <div style="font-family: %s; font-size: 22px; font-weight: 500; color: %s; line-height: 1.25;">%s</div>
      <div style="font-size: 18px; font-weight: 300; line-height: 1.6; color: %s;">%s</div>
    </div>""" % (LINE, SERIF, ACCENT, t, CREME, c) for t, c in CALCULS)
P["Rentabilite"] = page("""%s
  <div style="height: 30px;"></div>
  %s
  <p style="margin: 0 0 12px; font-size: 20px; font-weight: 300; line-height: 1.55; color: %s; max-width: 720px;">La bonne question n%sest pas ce que %sa co%ste. C%sest combien de clients il faut pour que ce soit rembours%s.</p>
  <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center;">%s
    <div style="border-top: 1px solid %s;"></div>
  </div>
%s""" % (eyebrow("07", "Ce que %sa doit vous rapporter" % "ç"),
         titre("Le calcul %s faire" % "à", 54, 20), DIM,
         "’", "ç", "û", "’", "é", rows, LINE, folio("08")))

# ------------------------------------------------------------ 09 comment on démarre
DEPART = [
    ("01", "On se parle trente minutes.", "Votre métier, votre saison, vos clients."),
    ("02", "Vous m’ouvrez un album partagé.", "Vous y déposez vos photos au fil de l’eau, depuis votre téléphone. Dix par mois suffisent."),
    ("03", "Je vous envoie le premier mois.", "Le calendrier complet, les visuels, les textes. Vous voyez exactement ce que vous achetez avant de signer."),
    ("04", "On lance.", "Vous validez, %ca part, et vous n%sy repensez plus." % ("ç", "’")),
]
etapes = "".join("""
    <div style="display: grid; grid-template-columns: 76px minmax(0, 1fr); gap: 28px; align-items: baseline; padding: 22px 0; border-top: 1px solid %s;">
      <div style="font-family: %s; font-size: 30px; font-weight: 400; color: %s; line-height: 1;">%s</div>
      <div>
        <div style="font-size: 23px; font-weight: 500; color: %s; margin-bottom: 6px;">%s</div>
        <div style="font-size: 17px; font-weight: 300; line-height: 1.55; color: %s;">%s</div>
      </div>
    </div>""" % (LINE, SERIF, ACCENT, n, CREME, t, DIM, c) for n, t, c in DEPART)
P["Demarrage"] = page("""%s
  <div style="height: 30px;"></div>
  %s
  <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center;">%s
    <div style="border-top: 1px solid %s;"></div>
  </div>
%s""" % (eyebrow("08", "Comment on démarre"),
         titre("Quatre %stapes, et c%sest parti" % ("é", "’"), 54, 6),
         etapes, LINE, folio("09")))

# ------------------------------------------------------------ 10 contact
P["Contact"] = page("""%s
  <div style="flex-grow: 1;"></div>
  <h1 style="margin: 0 0 48px; font-family: %s; font-weight: 400; font-size: 92px; line-height: 1; letter-spacing: -0.015em; color: %s;">On en parle ?</h1>
  <div style="width: 92px; height: 2px; background: %s; margin-bottom: 40px;"></div>
  <div style="font-family: %s; font-size: 13px; font-weight: 500; letter-spacing: 0.28em; text-transform: uppercase; color: %s; margin-bottom: 14px;">OTEA Production</div>
  <div style="font-size: 27px; font-weight: 300; color: %s; margin-bottom: 46px;">contact@oteaproduction.com</div>
  <div style="font-size: 18px; font-weight: 300; line-height: 1.55; color: %s;">Le premier mois se pr%spare avant de signer. Vous jugez sur pi%sces.</div>
%s""" % (eyebrow("09", "Contact"), SERIF, CREME, ACCENT, MONO, DIM,
         ACCENT, DIM, "é", "è", folio("10")))

ORDRE = ["Main", "Constat", "Services", "Methode", "Distinction",
         "Preuve", "Formules", "Rentabilite", "Demarrage", "Contact"]
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for nom in ORDRE:
    io.open(nom + ".dc.html", "w", encoding="utf-8").write(P[nom])

XS = [0, 1560, 3120, 4680]
arts = []
for i, nom in enumerate(ORDRE):
    arts.append({"file": nom + ".dc.html", "x": XS[i % 4], "y": (i // 4) * 970,
                 "w": W, "h": H})
json.dump({"artboards": arts, "launch": {"view": "canvas"}},
          io.open("canvas.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("planches :", len(ORDRE))
