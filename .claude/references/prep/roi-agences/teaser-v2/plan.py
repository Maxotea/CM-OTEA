# Plan du teaser R.O.I. v2, calé sur « Runaway » (138 BPM).
# Tout est exprimé en temps (beats) depuis le début de la vidéo.
# Analyse musique : grille à 138 BPM, impact à 44,60 s, silence 44,85 à 45,45 s,
# drop à 46,35 s, fin du drop à 72,44 s (dans le morceau).

BPM = 138.0
T = 60.0 / BPM            # 0,4348 s par temps
DROP_MUSIQUE = 46.35      # drop dans le morceau (s)
K_DROP = 32               # le drop tombe au temps 32 de la vidéo
MUSIQUE_DEBUT = DROP_MUSIQUE - K_DROP * T   # 32,437 s dans le morceau
K_FIN = 97                # fin de la vidéo (42,17 s)
FPS = 25

# Plans : (temps début, temps fin, clip, entrée source en s, vitesse, options)
# vitesse : nombre (constante) ou (v1, v2) pour une rampe de v1 à v2.
# options : push = zoom lent, punch = coup de zoom à la coupe, noir = écran noir
PLANS = [
    # La montée : coupes toutes les 4 temps, puis 2, puis 1
    (0, 4, '00_depart', 0.0, 0.5, {'push': 0.10}),
    (4, 8, '00_depart', 2.0, 0.7, {'push': 0.06}),
    (8, 12, '02_coureur', 0.0, 0.7, {'push': 0.05}),
    (12, 16, '03_coureuse', 0.0, 0.7, {'push': 0.05}),
    (16, 18, '01_chaussures', 0.0, 0.5, {}),
    (18, 20, '02_coureur', 2.0, 1.0, {'punch': 1}),
    (20, 22, '03_coureuse', 2.0, 1.0, {'punch': 1}),
    (22, 24, '00_depart', 3.6, 1.0, {'punch': 1}),
    (24, 25, '01_chaussures', 1.6, 1.2, {'punch': 1}),
    (25, 26, '02_coureur', 3.6, 1.2, {'punch': 1}),
    (26, 27, '03_coureuse', 3.9, 1.0, {'punch': 1}),
    (27, 28, '01_chaussures', 3.4, (0.5, 3.0), {}),
    # l'impact, le silence, la respiration qui accélère vers le drop
    (28, 28.6, '05_arena', 0.0, 0.3, {'punch': 1}),
    (28.6, 30, None, 0, 0, {'noir': 1}),
    (30, 32, '07_souffle', 2.0, (0.3, 2.5), {'push': 0.08}),
    # Le drop : coupes sur chaque temps, puis respirations en ralenti
    (32, 33, '00_depart', 2.6, 1.6, {'punch': 1, 'shake': 1}),
    (33, 34, '02_coureur', 0.4, 1.6, {'punch': 1}),
    (34, 35, '01_chaussures', 0.6, 1.2, {'punch': 1}),
    (35, 36, '03_coureuse', 1.0, 1.6, {'punch': 1}),
    (36, 38, '05_arena', 0.0, (2.0, 0.4), {'punch': 1}),
    (38, 40, '05_arena', 3.3, 0.5, {'push': 0.05}),
    (40, 42, '02_coureur', 3.4, (0.3, 1.6), {'punch': 1}),
    (42, 44, '05_arena', 1.4, 0.6, {'punch': 1}),
    (44, 46, '06_networking', 1.8, 0.6, {'push': 0.06}),
    (46, 48, '06_networking', 2.4, 0.7, {'punch': 1}),
    (48, 52, '06_networking', 3.3, 0.5, {'push': 0.05}),
    (52, 54, '00_depart', 1.5, 0.6, {'punch': 1}),
    (54, 55, '02_coureur', 2.0, 1.5, {'punch': 1}),
    (55, 56, '03_coureuse', 2.2, 1.5, {'punch': 1}),
    (56, 60, '00_depart', 3.0, (1.2, 0.4), {'push': 0.06}),
    (60, 64, '03_coureuse', 2.6, 0.8, {'push': 0.05}),
    (64, 68, '02_coureur', 1.0, 0.8, {'push': 0.05}),
    (68, 72, '07_souffle', 0.0, 0.6, {'push': 0.06}),
    (72, 76, '01_chaussures', 2.4, 0.5, {'push': 0.05}),
    (76, 77, '00_depart', 3.6, 1.6, {'punch': 1}),
    (77, 78, '01_chaussures', 3.0, 1.4, {'punch': 1}),
    (78, 79, '02_coureur', 4.0, 1.4, {'punch': 1}),
    (79, 80, '03_coureuse', 3.8, 1.4, {'punch': 1}),
    (80, 81, '05_arena', 3.9, 1.0, {'punch': 1}),
    (81, 82, '00_depart', 1.2, 1.6, {'punch': 1}),
    (82, 83, '02_coureur', 2.6, 1.6, {'punch': 1}),
    (83, 84, '05_arena', 3.4, (0.6, 2.5), {'punch': 1}),
    # La signature
    (84, K_FIN, None, 0, 0, {'noir': 1}),
]

# Flashs rouges : sur l'impact avant le silence et sur le drop
FLASHS = [28, 32]
