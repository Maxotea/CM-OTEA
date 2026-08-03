#!/usr/bin/env python3
"""
Compose les fonds sonores des stories en synthèse procédurale pure.

Aucun modèle génératif, aucun sample tiers : uniquement des oscillateurs et
des enveloppes. Zéro question de droits — utilisable commercialement sur les
comptes clients sans licence.

    python3 fond-sonore-stories.py <dossier-sortie>

Écrit jl.wav (J Lawson — pulse électronique premium, ~100 BPM) et
lg.wav (La Galerie — arpège feutré type piano, élégant) : 7,5 s, 44,1 kHz.
"""

import math
import struct
import sys
import wave
from pathlib import Path

SR = 44100
DUREE = 7.5
N = int(SR * DUREE)


def env_attaque(t, attaque):
    return min(1.0, t / attaque) if attaque > 0 else 1.0


def fondu_sortie(t, debut, fin):
    if t < debut:
        return 1.0
    return max(0.0, 1.0 - (t - debut) / (fin - debut))


def note(freq, t, harmoniques=((1, 1.0),)):
    return sum(a * math.sin(2 * math.pi * freq * h * t) for h, a in harmoniques)


def synth_jlawson():
    """Nappe A majeur + pulse de basse : feutré, tech, premium."""
    accord = [110.0, 164.81, 220.0, 277.18, 329.63]  # A2 E3 A3 C#4 E4
    bpm, batt = 100.0, 60.0 / 100.0
    sortie = []
    for i in range(N):
        t = i / SR
        pad = sum(note(f, t, ((1, 1.0), (2, 0.15))) for f in accord) / len(accord)
        pad *= env_attaque(t, 1.2) * (0.82 + 0.18 * math.sin(2 * math.pi * 0.25 * t))
        # pulse de basse en croches, décroissance exponentielle
        ph = (t / (batt / 2)) % 1.0
        basse = math.sin(2 * math.pi * 55.0 * t) * math.exp(-6.0 * ph) * 0.55
        ech = 0.30 * pad + 0.22 * basse
        ech *= fondu_sortie(t, DUREE - 0.9, DUREE)
        sortie.append(ech)
    return sortie


def synth_galerie():
    """Arpège Cmaj9 feutré + nappe basse discrète : élégant, parisien."""
    notes = [  # (temps de départ, fréquence)
        (0.0, 261.63), (1.2, 329.63), (2.4, 392.00),
        (4.0, 493.88), (5.2, 587.33), (6.0, 392.00),
    ]
    sortie = []
    for i in range(N):
        t = i / SR
        s = 0.0
        for depart, f in notes:
            if t >= depart:
                dt = t - depart
                s += (math.sin(2 * math.pi * f * dt)
                      + 0.25 * math.sin(2 * math.pi * f * 2 * dt)) \
                     * min(1.0, dt / 0.006) * math.exp(-1.6 * dt) * 0.5
        nappe = (math.sin(2 * math.pi * 130.81 * t)
                 + 0.5 * math.sin(2 * math.pi * 196.0 * t)) \
                * env_attaque(t, 2.0) * 0.10
        ech = 0.5 * s + nappe
        ech *= fondu_sortie(t, DUREE - 1.0, DUREE)
        sortie.append(ech)
    return sortie


def ecrire(chemin, ech):
    pic = max(abs(x) for x in ech) or 1.0
    gain = 0.45 / pic  # marge large : c'est un fond, pas un premier plan
    with wave.open(str(chemin), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(
            struct.pack("<h", int(max(-1.0, min(1.0, x * gain)) * 32767))
            for x in ech))
    print(f"{chemin} ({Path(chemin).stat().st_size // 1024} Ko, pic {pic:.2f})")


if __name__ == "__main__":
    dossier = Path(sys.argv[1])
    dossier.mkdir(parents=True, exist_ok=True)
    ecrire(dossier / "jl.wav", synth_jlawson())
    ecrire(dossier / "lg.wav", synth_galerie())
