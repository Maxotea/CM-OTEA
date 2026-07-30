# SOCIAL MEDIA CEO — Le workflow contenu

Le pipeline le plus utilisé du système. C'est celui qui se branche directement
sur le skill `cm-metricool`.

---

## Le pipeline en 11 statuts

```
┌─ CAPTURE ────────────────────────────────────────────────┐
│  Idée                    Labo à idées                     │
└───────────────────────────────────────────────────────────┘
                    ↓
┌─ PRÉPARATION ────────────────────────────────────────────┐
│  À préparer              vue « A PRÉPARER »               │
└───────────────────────────────────────────────────────────┘
                    ↓
┌─ VALIDATION CLIENT (clients uniquement) ─────────────────┐
│  À approuver  ⇄  Demande de modif                         │
│  → Validé client                                          │
└───────────────────────────────────────────────────────────┘
                    ↓
┌─ PRODUCTION (branches selon le format) ──────────────────┐
│  Créer visuel  |  Rédaction  |  Tournage  →  Montage      │
└───────────────────────────────────────────────────────────┘
                    ↓
┌─ DIFFUSION ──────────────────────────────────────────────┐
│  Prêt à programmer / publier  →  Programmé / Publié       │
└───────────────────────────────────────────────────────────┘
                    ↓
┌─ APRÈS ──────────────────────────────────────────────────┐
│  saisie des métriques → Analyse par post → On recycle ? → │
│  À recycler → (nouveau Contenu lié au précédent)          │
└───────────────────────────────────────────────────────────┘
```

Le champ **« Valider ! » (bouton)** fait avancer le statut d'un cran.
Le flag **« On recycle ? » (formule)** décide de l'éligibilité au recyclage à
partir des performances ; **« Déjà Recyclé ! »** évite de recycler deux fois.

---

## Les 4 vues de pilotage (identiques côté CLIENTS et côté PERSO)

| Vue | Question à laquelle elle répond |
|---|---|
| **À SUIVRE CETTE SEMAINE** | qu'est-ce qui doit sortir dans les 7 jours ? |
| **À SUIVRE CE MOIS** | le mois est-il rempli ? |
| **PREVIEW FEED** | à quoi ressemble le feed visuellement (filtrable par portail client) |
| **A PRÉPARER** | sur quoi je bosse maintenant |

Plus **MASTER PLANNING** : la vue calendrier de tout, tous clients confondus.

---

## Les 6 piliers éditoriaux

| Pilier | Rôle |
|---|---|
| **Vente** | offre, preuve, appel à l'action |
| **Éduquer** | apporter du savoir, méthode, how-to |
| **Inspirer** | vision, résultats, projection |
| **Captiver** | hook fort, format à forte rétention |
| **Connecter** | interaction, question, communauté |
| **Backstage / Lifestyle** | coulisses, humain, incarnation |

**Règle d'équilibrage** : un mois de contenu ne doit jamais reposer sur un seul
pilier. Vérifier la répartition avant de valider un calendrier — c'est le premier
contrôle qualité à faire.

### ⚠️ Deux systèmes de piliers coexistent dans ce projet

Le skill `cm-metricool` définit **5 piliers avec des quotas**, calibrés pour les
comptes clients d'OTEA :

| cm-metricool | Quota | Équivalent SOCIAL MEDIA CEO |
|---|---|---|
| P1 — pédagogie métier | 30 % | `Éduquer` |
| P2 — actu secteur | 25 % | `Captiver` (+ `Éduquer`) |
| P3 — coulisses | 20 % | `Backstage / Lifestyle` |
| P4 — saisonnalité client | 15 % | `Vente` ou `Inspiration` selon l'angle |
| P5 — preuve sociale | 10 % | `Vente` (+ `Inspiration`) |
| — | — | `Connecter` : **non couvert** par cm-metricool |

**Règle d'arbitrage :**

- Sur un **compte client**, les quotas de `cm-metricool` font foi. Ils sont
  calibrés par secteur, avec une cadence lundi/mercredi/vendredi. Ne pas les
  écraser avec les 6 piliers.
- Les 6 piliers SOCIAL MEDIA CEO servent alors uniquement de **taxonomie de
  classement** dans la base `Contenu` — on tague via la colonne d'équivalence
  ci-dessus.
- Sur le **contenu PERSO** (OTEA, personnel), ce sont les 6 piliers qui pilotent,
  sans quota fixe.
- `Connecter` n'a pas d'équivalent dans cm-metricool. C'est un angle mort à
  combler volontairement : prévoir au moins un contenu d'interaction par mois et
  par compte, en plus des 5 piliers.

---

## Stratégie hashtags

Le système ne raisonne pas hashtag par hashtag mais **par groupe** :

1. La base `Hashtags` qualifie chaque tag : **thème** (CIBLE / BUSINESS / METIER /
   Podcast / MINDSET), **taille** (Petit / Moyen / Gros), **reach**, **préférence** (⭐→⭐⭐⭐).
2. La base `Strat' Hashtag` assemble des **groupes** de tags. La formule
   *Nombre de Hashtags (Max 30)* garde le groupe sous la limite Instagram.
3. Un contenu pointe vers un groupe ; la formule *Hashtag à copier coller*
   restitue la chaîne prête à coller.

**Bonne pratique de composition d'un groupe** : mélanger les 3 tailles (les
« Gros » pour la portée, les « Petits » pour se classer réellement) et couvrir
au moins CIBLE + METIER.

---

## Métriques saisies après publication

Par contenu : `Impressions` · `J'aime reçus` · `Commentaires reçus` ·
`Enregistrements` · `Nombre de caractères`.

Calculées : `Taux d'engagement / Publication` · `Taux d'engagement / impression` ·
`On recycle ?` · `Bravo !`.

Ces lignes alimentent `Analyse Contenu`, qui alimente `KPIS` du mois.

---

## Articulation avec le skill `cm-metricool`

Les deux systèmes se recouvrent volontairement. Répartition :

| Étape | Qui fait quoi |
|---|---|
| Idée / veille sectorielle | `cm-metricool` (calendrier calé sur l'actualité du secteur) |
| Cadrage éditorial (piliers, équilibrage, format) | **SOCIAL MEDIA CEO** |
| Rédaction des légendes | `cm-metricool` |
| Script de vidéo courte | skill `reel-script` puis `reel-lint` |
| Hashtags | **SOCIAL MEDIA CEO** (groupes) |
| Validation client | **SOCIAL MEDIA CEO** (statuts À approuver / Demande de modif / Validé client) |
| Programmation en brouillon | `cm-metricool` (Metricool via Zapier) |
| Saisie des métriques + analyse mensuelle | **SOCIAL MEDIA CEO** |
| Recyclage | **SOCIAL MEDIA CEO** |

**Statut pivot** : `Prêt à programmer / publier`. C'est là que la main passe à
`cm-metricool`. Une fois planifié dans Metricool, le statut passe à
`Programmé / Publié`.
