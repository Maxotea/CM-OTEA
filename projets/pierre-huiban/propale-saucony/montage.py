#!/usr/bin/env python3
"""Propale vidéo Saucony : monte les deux formats (9:16 et 16:9) depuis `spec.json`.

    python3 projets/pierre-huiban/propale-saucony/montage.py \
        projets/pierre-huiban/propale-saucony/spec.json --sortie DOSSIER [--seulement 9x16]

1. Chaque plan est extrait du rush Drive (lu par plages, relais de `pierre-reel-ralenti.py`),
   étalonné (LUT S-Log3 → Rec.709 si `log`), ralenti réellement (`ralenti` x4 sur un rush 100p)
   et ramené à 25 i/s : un fichier intermédiaire par plan, gardé en cache.
2. Chaque format recadre l'intermédiaire (`x` = centre du recadrage vertical, 0 à 1), pose le
   carton texte en bas, puis enchaîne les plans en fondu au noir court.
3. Les cartons de fin sont du texte blanc sur fond noir.

Sorties muettes : la musique se pose au moment de l'envoi (règle reels-musique-instagram).
"""

import argparse
import importlib.util
import json
import os
import subprocess

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
POLICE = os.path.join(RACINE, "fonts", "inter-display", "InterDisplay-Bold.ttf")
FPS = 25
FONDU = 0.2

spec_m = importlib.util.spec_from_file_location(
    "prr", os.path.join(RACINE, "scripts", "pierre-reel-ralenti.py"))
prr = importlib.util.module_from_spec(spec_m)
spec_m.loader.exec_module(prr)

FORMATS = {"9x16": (1080, 1920), "16x9": (1920, 1080)}


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def intermediaire(plan, sources, lut, dossier):
    """Plan étalonné et ralenti, plein cadre, 25 i/s, sans son."""
    sortie = os.path.join(dossier, f"plan-{plan['id']}.mp4")
    if os.path.exists(sortie):
        return sortie
    src, entree = sources(plan["clip"])
    filtres = []
    if plan.get("log"):
        filtres.append(f"lut3d={lut}")
    r = plan.get("ralenti", 1)
    filtres += [f"setpts={r}*PTS", f"fps={FPS}"]
    ff(*entree, "-ss", str(plan["debut"]), "-t", str(plan["duree"]), "-i", src,
       "-an", "-vf", ",".join(filtres), "-c:v", "libx264", "-crf", "14", "-preset", "medium",
       "-pix_fmt", "yuv420p", sortie + ".part.mp4")
    os.replace(sortie + ".part.mp4", sortie)
    return sortie


def duree_video(chemin):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", chemin], capture_output=True, text=True, check=True)
    return float(o.stdout.strip())


def taille_video(chemin):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height", "-of", "csv=p=0:s=x", chemin],
                       capture_output=True, text=True, check=True)
    w, h = o.stdout.strip().split("x")
    return int(w), int(h)


def filtre_texte(texte, fichier, W, H, duree):
    """Carton blanc, ombre portée, calé dans le tiers bas ; fondu d'entrée et de sortie."""
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(texte)
    taille = int(W * (0.062 if W < H else 0.036))
    bas = int(H * (0.16 if W < H else 0.11))
    alpha = (f"if(lt(t,0.35),0,if(lt(t,0.75),(t-0.35)/0.4,"
             f"if(gt(t,{duree - 0.5:.2f}),max(0,({duree - 0.1:.2f}-t)/0.4),1)))")
    return (f"drawtext=fontfile={POLICE}:textfile={fichier}:fontcolor=white:fontsize={taille}"
            f":line_spacing={int(taille * 0.25)}:x=(w-text_w)/2:y=h-text_h-{bas}"
            f":shadowcolor=black@0.55:shadowx=0:shadowy={max(2, taille // 14)}:alpha='{alpha}'")


def segment(plan, inter, fmt, dossier):
    W, H = FORMATS[fmt]
    sortie = os.path.join(dossier, f"{fmt}-{plan['id']}.mp4")
    d = duree_video(inter)
    w0, h0 = taille_video(inter)
    if w0 >= h0 and W < H:          # source paysage → vertical : recadrage autour de x
        cadre = (f"crop=ih*{W}/{H}:ih:(iw-ih*{W}/{H})*{plan.get('x', 0.5)}:0,"
                 f"scale={W}:{H}:flags=lanczos")
        base = f"[0:v]{cadre},setsar=1[v0]"
    elif w0 < h0 and W > H:         # source verticale → paysage : fond flou + image au centre
        base = (f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,"
                f"crop={W}:{H},boxblur=30:2,eq=brightness=-0.12[fond];"
                f"[b]scale=-2:{H}:flags=lanczos[av];[fond][av]overlay=(W-w)/2:0,setsar=1[v0]")
    else:
        base = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1[v0]"
    texte = filtre_texte(plan["texte"], os.path.join(dossier, f"{fmt}-{plan['id']}.txt"), W, H, d)
    voile = "drawbox=x=0:y=ih*0.55:w=iw:h=ih*0.45:color=black@0.28:t=fill"
    fondus = f"fade=t=in:st=0:d={FONDU},fade=t=out:st={d - FONDU:.2f}:d={FONDU}"
    ff("-i", inter, "-filter_complex", f"{base};[v0]{voile},{texte},{fondus},format=yuv420p[v]",
       "-map", "[v]", "-r", str(FPS), "-c:v", "libx264", "-crf", "16", "-preset", "medium", sortie)
    return sortie


def carton(c, i, fmt, dossier):
    W, H = FORMATS[fmt]
    sortie = os.path.join(dossier, f"{fmt}-fin-{i}.mp4")
    texte = filtre_texte(c["texte"], os.path.join(dossier, f"{fmt}-fin-{i}.txt"), W, H, c["duree"])
    texte = texte.replace("y=h-text_h-", "y=(h-text_h)/2+0*")
    ff("-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d={c['duree']}",
       "-vf", f"{texte},format=yuv420p", "-c:v", "libx264", "-crf", "16", sortie)
    return sortie


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--seulement", choices=list(FORMATS), default=None)
    args = ap.parse_args()
    spec = json.load(open(args.spec, encoding="utf-8"))
    os.makedirs(args.sortie, exist_ok=True)
    lut = os.path.join(args.sortie, f"slog3-e{spec.get('exposition', 0.9)}.cube")
    if not os.path.exists(lut):
        prr.ecrire_lut(lut, exposition=spec.get("exposition", 0.9))
    dossier_spec = os.path.dirname(os.path.abspath(args.spec))
    index = {}
    for nom in (spec["index"] if isinstance(spec["index"], list) else [spec["index"]]):
        index.update(prr.charger_index_drive(os.path.join(dossier_spec, nom)))
    sources = prr.Sources(index=index, cache=os.path.join(args.sortie, "_cache_rushes"))
    try:
        inters = [intermediaire(p, sources, lut, args.sortie) for p in spec["plans"]]
    finally:
        sources.fermer()
    for fmt in ([args.seulement] if args.seulement else FORMATS):
        morceaux = [segment(p, i, fmt, args.sortie) for p, i in zip(spec["plans"], inters)]
        morceaux += [carton(c, k, fmt, args.sortie) for k, c in enumerate(spec.get("cartons_fin", []))]
        liste = os.path.join(args.sortie, f"{fmt}-liste.txt")
        with open(liste, "w") as f:
            f.writelines(f"file '{os.path.abspath(m)}'\n" for m in morceaux)
        final = os.path.join(args.sortie, f"propale-saucony-{fmt}.mp4")
        ff("-f", "concat", "-safe", "0", "-i", liste, "-c", "copy", "-movflags", "+faststart", final)
        print(f"{final} : {duree_video(final):.1f} s")


if __name__ == "__main__":
    main()
