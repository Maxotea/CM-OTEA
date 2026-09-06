# Mandat Vidéo : l'outil « photos → vidéo d'annonce », état au 06/09/2026

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

## Ce que fait l'outil

1. L'agent dépose 3 à 8 photos de l'annonce. Chaque photo est recadrée dans
   le navigateur au format choisi (vertical 9:16 ou horizontal 16:9) **avant**
   d'être animée, pour que le modèle ne réinvente jamais la pièce.
2. Il nomme chaque pièce, indique le type de bien, l'agence, la ville, et ce
   qu'il accepte d'afficher (surface, étage, prix). Rien d'autre n'est affiché
   ni écrit.
3. Une phrase par photo est rédigée par le LLM de la plateforme à partir de
   ces seuls faits (repli sur des phrases neutres si le LLM est indisponible).
   L'agent peut la relire et la corriger avant de lancer.
4. Chaque photo est animée en image-to-video, caméra fixe, 5 secondes,
   modèle `seedance_2_0` en mode rapide 720p : **18 crédits par photo**
   (6 photos = 108 crédits). Chaque animation passe par la validation
   Higgsfield, donc une confirmation par photo.
5. Le montage se fait **dans le navigateur** avec ffmpeg en WebAssembly :
   intro à la couleur de l'agence, clips enchaînés en fondu avec le nom de la
   pièce et la phrase incrustés, outro « visite sur rendez-vous », musique en
   synthèse procédurale (zéro droits). Environ 32 secondes, 720×1280 ou
   1280×720. Compter deux à quatre minutes de montage selon la machine.
6. La vidéo est enregistrée dans le stockage de l'appli, lisible et
   téléchargeable depuis l'onglet « Mes vidéos ».

Ce que l'outil s'interdit, comme la proposition du 02/09 : aucun visage
généré, aucune vue drone inventée, aucun chiffre qui ne vienne pas de l'agent.

## Ce qui manque encore par rapport à Diane

- **Pas de voix off** : la plateforme n'expose pas de synthèse vocale dans son
  SDK d'applications. Le texte est à l'écran, pas dit. À ajouter dès qu'un
  modèle de voix est disponible côté SDK, ou via un service tiers.
- Pas d'avatar, et ce n'est pas prévu : règle absolue du dépôt.
- Le montage dépend du navigateur de l'agent (onglet ouvert pendant le
  montage). Le conteneur ffmpeg côté serveur a été écrit
  (`app/container/`), mais la plateforme ne sait pas encore déployer les
  conteneurs : trois tentatives, échec au provisionnement du Durable Object.
  Le code est prêt le jour où elle le permet.
- Rendu en 720p pour tenir le temps de montage dans le navigateur.
- Pas d'import d'annonce depuis un portail : les photos se déposent à la
  main.

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
| `app/src/layouts/app-detail.tsx` | l'écran : photos, réglages, lancement, suivi, résultat, liste des vidéos |
| `app/src/lib/assemble.browser.ts` | le montage ffmpeg dans le navigateur, calques de texte au canvas, musique |
| `app/src/lib/videos.functions.ts` | fonctions serveur : création, statut, liste, suppression, narration |
| `app/src/lib/narration.server.ts` | la phrase par pièce, LLM de la plateforme avec repli |
| `app/src/routes/api/videos/$id/output.ts` | dépôt du mp4 monté dans R2 |
| `app/src/routes/api/videos/$id/file.ts` | lecture et téléchargement, réservés au propriétaire |
| `app/src/routes/api/proxy.ts` | relais des clips générés vers ffmpeg (CORS) |
| `app/migrations/0002_videos.sql` | la table `videos` (D1) |
| `app/container/` | l'assemblage serveur (ffmpeg + Node), prêt mais non déployable aujourd'hui |
| `app/public/ffmpeg/` | le moteur ffmpeg WebAssembly, en deux morceaux (limite de 25 Mo par fichier) |

## Ce qui a été vérifié, et ce qui ne l'a pas été

Vérifié : la compilation TypeScript est propre, le site est construit et en
ligne, les fichiers du moteur de montage et les médias d'exemple sont servis,
la connexion renvoie bien vers l'authentification Higgsfield.

Non vérifié : le parcours complet dans un navigateur connecté (dépôt des
photos, animation, montage, dépôt du fichier). La plateforme refuse tout
accès sans session Higgsfield, y compris à la page d'accueil, et cet
environnement n'en a pas. Le premier essai réel sera donc celui de Maxime
ou de Rémi. Les points à surveiller au premier passage : la validation
Higgsfield par photo, le temps de montage, la lecture de la vidéo dans
l'onglet « Mes vidéos ».

## Pour Rémi

Lui envoyer le lien, avec trois consignes : se connecter avec un compte
Higgsfield (crédits nécessaires, 18 par photo), déposer 4 à 6 photos d'une
annonce en ligne, laisser l'onglet ouvert pendant le montage. Le premier
retour utile : le rendu lui convient-il, et combien de temps a pris le
montage sur sa machine.
