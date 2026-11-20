# Plan du teaser R.O.I. v3 : motion design + flashs de vrais rushs OTEA.
# Musique « Runaway », 138 BPM. Temps exprimés en temps musicaux (beats) depuis
# le début de la vidéo. Le drop tombe au temps 32 (46,35 s dans le morceau).
#
# Types de segment :
#   'm' : motion design seul (fond noir, le graphisme vient de titres.html)
#   'c' : plan vidéo, titres éventuels par-dessus
#   'k' : plan vidéo vu à travers un texte (masque rendu par titres.html?masque)
# vitesse : 1.0 = temps réel, 0.25 = ralenti natif des rushs à 100 i/s,
#           (v1, v2) = rampe de v1 vers v2.

BPM = 138.0
T = 60.0 / BPM
DROP_MUSIQUE = 46.35
K_DROP = 32
MUSIQUE_DEBUT = DROP_MUSIQUE - K_DROP * T
K_FIN = 97
FPS = 25

# Extraits de rushs (dossier rushs/, 1080p, LUT déjà appliquée sur les S-Log3)
# 7xxx : HYROX Rome (7319 à 7374) et Bordeaux (7086 à 7138), 1065/1135 : HYROX Toulouse,
# 12xx/13xx : GO Entrepreneurs à Paris La Défense Arena (filmés à la verticale, recadrés en 16:9).
# Aucun coureur torse nu.
SEGMENTS = [
    # La montée
    (0, 2, 'm'),
    (2, 4, 'c', '1261', 1.0, 0.6, {'push': 0.08}),
    (4, 5, 'm'), (5, 6, 'm'),
    (6, 8, 'c', '7086', 2.2, 0.4, {'push': 0.06}),
    (8, 10, 'k', '7341', 0.5, 0.4, {'gain': 1.7}),
    (10, 12, 'c', '7319', 0.2, 0.8, {'zoom': 1.22, 'dy': 110, 'push': 0.05}),
    (12, 13, 'm'), (13, 14, 'm'),
    (14, 15, 'c', '7366', 0.1, 0.3, {'punch': 1}),
    (15, 16, 'c', '7127', 0.5, 0.35, {'punch': 1}),
    (16, 18, 'm'),
    (18, 19, 'c', '7088', 1.6, 0.5, {'punch': 1}),
    (19, 20, 'c', '7338', 1.0, 0.5, {'punch': 1}),
    (20, 21, 'm'), (21, 22, 'm'),
    (22, 23, 'c', '1065', 6.5, 0.6, {'punch': 1, 'zoom': 1.25, 'dy': -130}),
    (23, 24, 'c', '7374', 0.8, 0.4, {'punch': 1}),
    (24, 24.5, 'c', '7341', 3.2, 0.5, {'punch': 1}), (24.5, 25, 'm'),
    (25, 25.5, 'c', '7137', 2.0, 0.4, {'punch': 1}), (25.5, 26, 'm'),
    (26, 26.5, 'c', '7104', 2.0, 0.5, {'punch': 1}), (26.5, 27, 'm'),
    (27, 28, 'c', '7086', 1.2, (0.3, 2.5), {}),
    # L'impact, le silence, la respiration
    (28, 28.6, 'c', '1135', 1.0, 0.3, {'punch': 1, 'zoom': 1.3, 'dx': 220}),
    (28.6, 30, 'm'),
    (30, 31, 'c', '7138', 1.5, 0.25, {'push': 0.06}),
    (31, 32, 'c', '7341', 4.5, (0.25, 2.0), {}),
    # Le drop
    (32, 32.5, 'm'),
    (32.5, 33, 'c', '7105b', 1.6, 1.0, {'punch': 1, 'shake': 1}),
    (33, 33.5, 'c', '7106b', 0.5, 1.0, {'punch': 1}),
    (33.5, 34, 'c', '7374', 0.3, 0.6, {'punch': 1}),
    (34, 35, 'c', '7319', 1.6, 1.0, {'zoom': 1.22, 'dy': 110, 'punch': 1}),
    (35, 36, 'c', '7341', 1.2, 0.6, {'punch': 1}),
    (36, 37, 'c', '1256', 1.0, 1.0, {'push': 0.05}),
    (37, 38, 'c', '1270', 2.5, 1.0, {'push': 0.05}),
    (38, 39, 'c', '7367', 1.0, 0.4, {'punch': 1}),
    (39, 40, 'c', '7137', 3.5, 0.4, {'punch': 1}),
    (40, 41, 'm'), (41, 42, 'm'),
    (42, 44, 'c', '1339', 3.0, 1.0, {'push': 0.05}),
    (44, 45, 'c', '1270', 1.0, 1.0, {'punch': 1}),
    (45, 46, 'c', '1270', 3.5, 1.0, {'punch': 1}),
    (46, 48, 'm'),
    (48, 50, 'k', '1261', 3.0, 1.0, {'gain': 2.0}),
    (50, 50.5, 'm'), (50.5, 51, 'm'), (51, 51.5, 'm'), (51.5, 52, 'm'),
    (52, 53, 'c', '7105b', 0.8, 0.5, {'punch': 1}),
    (53, 54, 'c', '7106b', 2.5, 0.6, {'punch': 1}),
    (54, 55, 'c', '7088', 0.6, 0.6, {'punch': 1}),
    (55, 56, 'c', '7341', 5.6, 0.5, {'punch': 1}),
    (56, 57, 'm'), (57, 58, 'm'),
    (58, 59, 'c', '1349', 0.4, 1.0, {'punch': 1}),
    (59, 60, 'm'),
    (60, 62, 'm'),
    (62, 63, 'c', '7104', 0.3, 0.5, {'punch': 1}),
    (63, 64, 'c', '7338', 0.2, 0.5, {'punch': 1}),
    (64, 65, 'm'), (65, 66, 'm'),
    (66, 68, 'c', '7341', 6.0, 0.25, {'push': 0.05}),
    (68, 70, 'm'),
    # Montage sur chaque demi-temps
    (70, 70.5, 'c', '1065', 7.5, 1.0, {'punch': 1, 'zoom': 1.25, 'dy': -130}),
    (70.5, 71, 'c', '7127', 2.0, 0.6, {'punch': 1}),
    (71, 71.5, 'c', '7137', 4.8, 0.6, {'punch': 1}),
    (71.5, 72, 'c', '7319', 2.6, 1.0, {'zoom': 1.22, 'dy': 110, 'punch': 1}),
    (72, 72.5, 'c', '1256', 5.0, 1.0, {'punch': 1}),
    (72.5, 73, 'c', '7341', 2.2, 0.6, {'punch': 1}),
    (73, 73.5, 'c', '7374', 1.5, 0.6, {'punch': 1}),
    (73.5, 74, 'c', '7338', 1.6, 0.6, {'punch': 1}),
    (74, 74.5, 'c', '1256', 7.0, 1.0, {'punch': 1}),
    (74.5, 75, 'c', '7106b', 4.0, 1.0, {'punch': 1}),
    (75, 75.5, 'c', '7367', 2.0, 0.6, {'punch': 1}),
    (75.5, 76, 'c', '7105b', 2.2, 1.0, {'punch': 1}),
    # Les quatre frappes finales, texte sur image
    (76, 78, 'c', '1135', 4.0, 0.4, {'push': 0.05, 'zoom': 1.3, 'dx': 220}),
    (78, 80, 'c', '7319', 2.8, 0.4, {'zoom': 1.22, 'dy': 110, 'push': 0.05}),
    (80, 82, 'c', '1261', 4.5, 1.0, {'push': 0.05}),
    (82, 84, 'c', '7341', 7.0, 0.4, {'push': 0.05}),
    # La signature
    (84, K_FIN, 'm'),
]

FLASHS = [28, 32]
