# Audit de l'usage de Claude, 16/10/2026

Demande de Maxime : « J'ai l'impression de mettre beaucoup de choses dans Claude Code alors que
je pourrais les mettre dans Cowork ou dans Normal. » Verdict : l'impression est juste, mais le
problème est plus large que Code contre Cowork. Le plan d'action est dans
`.claude/references/organisation-claude.md`.

## Ce que j'ai pu voir, et ce que je n'ai pas vu

Vu, avec des chiffres : le dépôt CM-OTEA, les 15 routines cloud, les 520 runs GitHub Actions,
les PR, les connecteurs attachés à chaque routine.

Pas vu : les tâches planifiées locales de Cowork, les Projets et conversations de claude.ai, le
contenu des 19 skills `anthropic-skills:*` du compte, les statistiques de consommation du
forfait. Tout ce qui touche à ces points est marqué « à vérifier ». La consommation de tokens n'a pas été
mesurée : le chapitre 8 de `organisation-claude.md` la traite par les leviers qu'on peut établir
sans ces chiffres.

## 1. Photographie

| Surface | Ce qui s'y trouve | Chiffres |
|---|---|---|
| Claude Code, dépôt CM-OTEA | moteur CM (carrousels, review, montage vidéo, pub Meta), 8 skills, 14 mémoires, 4 workflows | 29 scripts Python (8 450 lignes), 91 tests, 56 fichiers Excel versionnés, 50 commits en 6 semaines dont 27 par robot |
| Routines cloud | briefings perso, compta, revue d'outil, review client, vidéo TikTok, posts | 15 routines : 12 récurrentes actives, 2 rappels uniques, 1 coupée |
| GitHub Actions | relève de la review, carrousels, boîtes Drive, tests | 520 runs depuis août |
| Compte (hors dépôt) | 19 skills `anthropic-skills:*`, plugin small-business (une quarantaine de skills), 27 connecteurs | non mesuré |

Répartition des 3,1 Mo de fichiers suivis par git, hors images, polices et catalogue d'API
(mesurée le 16/10) :

| Nature | Poids | Part | Exemples |
|---|---|---|---|
| Savoir métier lu par Claude | 1 362 Ko | 44 % | fiches clients, skills, mémoires, références (dont un PDF d'offres de 0,9 Mo) |
| État et données d'exécution | 889 Ko | 29 % | `reviews/` (56 xlsx et journaux), `recaps/`, `photos/*.json`, specs de carrousels |
| Code et tests | 469 Ko | 15 % | `scripts/`, `tests/`, `.github/` |
| Documents commerciaux et d'agence | 254 Ko | 8 % | `offre/`, `design-presentation/`, devis, pitch, kit de la semaine |
| Divers | 125 Ko | 4 % | |

Seuls 15 % du poids sont du code, le seul travail qui exige vraiment Claude Code. Le reste est du
savoir, de l'état et des documents.

## 2. Constats, du plus urgent au moins urgent

### C1. La routine « POST CM-OTEA » repart lundi 19/10 à 05h02 (Paris) sans garde-fous

Son prompt tient en une ligne : « Rédige, réalise et/ou vérifie les posts de tous les clients
CM-OTEA sur Metricool pour les 2 semaines qui arrivent ». Aucun dépôt n'y est attaché, donc
`CLAUDE.md` n'est pas chargé. La règle non négociable (tout en brouillon) n'est écrite nulle
part dans ce que la routine lit. Elle a quand même tourné le 12/10 sans incident connu, mais
rien ne l'y oblige. Un rappel existe déjà (18/10 à 19h00 Paris) mais demande à Maxime de coller
lui-même le texte. Le texte prêt à coller est dans le plan.

### C2. Six sorties quotidiennes pour une seule question : « quoi faire maintenant ? »

| Routine | Heure (Paris, été) | Canal |
|---|---|---|
| Résumé matinal | 05h30 | page HTML |
| Point du matin | 07h00 | mail |
| Point compta du matin | 08h00 | tableau de bord + message |
| Point tâches quotidien | 08h30 | conversation |
| Point du midi | 12h30 | mail |
| Point du soir | 18h30 | mail |

Quatre bilans entre 05h30 et 08h30, tous lisent Gmail et l'agenda, trois répètent les mêmes
règles d'écriture et le même « contexte connu » daté. Les prompts disent eux-mêmes que le but est
de ne pas se disperser : six messages par jour dans quatre formats produisent l'inverse. Le
contexte copié dans les prompts date du 18 et du 23 septembre : factures, devis et échéances y
sont périmés depuis des semaines.

### C3. Le quota est épuisé le matin, et ce sont les routines de développement qui tombent

Ce matin, « Revue quotidienne de l'outil CM » (07h04 UTC) et « Upgrade quotidien de La Chasse »
(07h14 UTC) ont échoué avec la même cause : limite d'usage atteinte. Avant elles, entre 03h et
07h UTC, passent le résumé matinal, la production de la vidéo TikTok quotidienne, le point du
matin, le point compta et le point tâches. Je n'ai pas la consommation exacte : le lien de cause
à effet est une hypothèse, l'échec par limite d'usage est un fait.

Résultat visible dans le dépôt : sur `main`, une seule revue datée (06/09) en 40 jours, et un
backlog jamais remis à jour depuis le 06/09. La routine existe, ses revues n'arrivent pas.

### C4. Une chaîne vidéo autonome tourne chaque jour ouvré sur un projet que les routines classent « sans revenu »

« ExpliqueMoi vidéo quotidienne » (04h00 UTC) génère et publie en automatique une vidéo TikTok :
crédits Higgsfield et gros bloc de quota Claude, sans validation. Les prompts du matin et du
midi rangent ExpliqueMoi parmi les projets annexes qui dispersent et ne rapportent rien pour
l'instant, avec une trésorerie décrite comme tendue. C'est une décision de priorité, pas
technique, mais elle pèse sur le quota des autres routines.

### C5. Les routines portent trop de connecteurs

« Point du matin » et « Point du midi » ont chacune 22 à 25 connecteurs attachés, dont Uber,
Uber Eats, Booking, Spotify, Strava, Meta Ads, Higgsfield. Elles lisent des mails de tiers et
peuvent mettre des mails à la corbeille. Meta Ads, qui peut dépenser de l'argent, est joignable
depuis une routine qui lit du texte venu de l'extérieur, alors que la règle « tout en PAUSE » ne
vit que dans le skill du dépôt. Les prompts interdisent d'agir hors périmètre, mais un
connecteur qui n'est pas attaché est une protection plus solide qu'une consigne.

### C6. La review client du vendredi copie un fichier Excel en le retranscrivant à travers le modèle

La routine « Review, préparation du vendredi » dépose chaque xlsx dans le Drive du client par un
« protocole de transcription base64 vérifiée (cat, écrire, cmp, corriger, cmp, émettre) ».
C'est la manière la plus chère possible de copier un fichier : le contenu passe par le contexte
du modèle. Autour, la chaîne empile un cron GitHub qui ne part pas (7 vendredis manqués), une
relève qui rate un passage sur trois, 56 xlsx et des journaux JSON versionnés. Les fichiers les
plus modifiés du dépôt sont `reviews/config.json` (9 fois), `reviews/etat/*.json` et les xlsx.
27 commits sur 50 sont des commits de robot « Génère les fichiers de review » ou « Applique les
décisions ». Git sert de base de données et de messagerie de fichiers.

Deux pistes plus légères, à tester :
- Le connecteur Metricool natif (déjà connecté) expose `createScheduledPostForReview` : un post
  envoyé en validation à des relecteurs par mail, avec règle d'approbation. Il demande un forfait
  Metricool avec gestion d'équipe, à vérifier.
- Le tableau de review écrit directement en Google Sheet natif via le connecteur Google Sheets
  ou Zapier, sans xlsx ni base64.

### C7. Le connecteur Metricool natif existe et n'est utilisé nulle part

Aucun fichier du dépôt ne mentionne `createScheduledPost` ni le serveur `ai.metricool.com`. Tout
passe par 21 actions de code Zapier avec des défauts documentés : décalage horaire de 7 h sur
l'action unitaire, limite de 6 créations, rattrapage `bulk_set_draft`. Le connecteur natif prend
`draft`, `autoPublish`, un fuseau IANA explicite dans `publicationDate`, et renvoie un lien vers
le post. À tester sur un compte de test avant de migrer. Le point 17 du backlog le prévoyait déjà
sous la forme d'un script d'API directe.

### C8. Le récap du lundi n'a plus de routine

La mémoire `recap-hebdo-lundi` et la tâche `recap-hebdo-publications` décrivent un récap chaque
lundi à 9h. Aucune des 15 routines ne porte ce nom, le README et la passation disent « la routine
reste à créer », et le dernier récap du dépôt date du 24/08. Si une tâche locale Cowork le fait,
je ne peux pas le voir. À vérifier.

### C9. Six skills « SOCIAL MEDIA CEO » vivent dans un dépôt de code

`smc-ceo-day`, `smc-client`, `smc-contenu`, `smc-kpi-review`, `smc-ops-finance`, `smc-veille`
viennent d'un Notion de formation. Ils ont été posés en un seul commit, jamais modifiés depuis,
et aucune routine ni script ne les appelle. Ils décrivent des bases (Contacts, My Brain, KPIS)
qui existent dans Notion, pas dans le dépôt, et le connecteur Notion n'est pas authentifié ici.
Ce sont des cadres de réflexion et de rédaction : leur place est un Projet claude.ai ou Cowork,
avec Notion connecté. Ils alourdissent aussi la liste de skills de chaque session Code (environ
3 Ko de descriptions).

### C10. Des documents d'agence s'accumulent dans le dépôt

`offre/`, `design-presentation/`, `design-video-annonce/`, les devis Amundi et Puteaux, le pitch
CCI, le kit de la semaine : environ 250 Ko de documents commerciaux, dont des HTML de devis, que
Claude Code n'exécute pas. Ils vivent là parce que la session était ouverte à cet endroit. Le
dossier `medias/` (1,5 Go, hors git, copié à la main) est l'inverse : du travail sur fichiers
locaux que Cowork fait mieux que Code.

### C11. Les règles d'écriture sont copiées dans 9 endroits

« Pas de tiret cadratin » est dans la mémoire, dans `CLAUDE.md`, dans un test, et dans au moins
7 prompts de routines. Le tutoiement, l'autonomie de décision, le périmètre « jamais d'envoi » :
même schéma. Une règle qui vit partout n'est tenue nulle part le jour où on la change.

### C12. Horloge d'hiver : 9 routines glisseront d'une heure le 25 octobre

Les crons sont écrits en UTC. Seules « Résumé matinal » et « BNI » utilisent `CRON_TZ=Europe/Paris`.
Les points matin, midi, soir, la revue d'outil, La Chasse et la préparation du vendredi
passeront à 06h, 11h30, 17h30, 08h, 08h et 07h. Seul « Point compta » contient une consigne qui
corrige l'horaire.

### C13. Dette d'hygiène, petite mais réelle

- L'index `MEMORY.md` pointe vers `project_make_people.md`, qui n'existe pas.
- Trois fichiers gardent des chemins macOS `/Users/oteaproduction/` (deux mémoires et la note de portage).
- `_to_delete/smc-install.zip` est là depuis la migration.
- Les runs « Boîtes de dépôt Drive » échouent 4 fois sur 4 dans l'échantillon récent, cause
  connue du backlog depuis le 19/08 (dossier non partagé en édition). Un run vert sur deux est
  « Tests », qui ne dit rien de la production.
- La dette de PR s'est résorbée : 16 PR ouvertes le 06/09, une seule aujourd'hui.

## 3. Ce qui est bien placé et doit rester dans Claude Code

À ne pas déplacer : `scripts/carrousel.py`, `publier.py`, `review.py` (le moteur, tant qu'il
existe), `reel-montage.py`, `aftermovie.py`, `habillage.py`, `campagne.py`, les tests, les
workflows déterministes, les skills `cm-metricool` et `cm-meta-ads` (liés aux scripts, aux specs
JSON et aux règles « brouillon » et « PAUSE »), et `CLAUDE.md`. Les règles non négociables sont
bien versionnées, et c'est la bonne leçon de la migration d'août.

## 4. Lecture d'ensemble

Le dépôt est devenu trois choses à la fois : un moteur de code (ce qu'il doit être), le tableau
de bord et l'archive de l'agence (qui devrait être ailleurs), et une base de données de l'état
des clients (qui devrait être un tableur). Parallèlement, les routines cloud sont devenues le
système de pilotage perso, avec beaucoup de doublons, sans règle commune, et elles se disputent
le même quota que le travail client. Le backlog parle de rendre l'outil vendable à d'autres
community managers (marque blanche, onboarding en une commande) : ce chantier produit est
légitime, mais c'est lui que la limite d'usage a tué ce matin, pendant que le revenu récurrent de
community management est décrit comme tombé à zéro dans tes propres prompts. Ordre des priorités
à trancher par Maxime, pas par l'outil.
