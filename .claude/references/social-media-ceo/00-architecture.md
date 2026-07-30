# SOCIAL MEDIA CEO — Architecture du système

Source : Notion « SOCIAL MEDIA CEO » (Social Media Lab).
36 pages · 4 boards · 33 bases de données.

Ce document est la **carte** du système. Il sert à savoir *où vit une information*
avant de décider quoi en faire.

---

## Principe de fonctionnement

Le système repose sur **4 boards** (tableaux de bord) qui pointent tous vers un
**socle unique de bases de données partagées**. Une même base est affichée
plusieurs fois, filtrée différemment selon le board.

Conséquence pratique : **une donnée n'existe qu'à un seul endroit.** Une tâche
créée depuis le CONTENT BOARD est la même que celle vue depuis l'OPS BOARD.
C'est le principe à respecter quand on reproduit ou automatise ce système.

Les 4 groupes de bases (nommés ainsi dans la page racine) :

| Groupe | Contenu |
|---|---|
| GESTION DES OPÉRATIONS & FINANCES | Tâches, Projets, Devis/Factures, Recettes & dépenses, Compta, Prévisionnel, Objectifs, Key results, KPIs |
| GESTION DES RESSOURCES | My Brain, Areas brain, Base de connaissances, Documents, Process |
| GESTION DE LA CLIENTÈLE | Contacts, Suivi des échanges, Gestion des missions, Portails clients, Produits & services, Améliorations, Témoignages, Réponses types, Concurrents |
| GESTION DU CONTENU | Contenu, Analyse contenu, Plateformes, Hashtags, Strat' Hashtag, Actions marketing |

Une cinquième zone, **« BDD FILTRÉES ET PUBLIÉES / NE PAS TOUCHER »**, contient
les vues techniques dont dépendent les formules et rollups. Les bases suffixées
« publiée ne pas toucher » (Contenu, Portail client, Plateformes) sont des vues
miroir : ne jamais y écrire directement.

---

## 1. OPS BOARD — piloter l'activité

Le board « CEO ». Tout ce qui fait tourner la boîte.

### Vues du board
- TRACKER DE TÂCHES · MA SUPER TO-DO · MA SEMAINE SOCIAL MEDIA
- PIPE PROSPECTS & MISSIONS
- PROJETS · PORTAILS CLIENTS
- Bloc « ACTIONS RAPIDES » (boutons de création)

### Sous-pages

**Suivi CRM**
Clients en cours · Prospects chauds · Pipe · Suivi des échanges · Tâches CRM

**Suivi Facturation**
Factures en retard · Devis à relancer · Factures et échéances · Devis

**Suivi Finances**
Recettes & dépenses · Mon année · Mon mois · Prévisionnel · Relevé solde de banque

**Suivi Objectifs**
Tâches · Areas · Objectifs · Key results (structure OKR)

**Suivi KPIs**
Bloc « ajouter le mois pour le calcul des KPIs », puis 3 axes :
FINANCIER · MARKETING · OPÉRATIONNEL
Toggles de rattachement : Projets, Tâches, Contenus, Dépenses, Factures & devis,
Prospects, Clients, Échanges.

**CEO DAY** — une base unique, le rituel de pilotage périodique.

**GTD PLAN** — la boîte de tri. Une base CAPTURE, puis 8 zones de dispatch :
1. C'est actionnable ! → Tâche
2. À faire plus tard… → Tâche différée
3. C'est un projet → Projets
4. C'est une action marketing → Actions marketing
5. Ressources → Base de connaissances
6. Objectifs → Objectifs
7. Un contenu → Contenu
8. Un service / produit → Produits et services

**MARKETING 90 DAYS**
Actions marketing à actionner · Produit / service à actionner (horizon trimestriel).

---

## 2. BRAIN BOARD — capitaliser

Le cerveau externe : ce qu'on apprend, ce qu'on garde, ce qu'on formalise.

### Vues du board
- AREAS (domaines de vie/business, colonne vertébrale du classement)
- VIDE CERVEAU / IDÉES NON TRAITÉES (inbox `My Brain`)

### Sous-pages
- **Apprentissages** — Areas · Formations · Podcast
- **Ressources** — Areas · Ressources · Mise à jour
- **Documents** — Areas · Mes documents
- **Process** — Areas · À mettre à jour · Process (SOPs)
- **Mises à jour** — Ressources · Process (ce qui est périmé et doit être révisé)
- **GTD PLAN** — même boîte de tri que dans OPS

Point clé : `Process` et `Base de connaissances` portent une **date de dernière
MAJ + une fréquence de révision**, ce qui génère une alerte automatique quand un
contenu devient périmé. C'est le mécanisme anti-obsolescence du système.

---

## 3. CX BOARD — la relation client

### Vues du board
- Espace client en cours (Portails clients)
- Missions en cours (Gestion des missions)

### Sous-pages

**Customer Care**
Templates de réponses · Améliorations · Témoignages · Process

**Gestion des missions clients**
Missions · Portails clients

**Mes offres**
Mes offres et services (base Produits et services)

**Veille concurrentielle**
Contacts concurrents · Analyse entreprises concurrentes · Veille des offres et lancements

**Objectifs** (volet vente/clientèle)
Areas · Objectifs vente et clientèle · Key results

**KPIs** — Ventes et clientèle

---

## 4. CONTENT BOARD — la production

Séparé en deux moitiés symétriques : **CLIENTS** et **PERSO**. Les deux tapent
dans la même base `Contenu`, discriminée par le champ `PRO / PERSO`.

### Vues du board
VISION ANALYSE · AREAS / TÂCHES · PIPELINE · MASTER PLANNING

### Côté CLIENTS
- **Labo à idées** — Toutes mes idées
- **Planification** — À suivre cette semaine · À suivre ce mois · Preview Feed (filtrable par portail client) · À préparer
- **Master Planning** — la vue calendrier globale
- **À recycler** — contenus éligibles au recyclage
- **KPIs** — Analyse par post
  *(les analyses mensuelles par client vivent dans la page « Analyse » de chaque portail client)*

### Côté PERSO
- **Mon Labo à idées**
- **Ma Planification** — mêmes 4 vues
- **Mon contenu à recycler**
- **Hashtags** — Ma base de hashtags · Stratégie de hashtags
- **Mes Objectifs** — Areas · Objectifs · Key results
- **Mes KPIs** — une vue par plateforme : LINKEDIN · X · FACEBOOK · INSTAGRAM ·
  YOUTUBE · TIKTOK, puis Analyse marketing du mois, Analyse par post,
  Analyse globale social media, Analyse marketing

---

## Carte des dépendances (ce qui casse si on touche)

```
Contacts ──┬─> Suivi des échanges ──> KPIS/MOIS
           ├─> Gestion des missions ──> Portails clients ──> Contenu
           ├─> Devis et factures ──> Recettes et dépenses ──> Compta mensuelle ──> Compta annuelle
           └─> Projets ──> Tâches

Contenu ──┬─> Analyse Contenu ──> KPIS
          ├─> Plateformes
          ├─> Strat' Hashtag ──> Hashtags
          └─> Portail client

Areas ──> Objectifs ──> Key results ──> KPIS
Areas brain ──> My Brain / Base de connaissances / Documents / Process
```

`KPIS` est le point de convergence : presque toutes les bases y remontent via des
relations mensuelles. C'est aussi la base la plus lourde (~200 champs, dont une
grille complète métrique × plateforme).
