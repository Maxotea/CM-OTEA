# Banques photos par client

## jlawsongolf (banque validée juillet 2026 — 42 photos)
- Shooting pro HOMESANFAUTE (mai 2026) : portraits fitteur (bio/coulisses), sessions fitting client (P1/P5), détails clubs/shafts (P1/P2), ambiance studio+écrans (P3/P4)
- Photos terrain IMG_14xx-16xx : atelier gripping/loft-lie (P3 reels bruts), mur de shafts (P1/P2), clubs finis (P5), écrans de mesure/data (P1/P5)
- Trous à combler : verticales 9:16 pour stories, avant/après client, photos extérieur parcours
- Élément IA Higgsfield : "JLawson-Studio" (id 12942370-e8c1-465c-9ea0-2583a9384e0c) — DA moderne tech premium, métal noir mat, LED accent chaud, bleu marine + vert, AUCUN bois

## Autres clients (Le Loft, Gossip Beauty Center, La Galerie Immobilière, Otea)
Banques à constituer : demander les photos existantes, les classer par pilier (même méthode : planches contact via ImageMagick puis tableau fichier→pilier→usage), identifier les trous, créer l'élément Higgsfield de la marque si besoin d'IA d'appoint.

## OTEA Production et Otea Filmakers : la banque de vraies photos (relevé du 12/10/2026, mis à jour le 13/10)
- Source : shooting HOME SANFAUTE et portrait pro, provenance client. Originaux sur le Drive, dossier
  `1_0BHQiHAwDs-4pXp6cXBIfMC7u7ezydY` (31 fichiers de 3 à 7 Mo) ; aperçus 1440x960 sur cloudfront. 46 URL dans
  l'inventaire, 32 photos uniques, 11 doublons exacts, 3 cartes story de juillet exclues. Aucune image IA sur ces deux
  comptes (règle du 21/08/2026).
- Manifestes : `photos/otea-production.json` (32 photos) et `photos/otea-filmakers.json` (22 photos ouvertes à
  Filmakers), mêmes clés 01 à 46. Ils portent le recadrage 4:5, le recadrage 9:16 pris sur l'original (une story
  plein cadre ne part jamais d'un aperçu), les boîtes de visage YuNet et le contrôle de rendu carrousel.
- Q4 : Maxime = le vidéaste barbu en t-shirt noir, sans casquette (photo 01), réponse du 13/10/2026 ; seule personne
  présentable en « je » sur Filmakers (ailleurs il porte parfois une casquette jaune ou orange, planche d'identité
  dans `clients/banque-photos-otea.md`). Le champ `qui` de la 01 le dit ; sur les autres photos de 01 à 46 il reste
  « à confirmer », aucune légende Filmakers ne pose un « je » sur une autre personne visible, et la 34 (portrait N&B)
  reste hors rotation. La 40 (texte d'écran d'un tiers) ne sert pas de fond.
- Rotation : une même photo ne repasse pas au feed avant 30 jours, carrousels compris, et pas le même jour sur les
  deux comptes. Les deux comptes puisent dans le même stock : en décembre, OTEA utilise les clés 02, 03, 04, 05, 06,
  07, 08, 09, 10, 11, 12, 13, 14, 17, 20, 21, 23, 26, 27, 30, 42 et 44 ; Filmakers est passé en cartes
  typographiques, avec la seule 03 le 25/12.
- i2v (kling3_0_turbo, 13/10) : 5 plans sur 5 avec un visage ont dérivé malgré le prompt verrouillé (expression,
  menton, visage complété), et un plan sans visage a inventé une main et un faux logo. Les seuls plans retenus n'ont
  aucun visage (OTEA sam 17, Filmakers 08c et 09t). Choisir pour les stories des photos sans visage visible, et
  contrôler chaque plan frame par frame.
- Banque d'instantanés faite le 13/10 depuis le Mac : 114 photos OTEA Production, 73 Otea Filmakers, ajoutées aux
  manifestes après les clés 01 à 46 ; détail, accords à obtenir et trous dans `clients/banque-photos-otea.md`.

## Run On Invest : la banque IA (relevé du 12/10/2026)
- Seul compte autorisé aux photos IA ultra réalistes (Maxime, 04/08/2026), tant qu'aucune édition n'a eu lieu.
  Jamais une personne identifiable, jamais un faux lettrage, jamais de marque lisible.
- Manifeste `photos/run-on-invest.json` : générations Higgsfield du 19/08/2026. b, g, j, k utilisables partout ;
  f et l en 4:5 seulement (faux lettrage hors du recadrage carrousel, pas en story plein cadre) ; d hors rotation
  (marques réelles) ; c, e, h exclues (visages de profil, pseudo lettrage).
- Réserves : g (skyline) et k (arche) ne ressemblent pas à La Défense alors que la mention dit LA DÉFENSE ; l (le
  groupe sur le parvis) revient trop souvent ; presque toutes ont les coureurs dans le bas du cadre, là où va le texte.
- Q13 (décision) : 4 à 6 photos neuves, coureurs de dos dans le tiers haut, sol nu en bas. Pas encore faites (solde
  Higgsfield au plancher de 100 le 13/10). Chaque visuel publié est à déclarer « contenu IA » (Q12).
