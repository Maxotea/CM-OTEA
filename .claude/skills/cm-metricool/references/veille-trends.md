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
- Français (règles de Maxime, 18/11/2026) : « combien d'HYROX », « un HYROX », « des HYROX », « l'HYROX de Bordeaux », « à l'HYROX de Rome ». Jamais « de HYROX », « le HYROX », « au HYROX », ni « HYROX Bordeaux » au milieu d'une phrase (hashtags exceptés). Chercher `(de|le|du|au|que) HYROX` et `HYROX [A-Z]` dans légendes, cartes et textes alternatifs avant de créer.
- Mode : la tâche planifiée crée en **brouillon** (`draft: true`, `autoPublish: false`) ; seul Maxime, dans
  une conversation, fait passer en publication automatique.

## Journal (le plus récent en haut)

| Date | Trend | Compte | Réseau | Publication | État |
|---|---|---|---|---|---|
| 24/11/2026 | Aucune trend retenue : rien créé. Calendriers relus : Filmakers a un post feed les 24, 25, 26, 27, 29 et 30/11 et le 1/12 (libre : 28), OTEA Production les 24, 25, 26 et 27/11 et le 1/12 (libres : 28, 29 et 30) | les deux | | | rien à valider |
| 24/11/2026 | « First to react loses challenge », « POV : you're the villain but... », « Morning brain stack » (Virlo, semaine au 23/11) | les deux | Instagram, Reel | | écartées : une seule source (Virlo), aucune autre page ne les décrit ; jeu de réaction ou playback sans lien avec la course ni la vidéo d'entreprise |
| 24/11/2026 | Spotify Wrapped 2026 : toujours aucune annonce de Spotify (prédiction mercredi 2/12, Official Charts, Techloy) | les deux | | | écartée : date non confirmée. Toujours en attente des vrais chiffres 2026 de Maxime si on le fait |
| 24/11/2026 | HYROX : Dallas fini (aucun résultat 2026 publié), Utrecht du 26 au 30/11 ; ciné du 25/11 (« Billie, à la croisée des mondes », « Mon beau-père, ma belle-fille et moi »), « Blade Runner 2099 » sur Prime Video le 25/11 | les deux | | | écartées : Maxime n'y filme pas, rien qui porte la course ou la vidéo d'entreprise |
| 24/11/2026 | Toujours en tête : « Housewife », « Stop the Wedding », « It's time » (Noël), « Dame Hombro » ; LinkedIn : aucun format daté de novembre (études générales 2026 : carrousels document en tête) | les deux | | | écartées : mêmes raisons que les 21 au 23/11 |
| 23/11/2026 | Aucune trend retenue : rien créé. Calendriers relus : Filmakers a un post feed les 23, 24, 25, 27, 29 et 30/11 (libres : 26 et 28), OTEA Production les 23, 24, 25, 26 et 27/11 (libres : 28, 29 et 30) | les deux | | | rien à valider |
| 23/11/2026 | « Vlog timestamps » / journée racontée heure par heure (Later au 23/10, Inmagic au 16/11) | OTEA Production | Instagram, Reel | | écartée : pic passé (Later d'octobre), et il faut de vrais rushes horodatés d'une journée de tournage. Idée qui attend Maxime : filmer sa prochaine journée de tournage en plans courts avec l'heure |
| 23/11/2026 | « I feel like I haven't done much this year » (Later), toujours une seule source | Otea Filmakers | Instagram | | déjà en attente de Maxime (21/11) : une vraie photo par mois de 2026 et la course filmée chaque mois |
| 23/11/2026 | Spotify Wrapped 2026 : toujours aucune date officielle (prédiction 2/12, Official Charts, Techloy) ; HYROX Dallas fini, aucun résultat 2026 publié ; Hunger Games préquelle (date FR 18 ou 25/11 selon les sources) | les deux | | | écartées : date non confirmée, Maxime n'y filme pas, rien qui porte la course ou la vidéo d'entreprise |
| 23/11/2026 | Toujours en tête : « Housewife », « Stop the Wedding », « Coming Up Roses », « Dear Santa », « My moon my man », transitions maquillage (Virlo au 18/11) ; LinkedIn : aucun format daté de novembre | les deux | | | écartées : mêmes raisons que les 21 et 22/11 |
| 22/11/2026 | Aucune trend retenue : rien créé. Calendriers relus : Filmakers a un post feed les 22, 23, 24, 25, 27 et 29/11 (libres : 26 et 28), OTEA Production les 23, 24, 25, 26 et 27/11 (libres : 22, 28 et 29) | les deux | | | rien à valider |
| 22/11/2026 | Spotify Wrapped 2026, date seulement prédite au mercredi 2/12 (Official Charts), aucune annonce de Spotify | les deux | Instagram, LinkedIn | | écartée : hors fenêtre de 7 jours et date non confirmée. À revoir dès que Spotify l'annonce (format « mon année en chiffres » possible si Maxime fournit ses vrais chiffres 2026) |
| 22/11/2026 | « Yes… But » (écran partagé, l'attrait puis le revers) | Otea Filmakers | Instagram | | écartée : une seule source (SocialBee, liste du 29/10), pic passé |
| 22/11/2026 | Toujours en tête : « Housewife », « Stop the Wedding », « Coming Up Roses », « It's time », « Dear Santa », « Dame Hombro » ; formats FR début novembre « La plus belle photo », « Deux quotidiens, une journée » (Media.io, non daté) | les deux | | | écartées : mêmes raisons que le 21/11 (Noël, playback, danse) ; formats FR sur une seule source non datée |
| 22/11/2026 | HYROX Dallas finit aujourd'hui (résultats 2026 pas encore publiés), Utrecht du 26 au 30/11 ; Thanksgiving 26/11 ; ciné du 25/11 | les deux | | | écartées : Maxime n'y filme pas, fête américaine, aucun mème lié |
| 21/11/2026 | Aucune trend retenue : rien créé. Calendriers relus : Filmakers a un post feed les 22, 23, 24, 25 et 27/11 (libres : 21, 26 et 28), OTEA Production les 23, 24, 25, 26 et 27/11 (libres : 21, 22 et 28) | les deux | | | rien à valider |
| 21/11/2026 | « I feel like I haven't done much this year » (récap mois par mois de la pellicule, Later au 20/11) | Otea Filmakers | Instagram, carrousel ou Reel | | écartée : une seule source, et il faut savoir quelle course Maxime a filmée chaque mois de 2026 avec une vraie photo par mois. Idée qui attend Maxime, plutôt pour début décembre |
| 21/11/2026 | « It's NO-vember », « Christmas Wrapping Paper Reveal », « Dear Santa », « Coming Up Roses » (Harry Styles), sons « Housewife », « Last Christmas » | les deux | | | écartées : Noël (interdit sur Filmakers), une seule source par format, rien qui porte la course ou la vidéo d'entreprise |
| 21/11/2026 | « Purple Rain » riff, « I'm still Gibby », « Oops, wrong way », « Dame Hombro » | les deux | | | écartées : sources faibles (blog d'outil IA, presse espagnole), playback ou danse sans lien avec les deux comptes |
| 21/11/2026 | Novemb'Run à Paris le 22/11 ; HYROX Dallas (18 au 22/11) puis Utrecht (26 au 30/11), aucun résultat 2026 publié | Otea Filmakers | | | écartée : Maxime n'y filme pas |
| 20/11/2026 | Aucune trend retenue : rien créé. Calendriers relus : Filmakers a un post les 20, 22, 23, 24, 25 et 27/11 (libres : 21 et 26), OTEA Production les 20, 23, 24, 25, 26 et 27/11 (libres : 21 et 22) | les deux | | | rien à valider |
| 20/11/2026 | Black Friday, vendredi 27/11 (entré dans la fenêtre de 7 jours) | les deux | Instagram, LinkedIn | déjà au calendrier : Filmakers 27/11 18 h « le matériel qui a vraiment filmé l'HYROX de Rome » (uuid 2999143641081135997), OTEA Production 27/11 12 h « pas de promo chez nous. Une date, oui. » (uuid 1854608371791383726) | écartée : déjà faite sur les deux comptes, un second post doublerait le créneau |
| 20/11/2026 | Son « Flower In A Hurricane » (bande originale de GTA VI), son le plus utilisé en Reels selon Virlo au 18/11 | les deux | Instagram, Reel | | écartée : GTA 6 déjà fait le 19/11 sur les deux comptes, une seule source, pas de Reel prêt |
| 20/11/2026 | « I saw you on 8th Avenue » et « Entiende, corazón glow-up » (liste Postdom du 16/11) | Otea Filmakers | Instagram, Reel | | écartées : une seule source, aucune explication du format trouvée ailleurs ; le glow-up ferait doublon avec le Reel avant / après du 25/11 |
| 20/11/2026 | Toujours en tête : « My moon, my man », « Time : then and now », « It's time » et sons de Noël | les deux | | | écartées le 19/11, mêmes raisons (couple, photo ancienne de Maxime à fournir, Noël) |
| 20/11/2026 | HYROX : Dallas en cours (18 au 22/11), Utrecht du 26 au 30/11 | Otea Filmakers | | | écartée : Maxime n'y filme pas, aucun résultat officiel 2026 publié dans les sources |
| 20/11/2026 | Sorties du 25/11 au cinéma (« Billie, à la croisée des mondes », « Mon beau-père, ma belle-fille et moi ») et « Quasimodo » sur Netflix le 27/11 | les deux | | | écartées : rien qui porte la course ou la vidéo d'entreprise, aucun mème associé repéré |
| 19/11/2026 | Aucune trend retenue : rien créé (les deux calendriers ont déjà un post par jour du 19 au 26/11, sauf le 21 et le 22 sur OTEA Production) | les deux | | | rien à valider |
| 19/11/2026 | « Then and now » sur « Time » de Pink Floyd (vieille photo, puis la même pose aujourd'hui, années à l'écran) | Otea Filmakers | Instagram | | écartée : trop proche du GTA 5 / GTA 6 de la veille, et demande une vraie photo ancienne de Maxime (ses premiers appareils à 16 ans). En attente de Maxime |
| 19/11/2026 | « Lately on my SD card » (visuel de carte SD, puis une rafale d'images récentes) | Otea Filmakers | Instagram, Reel | | écartée : une seule source (New Engen, 13/11), et il faut des rushes vraiment récents montés en Reel. En attente de Maxime |
| 19/11/2026 | Black Friday, vendredi 27/11 (« Add to cart », « Zoom in » avec code caché) | les deux | Instagram, LinkedIn | | écartée aujourd'hui : hors fenêtre de 7 jours, et aucune offre décidée. À revoir dès le 20/11 si Maxime fixe une offre athlètes ou un angle « une vidéo ne se solde pas » |
| 19/11/2026 | « My moon, my man », « Paid me no mind », « It's time » et sons de Noël, « Housewife », planches de Thanksgiving (26/11) | les deux | | | écartées : couple, playback, Noël (interdit sur Filmakers) ou fête américaine, rien qui porte la course ou la vidéo d'entreprise |
| 19/11/2026 | HYROX : Dallas du 18 au 22/11, Utrecht du 26 au 30/11 ; résultats du 13 au 15/11 (Le Caire, Dublin, Denver, Séoul, Barcelone) | Otea Filmakers | | | écartée : Maxime n'y filme pas, aucun athlète suivi cité par les sources |
| 18/11/2026 | GTA 6 sort le 19/11 (mèmes « We got X before GTA 6 », « moi à la sortie de GTA 5 / de GTA 6 ») | Otea Filmakers | Instagram, carrousel 5 photos « On a eu HYROX avant GTA 6 » | 19/11 12 h (uuid -6016211617704819680) | armé, demandé par Maxime dans la conversation |
| 18/11/2026 | idem | OTEA Production | Page LinkedIn, carrousel 6 cartes « 2013 / 2026 : la vidéo sur les réseaux » | 19/11 8 h 30 (uuid -3492881609517675769) | armé, demandé par Maxime |
| 18/11/2026 | idem | OTEA Production | Instagram, même carrousel | 19/11 12 h 30 (uuid -2148991710398429454) | armé, demandé par Maxime |
| 18/11/2026 | « moi à la sortie de GTA 5 / moi aujourd'hui » version perso de Maxime | Maxime | à décider | | en attente d'une photo de Maxime en 2013 |

Trends vues le 18/11 et non retenues : son « All I Want for Christmas » (pas de Reel prêt), « soft launch »
sur « My Moon My Man » (rien à annoncer), « 5 stages of » (à garder pour un Reel Filmakers, Roxzone).
