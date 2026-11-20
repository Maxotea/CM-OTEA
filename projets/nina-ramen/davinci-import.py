#!/usr/bin/env python3
"""Importe la timeline du reel (.fcpxml) dans le projet DaVinci Resolve déjà
ouvert, sans passer par le menu.

    python3 projets/nina-ramen/davinci-import.py o/nina-ramen-reel-v1.fcpxml

Conditions : Resolve ouvert sur le projet Nina Ramen, et « Scripting externe »
réglé sur Local (Préférences > Système > Général). Si l'API n'est pas joignable,
faire la même chose à la main : Fichier > Importer > Timeline > le .fcpxml.

Les rushs déjà présents dans la bibliothèque de médias sont réutilisés quand
leur chemin correspond ; les autres sont importés. Rien n'est copié."""
import os
import sys

APP = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
MODULES = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"


def main():
    if len(sys.argv) < 2 or not sys.argv[1].endswith(".fcpxml"):
        sys.exit("usage : davinci-import.py <timeline.fcpxml> [nom de la timeline]")
    fichier = os.path.abspath(sys.argv[1])
    if not os.path.exists(fichier):
        sys.exit("✗ fichier introuvable : %s" % fichier)
    nom = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(os.path.basename(fichier))[0]

    os.environ.setdefault("RESOLVE_SCRIPT_API",
                          "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting")
    os.environ.setdefault("RESOLVE_SCRIPT_LIB", APP)
    sys.path.append(MODULES)
    try:
        import DaVinciResolveScript as dvr
    except ImportError:
        sys.exit("✗ API DaVinci introuvable (%s). À la main : Fichier > Importer > Timeline > %s"
                 % (MODULES, fichier))
    resolve = dvr.scriptapp("Resolve")
    if not resolve:
        sys.exit("✗ Resolve n'est pas ouvert, ou « Scripting externe » n'est pas sur Local "
                 "(Préférences > Système > Général).")
    projet = resolve.GetProjectManager().GetCurrentProject()
    if not projet:
        sys.exit("✗ aucun projet ouvert dans Resolve : ouvre le projet Nina Ramen d'abord.")
    pool = projet.GetMediaPool()
    timeline = pool.ImportTimelineFromFile(fichier, {"timelineName": nom, "importSourceClips": True})
    if not timeline:
        sys.exit("✗ import refusé par Resolve. À la main : Fichier > Importer > Timeline > %s" % fichier)
    projet.SetCurrentTimeline(timeline)
    print("✓ timeline « %s » importée dans le projet « %s » : %d plans"
          % (timeline.GetName(), projet.GetName(), timeline.GetTrackItemCount("video", 1)))
    print("  vérifier : réglages de la timeline 1080×1920, 30 i/s ; mise à l'échelle "
          "« remplir le cadre » pour les rushs horizontaux ; marqueurs sur les plans à corriger.")


if __name__ == "__main__":
    main()
