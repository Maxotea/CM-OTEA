# SOCIAL MEDIA CEO — contexte projet

Système de gestion issu de la formation Social Media Lab, transposé pour le
projet **CM OTEA**. Source : Notion « SOCIAL MEDIA CEO » (36 pages, 4 boards,
33 bases de données).

## En une phrase

Quatre tableaux de bord — **OPS** (piloter), **BRAIN** (capitaliser),
**CX** (les clients), **CONTENT** (produire) — assis sur un socle unique de
bases de données partagées. Une donnée n'existe qu'à un seul endroit.

## Où trouver quoi

| Fichier | Contenu |
|---|---|
| `.claude/references/social-media-ceo/00-architecture.md` | la carte des 4 boards et des 36 pages, les dépendances entre bases |
| `.claude/references/social-media-ceo/01-bases-de-donnees.md` | les 33 bases, champs par champ |
| `.claude/references/social-media-ceo/02-taxonomies.md` | le vocabulaire contrôlé — statuts, piliers, catégories |
| `.claude/references/social-media-ceo/03-workflow-contenu.md` | le pipeline de production de contenu |
| `.claude/references/social-media-ceo/04-kpis.md` | le dictionnaire KPI et la lecture des chiffres |
| `.claude/references/social-media-ceo/05-rituels.md` | les boucles quotidienne, hebdo, mensuelle, trimestrielle |
| `.claude/references/public-apis/README.md` | le catalogue public-apis (1 958 API gratuites), la sélection utile pour OTEA et comment le brancher sur Claude |
| `.claude/references/organisation-claude.md` | où faire quoi entre Claude Code, Cowork, conversation, routines et Actions ; le plan de migration issu de l'audit du 16/10/2026 |
| `.claude/references/kit-cowork.md` | ce qui passe en Projet Claude ou en tâche Cowork, avec les instructions à coller |
| `.claude/cowork-kit/` | le dossier de travail Cowork à copier : agents, skills d'aiguillage du compte, skill hyrox pour MONTAGE-OTEA |

## Ce dépôt est le moteur, pas le bureau

Claude Code sert ici à ce qui est du code, versionné et testé : scripts, tests, workflows, skills
`cm-metricool` et `cm-meta-ads`, règles non négociables. Les documents d'agence (devis, offres,
présentations), les bilans du jour, la rédaction ponctuelle et les cadres SOCIAL MEDIA CEO ont
leur place dans Cowork ou dans un Projet Claude. La règle de routage complète est dans
`.claude/references/organisation-claude.md` ; ne pas ajouter ici un nouveau document d'agence sans
l'avoir relue.

## Les skills

| Skill | Déclenche sur |
|---|---|
| `cm-metricool` | planifier, programmer, calendrier éditorial, événement du secteur, Metricool, un compte client |
| `cm-meta-ads` | campagne, pub, sponsoriser ou booster un post, budget publicitaire, Ads Manager, audience, coût par prospect, ROAS |
| `cm-hyrox` | client athlète HYROX ou hybride, Pierre Huiban, une course, dossier de sponsoring, offre « CM athlète » (importé de CM-BTOC le 19/10/2026) |

Les six cadres SOCIAL MEDIA CEO (`smc-ceo-day`, `smc-client`, `smc-contenu`, `smc-kpi-review`,
`smc-ops-finance`, `smc-veille`) ne sont plus des skills de ce dépôt depuis le 19/10/2026 : ils
vivent dans `.claude/references/social-media-ceo/cadres/` et sont chargés dans le Projet Claude
« OTEA, pilotage » (voir `kit-cowork.md`). Aucun script ne les appelait.

## Articulation avec les skills existants

- **`cm-metricool`** — le calendrier calé sur l'actualité du secteur, la rédaction
  des légendes et la programmation Metricool. Point de jonction : le statut
  `Prêt à programmer / publier` de la base `Contenu`. En amont c'est SOCIAL MEDIA
  CEO (cadrage, validation client, hashtags), en aval c'est `cm-metricool`.

  **Conflit de piliers, arbitré :** `cm-metricool` définit 5 piliers avec quotas
  (P1 30 %, P2 25 %, P3 20 %, P4 15 %, P5 10 %), SOCIAL MEDIA CEO en définit 6
  sans quota. Sur un **compte client, les quotas cm-metricool font foi** ; les
  6 piliers ne servent que de taxonomie de classement. Sur le **contenu perso**,
  ce sont les 6 piliers qui pilotent. Table d'équivalence dans
  `.claude/references/social-media-ceo/03-workflow-contenu.md`.
- **`reel-script` / `reel-lint`** — l'écriture et la notation des vidéos courtes,
  appelées depuis le statut `Rédaction` / `Tournage`.
- **`cm-meta-ads`** — la publicité Meta (Facebook, Instagram) par client :
  registre `campagnes/comptes.json`, une spec JSON par campagne dans
  `campagnes/<client>/`, `scripts/campagne.py` pour valider et planifier. Le pont
  avec `cm-metricool` : un post publié et validé peut être boosté, jamais un
  brouillon. Banc d'essai : OTEA PRODUCTION et Otea Filmakers (compte pub
  Maks Otéa). Règle de même rang que le brouillon Metricool : **tout est créé
  en PAUSE, seule une phrase explicite de Maxime nommant la campagne l'active.**
  → `.claude/memories/meta-ads-jamais-activer-sans-ok.md`

## Règles permanentes du CM (non négociables)

Ces règles priment sur toute autre considération d'exécution. Elles
vivaient dans les mémoires Claude, hors du repo — elles sont désormais
versionnées dans `.claude/memories/` pour survivre à tout changement de poste.

1. **Tout contenu créé dans Metricool reste en BROUILLON** (`draft:true`,
   jamais `autoPublish`). Maxime valide lui-même dans l'interface. Toute code
   action qui crée du contenu doit vérifier le `draft` après création.
   Seule exception (07/10/2026) : OTEA Production et Otea Filmakers, dont
   Maxime est le client. Le contenu y est créé en brouillon, puis la relève
   GitHub le passe en publication automatique (`validation_auto`).
   → `.claude/memories/autonomie-decisions-cm.md`
2. **Les stories partent des VRAIES photos du client, animées en IA.**
   Deux choses distinctes, à ne pas confondre (règle reprécisée le 21/08/2026) :
   - ✅ **L'animation i2v est la méthode standard**, sur tous les comptes. Un
     simple mouvement de caméra ffmpeg (`zoompan`) ne suffit pas — Maxime l'a
     refusé le 01/08 (« pas des images animées mais juste des zooms »). Il veut
     du vrai mouvement dans l'image. Le `zoompan` n'est qu'un secours si un
     visage se déforme malgré le prompt renforcé.
   - ⛔ **Les images 100 % générées par IA restent interdites** sur un compte
     qui possède de vraies photos. C'est ce que William du Loft a reproché le
     21/08 : « 80 % des posts sont des photos qui ne sont pas prises chez moi ».
     Elles ne sont autorisées que sur un compte **sans aucune banque photo**, et
     compte par compte (Run On Invest, accordé le 04/08/2026).
   Prompt i2v **verrouillé sur l'identité** et **contrôle de la dernière frame**
   contre la photo source avant de brancher quoi que ce soit.
   → `.claude/memories/stories-vraies-photos-sans-ia.md`
   → Chaîne complète validée le 28/08/2026 (crop 9:16 → i2v → plein cadre
     1080×1920 → texte en overlay → muette → brouillon) :
     `.claude/memories/story-video-plein-cadre.md`
   - **Limite absolue, quel que soit le compte : aucune personne réelle
     identifiable générée.** On ne fabrique jamais le visage d'un client, d'un
     participant ou de Maxime.
3. **Aucune bande son sur les vidéos de story.** Elles partent muettes, Maxime
   ajoute l'audio dans Instagram au moment de valider.
   → `.claude/memories/stories-sans-son.md`
4. **Un à deux mois d'avance sur tout événement** (vacances scolaires, vœux,
   galette des rois, séminaires, salons, événements corpo). Une offre liée à un
   temps fort se publie entre J-60 et J-30, jamais pendant : un prospect qui
   lit « c'est le moment de filmer » le premier jour des vacances ne peut plus
   rien en faire (Maxime, 12/10/2026). Seule une actualité annoncée pour
   information sort à J-7 / J.
   → `.claude/memories/anticipation-evenements.md`

Index complet des mémoires : `.claude/memories/MEMORY.md`.

## Règles transverses

1. **Ne jamais inventer une valeur de statut, de pilier ou de catégorie.** Les
   listes fermées sont dans `.claude/references/social-media-ceo/02-taxonomies.md` ; les vues et formules
   en dépendent.
2. **Ne jamais écrire dans les bases « publiée ne pas toucher »** (Contenu,
   Portail client, Plateformes) : ce sont des vues techniques.
3. **Ne jamais saisir un champ formule ou rollup**, en particulier ceux dont le
   nom contient « (affichage) ».
4. **Respecter le champ `Ton utilisé`** (tutoiement / vouvoiement) de chaque
   contact dans toute rédaction.
5. **Distinguer facturé et encaissé** dans toute réponse financière.
6. **Rattacher au mois** : sans rattachement, les KPIs et la compta sont faux.
7. Sur les questions fiscales, comptables ou juridiques : donner les chiffres et
   les règles du système, renvoyer vers un professionnel pour la décision.
