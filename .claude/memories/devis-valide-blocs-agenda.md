# Devis validé : les blocs se posent dans l'agenda le jour même

Règle posée par Maxime le 3 octobre 2026, après une semaine où les montages
Galec et plusieurs devis ont failli passer à la trappe.

## La règle

Dès qu'un devis est validé (statut accepté dans Pennylane, ou accord écrit du
client par mail), on bloque dans l'agenda Google de Maxime, le jour même, les
trois temps du projet. Le tournage seul dans l'agenda ne suffit pas : c'est la
post-production qui déborde, pas le tournage.

| Temps | Quand | Taille par défaut |
|---|---|---|
| Préprod | entre J-3 et J-1 avant le tournage | 1 h par demi-journée de tournage (brief, matériel, déroulé, repérage) |
| Prod | le jour du tournage, déjà dans l'agenda | la durée réelle, plus le trajet |
| Post | dans les 5 jours ouvrés après le tournage | voir la grille ci-dessous |
| Livraison | la date promise au client, en événement d'une heure | « Livraison V1 [client] » |

Grille de post par défaut, à ajuster au devis :

| Livrable | Post à bloquer |
|---|---|
| 1 vidéo courte (reel, capsule) | 1 h 30 |
| 4 reels d'un même tournage | 2 blocs de 2 h 30 |
| Aftermovie demi-journée | 1 bloc de 3 h |
| Aftermovie journée, film 2 min + extraits | 2 blocs de 3 h |
| Journée corporate multi-vidéos (type Galec, RAJA) | 2 blocs de 3 h, puis 1 bloc par cycle de retours |
| Série podcast, 3 épisodes | 3 blocs de 3 h |

Les retours clients comptent : chaque cycle de corrections demandé ouvre un
nouveau bloc, posé le jour où les retours arrivent.

## Comment Claude l'applique

1. Au moment où Claude crée un devis dans Pennylane, il prépare aussi le mail
   d'envoi. Le devis part dans l'heure (règle du 3 octobre).
2. Au point de 8h30, Claude vérifie les devis passés en « accepté » depuis la
   veille (code action `pennylane_list_quotes`) et les accords reçus par mail.
   Pour chacun, il pose les blocs selon la grille et le dit à Maxime.
3. Les blocs sont en couleur orange (colorId 6), avec dans la description le
   numéro de devis, le montant, les livrables et la date de livraison promise.
4. Si un bloc chevauche un créneau déjà pris, Claude propose le déplacement, il
   ne supprime rien.
5. Les créneaux fixes du cadre (devis et factures à 9h, montage Galec lundi et
   jeudi 14h, revue du vendredi 16h30) ne bougent pas pour faire de la place :
   un nouveau projet se case autour.

## Premier passage, le 3 octobre 2026

- RAJA Sorgues (DEVIS-2026-08-20116, 4 000 € HT) : post le mercredi 7 (10h à
  12h30 et 14h à 17h).
- Nina Ramen ChatGPT Work (2 000 € HT, tournage le 9/10) : préprod le jeudi 8
  (11h30), post le mardi 13 (10h30 à 12h30 et 14h à 17h).
- Galec saison 3 : quatre blocs de montage, lundi 5, jeudi 8, lundi 12, jeudi 15,
  14h à 16h30.
- Amundi (2 novembre) : les blocs seront posés quand le devis mis à jour sera
  accepté.
