#!/usr/bin/env python3
"""V2 du reel Nina Ramen, faite DANS le projet DaVinci Resolve « Nina Ramen /
Chatgpt » : à partir de la timeline V1 montée par Maxime, une nouvelle
timeline sans les blancs entre les phrases, le carton d'appel à l'action au
bout, et si demandé le mp4 rendu par Resolve pour Submagic (sous-titres).

    python3 projets/nina-ramen/davinci-v2.py                      # projet « Nina Ramen / Chatgpt », timeline courante
    python3 projets/nina-ramen/davinci-v2.py --timeline "Reel V1" \\
        --carton-fin "Réservez votre table\\nninaramen.fr" \\
        --cta-fond "#F3E9D2" --cta-texte "#1F1F1F" \\
        --cta-police projets/nina-ramen/charte/Police.otf \\
        --cta-logo projets/nina-ramen/charte/logo.png --rendre

Ce que fait le script, dans l'ordre :
1. ouvre le projet (dossier « Nina Ramen », projet « Chatgpt », ou tout nom
   passé avec --projet) et prend la timeline V1 (--timeline, sinon la courante) ;
2. lit chaque clip vidéo de la V1 (fichier source, entrée, sortie), mesure
   les blancs dans le fichier avec ffmpeg (mêmes réglages que reel-montage.py :
   silences de plus de 0,4 s, 0,12 s de respiration gardés) ;
3. crée la timeline « <V1> V2 blancs coupés » (1080×1920, 30 i/s) et y pose,
   dans l'ordre de la V1, un clip par bout de phrase, coupe franche entre eux.
   La V1 n'est pas touchée. Les étalonnages des clips V1 sont recopiés sur
   leurs bouts (CopyGrades) ;
4. ajoute le carton d'appel à l'action (PNG généré aux couleurs de la charte)
   en fin de timeline ;
5. avec --rendre : rendu H.264 1080×1920 dans o/, prêt pour Submagic.

Ce qu'il ne reproduit pas (à refaire à la main, il le dit à la fin) : les
titres Fusion/Text+ et autres éléments qui ne sont pas des clips média, les
transitions, les effets de la timeline.

Conditions : Resolve ouvert, « Scripting externe » sur Local (Préférences >
Système > Général), ffmpeg dans le PATH ou ~/.local/node/bin."""
import argparse
import os
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
sys.path.insert(0, os.path.join(RACINE, "scripts"))

APP = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
MODULES = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
PROJET_DEFAUT = "Nina Ramen / Chatgpt"
W, H, FPS = 1080, 1920, 30
DUREE_CARTON = 3.0


def log(msg):
    print(msg, flush=True)


# ------------------------------------------------------------- logique pure ---

def segments_clip(entree, sortie, plages, fps, minimum):
    """Bouts de parole (entrée, sortie exclusive, en images source) qu'il reste
    d'un clip [entree, sortie) une fois les blancs retirés. `plages` sont les
    plages de parole du fichier en secondes. Sans blanc dans le clip, le clip
    entier ; si rien ne reste, le clip entier aussi (on ne perd pas d'image)."""
    segs = []
    for p0, p1 in plages:
        a, b = max(entree, int(round(p0 * fps))), min(sortie, int(round(p1 * fps)))
        if b - a >= max(1, int(round(minimum * fps))):
            segs.append((a, b))
    if not segs:
        return [(entree, sortie)]
    if len(segs) == 1 and segs[0] == (entree, sortie):
        return [(entree, sortie)]
    return segs


def nom_projet(spec):
    """'Nina Ramen / Chatgpt' -> ('Nina Ramen', 'Chatgpt') ; 'Chatgpt' -> (None, 'Chatgpt')."""
    if "/" in spec:
        dossier, projet = spec.rsplit("/", 1)
        return dossier.strip(), projet.strip()
    return None, spec.strip()


# ------------------------------------------------------------------ Resolve ---

def connecter():
    os.environ.setdefault("RESOLVE_SCRIPT_API",
                          "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting")
    os.environ.setdefault("RESOLVE_SCRIPT_LIB", APP)
    sys.path.append(MODULES)
    try:
        import DaVinciResolveScript as dvr
    except ImportError:
        sys.exit("✗ API DaVinci introuvable (%s) : Resolve est-il installé ?" % MODULES)
    resolve = dvr.scriptapp("Resolve")
    if not resolve:
        sys.exit("✗ Resolve n'est pas ouvert, ou « Scripting externe » n'est pas sur Local "
                 "(Préférences > Système > Général).")
    return resolve


def ouvrir_projet(pm, spec):
    """Le projet demandé : déjà ouvert, ou chargé depuis 'Dossier / Projet',
    ou trouvé par son nom (sans tenir compte de la casse) dans le dossier
    courant et ses sous-dossiers."""
    dossier, projet = nom_projet(spec)
    courant = pm.GetCurrentProject()
    if courant and courant.GetName().strip().lower() in (spec.strip().lower(), projet.lower()):
        return courant
    if pm.LoadProject(spec):
        return pm.GetCurrentProject()
    pm.GotoRootFolder()
    if dossier:
        for d in pm.GetFolderListInCurrentFolder() or []:
            if d.strip().lower() == dossier.lower():
                pm.OpenFolder(d)
                break
    for nom in pm.GetProjectListInCurrentFolder() or []:
        if nom.strip().lower() == projet.lower():
            if pm.LoadProject(nom):
                return pm.GetCurrentProject()
    # dernier recours : un projet dont le nom contient le mot demandé
    for nom in pm.GetProjectListInCurrentFolder() or []:
        if projet.lower() in nom.lower():
            if pm.LoadProject(nom):
                return pm.GetCurrentProject()
    sys.exit("✗ projet « %s » introuvable dans Resolve. Projets vus ici : %s"
             % (spec, ", ".join(pm.GetProjectListInCurrentFolder() or []) or "aucun"))


def trouver_timeline(projet, nom):
    if not nom:
        tl = projet.GetCurrentTimeline()
        if not tl:
            sys.exit("✗ aucune timeline ouverte dans le projet : passe --timeline « nom »")
        return tl
    for i in range(1, projet.GetTimelineCount() + 1):
        tl = projet.GetTimelineByIndex(i)
        if tl and tl.GetName().strip().lower() == nom.strip().lower():
            return tl
    sys.exit("✗ timeline « %s » introuvable. Timelines du projet : %s" % (
        nom, ", ".join(projet.GetTimelineByIndex(i).GetName()
                       for i in range(1, projet.GetTimelineCount() + 1))))


def clips_v1(timeline):
    """Les clips média de la V1, dans l'ordre, sur toutes les pistes vidéo :
    (item, mediaPoolItem, fichier, entrée, sortie exclusive, fps)."""
    clips, autres = [], []
    for piste in range(1, timeline.GetTrackCount("video") + 1):
        for item in timeline.GetItemListInTrack("video", piste) or []:
            mpi = item.GetMediaPoolItem()
            fichier = mpi.GetClipProperty("File Path") if mpi else None
            if not mpi or not fichier or not os.path.exists(fichier):
                autres.append((piste, item.GetName()))
                continue
            try:
                fps = float(mpi.GetClipProperty("FPS") or FPS)
            except (TypeError, ValueError):
                fps = FPS
            entree = int(item.GetLeftOffset())
            sortie = entree + int(item.GetDuration())
            clips.append(dict(item=item, mpi=mpi, fichier=fichier, entree=entree,
                              sortie=sortie, fps=fps, piste=piste,
                              debut_tl=item.GetStart()))
    clips.sort(key=lambda c: (c["debut_tl"], c["piste"]))
    return clips, autres


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--projet", default=PROJET_DEFAUT,
                   help="projet Resolve, « Dossier / Projet » ou nom seul (défaut : %s)" % PROJET_DEFAUT)
    p.add_argument("--timeline", default=None, help="timeline V1 de départ (défaut : la courante)")
    p.add_argument("--nom", default=None, help="nom de la timeline V2 (défaut : « <V1> V2 blancs coupés »)")
    p.add_argument("--carton-fin", default="", dest="carton_fin",
                   help="texte du carton de fin ; \\n pour une 2e ligne (rien = pas de carton)")
    p.add_argument("--cta-fond", default=None, dest="cta_fond")
    p.add_argument("--cta-texte", default=None, dest="cta_texte")
    p.add_argument("--cta-police", default=None, dest="cta_police")
    p.add_argument("--cta-logo", default=None, dest="cta_logo")
    p.add_argument("--sans-coupes", action="store_true", dest="sans_coupes",
                   help="ne pas couper les blancs (juste le carton)")
    p.add_argument("--rendre", action="store_true",
                   help="rendre la V2 en mp4 (H.264 1080×1920) dans o/ pour Submagic")
    p.add_argument("--sortie", default=os.path.join(RACINE, "o", "nina-ramen-reel-v2.mp4"))
    p.add_argument("--ffmpeg", default=None)
    a = p.parse_args()

    import importlib
    rm = importlib.import_module("reel-montage")
    am = importlib.import_module("aftermovie")
    ffmpeg = am.trouver_binaire("ffmpeg", a.ffmpeg)

    resolve = connecter()
    pm = resolve.GetProjectManager()
    projet = ouvrir_projet(pm, a.projet)
    log("• projet Resolve : %s" % projet.GetName())
    v1 = trouver_timeline(projet, a.timeline)
    log("• timeline V1 : %s" % v1.GetName())
    clips, autres = clips_v1(v1)
    if not clips:
        sys.exit("✗ aucun clip média dans cette timeline")
    log("• %d clips média dans la V1" % len(clips))

    # --- les blancs, mesurés une fois par fichier source
    plages = {}
    if not a.sans_coupes:
        for c in clips:
            f = c["fichier"]
            if f in plages:
                continue
            info = am.sonder(None, ffmpeg, f)
            duree = info["duree"] if info else c["sortie"] / c["fps"]
            plages[f] = rm.plages_parole(rm.detecter_silences(ffmpeg, f, duree), duree)
            log("  ▸ %s : %d plages de parole" % (os.path.basename(f), len(plages[f])))

    # --- la timeline V2
    pool = projet.GetMediaPool()
    nom_v2 = a.nom or ("%s V2 blancs coupés" % v1.GetName())
    v2 = pool.CreateEmptyTimeline(nom_v2)
    if not v2:
        sys.exit("✗ impossible de créer la timeline « %s » (elle existe déjà ?)" % nom_v2)
    projet.SetCurrentTimeline(v2)
    for cle, val in (("useCustomSettings", "1"), ("timelineResolutionWidth", str(W)),
                     ("timelineResolutionHeight", str(H)), ("timelineFrameRate", str(FPS))):
        v2.SetSetting(cle, val)

    n_bouts, images_v1, images_v2 = 0, 0, 0
    for c in clips:
        if a.sans_coupes:
            segs = [(c["entree"], c["sortie"])]
        else:
            segs = segments_clip(c["entree"], c["sortie"], plages[c["fichier"]], c["fps"], rm.SEGMENT_MIN)
        images_v1 += c["sortie"] - c["entree"]
        poses = []
        for s0, s1 in segs:
            ajout = pool.AppendToTimeline([{"mediaPoolItem": c["mpi"],
                                            "startFrame": s0, "endFrame": s1 - 1}])
            if ajout:
                poses += ajout
            images_v2 += s1 - s0
        n_bouts += len(segs)
        if poses:
            try:
                c["item"].CopyGrades(poses)          # l'étalonnage de la V1 suit
            except Exception:
                pass
        if len(segs) > 1:
            log("  ▸ %-32s %d bouts, %.1f s de blanc retirés" % (
                os.path.basename(c["fichier"])[:32], len(segs),
                ((c["sortie"] - c["entree"]) - sum(s1 - s0 for s0, s1 in segs)) / c["fps"]))

    # --- le carton d'appel à l'action
    if a.carton_fin:
        dossier_o = os.path.dirname(a.sortie) or "."
        os.makedirs(dossier_o, exist_ok=True)
        png = os.path.join(dossier_o, "nina-ramen-carton-cta.png")
        if a.cta_fond or a.cta_texte or a.cta_police or a.cta_logo:
            rm.carton_cta(png, a.carton_fin, W, H, a.cta_fond, a.cta_texte, a.cta_police, a.cta_logo)
        else:
            am.carton_fin(png, a.carton_fin, W, H)
        items = pool.ImportMedia([png]) or []
        if items:
            pool.AppendToTimeline([{"mediaPoolItem": items[0], "startFrame": 0,
                                    "endFrame": int(DUREE_CARTON * FPS) - 1}])
            log("• carton d'appel à l'action ajouté (%s)" % png)
        else:
            log("⚠ carton non importé dans la bibliothèque : %s" % png)

    fps_tl = float(v2.GetSetting("timelineFrameRate") or FPS)
    log("✓ timeline « %s » : %d bouts, %.1f s (V1 : %.1f s), %.1f s de blanc en moins"
        % (nom_v2, n_bouts, images_v2 / fps_tl, images_v1 / fps_tl, (images_v1 - images_v2) / fps_tl))
    if autres:
        log("⚠ à refaire à la main sur la V2 (pas des clips média) : %s"
            % ", ".join("%s (piste V%d)" % (n, p) for p, n in autres))
    log("  transitions et titres de la V1 ne sont pas recopiés ; les sous-titres se font dans Submagic sur le mp4.")

    # --- le rendu pour Submagic
    if a.rendre:
        dossier_o = os.path.dirname(os.path.abspath(a.sortie))
        os.makedirs(dossier_o, exist_ok=True)
        nom_fichier = os.path.splitext(os.path.basename(a.sortie))[0]
        projet.SetCurrentRenderFormatAndCodec("mp4", "H264")
        projet.SetRenderSettings({"SelectAllFrames": True, "TargetDir": dossier_o,
                                  "CustomName": nom_fichier, "FormatWidth": W, "FormatHeight": H,
                                  "FrameRate": FPS, "ExportVideo": True, "ExportAudio": True})
        job = projet.AddRenderJob()
        if not job:
            sys.exit("✗ Resolve a refusé le rendu : vérifier la page Rendu")
        projet.StartRendering(job)
        log("• rendu en cours vers %s…" % dossier_o)
        while projet.IsRenderingInProgress():
            time.sleep(2)
        log("✓ mp4 rendu : %s → à passer dans Submagic pour les sous-titres" % a.sortie)


if __name__ == "__main__":
    main()
