# Organisation de l'usage de Claude : où faire quoi

Issu de l'audit du 16/10/2026 (`ameliorations/2026-10-16-audit-usage-claude.md`). Ce fichier est
la règle de routage et le plan de migration. Les décisions marquées « Maxime » ne sont pas
prises par l'outil.

## 1. La règle de routage

Une question à se poser dans l'ordre : est-ce que le résultat est du code ou un fichier produit
par du code ? Est-ce que ça tourne sans moi ? Est-ce que ça touche mes fichiers locaux ou mes
outils métier ? Sinon, c'est une conversation.

| Surface | Ce qui y va | Ce qui n'y va pas |
|---|---|---|
| **Claude Code** (le dépôt) | scripts Python, tests, workflows Actions, montage ffmpeg, skills `cm-metricool` et `cm-meta-ads`, `CLAUDE.md`, règles non négociables | documents d'agence, état des clients, bilans du jour, rédaction ponctuelle |
| **Cowork** (dossier local « OTEA ») | devis, offres, présentations, pitchs (docx, pptx, xlsx, pdf), tri et nommage du dossier `medias/`, compta (Pennylane, Qonto, Finary), tâches du vendredi et du lundi sur la review client | tout ce qui doit tourner ordinateur éteint, tout ce qui est versionné et testé |
| **Claude en conversation + Projets** | légendes, réponses clients, relances, scripts de reels (`reel-script`, `reel-lint`), veille concurrentielle, analyse de performances, préparation de pitch, cadrage d'idées, les 6 cadres SOCIAL MEDIA CEO | exécution répétitive, écriture dans Metricool en masse |
| **Routines cloud** | bilans du matin et du soir, posts de la semaine, revue d'outil hebdomadaire : tout ce qui part seul, de nuit ou tôt | tout ce qui demande un fichier local, plus de 5 connecteurs |
| **GitHub Actions** | jobs déterministes sans modèle : tests, relève de la review, rendu des carrousels, boîtes Drive | tout ce qui demande du jugement, tout ce qui n'alerte pas quand il échoue |

Cowork et les tâches locales ne tournent que ordinateur allumé (c'est écrit dans la mémoire
`recap-hebdo-lundi`). Un bilan à 05h30 reste donc une routine cloud ; la review du vendredi et le
rangement des médias vont bien à Cowork.

## 2. L'architecture cible

**Dans le dépôt (Code), après allègement** : `scripts/`, `tests/`, `.github/`,
`.claude/skills/cm-metricool` et `cm-meta-ads`, `.claude/memories/`, `CLAUDE.md`, les fiches
clients et les specs que le code lit. Rien d'autre.

**Dans Claude (Projets)** : un Projet « OTEA, pilotage » (offres et tarifs, règles d'agence, les
6 cadres SOCIAL MEDIA CEO, mémoire du contexte) et un Projet par client actif (J Lawson Golf,
La Galerie Immobilière, Pierre Huiban, ConfShine, Run On Invest, OTEA et Otea Filmakers) dont la
base de connaissances est la fiche client. ConfShine fonctionne déjà ainsi
(`references/clients/confshine/instructions-projet-claude.md`) : c'est le modèle à copier.

**Dans Cowork** : un dossier de travail « OTEA » (devis, offres, présentations, `medias/`, compta)
et deux tâches planifiées : « Review client du vendredi » et « Récap du lundi ».

**Dans les préférences personnelles de Claude** (une seule fois, valables partout) : voir §5.

## 3. Les routines : de 12 récurrentes à 6

| Routine actuelle | Décision proposée | Raison |
|---|---|---|
| Résumé matinal 05h30 | **fusionner** dans « Bilan du matin » | doublon |
| Point du matin 07h00 | **fusionner** (devient la base) | doublon |
| Point compta du matin 08h00 | **fusionner** : une ligne de cash par jour, le détail le mardi | doublon |
| Point tâches quotidien 08h30 | **fusionner** | doublon |
| Point du midi 12h30 | à **arrêter pendant 2 semaines**, à rétablir si tu le regrettes | je n'ai aucune donnée de lecture |
| Point du soir 18h30 | **garder** (devient « Bilan du soir ») | fermeture de journée |
| Revue quotidienne de l'outil CM | passer à **hebdomadaire** (lundi) | 1 revue sur `main` en 40 jours, échec sur limite d'usage |
| Upgrade quotidien de La Chasse | passer à **hebdomadaire**, ou couper | même échec ce matin |
| ExpliqueMoi vidéo quotidienne | **pause**, décision Maxime | gros consommateur, classé « sans revenu » par tes propres prompts |
| Review, préparation du vendredi | **garder**, à réécrire sans base64 | voir audit C6 |
| Review, envoi du lundi (coupée) | **supprimer** | morte depuis le 24/08 |
| POST CM-OTEA | **réécrire le prompt avant lundi** | audit C1 |
| BNI demandes spécifiques (vendredi) | garder | utile, bien écrite |
| Rappels uniques (CEO Day, garde-fous) | le second devient inutile une fois le prompt de POST CM-OTEA remplacé | |

Effet : de 9 sessions par jour ouvré à 2 ou 3, et le quota du matin n'est plus mangé par les
routines de développement.

À faire sur **toutes** les routines conservées :
- ne garder que les connecteurs qu'elles utilisent (un bilan : Gmail, Agenda, Drive, Todoist ; pas
  d'Uber, Booking, Spotify, Strava, Higgsfield, Meta Ads) ;
- passer le cron en `CRON_TZ=Europe/Paris` avant le 25/10, pour que l'heure d'hiver ne les décale pas ;
- sortir le « contexte connu au 23 septembre » du prompt : il vit dans le Projet « OTEA, pilotage »
  ou le tableau de bord compta, une seule fois.

## 4. Plan, dans l'ordre

| Quand | Quoi | Qui | Durée |
|---|---|---|---|
| **Avant lundi 19/10, 05h02** | remplacer le prompt de POST CM-OTEA par celui du §6 | Maxime (routine, lien dans le rappel du 18/10) | 3 min |
| Cette semaine | décider : ExpliqueMoi en pause ? midi arrêté ? La Chasse en hebdo ? | Maxime | 5 min |
| Cette semaine | retirer les connecteurs inutiles des routines conservées, passer en `CRON_TZ`, supprimer la routine coupée | Claude sur demande, ou Maxime | 20 min |
| Cette semaine | créer le « Bilan du matin » fusionné et désactiver les quatre anciens (une fois le nouveau lu 3 jours) | Claude sur demande | 30 min |
| Semaine du 19/10 | créer le Projet « OTEA, pilotage » et y charger les 6 cadres SOCIAL MEDIA CEO ; retirer les skills `smc-*` du dépôt (le zip d'origine est dans `_to_delete/`) | Maxime pour le Projet, Claude pour le dépôt | 1 h |
| Semaine du 19/10 | créer un Projet par client actif sur le modèle ConfShine | Maxime et Claude | 20 min par client |
| Semaine du 26/10 | créer le dossier Cowork « OTEA », y déplacer `offre/`, `design-*`, devis, pitch, kit ; l'ouvrir pour `medias/` | Maxime | 1 h |
| Novembre | tester le connecteur Metricool natif (brouillon, fuseau, envoi en validation) sur un compte de test, puis migrer les actions Zapier une à une | Claude | 1 session |
| Novembre | remplacer le xlsx + base64 par un Google Sheet natif ou l'envoi en validation Metricool ; arrêter de versionner les xlsx | Claude | 1 à 2 sessions |
| Novembre | corriger la cause des « Boîtes de dépôt Drive » rouges (partage en édition) et ajouter l'alerte d'échec | Maxime (2 min) + Claude | 30 min |
| Au fil de l'eau | nettoyer : lien mort de `MEMORY.md`, chemins macOS, zip de `_to_delete/` | Claude | 15 min |

## 5. Préférences personnelles à poser une fois pour toutes

À coller dans les préférences de ton compte Claude, pour que Code, Cowork et la conversation
les partagent, au lieu de les recopier dans chaque prompt :

```
Je m'appelle Maxime, fondateur d'OTEA Production (vidéo, événementiel, community management).
Réponds en français, en me tutoyant, de façon courte et directe.
N'utilise jamais de tiret cadratin ni demi-cadratin : virgule, deux-points ou nouvelle phrase.
Tranche et avance sans me poser de micro-questions ; rends compte à la fin.
Ne publie, n'envoie et n'active jamais rien en mon nom sans que je l'aie demandé :
brouillons pour les posts et les mails, campagnes en pause.
Quand une information manque, dis-le au lieu de l'inventer.
```

## 6. Texte de remplacement pour la routine POST CM-OTEA

```
Tu travailles pour Maxime (OTEA Production). Attache le dépôt Maxotea/CM-OTEA (accès lecture
et écriture), place-toi sur main à jour, puis lis dans cet ordre : CLAUDE.md, le skill
.claude/skills/cm-metricool/SKILL.md, recaps/clients-config.json et le dossier plans/.

Mission : rédiger, réaliser ou vérifier les posts des comptes actifs pour les deux semaines qui
arrivent, en suivant le skill.

Garde-fous, non négociables :
1. Tout contenu créé dans Metricool reste en BROUILLON (draft true, autoPublish false).
   Après chaque création, relis le post et vérifie que draft vaut true.
2. Tu ne publies rien toi-même et tu ne passes aucun brouillon en publication.
3. Ne touche pas aux brouillons déjà posés pour Pierre Huiban et Run On Invest.
4. Ne traite pas un compte dont actif vaut false dans recaps/clients-config.json.
5. Relis l'état réel de Metricool (posts programmés) avant d'écrire, pour ne créer aucun doublon.
6. Aucune image entièrement générée par IA sur un compte qui possède de vraies photos, et aucune
   personne réelle générée.
7. Pas de tiret cadratin dans les textes rédigés.

Termine par un compte rendu court : posts créés par compte (dates), posts vérifiés, points qui
attendent Maxime. Si Metricool ou le dépôt ne répondent pas, dis-le et arrête-toi.
```

## 7. Ce qui n'est pas dans ce plan, faute de données

- Les tâches planifiées locales de Cowork et les Projets existants de claude.ai : je ne les vois pas.
- Le contenu des skills `anthropic-skills:cm-otea` et `anthropic-skills:cm-b2c` du compte :
  à comparer avec `cm-metricool` pour éviter deux sources de vérité.
- La consommation réelle du forfait par routine : à lire dans les réglages d'usage avant de
  conclure sur ExpliqueMoi et les routines de développement.
- Le plugin small-business (une quarantaine de skills orientés Gusto, Xero, MYOB, QuickBooks,
  Square) est chargé dans cette session alors que tu utilises Pennylane, Qonto et Zapier : à
  désactiver dans Code, à garder éventuellement dans Cowork.
