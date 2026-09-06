# Mandat Vidéo : l'outil « photos → vidéo d'annonce », état au 06/09/2026, version 2

Ce que Maxime a précisé le 06/09 : le but n'est pas de faire une vidéo pour
La Galerie, c'est de **recréer l'outil** de diane.estate (des photos entrent,
une vidéo d'annonce sort) pour le proposer à moyen terme à toutes les agences
immobilières indépendantes. Rémi de La Galerie en est le premier testeur.

## Où l'essayer

**https://mandatvideo.higgsfield.app**

L'appli tourne sur la plateforme d'applications Higgsfield : l'utilisateur se
connecte avec son compte Higgsfield et l'animation des photos est facturée
sur ses crédits. C'est la seule voie de déploiement disponible depuis cet
environnement, et c'est aussi ce qui rend l'outil testable par Rémi sans
serveur à administrer. À noter pour la suite commerciale : chaque agence
cliente devra avoir un compte Higgsfield, ou bien il faudra reconstruire le
même produit sur une infrastructure à nous.

## Ce que fait l'outil, calqué sur le parcours Diane

Le parcours de diane.estate, tel que reconstitué le 06/09 : l'agent colle le
lien d'une annonce (ou dépose photos et détails à la main), l'IA rédige une
narration propre au bien à partir de ses faits, la voix de l'agence la lit,
les photos sont animées et montées avec intro, outro, musique, transitions,
en vertical et en horizontal, en Full HD. Mandat Vidéo refait ce parcours,
étape par étape :

1. **Import de l'annonce par lien.** L'agent colle l'URL de l'annonce sur son
   site ou un portail. Le serveur lit la page : titre, description, photos
   (JSON-LD et balises images, 24 candidates au plus), et repère surface,
   pièces, chambres et prix dans le texte. L'agent coche les photos à garder,
   les faits sont pré-remplis. Les portails qui refusent les robots renvoient
   « bloqué » ; dans ce cas, dépôt manuel des photos comme avant.
2. **Dépôt manuel** possible en complément ou à la place : 3 à 8 photos,
   une pièce nommée par photo.
3. **Profil d'agence mémorisé une fois** : nom, ville, couleur, logo, voix.
   Bouton « Mémoriser l'agence », rechargé à chaque visite. Le logo se pose
   sur l'intro, l'outro et chaque plan.
4. **Narration** : une phrase par photo, rédigée par le LLM de la plateforme à
   partir des seuls faits importés ou saisis (repli sur des phrases neutres si
   le LLM est indisponible). Relecture et correction avant de lancer.
5. **Voix off** : sans voix, voix féminine, voix masculine, ou « ma voix »
   avec un identifiant de voix clonée ElevenLabs (l'équivalent de la voix
   enregistrée une fois chez Diane). Synthèse ElevenLabs `eleven_multilingual_v2`
   côté serveur, une piste par plan, calée au début du plan, musique baissée
   dessous. Quand la voix dure plus de 5 secondes, la dernière image du plan
   est tenue (8 secondes au plus) pour que la phrase se termine à l'écran.
6. **Animation** : chaque photo est animée en image-to-video, caméra fixe,
   5 secondes, `seedance_2_0` mode rapide 720p, **18 crédits par photo**,
   dans le cadre d'origine de la photo (dimensions mesurées dans le
   navigateur et transmises au modèle). Une validation Higgsfield par photo.
7. **Réglages de rendu** : qualité 720p (rapide) ou **Full HD 1080p** ;
   mouvement « caméra fixe » ou « rapproché lent » (léger travelling avant
   ajouté au montage, en plus de l'animation) ; format vertical, horizontal,
   ou **les deux d'un coup** avec les mêmes animations, donc sans crédits
   supplémentaires.
8. **Montage dans le navigateur** avec ffmpeg en WebAssembly : intro à la
   couleur de l'agence, plans en fondu avec pièce et phrase incrustées, logo,
   outro « visite sur rendez-vous », musique en synthèse procédurale (zéro
   droits), voix mixée. 30 à 45 secondes. Compter deux à quatre minutes en
   720p, davantage en 1080p, onglet ouvert.
9. La vidéo est enregistrée dans le stockage de l'appli, lisible et
   téléchargeable depuis l'onglet « Mes vidéos », le rendu 1080p (montage plus long), la lecture
d'un site d'annonce précis (chaque portail a sa structure).

Ce que l'outil s'interdit, comme la proposition du 02/09 : aucun visage
généré, aucune vue drone inventée, aucun chiffre qui ne vienne pas de
l'annonce ou de l'agent.

## Ce qui manque encore par rapport à Diane

- **Clé ElevenLabs à poser** avant que la voix fonctionne : secret
  `ELEVENLABS_API_KEY` du site (outil `website_secrets`, puis redéploiement).
  Sans clé, l'appli le dit et produit la vidéo sans voix.
- Pas d'avatar incrusté, et ce n'est pas prévu : règle absolue du dépôt.
- Pas de publication ni de programmation directe vers Instagram, TikTok,
  LinkedIn, YouTube : la vidéo se télécharge, la programmation passe par
  Metricool (en brouillon, règle permanente).
- Pas d'extension Chrome : l'import se fait en collant le lien.
- Une seule langue de narration, le français. Diane en annonce 42.
- Le montage dépend du navigateur de l'agent (onglet ouvert). Le conteneur
  ffmpeg côté serveur a été écrit (`app/container/`), mais la plateforme ne
  sait pas encore déployer les conteneurs : trois tentatives, échec au
  provisionnement du Durable Object. Le code est prêt le jour où elle le
  permet.

## Où est le code

Dépôt de l'appli (hébergé par Higgsfield, accessible depuis la sandbox
Higgsfield, pas depuis GitHub) :
`https://apps-repos.higgs.ai/hfu-user2zae6klRfE97hlBWhyQP6j7d9cR/mandatvideo-3f0e19ac-0800-454c-a0d3-c4e2204167e7.git`

Site : `mandatvideo`, identifiant `3f0e19ac-0800-454c-a0d3-c4e2204167e7`.
Un premier site `mandat-video` (`a9928943-36cc-4d25-84bd-dc6731e758c0`) a
servi aux essais de déploiement du conteneur ; il est abandonné.

Fichiers qui portent le produit :

| Fichier | Rôle |
|---|---|
| `app/src/layouts/app-detail.tsx` | l'écran : import par lien, photos, profil, réglages, lancement, suivi, résultat, liste des vidéos |
| `app/src/components/listing-import.tsx` | le bloc « coller le lien de l'annonce » et le choix des photos |
| `app/src/lib/listing.functions.ts` | lecture serveur de la page d'annonce : titre, photos, faits |
| `app/src/routes/api/import/image.ts` | rapatriement serveur d'une photo d'annonce (https, 20 Mo max) |
| `app/src/lib/profile.functions.ts` | profil d'agence : lecture et mémorisation |
| `app/src/routes/api/tts.ts` | la voix off, ElevenLabs côté serveur, clé dans le secret du site |
| `app/src/lib/assemble.browser.ts` | le montage ffmpeg dans le navigateur : calques au canvas, logo, voix, musique, 720p/1080p, travelling |
| `app/src/lib/videos.functions.ts` | fonctions serveur : création, statut, liste, suppression, narration |
| `app/src/lib/narration.server.ts` | la phrase par pièce, LLM de la plateforme avec repli |
| `app/src/routes/api/videos/$id/output.ts` | dépôt du mp4 monté dans R2 |
| `app/src/routes/api/videos/$id/file.ts` | lecture et téléchargement, réservés au propriétaire |
| `app/src/routes/api/proxy.ts` | relais des clips générés et du logo vers ffmpeg (CORS) |
| `app/migrations/0002_videos.sql`, `0003_profiles.sql` | les tables `videos` et `agency_profiles` (D1) |
| `app/container/` | l'assemblage serveur (ffmpeg + Node), prêt mais non déployable aujourd'hui |
| `app/public/ffmpeg/` | le moteur ffmpeg WebAssembly, en deux morceaux (limite de 25 Mo par fichier) |

## Ce qui a été vérifié, et ce qui ne l'a pas été

Vérifié : la compilation TypeScript est propre, le site est construit et en
ligne, les fichiers du moteur de montage et les médias d'exemple sont servis,
la connexion renvoie bien vers l'authentification Higgsfield.

Non vérifié : le parcours complet dans un navigateur connecté (import par
lien, dépôt des photos, animation, voix, montage, dépôt du fichier). La plateforme refuse tout
accès sans session Higgsfield, y compris à la page d'accueil, et cet
environnement n'en a pas. Le premier essai réel sera donc celui de Maxime
ou de Rémi. Les points à surveiller au premier passage : la validation
Higgsfield par photo, le temps de montage, la lecture de la vidéo dans
l'onglet « Mes vidéos ».

## Pour Rémi

Lui envoyer le lien, avec trois consignes : se connecter avec un compte
Higgsfield (crédits nécessaires, 18 par photo), coller le lien d'une de ses
annonces en ligne (ou déposer 4 à 6 photos), laisser l'onglet ouvert pendant
le montage. Remplir le profil d'agence une fois et le mémoriser. Le premier
retour utile : le rendu lui convient-il, et combien de temps a pris le
montage sur sa machine.
