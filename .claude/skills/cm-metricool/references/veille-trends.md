# Veille trends quotidienne · Otea Filmakers et OTEA Production

Mise en place le 18/11/2026 à la demande de Maxime : « on va le faire tous les jours ». Avant,
la veille était une étape du lundi, et elle a été sautée : la trend « GTA 5 contre GTA 6 » a été
repérée par Maxime, pas par nous. Tâche planifiée locale : `veille-trends-quotidienne` (7 h 45).

## Les deux comptes et ce qu'une trend doit y devenir

| Compte | blogId | Réseaux visés | Voix | Ce que la trend doit porter |
|---|---|---|---|---|
| Otea Filmakers | 4728418 | Instagram (+ TikTok si le format est photo ou vidéo prête) | « je », tutoiement, B2C athlètes | la course, l'athlète, l'émotion de l'arrivée, le film de sa course |
| OTEA Production | 5733269 | Page LinkedIn + Instagram | « je » et « chez OTEA PRODUCTION, on », **vouvoiement** | la vidéo d'entreprise, mettre les gens à l'aise devant la caméra |

Le LinkedIn branché sur Filmakers est le profil perso de Maxime : n'y rien mettre sans sa demande.

## Où chercher, chaque matin

1. Formats et mèmes de la semaine : TikTok Creative Center, pages « trends this week » (Later, NewEngen,
   SocialPilot, Napoleon Cat), Know Your Meme (entrées récentes), Google Trends France.
2. Sons Reels en hausse (seulement pour un Reel qu'on peut vraiment monter, la musique se pose à la main).
3. Le calendrier des 7 jours : sorties culturelles attendues (jeux, films, séries), fêtes, Black Friday,
   courses HYROX et résultats, événements business (salons, chiffres du marché vidéo).
4. LinkedIn : ce qui tourne dans le fil en France (formats « avant / après », « ce que j'aurais aimé savoir »,
   carrousels), sans copier un post nommé.

Recouper chaque fait cité (date, chiffre, nom) avec deux sources, ou une source officielle.

## Filtre (une trend ne passe que si les quatre sont oui)

1. **Elle se joue maintenant** : pic dans les 72 h, ou date fixe dans les 7 jours.
2. **Elle porte le message du compte sans le tordre** (test Filmakers : un athlète a-t-il envie de la lire ?
   test OTEA : un responsable communication y voit-il la vidéo d'entreprise ?).
3. **On a de quoi la faire vrai** : vraies photos ou vrais rushes, faits vérifiables. Jamais de personne
   générée par IA, jamais de chiffre inventé, jamais de souvenir personnel de Maxime qu'il n'a pas raconté
   (lui demander plutôt la photo ou le fait).
4. **Elle ne vient pas déjà d'être faite** sur le compte (voir le journal ci-dessous).

Pas de trend qui passe le filtre ce jour-là : on ne publie rien, et on le note. Une trend forcée fait
plus de mal qu'un jour sans post.

## Fabrication

- Visuels : photos retouchées de Maxime (`~/Desktop/DOSSIER HYROX/SELECTION GOLD/`, iCloud
  « photo concours selection », Nice dans `~/Pictures/Adobe Lightroom/`) ; cartes Filmakers jaune
  #F2E600 et noir en Inter Black ; cartes OTEA en orange #FF5800 et encre #201E1E, Forma DJR, monogramme.
  Exemple de script : `~/CLAUDE CODE/trends/2026-11-19-gta6/rendu.py`.
- Hooks : `~/.claude/skills/ig-reel/hookscore.py` (prendre le premier à 70 ou plus) ; légendes :
  `ig-caption/caption.py` (READY) puis `ig-human/detect.py` (PASS). Garder l'espace avant « ? : ! »,
  ne pas reprendre la sortie de `humanize.py` qui l'enlève.
- LinkedIn : jamais de lien dans le texte, Calendly en premier commentaire, ligne « 📅 Un projet vidéo ?
  Le lien de l'appel découverte est en commentaire. »
- Hébergement des médias : Higgsfield `media_upload` puis PUT (`Content-Type` + `If-None-Match: *`) puis
  `media_confirm`, et l'URL cloudfront dans Metricool.
- Français : « combien d'HYROX », « un HYROX », « des HYROX » ; jamais « de HYROX », « le HYROX », « au HYROX » (règle de Maxime, 18/11/2026). Chercher `(de|le|du|au|que) HYROX` dans légendes et cartes avant de créer.
- Mode : la tâche planifiée crée en **brouillon** (`draft: true`, `autoPublish: false`) ; seul Maxime, dans
  une conversation, fait passer en publication automatique.

## Journal (le plus récent en haut)

| Date | Trend | Compte | Réseau | Publication | État |
|---|---|---|---|---|---|
| 18/11/2026 | GTA 6 sort le 19/11 (mèmes « We got X before GTA 6 », « moi à la sortie de GTA 5 / de GTA 6 ») | Otea Filmakers | Instagram, carrousel 5 photos « On a eu HYROX avant GTA 6 » | 19/11 12 h (uuid -6016211617704819680) | armé, demandé par Maxime dans la conversation |
| 18/11/2026 | idem | OTEA Production | Page LinkedIn, carrousel 6 cartes « 2013 / 2026 : la vidéo sur les réseaux » | 19/11 8 h 30 (uuid -3492881609517675769) | armé, demandé par Maxime |
| 18/11/2026 | idem | OTEA Production | Instagram, même carrousel | 19/11 12 h 30 (uuid -2148991710398429454) | armé, demandé par Maxime |
| 18/11/2026 | « moi à la sortie de GTA 5 / moi aujourd'hui » version perso de Maxime | Maxime | à décider | | en attente d'une photo de Maxime en 2013 |

Trends vues le 18/11 et non retenues : son « All I Want for Christmas » (pas de Reel prêt), « soft launch »
sur « My Moon My Man » (rien à annoncer), « 5 stages of » (à garder pour un Reel Filmakers, Roxzone).
