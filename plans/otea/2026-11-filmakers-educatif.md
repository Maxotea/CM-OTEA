# Otea Filmakers · le programme éducatif « Filmer le HYROX »

*Demande de Maxime, 08/11/2026 : de l'éducatif sur le contenu Filmakers, avec le système monté pour les posts et le motion design (cartes typographiques, mentions mono, barre d'accent, grain, animation calée sur la voix). Reprendre le pourquoi prendre un vidéaste, expliquer le métier de vidéaste sportif et HYROX de l'intérieur : mes journées, comment je filme, ce que c'est de suivre un athlète, le matériel. Le micro, pas seulement le macro. Deux posts par semaine où je me filme, beaucoup de motion design, et des carrousels éducatifs plus stylisés que ceux du moteur actuel.*

Ce plan complète le plan de bataille du 13/10 (`2026-10-plan-de-bataille.md`) et la fiche `otea-filmakers.md` (positionnement B2C du 25/10, ligne du 26/10). Il ne les remplace pas : les règles permanentes de `CLAUDE.md` priment, puis le plan de bataille, puis ce programme.

## 1. Le pari

Les reels HYROX de Filmakers touchent 3 000 à 5 300 personnes, les reels de conseils face caméra 200 à 400. Le programme ne revient pas aux conseils d'entrepreneur : il garde le sujet qui marche (le HYROX) et change le regard. **Personne ne raconte le HYROX du point de vue de celui qui le filme.** Nick Bare raconte l'athlète, HYROX France couvre l'événement, les vidéastes français connus (Monsieur Camera, Charles Schiele) parlent matériel sans jamais parler sport. La place à prendre, c'est le métier de vidéaste sportif expliqué de l'intérieur, au « je », au tutoiement, avec des images vraies.

Trois questions auxquelles chaque contenu répond pour l'audience (athlètes et passionnés de sport, jamais un directeur de la communication) :

1. **Pourquoi** un vidéaste sur ma course, alors qu'il y a les photos officielles et la story d'un pote ?
2. **Comment** il fait, concrètement : où il se met, quelle cadence, ce qu'il cadre, ce qu'il garde au dérush ?
3. **Ce que ça me fait** : revoir ma course de l'extérieur, une fois pour toutes.

## 2. Le micro avant le macro

Un épisode ne dit jamais « je filme des compétitions ». Il dit : « au sled push, je me mets au bout de la ligne, le plus bas possible, parce que le 70-200 me laisse serré sur le visage depuis le bord ». Le détail est la preuve. Six chapitres, chacun décliné en épisodes :

| Chapitre | Ce qu'il explique | Exemples de micro |
|---|---|---|
| **A · Pourquoi un vidéaste** | Ce que l'athlète perd sans images : les photos officielles ne sont pas à lui, personne ne filme sa roxzone, il ne revoit jamais sa course | la story floue du pote, le photographe qu'on croise une fois, l'arrivée que tout le monde a et la roxzone que personne n'a |
| **B · Mes journées** | Une journée de course heure par heure, le soir de dérush, la route, le montage en déplacement | l'heure d'arrivée dans l'arène, les 16 déplacements d'une course, la timeline ouverte le soir à l'hôtel |
| **C · Comment je filme** | Une station à la fois : position, cadence, cadrage, ce qu'on garde | sled push 50 m, wall balls, rameur, le passage de ligne, le son |
| **D · Suivre un athlète** | La roxzone, les transitions, anticiper la station suivante, ce qui se joue dans un regard | le moment où je perds l'athlète, le regard vers la station suivante, le « you go I go » en doubles |
| **E · Le matériel** | La FX3, le 70-200 GM II, le 100p, le S-Log3 : pourquoi, et ce que ça change à l'image | un seul boîtier, un seul objectif, l'image plate au tournage, l'étalonnage |
| **F · Après la course** | Le dérush, l'étalonnage, le montage, la livraison | les 3 règles pour garder un plan, l'avant/après sur le même plan, le plan raté qu'on garde |

Ce qui ne va **pas** dans ce programme : le plateau d'entreprise, l'interview en bureau, le mot « client », les délais de livraison, les salons. Tout cela est OTEA Production, au vouvoiement (`positionnement-filmakers-production.md`).

## 3. Les trois formats

### 3.1 Le reel face caméra avec motion design (2 par semaine)

Maxime se filme, une prise, un épisode. Le montage reprend le format dynamique du moteur de montage (MONTAGE-OTEA, `README.md` § « Format dynamique ») : **la personne reste à l'écran, détourée avec un liseré, et le motion design s'affiche derrière elle au rythme de ce qu'elle dit**. Coupes serrées (plans de 1,5 à 3 s, cadrage changé à chaque coupe), sous-titres qui surgissent mot à mot, transitions balayées à chaque nouvelle idée, signature en fin.

La grammaire motion, restreinte volontairement pour que la série soit reconnaissable :

| Élément | Quand | Exemple |
|---|---|---|
| `grand_mot` | le mot clé de la phrase, en très grand | « 8 STATIONS », « ROXZONE » |
| `compteur` | un chiffre qui monte | 0 → 16 déplacements, 25 → 100 images par seconde |
| `liste` / `checklist` | une énumération, les items s'allument au mot | heure de départ · tenue · stations |
| `tampon` | une affirmation posée comme un cachet | « PAS À TOI », « UNE SEULE PRISE » |
| `cliche` | une idée reçue, rayée au mot déclencheur | « les photos officielles suffisent » |
| `jauge` / `barres` | une comparaison sans chiffre | vitesse réelle contre ralenti |
| `fleche`, `regle`, `projecteur` | une montée, une mesure, une mise en lumière | 50 mètres, le faisceau sur le visage |

Palette du format : fonds encre `#201E1E` et graphite `#2E2B2B`, texte vert `#D5DEDD`, accent blanc `#F1F1F1`, mentions vert d'eau `#ACC1C0`. Police Inter Display, mentions en Space Mono. Charte prête à copier dans MONTAGE-OTEA : `reels/educatif/charte-dynamique-otea-filmakers.json`. Storyboards de la saison 1, au format du moteur (scènes calées sur des mots déclencheurs, pas sur des secondes) : `reels/educatif/storyboards-dynamique.json`.

**Les images de course s'insèrent derrière Maxime** (plein cadre, 1 à 2 s, à la place du fond animé) à chaque fois que le script parle d'un plan précis : rushes FX3 de Rome et de Nice, Pierre Huiban et Antoine Bouhana (accord du 27/10/2026), personne d'autre sans accord. Jamais une image générée.

**Le son, décisions de Maxime du 08/11/2026 : « Under the Sun » de Bakermat feat. Kidda (The Ringmaster, 2020) est la signature sonore de la série, en intro et en outro de chaque reel. Et il n'y a pas de licence de synchronisation sur ce titre.** Donc le morceau n'entre jamais dans le fichier : un son commercial incrusté sans licence expose le reel à une coupure du son ou à une portée bridée, comme « Bellatores » sur le teaser F1. Le fichier rendu porte **la voix de Maxime seule** (micro-cravate, aucune musique). À la publication, en mode notification, Maxime pose « Under the Sun » depuis la bibliothèque musicale d'Instagram, à volume bas sous la voix, sur toute la durée : c'est le chemin qui couvre les droits. La signature intro et outro se fait **par le montage image** : la carte d'ouverture (2 s) et la carte de fin avec la question binaire (2,5 s) sont sans voix, la musique s'y entend donc seule, et c'est ce qu'on reconnaît. Si le titre manque dans la bibliothèque le jour de la publication, choisir un autre son et le garder pour toute la série (le noter dans `storyboards-dynamique.json`, `commun.musique`). Cette façon de faire respecte la règle `reels-musique-instagram.md` : seule la voix réelle de Maxime est dans le fichier.

Règles de publication : voix de Maxime seule dans le fichier, musique posée dans Instagram, mode notification (`reels-musique-instagram.md`). Chaque reel finit par une **question binaire** (plan de bataille). **Un reel sur quatre au plus** porte un appel à écrire en message, les autres racontent. Scripts : `reels/educatif/E01-…md` à `E08-…md`, au format `reel-script` (hook chiffré, trois étapes, cliffhanger, 175 mots maximum), à passer dans `reel-lint` avant tournage.

### 3.2 Le carrousel éducatif stylisé (1 par semaine)

Le style « educatif » de `scripts/carrousel.py` (module `scripts/carrousel_educatif.py`), décidé le 08/11 : chaque slide est posée comme l'écran d'une caméra. Repères de viseur dans les coins, « REC » sur la couverture, mention technique en Space Mono en haut (série à gauche, compte ou matériel à droite), barre de progression et compteur « 03 / 07 » en bas, grain film 18. Six gabarits : `couverture`, `chapitre` (numéro géant en filigrane), `chiffre` (une valeur en très grand), `liste` (index mono), `duel` (deux colonnes), `cta` (fond inversé blanc). Typographique par construction : aucune photo, aucune image générée. Doctrine inchangée : 8 slides, 40 mots, deux accents par slide, archétypes de `carrousels-hebdo.md`.

Specs : `carrousels/otea-filmakers/`, planifiées en brouillon par l'action du vendredi, publiées par la relève (`validation_auto`).

### 3.3 Les stories (inchangées)

Lundi, mercredi, vendredi 10 h, vraies photos animées, muettes. Pas de changement : elles servent de rappel des épisodes (une carte « nouvel épisode » à partir de la semaine 2 si Maxime le souhaite).

## 4. La cadence et les créneaux

| Jour | 10 h | 18 h |
|---|---|---|
| Lundi | story | post existant du calendrier |
| **Mardi** | | **reel éducatif** (nouveau créneau) |
| **Mercredi** | story | **carrousel éducatif** (remplace le post simple du jour, règle du mercredi) |
| **Jeudi** | | **reel éducatif** (nouveau créneau) |
| Vendredi | story | post existant du calendrier |

Les reels prennent les créneaux vides du mardi et du jeudi : rien à retirer du calendrier. Quand un créneau porte déjà un contenu de la série avant/après et matériel (relue le 27/10), le reel passe à midi le même jour. Les carrousels remplacent les posts simples du mercredi ; `publier.py` ne touche ni à un reel ni à un carrousel déjà planifié.

## 5. Saison 1 · du 17 novembre au 16 décembre 2026

| Date | Créneau | Contenu | Chapitre | CTA |
|---|---|---|---|---|
| mar 17/11 | 18 h | **E01** Pourquoi un vidéaste sur ton HYROX | A | écris-moi en message |
| mer 18/11 | 18 h | **C1** Tes images de course : 5 idées reçues (A4, 7 slides) | A | écris-moi en message |
| jeu 19/11 | 18 h | **E02** Ma journée de course, heure par heure | B | question |
| ven 20/11 | 18 h | *existant* : carrousel « je t'accompagne » (407612665) | | |
| mar 24/11 | 18 h | **E03** Comment je filme le sled push | C | question |
| mer 25/11 | 18 h | *existant* : reel avant/après (407042888), pas de carrousel éducatif cette semaine | | |
| jeu 26/11 | 18 h | **E04** La roxzone, ce que personne ne filme | D | question |
| ven 27/11 | 18 h | *existant* : carrousel matériel B3 (407608209) | | |
| mar 01/12 | **12 h** | **E05** Un boîtier, un objectif (le carrousel C2 Pierre et Antoine tient 18 h) | E | question |
| mer 02/12 | 18 h | **C2** Comment je filme une station (A1, 7 slides) | C | question |
| jeu 03/12 | 18 h | **E06** Le même plan, brut puis étalonné | F | question |
| mar 08/12 | 18 h | **E07** J-4 : ce que je prépare avant Paris | B | question |
| mer 09/12 | 18 h | **C3** Ta course filmée : ce que je te demande (A7, 7 slides) | D | écris-moi en message |
| jeu 10/12 | 18 h | **E08** Le dérush : 3 règles pour garder un plan | F | question |
| ven 11/12 | 18 h | *existant* : carrousel 70-200 B2 (407610968) | | |
| mer 16/12 | 18 h | **C4** Un HYROX en chiffres, côté caméra (A6, 7 slides, pendant HYROX Paris) | C | aucun |

Appels à écrire en message : 3 sur 12 contenus du programme, sous la règle d'un sur quatre. Aucun prix dans les textes publiés. Aucun appel daté sur HYROX Paris (12 au 20/12) : la fenêtre J-60 à J-30 est passée, la campagne Meta « Réserve ton film HYROX, Paris » (01 au 11/12, plan de bataille § 6) porte l'offre.

Saison 2 (janvier) : le rameur et les wall balls (C), la journée de dérush complète (B et F), le « you go I go » en doubles avec Pierre et Antoine (D), la FX3 seule (E), le son (F), et le bilan de Paris. À écrire après les premiers chiffres de la saison 1.

## 6. Le tournage, en une séance

Les huit épisodes se tournent **en une seule séance face caméra** : **lundi 09/11/2026, de 9 h à 10 h** (décidé le 08/11), feuille de tournage dans `reels/educatif/TOURNAGE-2026-11-09.md`. Le montage a ainsi une semaine d'avance sur le premier épisode du 17/11 :

- FX3 ou iPhone, **vertical ou horizontal cadré large** (le format dynamique recadre : plein, serré, décalé à gauche ou à droite). Fond uni ou peu chargé, lumière de face, **micro-cravate** (le son direct est gardé : c'est la voix de Maxime ; la musique vient d'Instagram).
- Une prise par épisode, lue au téléprompteur ou en points, sans chercher la prise parfaite : les silences sautent au montage.
- Entre deux épisodes, **les plans de coupe** demandés en fin de chaque script (mains sur la FX3, l'objectif, le sac, la timeline) : 10 secondes chacun, ils tournent dans toute la saison.
- Pour le détourage, **ne pas porter de noir sur fond noir** : le t-shirt noir de Maxime demande un fond clair ou coloré.

### Les tournages dans l'agenda (posés le 08/11/2026)

Chaque créneau porte la feuille, les scripts, les storyboards, la charte et la liste de mise en place,
pour qu'aucun oubli ne dépende de la mémoire :

| Quand | Agenda | Ce qu'on tourne |
|---|---|---|
| lun 09/11, 9 h à 10 h | « Tournage 1/2 · saison 1 » | les 8 épisodes face caméra et les 12 plans de coupe |
| 12 au 20/12 (dates à confirmer) | « HYROX Paris · images de course pour la série » | roxzone, sled push en 100p et sa sortie, un plan brut S-Log3 gardé tel quel, le son, le point de vue caméra, les kilomètres à la montre |
| lun 04/01/2027, 9 h à 10 h | « Tournage 2/2 · saison 2 » | les 8 épisodes de la saison 2, scripts à écrire avant le 21/12 |

Le relevé des demandes BNI a quitté le lundi pour le vendredi 9 h, juste après la réunion BNI La
Défense (décision de Maxime du 08/11). Seul le bloc « Devis, factures, relances » du lundi reste sur
le créneau des deux séances face caméra : il se fait après le tournage, à 10 h.

## 7. Ce qui reste à confirmer

Les scripts ont été arrêtés le 08/11 **sans aucun crochet**, en version sans chiffre, pour la séance du 09/11. Rien n'est inventé ; ce qui n'était pas vérifié a été retiré de la phrase plutôt que supposé.

1. **E07** : la date exacte du premier jour de HYROX Paris (12/12 d'après la veille du 13/10). Deux prises du hook sont tournées (« Dans 4 jours » et « Dans quelques jours »), le montage garde la bonne.
2. Pour une saison 2 chiffrée : l'heure d'arrivée dans l'arène, les kilomètres marchés sur une course (montre, à Paris), le nombre de batteries et de cartes, la masse du 70-200 et la cadence 4K de la FX3 copiées depuis sony.fr, le nombre de plans d'une course et la durée du film livré.
3. Les coachs et athlètes qui peuvent apparaître en plus de Pierre Huiban et Antoine Bouhana (liste promise le 27/10). D'ici là, aucun autre nom, aucun autre visage en sujet principal.
4. « Under the Sun » dans la bibliothèque musicale d'Instagram : à vérifier à la première publication.

## 8. Ce qu'on mesure

Chaque lundi, dans le récap : la portée de chaque reel éducatif comparée à la médiane des reels HYROX (objectif : au-dessus de 2 000 personnes, plan de bataille § 8), les **sauvegardes et partages** des carrousels (la métrique du format), les commentaires aux questions binaires, et les messages reçus. Au bout de quatre semaines : quels chapitres tirent, quels gabarits se sauvegardent, et la saison 2 s'écrit sur ces chiffres.
