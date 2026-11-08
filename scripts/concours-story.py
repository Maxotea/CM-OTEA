#!/usr/bin/env python3
"""
Compose les stories d'un jeu concours à partir des VRAIES photos choisies par Maxime.

La photo est reprise telle quelle (recadrage 9:16 seulement, aucune IA), avec
un dégradé sombre en bas pour la lisibilité, le logo du compte en haut, le
texte de la story et, sauf mention contraire, le bandeau « plus de chances »
de scripts/concours-bandeau.py.

    python3 concours-story.py spec.json dossier_sortie/

spec.json : liste de stories, chacune :
  {
    "nom": "0511",
    "photo": "chemin/photo.jpg",
    "centre_x": 0.5,            // point à garder au centre du recadrage (0 à 1)
    "zoom": 1.0,                // > 1 resserre le cadre
    "cadre": {"largeur": 1080, "x": 0, "y": -250},  // à la place : photo remontée, bas fondu
    "logo": "chemin/logo.png",  // PNG blanc transparent
    "blocs": [
      {"type": "geant", "texte": "V1"},
      {"type": "label", "texte": "JEU CONCOURS · HYROX PARIS"},
      {"type": "titre", "lignes": [[["Ton shooting ", "blanc"], ["photo + vidéo", "orange"]]], "taille": 64},
      {"type": "texte", "texte": "Solo, duo, open ou pro."},
      {"type": "bouton", "texte": "TOUT EST SUR LE POST DU JEU", "couleur": "blanc"},
      {"type": "cartes", "numeros": true, "items": [["LIKE LE POST", "Le post du jeu"]]}
    ],
    "bandeau": true
  }

Règle complète : .claude/memories/jeu-concours-mecanique-virale.md
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

L, H = 1080, 1920
MARGE = 70
ORANGE = (255, 88, 0)
BLANC = (255, 255, 255)
GRIS = (215, 215, 215)
NOIR = (17, 17, 17)
COULEURS = {"blanc": BLANC, "orange": ORANGE}
HAUT_BANDEAU = 1606
POLICES = Path("/usr/share/fonts/opentype/inter")

ICI = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("bandeau", ICI / "concours-bandeau.py")
bandeau_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bandeau_mod)


def police(nom: str, taille: int) -> ImageFont.FreeTypeFont:
    return bandeau_mod.police(nom, taille)


def recadrer(photo: Path, centre_x: float, zoom: float) -> Image.Image:
    img = Image.open(photo).convert("RGB")
    ratio = L / H
    h = img.height / zoom
    w = h * ratio
    if w > img.width:
        w = img.width
        h = w / ratio
    x = min(max(centre_x * img.width - w / 2, 0), img.width - w)
    y = (img.height - h) / 2 if zoom == 1 else min(max(img.height * 0.5 - h / 2, 0), img.height - h)
    return img.crop((int(x), int(y), int(x + w), int(y + h))).resize((L, H), Image.LANCZOS)


def placer(photo: Path, cadre: dict) -> Image.Image:
    """Pose la photo à une taille et une position données sur un fond noir.

    Sert quand le sujet est trop bas pour un recadrage plein cadre : on remonte
    la photo pour que le texte ne couvre aucun visage. Le bas de la photo se
    fond dans le noir sur 260 px, sans arête visible.
    """
    img = Image.open(photo).convert("RGB")
    largeur = cadre.get("largeur", L)
    img = img.resize((largeur, int(img.height * largeur / img.width)), Image.LANCZOS)
    masque = Image.new("L", img.size, 255)
    dm = ImageDraw.Draw(masque)
    fondu = 260
    for i in range(fondu):
        dm.line([(0, img.height - 1 - i), (img.width, img.height - 1 - i)], fill=int(255 * i / fondu))
    fond = Image.new("RGB", (L, H), (10, 10, 10))
    fond.paste(img, (cadre.get("x", 0), cadre.get("y", 0)), masque)
    return fond


def degrade(img: Image.Image) -> Image.Image:
    voile = Image.new("RGBA", (L, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(voile)
    for y in range(H):
        if y < 420:                                    # haut : lisibilité du logo
            a = int(150 * (1 - y / 420))
        elif y > 820:                                  # bas : zone de texte
            t = min(1, (y - 820) / 700)
            a = int(235 * t ** 1.2)
        else:
            a = 0
        d.line([(0, y), (L, y)], fill=(10, 10, 10, a))
    return Image.alpha_composite(img.convert("RGBA"), voile)


def ajuster(d, texte, nom, taille, largeur):
    f = police(nom, taille)
    while d.textlength(texte, font=f) > largeur and taille > 18:
        taille -= 1
        f = police(nom, taille)
    return f


def mesurer(d, bloc) -> int:
    t = bloc["type"]
    if t == "geant":
        return bloc.get("taille", 280) - 30
    if t == "label":
        return 62
    if t == "titre":
        return len(bloc["lignes"]) * int(bloc.get("taille", 64) * 1.08)
    if t == "texte":
        return len(couper(d, bloc["texte"], police("InterDisplay-Medium.otf", 34), L - 2 * MARGE)) * 44
    if t == "bouton":
        return 66
    if t == "cartes":
        return len(bloc["items"]) * 118
    raise SystemExit(f"Type de bloc inconnu : {t}. Utilise geant, label, titre, texte, bouton ou cartes.")


def couper(d, texte, f, largeur):
    lignes, cour = [], ""
    for mot in texte.split():
        essai = (cour + " " + mot).strip()
        if d.textlength(essai, font=f) <= largeur:
            cour = essai
        else:
            lignes.append(cour)
            cour = mot
    if cour:
        lignes.append(cour)
    return lignes


def dessiner(d, bloc, y) -> None:
    t = bloc["type"]
    if t == "geant":
        taille = bloc.get("taille", 280)
        d.text((MARGE - 12, y - 60), bloc["texte"], font=police("InterDisplay-Black.otf", taille), fill=ORANGE)
    elif t == "label":
        f = police("InterDisplay-Black.otf", 34)
        w = d.textlength(bloc["texte"], font=f)
        d.rectangle((MARGE, y, MARGE + w + 32, y + 50), fill=ORANGE)
        d.text((MARGE + 16, y + 6), bloc["texte"], font=f, fill=BLANC)
    elif t == "titre":
        taille = bloc.get("taille", 64)
        f = police("InterDisplay-Black.otf", taille)
        for ligne in bloc["lignes"]:
            x = MARGE
            for morceau, couleur in ligne:
                d.text((x, y), morceau, font=f, fill=COULEURS[couleur])
                x += d.textlength(morceau, font=f)
            y += int(taille * 1.08)
    elif t == "texte":
        f = police("InterDisplay-Medium.otf", 34)
        for ligne in couper(d, bloc["texte"], f, L - 2 * MARGE):
            d.text((MARGE, y), ligne, font=f, fill=GRIS)
            y += 44
    elif t == "bouton":
        couleur = bloc.get("couleur", "blanc")
        f = police("InterDisplay-Black.otf", 34)
        w = d.textlength(bloc["texte"], font=f)
        fond, encre = (BLANC, NOIR) if couleur == "blanc" else (ORANGE, BLANC)
        d.rectangle((MARGE, y, MARGE + w + 36, y + 56), fill=fond)
        d.text((MARGE + 18, y + 9), bloc["texte"], font=f, fill=encre)
    elif t == "cartes":
        numeros = bloc.get("numeros", False)
        for i, (titre, sous) in enumerate(bloc["items"], 1):
            d.rounded_rectangle((MARGE, y, L - MARGE, y + 104), radius=10,
                                fill=(18, 18, 18, 215), outline=(255, 255, 255, 70), width=2)
            x = MARGE + 26
            if numeros:
                d.text((x, y + 18), str(i), font=police("InterDisplay-Black.otf", 56), fill=ORANGE)
                x += 64
            else:
                d.rectangle((MARGE, y, MARGE + 8, y + 104), fill=ORANGE)
            ft = ajuster(d, titre, "InterDisplay-Black.otf", 40, L - MARGE - 24 - x)
            d.text((x, y + 14), titre, font=ft, fill=BLANC)
            d.text((x, y + 64), sous, font=police("InterDisplay-Medium.otf", 27), fill=GRIS)
            y += 118


def composer(story: dict, base: Path, sortie: Path) -> Path:
    photo = (base / story["photo"]).resolve()
    if not photo.exists():
        raise SystemExit(f"Photo introuvable : {photo}. Vérifie le chemin dans le fichier de stories.")
    if story.get("cadre"):
        img = degrade(placer(photo, story["cadre"]))
    else:
        img = degrade(recadrer(photo, story.get("centre_x", 0.5), story.get("zoom", 1.0)))
    calque = Image.new("RGBA", (L, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)

    if story.get("logo"):
        logo = Image.open((base / story["logo"]).resolve()).convert("RGBA")
        logo = logo.resize((300, int(300 * logo.height / logo.width)), Image.LANCZOS)
        calque.alpha_composite(logo, (MARGE - 10, 200))

    avec_bandeau = story.get("bandeau", True)
    bas = HAUT_BANDEAU - 34 if avec_bandeau else 1730
    ecart = 22
    hauteurs = [mesurer(d, b) for b in story["blocs"]]
    y = bas - sum(hauteurs) - ecart * (len(hauteurs) - 1)
    if y < 520:
        raise SystemExit(f"Story {story['nom']} : trop de texte, il monte sur la photo. Retire une ligne.")
    for bloc, h in zip(story["blocs"], hauteurs):
        dessiner(d, bloc, y)
        y += h + ecart

    rendu = Image.alpha_composite(img, calque).convert("RGB")
    fichier = sortie / f"story-{story['nom']}.jpg"
    rendu.save(fichier, quality=93)
    if avec_bandeau:
        bandeau_mod.bandeau(fichier, fichier, story.get("compte", "@oteafilmakers"), HAUT_BANDEAU)
    return fichier


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("Usage : python3 concours-story.py spec.json dossier_sortie/")
    spec = Path(sys.argv[1]).resolve()
    sortie = Path(sys.argv[2])
    sortie.mkdir(parents=True, exist_ok=True)
    for story in json.loads(spec.read_text(encoding="utf-8")):
        print(composer(story, spec.parent, sortie))


if __name__ == "__main__":
    main()
