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

Le découpage exact (rush, point d'entrée, recadrage, raison du choix) est dans `spec.json`. V1 du
10/11, 31,8 s :

| # | Carton | Rush | Image |
|---|---|---|---|
| 1 | Depuis 1898, Saucony chausse des coureurs. | 7426 | Saucony orange au premier plan, Pierre accroupi |
| 2 | Pierre Huiban. Un travail à plein temps. Et une obsession : HYROX. | 7423 | laçage, logo Saucony sur le talon |
| 3 | Nice, 31 octobre. | 7449 | sas de départ en plan large, compte à rebours |
| 4 | 57:16. 6es sur 1 395 binômes. | 7463 | Pierre de dos en course |
| 5 | 1ers de leur catégorie sur 235. | 7464 | Pierre de dos, face à la piste |
| 6 | Pour aller plus loin, il a choisi Saucony. | 7465 | Saucony orange au sled pull |
| 7 | Qualifié pour le championnat du monde. Hong Kong, juin 2027. | 7464 | Pierre de dos |
| 8 | Le documentaire : Comment devenir champion du monde HYROX. | 0198 | podium |
| 9 | Saucony × Pierre Huiban. Run As One. | — | fond noir |
| 10 | Un film OTEA Production | — | fond noir |

## Ce qu'on a écarté, et pourquoi

Sur les rushs de Nice, Pierre court torse nu avec « TRAIN SWEAT EAT » écrit au feutre sur la
poitrine et un short « TEAM TSE » (il courait avec Julie, athlète TSE). Tout plan de face est donc
exclu, comme le stand TSE de l'échauffement. Écartés aussi : 7449 après 7,6 s (Pierre de face au
départ) et 7457 (grande bannière PUMA sur le bord du couloir).

## À confirmer par Maxime

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
