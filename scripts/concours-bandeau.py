#!/usr/bin/env python3
"""
Ajoute le bandeau « plus de chances » en bas d'une story de jeu concours.

Un jeu concours sans mécanique de partage ne rayonne pas (Maxime, 04/11/2026).
Chaque story de relance doit donc rappeler les deux leviers qui font circuler
le jeu : identifier des amis en commentaire, et partager en story en
identifiant le compte (on repartage chaque story reçue).

    python3 concours-bandeau.py story.jpg sortie.jpg
    python3 concours-bandeau.py story.jpg sortie.jpg --compte @oteafilmakers --haut 1585

Le bandeau se pose dans la zone libre sous le texte de la story, au-dessus
de la barre de réponse d'Instagram (les 160 derniers pixels restent vides).
La règle complète : .claude/memories/jeu-concours-mecanique-virale.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ORANGE = (255, 88, 0)
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)
DOSSIER_POLICES = Path("/usr/share/fonts/opentype/inter")


def police(nom: str, taille: int) -> ImageFont.FreeTypeFont:
    for chemin in (DOSSIER_POLICES / nom, Path(__file__).resolve().parent.parent / "assets" / "fonts" / nom):
        if chemin.exists():
            return ImageFont.truetype(str(chemin), taille)
    raise SystemExit(f"Police {nom} introuvable : dépose-la dans assets/fonts/ puis relance.")


# Les leviers ne sont pas les mêmes d'un réseau à l'autre (Maxime, 08/11/2026 : « ne pas faire
# du copier-coller » d'Instagram sur TikTok). Sur TikTok, pas de story à repartager : on republie
# (flèche de republication) ou on envoie la vidéo à un pote. Les zones libres changent aussi :
# TikTok couvre la colonne de droite (icônes) et le bas de l'image (légende).
PLATEFORMES = {
    "instagram": {"marge_droite": 120, "bas_max": 1760},
    "tiktok": {"marge_droite": 180, "bas_max": 1460},
}


def leviers(plateforme: str, compte: str) -> list[tuple[str, str]]:
    if plateforme == "tiktok":
        return [("1 POTE TAGUÉ EN COMMENTAIRE", "= 1 chance de plus"),
                ("REPUBLIE OU ENVOIE À UN POTE", "= 1 chance de plus")]
    return [("1 AMI TAGUÉ EN COMMENTAIRE", "= 1 chance de plus"),
            ("TA STORY + " + compte.upper(), "= 1 chance, je repartage")]


def bandeau(source: Path, sortie: Path, compte: str, haut: int, plateforme: str = "instagram") -> None:
    img = Image.open(source).convert("RGBA")
    largeur = img.width
    marge = 70
    calque = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)

    f_titre = police("InterDisplay-Black.otf", 31)
    f_sous = police("InterDisplay-Medium.otf", 26)
    f_plus = police("InterDisplay-Black.otf", 40)

    if plateforme not in PLATEFORMES:
        raise SystemExit(f"Réseau inconnu : {plateforme}. Choisis instagram ou tiktok.")
    zone = PLATEFORMES[plateforme]
    lignes = leviers(plateforme, compte)
    droite = largeur - zone["marge_droite"]
    hauteur_ligne = 58
    d.rounded_rectangle((marge, haut, droite, haut + 24 + hauteur_ligne * len(lignes)), radius=12,
                        fill=(18, 18, 18, 230), outline=(255, 88, 0, 255), width=3)
    # Réduit les deux polices tant qu'une ligne dépasse du cadre.
    taille = 31
    while taille > 20 and any(
        marge + 100 + d.textlength(t + " ", font=f_titre) + d.textlength(u, font=f_sous) > droite - 20
        for t, u in lignes
    ):
        taille -= 1
        f_titre = police("InterDisplay-Black.otf", taille)
        f_sous = police("InterDisplay-Medium.otf", taille - 5)
    y = haut + 12
    for titre, suite in lignes:
        d.text((marge + 24, y + 6), "+1", font=f_plus, fill=ORANGE)
        x = marge + 100
        d.text((x, y + 10), titre, font=f_titre, fill=BLANC)
        x += d.textlength(titre + " ", font=f_titre)
        d.text((x, y + 14), suite, font=f_sous, fill=GRIS)
        y += hauteur_ligne
    y += 12

    if y > zone["bas_max"]:
        raise SystemExit(f"Le bandeau déborde sur l'interface de {plateforme} (barre de réponse ou "
                         f"légende) : remonte-le avec --haut.")
    Image.alpha_composite(img, calque).convert("RGB").save(sortie, quality=93)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source", type=Path)
    p.add_argument("sortie", type=Path)
    p.add_argument("--compte", default="@oteafilmakers")
    p.add_argument("--haut", type=int, default=None, help="ordonnée du haut du bandeau, en pixels")
    p.add_argument("--reseau", choices=sorted(PLATEFORMES), default="instagram")
    a = p.parse_args()
    haut = a.haut if a.haut is not None else (1606 if a.reseau == "instagram" else 1310)
    bandeau(a.source, a.sortie, a.compte, haut, a.reseau)


if __name__ == "__main__":
    main()
