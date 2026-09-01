#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pierre Huiban — générateur des slides de carrousel (1080×1350).

Reproduit **à l'identique** le gabarit déjà en ligne sur le compte, relevé au
pixel sur les slides du 26/08 (post 358752104) :

    fond Pitch Black #0A0A0A · accent Rouge Sang #DC2626 · corps gris #9A9A9A
    surtitre rouge, interlettré, capitales · titre capitales, 1re ligne blanche
    puis rouge · corps gris avec une portion en gras · pied « n/8 » + « SWIPE → »
    la dernière slide s'inverse : fond rouge, texte noir

⚠️ Le gabarit visuel n'a **pas** été redessiné : Pierre n'a jamais reproché la
   DA, il a reproché les **textes** (« des fautes », « ça ne me ressemble pas »).
   Refaire la DA sans la lui faire valider serait refaire l'erreur d'origine.
   Ce qui change ici, c'est la langue et le registre : **anglais, première
   personne, chaleureux**, conformément à sa propre story de référence.
   Plus de « LFG », plus de « Pas d'excuses », plus d'impératif sec.

Usage (sandbox Higgsfield) :
    curl -sL -o pc.py <URL du script>
    python3 pc.py sled 1 2 3        # -> o/sled-01.png …
    python3 pc.py profiles          # les 8 slides
    python3 pc.py hongkong

Le script télécharge la police tout seul s'il ne la trouve pas.
"""
import os
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
NOIR = (10, 10, 10)
ROUGE = (220, 38, 38)
BLANC = (255, 255, 255)
GRIS = (154, 154, 154)
GRIS_PIED = (80, 80, 80)

M = 94                      # marge gauche/droite
Y_KICKER = 470
Y_TITRE = 590
Y_PIED = 1240

FD = "f"
FONT = FD + "/archivo.ttf"
FONT_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/"
            "archivo/Archivo%5Bwdth,wght%5D.ttf")


def _bootstrap():
    os.makedirs(FD, exist_ok=True)
    os.makedirs("o", exist_ok=True)
    if not os.path.exists(FONT):
        urllib.request.urlretrieve(FONT_URL, FONT)


def af(size, weight=700, width=100):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight, width])  # Archivo : axes [Weight, Width]
    except Exception:
        pass
    return f


def ls_text(d, x, y, txt, font, fill, tracking=0.0):
    """Texte lettre à lettre — le seul moyen d'obtenir l'interlettrage du kit."""
    for ch in txt:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    return x


def ls_width(d, txt, font, tracking=0.0):
    return sum(d.textlength(c, font=font) for c in txt) + tracking * (len(txt) - 1)


def fit(d, lines, maxw, start=126, floor=54):
    """Plus grand corps de titre qui tient en pleine largeur."""
    s = start
    while s > floor:
        f = af(s, 700)
        if max(ls_width(d, l, f, -s * 0.012) for l in lines) <= maxw:
            return s, f
        s -= 3
    return floor, af(floor, 700)


def wrap(d, txt, font, maxw):
    out, cur = [], ""
    for mot in txt.split():
        essai = (cur + " " + mot).strip()
        if d.textlength(essai, font=font) <= maxw or not cur:
            cur = essai
        else:
            out.append(cur)
            cur = mot
    if cur:
        out.append(cur)
    return out


def rich(d, x, y, segments, taille, couleur, maxw, interligne):
    """Corps de texte gris avec des portions en gras, balisées **ainsi**."""
    reg, gras = af(taille, 400), af(taille, 700)
    mots = []
    for i, seg in enumerate(segments.split("**")):
        f = gras if i % 2 else reg
        for mot in seg.split(" "):
            if mot:
                mots.append((mot, f))
    ligne, cx = [], x
    for mot, f in mots:
        lg = d.textlength(mot + " ", font=f)
        if cx + lg > x + maxw and ligne:
            for mx, mt, mf in ligne:
                d.text((mx, y), mt, font=mf, fill=couleur)
            y += interligne
            ligne, cx = [], x
        ligne.append((cx, mot, f))
        cx += lg
    for mx, mt, mf in ligne:
        d.text((mx, y), mt, font=mf, fill=couleur)
    return y + interligne


def slide(path, kicker, titre, corps, n, total=8, finale=False):
    fond = ROUGE if finale else NOIR
    c_kicker = NOIR if finale else ROUGE
    c_titre1 = NOIR if finale else BLANC
    c_titre2 = NOIR if finale else ROUGE
    c_corps = NOIR if finale else GRIS
    c_pied = NOIR if finale else GRIS_PIED

    im = Image.new("RGB", (W, H), fond)
    d = ImageDraw.Draw(im)
    maxw = W - 2 * M

    fk = af(30, 700)
    ls_text(d, M, Y_KICKER, kicker.upper(), fk, c_kicker, 8)

    lignes = [l.upper() for l in titre]
    s, ft = fit(d, lignes, maxw)
    lh = int(s * 1.10)
    y = Y_TITRE
    for i, l in enumerate(lignes):
        ls_text(d, M, y, l, ft, c_titre1 if i == 0 else c_titre2, -s * 0.012)
        y += lh

    rich(d, M, y + 74, corps, 38, c_corps, maxw, 52)

    fp = af(24, 500)
    d.text((M, Y_PIED), "%d/%d" % (n, total), font=fp, fill=c_pied)
    if n == 1:
        libelle = "SWIPE →"
        ls_text(d, W - M - ls_width(d, libelle, af(26, 700), 6), Y_PIED,
                libelle, af(26, 700), ROUGE, 6)
    im.save(path)


# --- Contenus, réécrits en anglais dans sa voix réelle (20/08/2026) ---------
# (kicker, lignes de titre, corps)
SLED = [
 ("SLED PUSH", ["THE STATION", "THAT ENDS", "YOUR RACE"],
  "Four fixes. Not one of them asks you to be stronger."),
 ("WHAT I GOT WRONG", ["IT'S NOT A", "STRENGTH", "PROBLEM"],
  "For two years I pushed harder instead of pushing better. The sled doesn't "
  "reward strength, **it rewards position**."),
 ("FIX 01", ["GET LOW", "AND STAY", "LOW"],
  "Arms long, hips low, chest close to the floor. **The angle does the work**, "
  "not the legs."),
 ("FIX 02", ["SHORT STEPS.", "NO PAUSE."],
  "Small fast steps keep the sled loaded. Long strides make you stop and "
  "restart, over and over."),
 ("FIX 03", ["NEVER LET", "IT STOP"],
  "Restarting a sled that has stopped **costs three times more** than keeping "
  "it moving. This is the one that changed my races."),
 ("FIX 04", ["BREATHE", "BEFORE,", "NOT AFTER"],
  "Set your breathing in the last 200 m of the run. Arrive already in debt and "
  "the sled will collect it."),
 ("SAME SLED", ["TWO", "COMPLETELY", "DIFFERENT", "RACES"],
  "Same weight, same legs. The difference is how you stand behind it — and it "
  "is worth far more than any extra session."),
 ("ROAD TO HONG KONG", ["TRY THEM", "THIS WEEK"],
  "Then tell me which one changed the most for you. **I read and answer "
  "everything**. Thank you for being here."),
]

PROFILES = [
 ("SEPTEMBER", ["EVERYONE", "TRAINS WHAT", "THEY'RE", "GOOD AT"],
  "I did it for two years. Four profiles, four priorities. Find yours."),
 ("HOW TO FIND YOURS", ["YOUR LAST", "RACE TIME", "KNOWS"],
  "Take your splits and look at where you lost it. **The answer is already "
  "written in there** — and it's never the one you'd have picked."),
 ("PROFILE 01", ["THE", "RUNNER"],
  "You hold the 8 km fine and fall apart on the stations. Your block: strength "
  "endurance. Sled, burpees, lunges."),
 ("PROFILE 02", ["THE", "STRONG ONE"],
  "The stations are easy, the running is not. Your block: **running volume**. "
  "Boring, and that's exactly where your minutes are."),
 ("PROFILE 03", ["THE ONE WHO", "DIES AT", "STATION SIX"],
  "The problem isn't the wall balls. It's everything you spent before them. "
  "Your block: pacing."),
 ("PROFILE 04", ["THE", "TECHNICIAN"],
  "Nothing is really weak, nothing is really fast. Your block: **transitions**. "
  "Free seconds, every single one of them."),
 ("THE HARD PART", ["IT WILL FEEL", "WORSE", "BEFORE IT", "FEELS BETTER"],
  "Training your weakness is uncomfortable and unflattering. That discomfort "
  "is the whole point."),
 ("ROAD TO HONG KONG", ["TELL ME", "YOURS"],
  "Which station costs you the most? Drop it below — **I read everything**. "
  "Thank you for the energy."),
]

HONGKONG = [
 ("ROAD TO HONG KONG", ["THE 2027", "WORLDS ARE", "IN HONG KONG"],
  "10–13 June. The first Hyrox World Championships ever held in "
  "Asia-Pacific."),
 ("THE NUMBER", ["TEN", "MONTHS"],
  "Not ten weeks. With ten months you get to **fix a weakness** instead of "
  "working around it."),
 ("MONTHS 1–3", ["BUILD", "THE BASE"],
  "Aerobic volume and general strength. No race pace. This is the boring part "
  "nobody posts about."),
 ("MONTHS 4–6", ["ATTACK THE", "WEAKNESS"],
  "One weak station, one block. For me it's the sled. **You only get to fix it "
  "now**, not in May."),
 ("MONTHS 7–9", ["PUT IT BACK", "TOGETHER"],
  "Race simulations, transitions, pacing. Where the pieces finally start "
  "behaving like a race."),
 ("THE LAST MONTH", ["DO LESS"],
  "Sharpen, sleep, and trust the ten months behind you. Nothing new gets added "
  "here."),
 ("NOT ALONE", ["TRAINING", "WITH", "ANTOINE"],
  "@antoine_bhna trains with me. On the days one of us would have skipped the "
  "session, **we don't**."),
 ("ROAD TO HONG KONG", ["IT'S A GOAL,", "NOT A STATUS"],
  "Nothing is earned yet. I'll document all of it here — the good sessions "
  "and the bad ones. Thank you for following along."),
]

JEUX = {"sled": SLED, "profiles": PROFILES, "hongkong": HONGKONG}

if __name__ == "__main__":
    _bootstrap()
    nom = sys.argv[1]
    jeu = JEUX[nom]
    voulus = [int(x) for x in sys.argv[2:]] or list(range(1, len(jeu) + 1))
    for n in voulus:
        kicker, titre, corps = jeu[n - 1]
        chemin = "o/%s-%02d.png" % (nom, n)
        slide(chemin, kicker, titre, corps, n, len(jeu), finale=(n == len(jeu)))
        print("ok", chemin)
