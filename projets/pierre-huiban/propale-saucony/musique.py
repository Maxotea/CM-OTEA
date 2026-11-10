#!/usr/bin/env python3
"""Bande-son originale de la propale Saucony, en synthèse pure (numpy) : aucun sample tiers,
aucune question de droits, comme `scripts/fond-sonore-stories.py`.

    python3 projets/pierre-huiban/propale-saucony/musique.py DOSSIER_RENDU [--foule FICHIER.wav]

Lit `9x16-liste.txt` dans DOSSIER_RENDU pour connaître la durée de chaque plan, et cale la
musique sur le montage : 150 BPM (un plan de 3,2 s = 2 mesures), en mineur (la, fa, do, sol).

- Chaussures et laçage : nappe seule, pulsation sourde.
- Rome, la saison, Antoine, Julie : la rythmique entre, le filtre s'ouvre, montée avant Nice.
- Départ de Nice : impact, tout le groupe, et le son réel du compte à rebours (`--foule`).
- Hong Kong et podium : second impact, accords longs.
- Cartons de fin : retombée, nappe et pulsation légère, note finale qui s'éteint.

Écrit `musique.wav` (44,1 kHz, stéréo) dans DOSSIER_RENDU.
"""

import argparse
import os
import subprocess
import wave

import numpy as np

SR = 44100
BEAT = 0.4                      # 150 BPM
RNG = np.random.default_rng(1898)


def durees(dossier):
    liste = os.path.join(dossier, "9x16-liste.txt")
    noms, ds = [], []
    for ligne in open(liste, encoding="utf-8"):
        chemin = ligne.strip()[6:-1]
        o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", chemin], capture_output=True, text=True, check=True)
        noms.append(os.path.basename(chemin)[5:-4])
        ds.append(float(o.stdout))
    return noms, ds


def passe_bas(x, fc):
    """Filtre passe-bas doux, appliqué dans le domaine fréquentiel."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))


def passe_haut(x, fc):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * (1 - 1 / np.sqrt(1 + (f / fc) ** 4)), len(x))


def reverb(x, duree=2.2, mix=0.25):
    n = int(SR * duree)
    ir = RNG.standard_normal(n) * np.exp(-np.linspace(0, 7, n))
    ir = passe_bas(ir, 6000)
    ir /= np.sqrt(np.sum(ir ** 2))
    taille = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, taille) * np.fft.rfft(ir, taille), taille)[:len(x)]
    return x + mix * y


def scie(freq, t, desaccord=0.0):
    out = np.zeros_like(t)
    for d in (-desaccord, 0.0, desaccord):
        f = freq * (1 + d)
        for h in range(1, 12):
            out += np.sin(2 * np.pi * f * h * t) / h
    return out / 3


def kick(n_total, debut, gain=1.0):
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    freq = 45 + 75 * np.exp(-t * 28)
    son = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-t * 7)
    son[:200] += np.linspace(0.6, 0, 200)          # attaque
    return place(n_total, debut, son * gain)


def bruit_court(n_total, debut, duree, haut, gain):
    n = int(duree * SR)
    son = RNG.standard_normal(n) * np.exp(-np.linspace(0, 9, n))
    son = passe_haut(son, haut)
    return place(n_total, debut, son * gain)


def impact(n_total, debut, gain=1.0):
    n = int(2.5 * SR)
    t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (38 + 40 * np.exp(-t * 6)) * t) * np.exp(-t * 1.6)
    souffle = passe_bas(RNG.standard_normal(n), 1800) * np.exp(-t * 3) * 0.5
    return place(n_total, debut, (boom + souffle) * gain)


def place(n_total, debut, son):
    out = np.zeros(n_total)
    a = int(debut * SR)
    b = min(n_total, a + len(son))
    if a < n_total:
        out[a:b] = son[:b - a]
    return out


def enveloppe(t, points):
    """Enveloppe linéaire par morceaux : [(temps, valeur), ...]."""
    xs, ys = zip(*points)
    return np.interp(t, xs, ys)


def composer(noms, ds, foule=None):
    debuts = dict(zip(noms, np.cumsum([0] + ds[:-1])))
    total = sum(ds) + 1.5
    n = int(total * SR)
    t = np.arange(n) / SR
    t_rome = debuts["rome-visage"]
    t_nice = debuts["depart"]
    t_hk = debuts["hongkong"]
    t_fin = debuts["fin-0"]
    t_cta = debuts["fin-2"]
    t_end = sum(ds)
    grille = debuts["lacage"]                        # les coupes tombent sur la grille

    # accords : la mineur, fa, do, sol, un par plan de 3,2 s
    accords = [(220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (261.6, 329.6, 392.0), (196.0, 246.9, 293.7)]
    basses = [55.0, 43.65, 65.41, 49.0]
    pad = np.zeros(n)
    basse = np.zeros(n)
    for k in range(int(total / 3.2) + 2):
        a = grille + (k - 1) * 3.2
        seg = (t >= a) & (t < a + 3.2)
        if not seg.any():
            continue
        tt = t[seg]
        accord = accords[k % 4]
        pad[seg] = sum(scie(f, tt, 0.004) for f in accord) / 3
        basse[seg] = scie(basses[k % 4], tt, 0.0)
    pad_sombre, pad_clair = passe_bas(pad, 500), passe_bas(pad, 3200)
    ouverture = enveloppe(t, [(0, 0), (t_rome, 0.1), (t_nice, 0.9), (t_fin, 0.9), (t_cta, 0.2), (total, 0)])
    pad = (1 - ouverture) * pad_sombre + ouverture * pad_clair
    pad *= enveloppe(t, [(0, 0), (1.5, 0.55), (t_nice, 0.6), (t_fin, 0.65), (t_end - 1, 0.5), (total, 0)])

    # rythmique
    batterie = np.zeros(n)
    hats = np.zeros(n)
    duck = np.ones(n)
    b = grille - 4 * 2 * BEAT
    while b < t_end:
        pas = int(round((b - grille) / BEAT))
        if b >= 0:
            if t_rome <= b < t_nice and pas % 2 == 0:            # demi-tempo
                batterie += kick(n, b, 0.8)
            elif t_nice <= b < t_fin:                            # plein tempo
                batterie += kick(n, b, 1.0)
                if pas % 2 == 1:
                    batterie += bruit_court(n, b, 0.18, 1500, 0.35)
            elif t_fin <= b < t_end - 2 and pas % 4 == 0:        # retombée
                batterie += kick(n, b, 0.45)
            if t_rome + 3.2 <= b < t_fin:
                hats += bruit_court(n, b + BEAT / 2, 0.05, 7000, 0.12)
            if t_nice <= b < t_fin:
                hats += bruit_court(n, b, 0.04, 8000, 0.08)
            a = int(b * SR)
            m = min(n, a + int(0.25 * SR))
            if (t_rome <= b < t_end) and a < n:
                duck[a:m] = np.minimum(duck[a:m], np.linspace(0.35, 1, m - a))
        b += BEAT
    # roulement de caisse avant Nice
    r = t_nice - 1.6
    while r < t_nice:
        batterie += bruit_court(n, r, 0.12, 1500, 0.1 + 0.3 * (r - (t_nice - 1.6)) / 1.6)
        r += BEAT / 4

    basse = passe_bas(basse, 220) * enveloppe(t, [(0, 0), (t_rome, 0.2), (t_rome + 6.4, 0.5),
                                                  (t_nice, 0.55), (t_nice + 0.01, 0.8), (t_fin, 0.8),
                                                  (t_fin + 0.5, 0.3), (t_end - 1, 0.25), (total, 0)])

    # montée (bruit filtré + sinus qui grimpe) avant Nice
    seg = (t >= t_nice - 3.2) & (t < t_nice)
    tt = t[seg] - (t_nice - 3.2)
    ton, souffle = np.zeros(n), np.zeros(n)
    ton[seg] = np.sin(2 * np.pi * np.cumsum(220 + 660 * (tt / 3.2) ** 2) / SR) * (tt / 3.2) ** 2
    souffle[seg] = RNG.standard_normal(seg.sum()) * (tt / 3.2) ** 3
    monte = 0.12 * ton + 0.04 * passe_bas(passe_haut(souffle, 800), 5000)

    chocs = impact(n, t_nice, 1.0) + impact(n, t_hk, 0.8) + impact(n, t_fin, 0.6)

    mix = 0.55 * pad + 0.7 * basse * duck + 0.9 * batterie + hats + monte + chocs
    mix = reverb(mix, 2.4, 0.18)
    # stéréo : la nappe un peu élargie
    gauche = mix + 0.08 * np.roll(pad, int(0.011 * SR))
    droite = mix + 0.08 * np.roll(pad, int(0.017 * SR))
    st = np.stack([gauche, droite], axis=1)

    if foule is not None:                       # son réel du sas de départ, synchrone avec l'image
        st[int(t_nice * SR):int(t_nice * SR) + len(foule)] += foule[:n - int(t_nice * SR)] * 0.9

    st *= 0.9 / np.max(np.abs(st))
    return st[:int(total * SR)]


def lire_wav(chemin):
    with wave.open(chemin) as w:
        d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        if w.getnchannels() == 1:
            d = np.stack([d, d], axis=1)
        else:
            d = d.reshape(-1, w.getnchannels())[:, :2]
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dossier")
    ap.add_argument("--foule", default=None, help="WAV 44,1 kHz du son réel du départ de Nice")
    args = ap.parse_args()
    noms, ds = durees(args.dossier)
    foule = lire_wav(args.foule) if args.foule else None
    st = composer(noms, ds, foule)
    sortie = os.path.join(args.dossier, "musique.wav")
    with wave.open(sortie, "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())
    print(f"{sortie} : {len(st) / SR:.1f} s")


if __name__ == "__main__":
    main()
