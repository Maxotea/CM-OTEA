#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aftermovie corporate d'une minute à partir d'un dossier de rushs.

Le script lit tous les rushs d'un dossier (récursif), en tire un dérushage
automatique réparti sur toute la journée de tournage, et monte un film de la
durée demandée (60 s par défaut) au rythme classique d'un aftermovie :

    plan d'ouverture long + titre  →  plans qui s'accélèrent  →  plan final
    posé  →  carton de fin.

Il ne remplace pas un monteur : il livre un **premier bout-à-bout propre**
à valider, plus un fichier `montage.json` (l'EDL) qui liste chaque plan
retenu. Tu peux y changer un plan, un point d'entrée, une durée, et relancer
le rendu sans refaire l'analyse.

## Ce que fait le dérushage

1. Tous les fichiers vidéo sont triés (date de tournage lue dans le fichier,
   sinon nom de fichier), et mis bout à bout dans une timeline « journée ».
2. Le film a besoin de N plans ; on prélève N moments répartis à intervalles
   réguliers sur cette timeline, en évitant les 8 % de début et de fin de
   chaque rush (démarrage caméra, arrêt, main devant l'objectif).
3. Chaque moment candidat est vérifié : une image trop sombre (luma moyenne
   < 28/255, cap ou plan noir) est écartée et le point est décalé plus loin.
4. Les plans sont recadrés en 1920×1080 (ou 1080×1920 avec `--vertical`)
   **sans déformation** : mise à l'échelle puis recadrage centré.

## Le son

Le son d'ambiance des rushs est conservé et fondu entre chaque plan. Avec
`--musique`, l'ambiance est baissée à -16 dB sous la musique, qui est coupée
à la durée du film avec un fondu de sortie. Le tout est normalisé à
-14 LUFS (niveau réseaux sociaux).

⚠️ Ce n'est pas une story : la règle « stories muettes » ne s'applique pas
à un film corporate. En revanche, aucune image n'est générée : ce sont les
rushs du client, et rien d'autre.

## Usage

    # 1. premier montage + EDL
    python3 scripts/aftermovie.py "/Volumes/VERT/Salomon" \\
        --titre "SALOMON" --sous-titre "Les Roches · 2026" \\
        --musique ~/Musique/track.mp3 --sortie o/salomon-aftermovie.mp4

    # 2. retoucher o/salomon-aftermovie.montage.json à la main, puis :
    python3 scripts/aftermovie.py --edl o/salomon-aftermovie.montage.json

ffmpeg et ffprobe doivent être dans le PATH (sur le Mac : `~/.local/node/bin`,
voir `.claude/memories/otea-brand-identity.md`) ou donnés par `--ffmpeg`.
"""
import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

EXTENSIONS = {".mov", ".mp4", ".m4v", ".mxf", ".mts", ".m2ts", ".avi", ".mkv"}
FPS = 25
TRANSITION = 0.35            # durée d'un fondu enchaîné, en secondes
MARGE_RUSH = 0.08            # part de chaque rush ignorée au début et à la fin
LUMA_MIN = 28                # sous ce niveau moyen, l'image est jugée noire
DUREE_OUVERTURE = 4.0        # premier plan, sur lequel s'affiche le titre
DUREE_FINALE = 3.0           # dernier plan posé avant le carton
DUREE_CARTON = 3.0           # carton de fin
PLAN_MAX, PLAN_MIN = 3.0, 1.0

ENCRE = (32, 30, 30)         # #201E1E
BLANC = (241, 241, 241)      # #F1F1F1

# Polices essayées dans l'ordre pour les cartons ; la première trouvée gagne.
POLICES = [
    os.path.expanduser("~/Desktop/DOC/CHARTRE GRAPHIQUE OTEA PRODUCTION/FONT/"
                       "FormaDJRDisplay-Black-Testing.ttf"),
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


# ---------------------------------------------------------------- outils ---

def log(msg):
    print(msg, flush=True)


def run(cmd, **kw):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       text=True, **kw)
    if r.returncode != 0:
        sys.exit("✗ %s\n%s" % (" ".join(cmd[:3]) + " …", r.stderr[-2000:]))
    return r


def trouver_binaire(nom, indice):
    if indice:
        cand = indice if os.path.basename(indice).startswith(nom) \
            else os.path.join(os.path.dirname(indice), nom)
        if os.path.exists(cand):
            return cand
    p = shutil.which(nom)
    if p:
        return p
    # binaire statique de imageio-ffmpeg, s'il est installé (pas de ffprobe)
    if nom == "ffmpeg":
        try:
            import imageio_ffmpeg
            return imageio_ffmpeg.get_ffmpeg_exe()
        except ImportError:
            pass
    sys.exit("✗ %s introuvable : ajoute-le au PATH ou passe --ffmpeg" % nom)


def police(taille):
    for chemin in POLICES:
        if os.path.exists(chemin):
            try:
                return ImageFont.truetype(chemin, taille)
            except OSError:
                continue
    return ImageFont.load_default()


# --------------------------------------------------------------- sondage ---

def sonder(ffprobe, ffmpeg, chemin):
    """Durée, dimensions, présence d'audio et date de tournage d'un rush."""
    if ffprobe:
        r = run([ffprobe, "-v", "error", "-print_format", "json",
                 "-show_format", "-show_streams", chemin])
        info = json.loads(r.stdout)
        video = next((s for s in info["streams"]
                      if s.get("codec_type") == "video"), None)
        if not video:
            return None
        audio = any(s.get("codec_type") == "audio" for s in info["streams"])
        duree = float(info["format"].get("duration") or
                      video.get("duration") or 0)
        tags = {**info["format"].get("tags", {}), **video.get("tags", {})}
        date = tags.get("creation_time") or \
            tags.get("com.apple.quicktime.creationdate") or ""
        return dict(fichier=chemin, duree=duree, largeur=int(video["width"]),
                    hauteur=int(video["height"]), audio=audio, date=date)
    # Sans ffprobe : on lit la sortie texte de ffmpeg -i.
    r = subprocess.run([ffmpeg, "-hide_banner", "-i", chemin],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    err = r.stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.?\d*)", err)
    if not m:
        return None
    duree = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])
    m = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", err)
    if not m:
        return None
    d = re.search(r"creation_time\s*:\s*(\S+)", err)
    return dict(fichier=chemin, duree=duree, largeur=int(m[1]),
                hauteur=int(m[2]), audio="Audio:" in err,
                date=d[1] if d else "")


def luma_moyenne(ffmpeg, chemin, t):
    """Luminosité moyenne (0-255) d'une image prise à l'instant t."""
    r = subprocess.run(
        [ffmpeg, "-hide_banner", "-ss", "%.3f" % t, "-i", chemin,
         "-frames:v", "1", "-vf", "scale=160:-2,signalstats,metadata=print",
         "-f", "null", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    m = re.search(r"lavfi\.signalstats\.YAVG=(\d+\.?\d*)", r.stderr)
    return float(m[1]) if m else 128.0


def lister_rushs(dossier):
    trouves = []
    for racine, _, fichiers in os.walk(dossier):
        for f in fichiers:
            if f.startswith(".") or os.path.splitext(f)[1].lower() not in EXTENSIONS:
                continue
            trouves.append(os.path.join(racine, f))
    return sorted(trouves)


# ------------------------------------------------------------ dérushage ---

def plan_de_durees(duree_totale, avec_carton):
    """La grille de durées des plans : ouverture longue, accélération, final.

    Les plans se chevauchent d'une transition ; la somme des durées moins les
    chevauchements tombe exactement sur `duree_totale`.
    """
    fixes = [DUREE_OUVERTURE, DUREE_FINALE] + ([DUREE_CARTON] if avec_carton else [])
    # temps que les plans du milieu doivent couvrir, chacun coûtant (d - T)
    budget = duree_totale - sum(fixes) + (len(fixes) - 1) * TRANSITION
    if budget < PLAN_MIN:
        sys.exit("✗ durée trop courte pour un aftermovie (%.0f s)" % duree_totale)
    milieu, cumul = [], 0.0
    while True:
        d = PLAN_MAX - (PLAN_MAX - PLAN_MIN) * (cumul / budget) ** 0.8
        if cumul + d - TRANSITION > budget:
            break
        milieu.append(round(d, 2))
        cumul += d - TRANSITION
    durees = [DUREE_OUVERTURE] + milieu + [DUREE_FINALE]
    if avec_carton:
        durees.append(DUREE_CARTON)
    # le reliquat (< une transition) va au plan final posé
    total = sum(durees) - (len(durees) - 1) * TRANSITION
    durees[-2 if avec_carton else -1] = round(
        durees[-2 if avec_carton else -1] + duree_totale - total, 3)
    return durees


def derusher(ffmpeg, rushs, durees_plans, analyser=True):
    """Choisit, pour chaque durée de plan, un moment dans la journée."""
    utiles = []
    for r in rushs:
        marge = r["duree"] * MARGE_RUSH
        utiles.append((r, marge, r["duree"] - marge))
    total = sum(fin - deb for _, deb, fin in utiles)
    n = len(durees_plans)
    plans = []
    for k, duree in enumerate(durees_plans):
        cible = (k + 0.5) / n * total
        # on retrouve le rush qui contient cet instant de la journée
        acc = 0.0
        r, deb, fin = utiles[-1]
        for i, (r, deb, fin) in enumerate(utiles):
            if acc + (fin - deb) >= cible or i == len(utiles) - 1:
                break
            acc += fin - deb
        debut = min(deb + (cible - acc), max(deb, fin - duree))
        if analyser:
            # une image noire ou une casquette devant l'objectif : on décale
            # dans le rush, puis on passe aux rushs suivants si tout est noir
            trouve, debut0 = False, debut
            for r2, deb2, fin2 in utiles[i:] + utiles[:i]:
                if trouve:
                    break
                if r2 is not r:
                    # point de repli dispersé (suite de Weyl) pour que deux
                    # plans relogés dans le même rush ne se répètent pas
                    frac = 0.1 + 0.75 * ((k * 0.381966) % 1)
                    debut = deb2 + (fin2 - deb2) * frac
                    deb, fin = deb2, fin2
                for essai in range(4):
                    if luma_moyenne(ffmpeg, r2["fichier"], debut + duree / 2) >= LUMA_MIN:
                        r, trouve = r2, True
                        break
                    debut = min(debut + (fin - deb) * 0.2, max(deb, fin - duree))
            if not trouve:
                debut = debut0
                log("  ⚠ plan %02d : tout est sombre, gardé tel quel" % (k + 1))
        plans.append(dict(fichier=r["fichier"], debut=round(debut, 3),
                          duree=duree))
    return plans


# --------------------------------------------------------------- cartons ---

def carton_titre(chemin, titre, sous_titre, W, H):
    """Titre en blanc sur fond transparent, incrusté sur le plan d'ouverture."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # un léger voile sombre en bas pour la lisibilité sur n'importe quel plan
    voile = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dv = ImageDraw.Draw(voile)
    for y in range(H // 2, H):
        a = int(140 * (y - H // 2) / (H / 2))
        dv.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    im = Image.alpha_composite(im, voile)
    d = ImageDraw.Draw(im)
    marge = int(W * 0.06)
    f_titre = police(int(H * 0.11))
    f_sous = police(int(H * 0.035))
    y = H - marge - int(H * 0.11)
    if sous_titre:
        y -= int(H * 0.06)
        d.text((marge, y + int(H * 0.125)), sous_titre.upper(), font=f_sous,
               fill=BLANC + (230,))
    d.text((marge, y), titre, font=f_titre, fill=BLANC + (255,))
    # le filet orange n'est pas là : la charte est celle du client, pas la nôtre
    im.save(chemin)


def carton_fin(chemin, texte, W, H):
    """Carton de fin : texte centré sur l'encre."""
    im = Image.new("RGB", (W, H), ENCRE)
    d = ImageDraw.Draw(im)
    lignes = [l for l in re.split(r"\\n|\n", texte) if l.strip()]
    f = police(int(H * 0.06))
    f_petit = police(int(H * 0.03))
    hauteurs = []
    for i, l in enumerate(lignes):
        fo = f if i == 0 else f_petit
        b = d.textbbox((0, 0), l, font=fo)
        hauteurs.append((l, fo, b[2] - b[0], b[3] - b[1]))
    total = sum(h for *_, h in hauteurs) + int(H * 0.025) * (len(lignes) - 1)
    y = (H - total) // 2
    for l, fo, w, h in hauteurs:
        d.text(((W - w) // 2, y), l, font=fo, fill=BLANC)
        y += h + int(H * 0.025)
    im.save(chemin)


# ---------------------------------------------------------------- rendu ---

def rendre_plan(ffmpeg, plan, sortie, W, H):
    """Un plan intermédiaire aux dimensions, cadence et son uniformes."""
    filtre = ("scale=%d:%d:force_original_aspect_ratio=increase,"
              "crop=%d:%d,setsar=1,fps=%d,format=yuv420p" % (W, H, W, H, FPS))
    cmd = [ffmpeg, "-hide_banner", "-y", "-ss", "%.3f" % plan["debut"],
           "-t", "%.3f" % plan["duree"], "-i", plan["fichier"],
           "-f", "lavfi", "-t", "%.3f" % plan["duree"],
           "-i", "anullsrc=r=48000:cl=stereo"]
    # l'anullsrc ne sert que si le rush n'a pas de piste audio
    if plan.get("audio", True):
        audio = "[0:a]aresample=48000,aformat=channel_layouts=stereo[a]"
    else:
        audio = "[1:a]anull[a]"
    cmd += ["-filter_complex", "[0:v]%s[v];%s" % (filtre, audio),
            "-map", "[v]", "-map", "[a]", "-t", "%.3f" % plan["duree"],
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", sortie]
    run(cmd)


def rendre_carton_clip(ffmpeg, png, sortie, duree, W, H):
    run([ffmpeg, "-hide_banner", "-y", "-loop", "1", "-t", "%.3f" % duree,
         "-i", png, "-f", "lavfi", "-t", "%.3f" % duree,
         "-i", "anullsrc=r=48000:cl=stereo",
         "-vf", "scale=%d:%d,setsar=1,fps=%d,format=yuv420p" % (W, H, FPS),
         "-c:v", "libx264", "-preset", "fast", "-crf", "17",
         "-c:a", "pcm_s16le", "-shortest", sortie])


def assembler(ffmpeg, clips, durees, titre_png, duree_titre, musique, sortie,
              W, H):
    """Fondu enchaîné vidéo et audio entre tous les clips, titre, musique."""
    n = len(clips)
    cmd = [ffmpeg, "-hide_banner", "-y"]
    for c in clips:
        cmd += ["-i", c]
    i_titre = n
    cmd += ["-loop", "1", "-t", "%.3f" % duree_titre, "-i", titre_png]
    i_musique = None
    if musique:
        i_musique = n + 1
        cmd += ["-i", musique]

    total = sum(durees) - (n - 1) * TRANSITION
    f = []
    # --- vidéo : chaîne de xfade
    prev = "[0:v]"
    decalage = 0.0
    for k in range(1, n):
        decalage += durees[k - 1] - TRANSITION
        out = "[v%d]" % k if k < n - 1 else "[vx]"
        f.append("%s[%d:v]xfade=transition=fade:duration=%.3f:offset=%.3f%s"
                 % (prev, k, TRANSITION, decalage, out))
        prev = out
    if n == 1:
        f.append("[0:v]null[vx]")
    # --- le titre : fondu d'entrée/sortie en alpha, incrusté sur l'ouverture
    f.append("[%d:v]format=rgba,fade=in:st=0.6:d=0.7:alpha=1,"
             "fade=out:st=%.3f:d=0.6:alpha=1[t]" % (i_titre, duree_titre - 0.9))
    f.append("[vx][t]overlay=0:0:eof_action=pass,"
             "fade=in:st=0:d=0.8,fade=out:st=%.3f:d=0.8,format=yuv420p[vout]"
             % (total - 0.8))
    # --- audio d'ambiance : chaîne de acrossfade
    prev = "[0:a]"
    for k in range(1, n):
        out = "[a%d]" % k if k < n - 1 else "[ax]"
        f.append("%s[%d:a]acrossfade=d=%.3f:c1=tri:c2=tri%s"
                 % (prev, k, TRANSITION, out))
        prev = out
    if n == 1:
        f.append("[0:a]anull[ax]")
    if musique:
        f.append("[ax]volume=-16dB[amb]")
        f.append("[%d:a]atrim=0:%.3f,asetpts=PTS-STARTPTS,"
                 "aresample=48000,aformat=channel_layouts=stereo,"
                 "afade=in:st=0:d=1,afade=out:st=%.3f:d=2.5[mus]"
                 % (i_musique, total, total - 2.5))
        f.append("[amb][mus]amix=inputs=2:duration=first:normalize=0,"
                 "loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    else:
        f.append("[ax]afade=out:st=%.3f:d=1.5,loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
                 % (total - 1.5))
    cmd += ["-filter_complex", ";".join(f), "-map", "[vout]", "-map", "[aout]",
            "-t", "%.3f" % total, "-r", str(FPS),
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", sortie]
    run(cmd)
    return total


# ----------------------------------------------------------------- main ---

def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("dossier", nargs="?", help="dossier des rushs (récursif)")
    p.add_argument("--edl", help="re-rendre depuis un montage.json existant")
    p.add_argument("--titre", default="", help="titre incrusté sur l'ouverture")
    p.add_argument("--sous-titre", default="", dest="sous_titre")
    p.add_argument("--carton-fin", default="", dest="carton_fin",
                   help="texte du carton de fin ; \\n pour une 2e ligne. "
                        "Vide : pas de carton, le film finit sur un plan.")
    p.add_argument("--duree", type=float, default=60.0, help="durée totale (s)")
    p.add_argument("--musique", help="fichier audio de fond (mp3, wav, m4a…)")
    p.add_argument("--sortie", help="fichier mp4 de sortie")
    p.add_argument("--vertical", action="store_true", help="1080×1920 (reel)")
    p.add_argument("--sans-analyse", action="store_true", dest="sans_analyse",
                   help="ne pas vérifier la luminosité des plans (plus rapide)")
    p.add_argument("--ffmpeg", help="chemin de ffmpeg (ffprobe cherché à côté)")
    p.add_argument("--garder", action="store_true",
                   help="garder les clips intermédiaires à côté de la sortie")
    a = p.parse_args()

    ffmpeg = trouver_binaire("ffmpeg", a.ffmpeg)
    ffprobe = shutil.which("ffprobe") or (
        os.path.join(os.path.dirname(ffmpeg), "ffprobe")
        if os.path.exists(os.path.join(os.path.dirname(ffmpeg), "ffprobe"))
        else None)

    W, H = (1080, 1920) if a.vertical else (1920, 1080)

    if a.edl:
        edl = json.load(open(a.edl, encoding="utf-8"))
        for cle in ("titre", "sous_titre", "carton_fin", "musique", "sortie"):
            if getattr(a, cle) in ("", None) and edl.get(cle):
                setattr(a, cle, edl[cle])
        if edl.get("vertical") and not a.vertical:
            W, H = 1080, 1920
        plans = edl["plans"]
        # la dernière entrée peut être le carton : on ne la garde pas ici
        plans = [pl for pl in plans if pl.get("fichier") != "__carton__"]
        durees = [pl["duree"] for pl in plans]
        if a.carton_fin:
            durees.append(DUREE_CARTON)
        log("↻ EDL relue : %d plans" % len(plans))
    else:
        if not a.dossier:
            p.error("donne un dossier de rushs, ou --edl montage.json")
        fichiers = lister_rushs(a.dossier)
        if not fichiers:
            sys.exit("✗ aucun rush dans %s" % a.dossier)
        log("• %d fichiers vidéo trouvés" % len(fichiers))
        rushs = []
        for fch in fichiers:
            info = sonder(ffprobe, ffmpeg, fch)
            if info and info["duree"] >= PLAN_MIN * 2:
                rushs.append(info)
            else:
                log("  – ignoré (illisible ou < 2 s) : %s" % os.path.basename(fch))
        if not rushs:
            sys.exit("✗ aucun rush exploitable")
        # tri chronologique quand la date de tournage est connue
        if all(r["date"] for r in rushs):
            rushs.sort(key=lambda r: r["date"])
        total_rushs = sum(r["duree"] for r in rushs)
        log("• %d rushs exploitables, %d min %02d s de matière"
            % (len(rushs), total_rushs // 60, total_rushs % 60))

        durees = plan_de_durees(a.duree, bool(a.carton_fin))
        durees_rushs = durees[:-1] if a.carton_fin else durees
        log("• %d plans à prélever (%s)" % (
            len(durees_rushs),
            "carton de fin" if a.carton_fin else "fin sur le dernier plan"))
        plans = derusher(ffmpeg, rushs, durees_rushs,
                         analyser=not a.sans_analyse)
        audio_par_fichier = {r["fichier"]: r["audio"] for r in rushs}
        for pl in plans:
            pl["audio"] = audio_par_fichier.get(pl["fichier"], True)

    sortie = a.sortie or os.path.join(
        "o", "aftermovie%s.mp4" % ("-vertical" if a.vertical else ""))
    os.makedirs(os.path.dirname(sortie) or ".", exist_ok=True)
    edl_chemin = os.path.splitext(sortie)[0] + ".montage.json"
    with open(edl_chemin, "w", encoding="utf-8") as fh:
        json.dump(dict(titre=a.titre, sous_titre=a.sous_titre,
                       carton_fin=a.carton_fin, musique=a.musique,
                       sortie=sortie, vertical=a.vertical, duree=a.duree,
                       plans=plans), fh, ensure_ascii=False, indent=2)
    log("• EDL écrite : %s" % edl_chemin)

    tmp = tempfile.mkdtemp(prefix="aftermovie-")
    try:
        clips = []
        for k, pl in enumerate(plans):
            c = os.path.join(tmp, "plan-%02d.mov" % k)
            log("  ▸ plan %02d  %-38s %7.2f s  +%.1f s" % (
                k + 1, os.path.basename(pl["fichier"])[:38], pl["debut"],
                pl["duree"]))
            rendre_plan(ffmpeg, pl, c, W, H)
            clips.append(c)
        if a.carton_fin:
            png = os.path.join(tmp, "carton-fin.png")
            carton_fin(png, a.carton_fin, W, H)
            c = os.path.join(tmp, "carton-fin.mov")
            rendre_carton_clip(ffmpeg, png, c, DUREE_CARTON, W, H)
            clips.append(c)
        titre_png = os.path.join(tmp, "titre.png")
        carton_titre(titre_png, a.titre, a.sous_titre, W, H)
        duree_titre = min(DUREE_OUVERTURE, durees[0])
        log("• assemblage…")
        total = assembler(ffmpeg, clips, durees, titre_png, duree_titre,
                          a.musique, sortie, W, H)
        if a.garder:
            garde = os.path.splitext(sortie)[0] + "-plans"
            shutil.copytree(tmp, garde, dirs_exist_ok=True)
            log("• clips intermédiaires : %s" % garde)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    verif = sonder(ffprobe, ffmpeg, sortie)
    log("✓ %s — %.1f s attendues, %.1f s mesurées, %dx%d" % (
        sortie, total, verif["duree"], verif["largeur"], verif["hauteur"]))


if __name__ == "__main__":
    main()
