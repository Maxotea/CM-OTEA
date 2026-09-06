# Backlog d'améliorations de l'outil CM

Liste vivante, tenue par la revue quotidienne. Priorité = ce que ça rapporte en temps
gagné (productivité), en délai (rapidité) ou en capacité à vendre l'outil (vendabilité),
divisé par l'effort. Une ligne sort d'ici quand elle est faite et protégée par un test,
ou quand Maxime l'écarte.

Dernière mise à jour : 06/09/2026.

## P0 : cette semaine

| # | Amélioration | Pourquoi | Effort | État |
|---|---|---|---|---|
| 1 | **Partager par lien le dossier « Validation hebdo » d'Otea Filmakers** (Partager → Accès général → Tous les utilisateurs disposant du lien → Éditeur) | 1 réglage manuel de Maxime. Sans lui, la relève sort rouge 3 fois par jour depuis le 19/08 (≈55 runs) et plus personne ne lit les échecs réels. | 2 min, Maxime | ⏳ à faire par Maxime |
| 2 | **Fusionner la PR #44** (carrousels sur fond photo, tableau lisible, Gossip et Le Loft retirés de la review) | Tant qu'elle attend, la review génère chaque vendredi deux tableaux pour deux comptes clos, et le tableau client reste « pas joli » (reproche du 02/09). | relecture, Maxime | ⏳ décision Maxime |
| 3 | **Écrire les specs des carrousels du 09/09 et du 16/09** pour J Lawson, La Galerie, Pierre Huiban, OTEA | Aucune spec après le 02/09 : l'action du vendredi 04/09 est sortie en erreur, la semaine du 07/09 part sans carrousel sur les quatre comptes. `scripts/sante.py` le signale désormais chaque matin. | 1 session contenu | ⏳ contenu, hors revue |
| 4 | Suite de tests + CI (`tests/`, `.github/workflows/tests.yml`) | Aucun test avant le 06/09 : chaque correction de `review.py` était un pari sur les tableaux clients. 69 tests, sans réseau. | fait | ✅ 06/09 |
| 5 | Bilan de santé sans réseau (`scripts/sante.py`) | Une commande qui dit en trois secondes ce qui manque pour la semaine : carrousel, fichiers de review, comptes clos, ✅ non honorés. | fait | ✅ 06/09 |
| 6 | Annotations et résumé dans les runs Actions (`review.py`, `publier.py`) | Un run rouge disait « exit code 1 » ; il dit maintenant quel compte et pourquoi, dans la liste des runs et dans l'onglet Summary. | fait | ✅ 06/09 |
| 7 | Tirets cadratins retirés des textes client (mode d'emploi du tableau, mail de review, modèles de CR) et test qui les interdit | Règle de la mémoire `redaction-sans-tirets.md`, jamais vérifiée : 13 textes client en faute. | fait | ✅ 06/09 |

## P1 : ce mois-ci

| # | Amélioration | Pourquoi | Effort |
|---|---|---|---|
| 8 | **Source unique des comptes** : un `comptes.json` (slug, blog_id, nom, prefixe, actif, ton, canaux, Drive, DA) qui alimente `publier.BLOG_IDS`, `reviews/config.json`, `recaps/clients-config.json` et les tableaux des SKILL.md | Aujourd'hui un client vit dans 5 fichiers. Fermer Gossip et Le Loft a demandé 5 modifications et une a été oubliée (la review). Pour vendre l'outil : onboarder un client = remplir UN fichier. | 1 session + migration des lecteurs |
| 9 | **La routine du lundi écrit les specs de carrousel** (POST CM-OTEA), validées par `carrousel.py --check`, deux mercredis d'avance | Le seul maillon de la chaîne carrousel qui dépend encore d'un geste humain. Le manque du 09/09 vient de là. | prompt de routine + test de couverture |
| 10 | **Alerte en cas de run rouge** : un message Slack ou un mail à Maxime quand `Review hebdo client`, `Carrousels hebdo` ou `Boîtes de dépôt Drive` échoue deux fois de suite | Personne ne regarde l'onglet Actions. La revue quotidienne le lit désormais, mais avec 24 h de retard. | 1 étape de workflow |
| 11 | **Nettoyer les 16 PR ouvertes** (la plus ancienne du 04/08) : fusionner ce qui est validé, fermer ce qui est périmé | Chaque PR ouverte est une décision en suspens et un risque de conflit. Une liste « à fusionner / à fermer » par la revue, décision Maxime. | 1 h, Maxime |
| 12 | **Journal des ✅ non honorés remonté dans le CR du lundi** (LGI-01 du 24/08 « post introuvable » n'a jamais été traité) | Un accord client sans suite, c'est le pire signal qu'on puisse envoyer à un client qui vient de valider. | petit, dans la routine du lundi |
| 13 | Passer les dossiers « Validation hebdo » des cinq clients en ÉDITEUR par lien (aujourd'hui LECTEUR) | Le client peut ouvrir son tableau mais pas le remplir : la review ne fonctionne réellement que pour La Galerie, à qui Maxime envoie le tableau à la main. | 5 réglages, Maxime |
| 14 | Mesurer le temps machine et humain par compte et par semaine (durée des routines, gestes manuels notés dans la revue) | La grille 290/690/1190 suppose 3,2 jours par mois par mission. Sans mesure, le prix est une hypothèse. | journal léger dans les routines |

## P2 : le produit vendable

| # | Amélioration | Pourquoi |
|---|---|---|
| 15 | **Tableau de bord par compte** (page HTML régénérée par un script) : horizon couvert dans Metricool, brouillons à valider, décisions de la semaine, publiés du mois, réserve de médias | La matière du « compte rendu mensuel chiffré » des offres SIGNATURE et CROISSANCE, et l'écran de démonstration pour vendre l'outil. |
| 16 | **Marque blanche** : nom d'agence, signature, couleurs et textes des mails dans un fichier de configuration, plus rien d'OTEA en dur dans les scripts et les prompts | Condition pour vendre l'outil à un autre CM sans le forker. |
| 17 | **Tout Metricool en API directe** (comme `publier.py`), plus de Zapier pour la planification en masse | Le bug de fuseau (+7 h), le rate limit à 6 créations et le `bulk_set_draft` de rattrapage sont des artefacts Zapier. Un script `planifier.py` les fait disparaître. |
| 18 | Hébergement des visuels sur un bucket maîtrisé (R2/S3) à la place d'imgbb | Metricool garde l'URL source : si imgbb tombe, les carrousels programmés perdent leurs slides. Seule fonction à changer : `publier.heberger`. |
| 19 | **Onboarding en une commande** : `python3 scripts/onboarder.py <slug>` crée la fiche client, la DA, le dossier Drive, l'entrée de config, et un premier mois de calendrier en brouillon | Promesse commerciale : « votre premier mois programmé le jour de la signature ». |
| 20 | Migrer les actions vers les versions à jour (Node 20 déprécié sur `actions/checkout@v4`, `setup-python@v5`, `upload-artifact@v4`) | Avertissement à chaque run ; GitHub finira par les couper. |
| 21 | Les mémoires `.claude/memories/` devenues des tests ou des garde-fous de code, une par une (comme la règle des tirets le 06/09) | Une règle dans une mémoire se relit ; une règle dans un test s'applique. |
