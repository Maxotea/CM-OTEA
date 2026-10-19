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

## 8. Économiser les tokens

L'audit initial n'avait pas mesuré la consommation. Ce chapitre reprend les leviers que les
fichiers et les routines permettent d'établir. Aucun chiffre de tokens ici : la consommation
réelle par routine se lit dans les réglages d'usage du compte, à comparer avant et après.

### Ce qui explique le pic de fin de semaine

Nombre de sessions lancées seules par les routines, avant plan :

| Jour | Sessions | Détail |
|---|---|---|
| Lundi à jeudi | 9 par jour | résumé matinal, point du matin, compta, tâches, midi, soir, revue d'outil, La Chasse, ExpliqueMoi |
| Vendredi | 11 | les 9 ci-dessus, plus la préparation de la review et la routine BNI |
| Samedi et dimanche | 5 par jour | point du matin, midi, soir, revue d'outil, La Chasse |
| Lundi, en plus | 1 | POST CM-OTEA |

Total : environ 58 sessions par semaine avant la première conversation de la journée. Les
routines du vendredi, les plus lourdes (review, base64, BNI), s'ajoutent à des journées déjà
pleines, d'où l'impression d'un quota qui fond en fin de semaine. Après le plan du §3 : environ
14 sessions par semaine.

### Les leviers, du plus rentable au moins rentable

1. **Choisir le modèle par tâche.** Toutes les routines ont le champ modèle vide, donc le modèle
   par défaut du compte. Un bilan du matin (lire mails et agenda, classer, écrire 20 lignes) n'a
   pas besoin du modèle le plus puissant : Sonnet suffit, et Haiku pour le tri de boîte mail. Le
   modèle le plus puissant se réserve au code difficile, aux montages et à la stratégie. Cet audit
   lui-même a été mené sur le niveau le plus haut ; la rédaction du plan pouvait se faire sur
   Sonnet. Changer le modèle d'une routine demande ton accord explicite.
2. **Supprimer les sessions, pas les raccourcir.** Fusionner les quatre bilans du matin
   (§3) retire 3 sessions par jour ouvré, chacune avec son propre chargement de connecteurs, de
   Gmail et d'agenda. Passer la revue d'outil et La Chasse en hebdomadaire retire 12 sessions par
   semaine. Arrêter le midi retire 7 sessions par semaine.
3. **Mettre ExpliqueMoi en pause ou en lot.** Une vidéo par jour ouvré, c'est la routine qui
   enchaîne le plus d'appels d'outils (génération, mesures de voix en deux prises, assemblage,
   publication, relecture). Produire cinq épisodes un jour par semaine coûte le même nombre
   d'appels de création mais un seul chargement de contexte.
4. **Réduire les connecteurs attachés.** Chaque serveur connecté ajoute ses instructions et la
   liste de ses outils au contexte de la session. Les bilans en portent 22 à 25 alors qu'ils en
   utilisent 4. Les retirer économise du contexte à chaque session et supprime le risque Meta Ads.
5. **Ne plus faire passer des fichiers par le modèle.** La copie des xlsx en base64 vers Drive
   fait lire puis réécrire le contenu du fichier plusieurs fois par client chaque vendredi. Un
   Google Sheet natif ou l'envoi en validation Metricool supprime ce poste entier.
6. **Sortir le « contexte connu » des prompts.** Environ 3 à 4 Ko de faits datés sont recopiés
   dans quatre prompts et relus à chaque passage, pour des informations périmées. Un seul
   Projet « OTEA, pilotage » les porte, chargé à la demande.
7. **Garder la session Code légère.** Moins de skills listés (retirer les six `smc-*` et le
   plugin small-business de Code), `CLAUDE.md` court, `cm-metricool/SKILL.md` (17 Ko) découpé pour
   que le détail de la review et des carrousels ne se charge que quand on en a besoin, et une
   session par tâche : `/clear` entre deux sujets plutôt qu'une conversation de plusieurs heures
   dont tout l'historique est relu à chaque message.
8. **Déléguer les balayages.** Pour « où est telle règle dans le dépôt » ou « qu'est-ce qui a
   changé cette semaine », un sous-agent d'exploration renvoie la conclusion sans faire entrer
   les fichiers dans la conversation principale.

### Règle de décision pour la suite

Avant de créer une routine ou un script avec un modèle dedans, poser trois questions : est-ce
que du code ordinaire le ferait sans modèle (Actions) ? est-ce que le modèle le plus petit y
arrive ? est-ce qu'une session par semaine suffit au lieu d'une par jour ? Une routine qui
répond non aux trois est justifiée.

### À mesurer avant et après

- Consommation hebdomadaire du forfait, relevée le lundi, avant de toucher aux routines puis
  deux semaines après.
- Nombre de routines échouées pour limite d'usage (aujourd'hui : 2 ce matin). Objectif : zéro.
- Sessions de routines par semaine : 58 avant, environ 14 visé.

## 9. Modèle par routine (appliqué le 16/10/2026)

Maxime a laissé le choix. Sonnet 5.5 est posé sur les routines qui créent une nouvelle session à
chaque lancement. Les autres gardent le modèle de leur conversation attachée : le changement n'a
pas d'effet sur elles, il se fait dans la conversation elle-même.

| Routine | Modèle | Pourquoi |
|---|---|---|
| Résumé matinal | Sonnet 5.5 | lecture d'agenda et de mails, rendu d'une page |
| Point du matin | Sonnet 5.5 | tri de boîte mail avec règles strictes et mise à la corbeille |
| Point du midi | Sonnet 5.5 | dictées vocales à corriger, actions possibles par mail |
| Point du soir | Sonnet 5.5 | idem, plus la ligne cash |
| Revue quotidienne de l'outil CM | Sonnet 5.5 | revue et petits correctifs testés |
| Upgrade quotidien de La Chasse | Sonnet 5.5 | améliorations incrémentales, PR relue par Maxime |
| ExpliqueMoi | Sonnet 5.5 | chaîne de production balisée par des règles écrites |
| POST CM-OTEA | inchangé | rédaction client, une fois par semaine, qualité d'abord |
| Point compta, Point tâches, BNI, Review du vendredi | inchangé | conversation attachée, voir ci-dessus |

Aucune routine sur Haiku : chacune mêle des mails (dictées à corriger, mise à la corbeille, envoi
possible au nom de Maxime) ou des chiffres de compta, où une erreur coûte plus que les tokens
économisés. Haiku devient pertinent après la fusion des bilans, pour une routine de tri de boîte
mail seule, en lecture et en étiquetage.

## 10. Mise en place du 19/10/2026 (ce qui est fait, ce qui reste)

Fait ce matin, sur demande de Maxime (« relance et mets tout en place ») :

| Routine | Avant | Après |
|---|---|---|
| Point du matin | 07h00 UTC, contexte daté du 23/09 | **Bilan du matin**, 07h00 Paris, fusionne matin, compta et tâches ; compta complète le mardi ; repères stables sans montants datés |
| Résumé matinal | 05h30 Paris | désactivée (doublon du bilan) |
| Point compta du matin | 08h00 Paris | désactivée (fondue dans le bilan ; sa conversation reste ouverte pour les questions à la demande) |
| Point tâches quotidien | 08h30 Paris | désactivée (fondue dans le bilan) |
| Point du midi | 12h30 | désactivée pour deux semaines, à rétablir si Maxime le regrette |
| Point du soir | 16h30 UTC | inchangée, cron en heure de Paris (18h30) |
| Revue quotidienne de l'outil CM | tous les jours 07h UTC | **hebdomadaire**, lundi 10h00 Paris |
| Upgrade quotidien de La Chasse | tous les jours 07h UTC | **hebdomadaire**, lundi 11h00 Paris |
| Review, préparation du vendredi | 06h UTC | inchangée, cron en heure de Paris (08h00) |
| Review, envoi du lundi | coupée depuis le 24/08 | supprimée |
| ExpliqueMoi | quotidienne | désactivée depuis le 16/10 |
| POST CM-OTEA | prompt d'une ligne, 03h UTC | **inchangée, à modifier par Maxime** : la routine a été créée hors agent, aucune session ne peut la modifier, et une routine jumelle créée depuis ici partirait sans connecteur Zapier, donc sans Metricool (essayé puis supprimé ce matin). Texte prêt au §6, à coller ici : https://claude.ai/code/routines/trig_013MDZrKLaYrcSJ9LY5vvLCG |

Sessions de routines par semaine : 58 avant, 19 maintenant (bilan et soir chaque jour, plus
revue d'outil, La Chasse et POST le lundi, BNI et review le vendredi).

Vérifié ce matin : la routine POST CM-OTEA du 19/10 (03h02 UTC, ancien prompt) n'a rien créé ni
modifié dans Metricool ; elle a seulement relu les deux semaines et signalé 12 brouillons sans
média (Le Loft 3, La Galerie 4, Pierre Huiban 5), à attacher par Maxime.

Ce que je ne peux pas faire depuis ici :
- retirer les connecteurs attachés aux routines (le paramètre n'existe pas pour ce compte) : à
  faire dans la page de chaque routine, en ne gardant que Gmail, Agenda, Drive, Todoist, Zapier
  et Finary pour le bilan du matin ;
- créer les Projets Claude et la tâche Cowork : zips prêts dans `o/projets-claude/`, texte dans
  `kit-cowork.md` ;
- poser les préférences personnelles du compte (texte au §5).

## 11. La carte des dépôts (audit intégral du 19/10/2026)

Détail : `ameliorations/2026-10-19-audit-integral-code-cowork.md`.

| Dépôt | Rôle | Statut |
|---|---|---|
| CM-OTEA | moteur CM, skills `cm-metricool`, `cm-meta-ads`, `cm-hyrox` | source unique du CM |
| PROSPECTION (OTEA Moteur) | prospection, CRM, « Ma journée » | code ; doublon partiel avec le Bilan du matin, à trancher |
| MONTAGE-OTEA (PostCam) | montage, DaVinci, splits HYROX | code ; reçoit le skill `hyrox-splits` du kit |
| TRESORIE-PARFAITE | plan de trésorerie | code ; `docs/etude-prix-cm.md` à rapatrier dans `offre/` |
| ACHILLE, RECMYRUN, makepeople-game | produits annexes | code ; le CM de MAKE PEOPLE sort du dépôt du jeu |
| COMMENT- | données de la chaîne ExpliqueMoi | reste tant que la routine existe |
| CM-BTOC | ancien dépôt B2C | fondu dans CM-OTEA le 19/10, à archiver |
| MAKEPEOPLE, SITE-OTEA-PRODUCTION | vides ou remplacés | à archiver |
| STRUCTUREOTEA | journal de bord (un README) | pas un dépôt : dossier Cowork « Journal » |

Skills du compte : `reel-script` et `reel-lint` restent ; `cm-otea` et `cm-b2c` deviennent des
aiguillages (kit) ; `hyrox-splits-montage` et `morning` sortent. Kit : `.claude/cowork-kit/`.
