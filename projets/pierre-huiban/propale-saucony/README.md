# Propale vidéo Saucony : Pierre Huiban

Demande de Maxime du 10/11/2026. Une vidéo courte, montée à partir des vrais rushs de Pierre, envoyée
à Michel Schoeny (Marketing Manager France, Saucony) avec le mail de prospection. Contact et note dans
HubSpot (contact 918254520563, entreprise Saucony France 464014260459).

## Angle (tranché par Maxime le 10/11)

**L'héritage Saucony, pas « Pierre en Saucony depuis toujours ».** Pierre et Antoine ont commencé à
s'entraîner en Saucony récemment (Clement Huber, Puma, a remarqué la nouvelle paire ; Maxime lui a
répondu le 09/11 « ils ont commencé à s'entraîner avec »). Écrire « depuis toujours » serait faux, et
le profil de Pierre interdit les partenariats inventés. C'est la marque qui est là depuis toujours
(1898) ; Pierre, lui, l'a choisie.

Style : sobre. Maxime a écarté le « vintage » imposé (« pas forcément »).

## Formats

- `propale-saucony-9x16.mp4` : vertical, à regarder sur téléphone.
- `propale-saucony-16x9.mp4` : horizontal, façon bande-annonce de documentaire.

## Script (cartons texte, en français : le destinataire est Saucony France)

Le découpage exact (rush, point d'entrée, recadrage, raison du choix) est dans `spec.json`. V2 du
10/11, 41,4 s : Maxime veut montrer une saison, pas une course isolée.

| # | Carton | Rush | Image |
|---|---|---|---|
| 1 | Depuis 1898, Saucony chausse des coureurs. | Nice 7426 | Saucony orange au premier plan, Pierre accroupi |
| 2 | Pierre Huiban. Un travail à plein temps. Et une obsession : HYROX. | Nice 7423 | laçage, logo Saucony sur le talon |
| 3 | Paris 54:42. Lyon 54:59. Mondiaux de Stockholm : 55:29. | Rome 7369 | Pierre et Antoine au farmers carry |
| 4 | Rome, 26 septembre. 53:34. | Rome 7348 | Saucony blanches au sled pull |
| 5 | 1ers des 35-39. | Rome 7361 | Pierre au rameur, regard caméra |
| 6 | Nice, 31 octobre. | Nice 7449 | sas de départ, compte à rebours |
| 7 | 57:16. 6es sur 1 395 binômes. | Nice 7463 | Pierre de dos en course |
| 8 | 1ers de leur catégorie sur 235. | Nice 7464 | Pierre de dos, face à la piste |
| 9 | De Rome à Nice, en Saucony. | Nice 7465 | Saucony orange au sled pull |
| 10 | Qualifié pour le championnat du monde. Hong Kong, juin 2027. | Nice 7464 | Pierre de dos |
| 11 | Le documentaire : Comment devenir champion du monde HYROX. | Nice 0198 | podium |
| 12 | Saucony × Pierre Huiban. Run As One. / Un film OTEA Production | — | fond noir |

Chronos de la saison : HYRESULT (`assets/hyrox/pierre-huiban_saison-2026_avec-antoine.json`).
Paris, Lyon et Stockholm n'ont aucun rush de course sur le Drive au 10/11 : ils sont en texte.
Rushs de Rome lisibles : dossier « PIERRE » (7345 à 7379). « AVANT HYROX » et HYROX ROME 2026
refusent la lecture (fichiers non partagés par lien).

## Ce qu'on a écarté, et pourquoi

Sur les rushs de Nice, Pierre court torse nu avec « TRAIN SWEAT EAT » écrit au feutre sur la
poitrine et un short « TEAM TSE » (il courait avec Julie, athlète TSE). Tout plan de face est donc
exclu, comme le stand TSE de l'échauffement. Écartés aussi : 7449 après 7,6 s (Pierre de face au
départ) et 7457 (grande bannière PUMA sur le bord du couloir).

## À confirmer par Maxime

- Rome 7348 : les Saucony blanches semblent être aux pieds d'Antoine (débardeur turquoise au-dessus), logo non lisible ; modèle reconnu à la couleur.
- Rome 7369 : petit logo Nike sur le short d'Antoine.

- Les pieds du laçage (7423) : manchons BV Booster et chaussettes blanches, comme Pierre en
  7428-7430, mais le visage n'est pas dans le cadre.
- Le podium (0198) : un inconnu est assis au premier plan.

## Faits utilisés et leur source

- Saucony fondée en 1898, signature « People over podiums. Run As One. » : fiche officielle Saucony
  (relevée via FullEnrich le 10/11/2026).
- Nice, 31/10/2026, doubles mixte pro 35-39 avec Julie Pecmézian, 57:16, 6es sur 1 395 binômes,
  1ers de catégorie sur 235 : mail de Maxime à Puma du 09/11/2026.
- Hong Kong, 10-13 juin 2027 : `saison-hyrox.md`.
- « Comment devenir champion du monde » est présenté comme le **titre du documentaire**, pas comme
  un résultat.

## Règles respectées

- Vraies images de Pierre uniquement, aucune image générée.
- Pas de logo Saucony incrusté : la marque est citée en texte, les chaussures parlent d'elles-mêmes.
- Rushs : index `rushes-nice-drive.json`, lus sur Drive par plages (relais de `pierre-reel-ralenti.py`).
