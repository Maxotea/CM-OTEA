# SOCIAL MEDIA CEO — Les 33 bases de données

Schémas extraits de la source Notion. Notation :
`nom (type)` — et pour les select/status/multi-select, les options sont listées.
`[f]` = formule, `[r]` = rollup (valeur calculée, jamais saisie à la main).

---

## GESTION DU CONTENU

### `Contenu` — la base centrale de production
> Affichée partout sous les noms : Toutes mes idées, À préparer, À suivre cette
> semaine / ce mois, Preview Feed, Master Planning, À recycler, Pipeline.

| Champ | Type | Valeurs |
|---|---|---|
| Publication | title | — |
| Statut | status | Idée → À préparer → À approuver → Demande de modif → Validé client → Créer visuel → Rédaction → Tournage / enregistrement → Montage → Prêt à programmer / publier → Programmé / Publié |
| Type de contenu | multi_select | Post instagram, Reels Instagram, Story Instagram, Post Facebook, Infolettre, Épingle Pinterest, Article de blog, Épisode podcast, TikTok, Post Threads, Post Linkedin, Post X, Vidéo Youtube |
| Piliers | multi_select | Vente, Inspiration, Captiver, Backstage / Lifestyle, Éduquer, Connecter |
| Type de visuel | select | Photo, Visuel Canva, Carrousel, Couverture Reel, Couverture Vidéo |
| PRO / PERSO | select | PERSO, CLIENT |
| Sujet | multi_select | (libre) |
| Doit être publié le | date | — |
| Portail client | relation | → Portails clients |
| Plateforme | relation | → Plateformes |
| Stratégie Hashtags | relation | → Strat' Hashtag |
| Contenu Recyclé | relation | → Contenu (auto-référence) |
| Déjà Recyclé ! | checkbox | — |
| Analyse | relation | → Analyse Contenu |
| KPI / MOIS | relation | → KPIS |
| Visuel / Fichiers | file | — |
| Lien Inspiration, Lien Audio reels | url | — |
| Impressions, J'aime reçus, Commentaires reçus, Enregistrements | number | saisie post-publication |
| Taux d'engagement / Publication | [f] | — |
| Taux d'engagement / impression | [f] | — |
| Nombre de caractères / Combien de caractères ? | [f] / text | — |
| Hashtag à copier coller | [f] | concatène les hashtags du groupe lié |
| On recycle ? | [f] | flag automatique d'éligibilité au recyclage |
| Cette semaine / Ce mois / Cette Année | [f] | filtres temporels |
| Bravo ! | [f] | feedback de perf |
| Valider ! | button | fait avancer le statut |

**Le pipeline de statut est le cœur opérationnel du système.** Voir `03-workflow-contenu.md`.

### `Analyse Contenu`
Contenu (relation) · Analyse [f] · Nom (title).
Une ligne d'analyse rattachée à un ou plusieurs contenus.

### `Plateformes` *(publiée — ne pas toucher)*
Nom (title) · Contenu (relation) · Tâches (relation) · Statistiques [f].

### `Hashtags`
| Champ | Type | Valeurs |
|---|---|---|
| HASHTAGS | title | — |
| THEME | select | CIBLE, BUSINESS, METIER, Podcast, MINDSET |
| Taille hashtag | select | Petit, Moyen, Gros |
| Préférence | select | ⭐ / ⭐⭐ / ⭐⭐⭐ |
| Reach | text | — |
| Groupes | relation | → Strat' Hashtag |

### `Strat' Hashtag`
Groupe (title) · Hashtags (relation) · Contenus (relation) ·
Nombre de Hashtags (Max 30) [f] · Hashtags à copier / coller [f].

> Logique : on ne choisit pas des hashtags un par un, on assemble des **groupes**
> mixant les 3 tailles et les 5 thèmes, plafonnés à 30, et on colle le groupe
> entier sur un contenu.

### `Actions Marketing`
| Champ | Type | Valeurs |
|---|---|---|
| Action | title | — |
| Type | multi_select | LEAD MAGNET, TEMPLATE, LANCEMENT, SERVICE PRODUIT |
| ✓ STATUT | status | Idée, Programmé, Projet en cours, Action validée |
| Mois | select | Janvier → Décembre |
| Trimestre | select | Q1–Q4 |
| ✓ Date début et fin de projet, ✓ Actif à partir du | date | — |
| Jours avant début / Actif dans | [f] | compte à rebours |
| Base de connaissances, My Brain, Tâches | relation | — |
| Pièce jointe | file | — |

---

## GESTION DE LA CLIENTÈLE

### `Contacts` — CRM unifié (prospects, clients, concurrents, collaborateurs)
| Champ | Type | Valeurs |
|---|---|---|
| ✓ Nom complet | title | — |
| Type | select | Collaborateur, Client, Prospect, Ancien client, Non converti, Concurrent, Autre |
| Statut | status | À contacter → Contacté → En contact → A rappeler → Appel découverte réservé → Faire un devis → Devis envoyé → En négo → Signé / Perdu |
| Ton utilisé | select | Tutoiement, Vouvoiement |
| E-mail, Téléphone, Social Media, Adresse | email/phone/url/text | — |
| Entreprise du contact, N°SIRET | text | — |
| Tarif proposé | number | — |
| À recontacter dans | number | délai de relance |
| Date de Naissance → Anniversaire | date / [f] | déclencheur de contact |
| Ancien client | checkbox | — |
| CA réalisé pour ce contact | [r] | — |
| Dernier contact, CLIENT SIGNÉ LE | [r] | — |
| relations | → Suivi des échanges, Gestion des missions, Devis et factures, Projets, Tâches, Process, Témoignage, Base de connaissances, Entreprise Concurrente, KPIS, Prospect pour quel service ? |

### `Suivi des échanges` — journal de toutes les interactions
| Champ | Type | Valeurs |
|---|---|---|
| Nom client - échange | title | — |
| Type | multi_select | Courrier, Mail, Appel téléphonique, Visio call, Rencontre présentielle, Messages vocaux |
| Sujet | select | Offre, Prospection, Relance impayé, Suivi, Brief créatif, Rencontre client, Appel découverte |
| Statut de l'échange | status | A traiter, En cours, Terminé |
| Statut du contact | [r] | Nouveau message, Message lu - en attente, Message répondu |
| Date, Créée par | date / created_by | — |
| relations | Contact, Mission client, Devis et factures, Documents clients, KPIS / MOIS |

### `Gestion des missions`
| Champ | Type | Valeurs |
|---|---|---|
| ✓ Prénom Nom du client | title | — |
| ✓ Statut mission | status | Onboarding à faire → Onboarding en cours → Attente paiement → Mission à venir → Mission en cours → Outboarding en cours → Mission terminée |
| ✓ Période | date | — |
| Montant facturé / Encaissé | [f] | — |
| Solde mission | [r] | — |
| Commentaire | text | — |
| relations | Client, Espace client, Produit, Tâches, Devis et factures, Suivi des échanges |

> Le cycle **onboarding → mission → outboarding** est explicite. L'outboarding
> (clôture) est une étape à part entière, pas un simple « terminé ».

### `Portails clients` *(publiée — ne pas toucher)*
Portail client (title) · Statut (status : Non débuté / En cours / Terminé) ·
Dates de la prestation (date) · Début / Fin de la mission [f] · Team (person) ·
Contact email [r] · Produit [r] · relations → Client, Mission, Contenu, Suivi des échanges.

> C'est l'espace partagé avec le client : son calendrier de contenus, ses
> analyses mensuelles, ses validations.

### `Produits et services`
Nom du produit (title) · Statut (status : Idée, En cours de création, Refonte,
Actif, Inactif) · Prix HT (number) · TVA (select : 20 % / 10 % / 5,5 % / sans) ·
Prix TTC [f] · CA Facturé [r] · Nbr missions [r] ·
relations → Devis et factures, Gestion des missions, Objectifs, Tâches, Améliorations, Témoignage.

### `Customer Care : réponses types`
Name (title) · Process lié (relation) ·
Catégorie (select) : STRUCTURE · PAIEMENTS · AVANT MISSION/ACHAT ·
PENDANT MISSION · APRÈS-VENTE · MARKETING / BUSINESS · TROLLS / HATERS ·
FORMATION/UTILISATION · AUTRES TEMPLATES.

> Bibliothèque de réponses pré-écrites, indexée par moment du cycle client.
> La catégorie TROLLS / HATERS est prévue nativement.

### `Améliorations clients`
Amélioration proposée (title) · Statut (status : Non commencé / En cours /
Terminé) · Équipe (person) · Progression [r] ·
relations → Produit ou service, Tâches, Témoignage.

### `Témoignages`
Témoignage (title) · Date · Client (relation) · Produit ou service (relation) ·
Plateforme (multi_select : Youtube, Site, Instagram) · Photo (file) ·
Contact (url) · Améliorations (relation).

### `Concurrents`
Nom de l'Entreprise (title) · État (status : À faire, En cours, À mettre à jour,
Tout est ok) · Date de dernière mise à jour · Info Maj [f] ·
Site / URL Instagram, Linkedin, Facebook, Twitter, podcast (url) ·
Thématiques, Communication média (multi_select : Publications, Journaux,
Magazines, Salons, Conférences) ·
Gamme de prix, Produits / Services proposés, Publicités / Offres spéciales,
Mots-clés / Placement Google (text) ·
Newsletter fréquence (select : 1x/mois → plusieurs fois/semaine) ·
**Par plateforme (IG, LK, FB, TW, Podcast) :** Nombre d'abonnés (number),
Fréquence des publications (text), Formats / Type de contenus (text) ·
Objectifs de comparaison visés (select) · Offres et lancements (relation).

### `Offres et lancements concurrents`
Offre (title) · Entreprise concurrente (relation) · Tarif (number) ·
Page de vente (url) · Stratégie (text) ·
Type de lancement (select : Hybride, Orchestré, Evergreen) ·
Durée du lancement en jours (number) ·
LeadMagnet (select : Challenge, E-book, MasterClass Live, MasterClass Evergreen,
Template) · Lien / Doc LeadMagnet (url/file) ·
Note de l'offre et Note du lancement (⭐ à ⭐⭐⭐⭐⭐) · Catégorie (multi_select).

---

## GESTION DES OPÉRATIONS & FINANCES

### `Tâches`
| Champ | Type | Valeurs |
|---|---|---|
| Tâche | title | — |
| Statut | status | A faire en urgence, A faire, En cours, En pause, Terminé ! |
| Type de tâche | select | 📂 CEO, 🫂 Client, 💻 Production, 📱 Marketing, 📆 RDV, 🌟 Perso |
| Priorité | select | P1, P2, P3 |
| Impact | select | Important, Moyen, Faible |
| Do Date, Heure de début / de fin | date | — |
| Démarrer / Terminer la tâche | button | chronomètre intégré |
| Temps en minutes, Contrôle du temps | [f] | — |
| Fait ? | checkbox | — |
| Jour de la semaine, Info Do Date, Priorité de la tâche | [f] | — |
| Cette semaine / Ce mois / Semaine prochaine | [f] | filtres |
| Responsable | person | — |
| relations | Projets, Contact, Mission, Objectifs, Produits, Actions Marketing, Plateforme contenu, Améliorations client, KPIS / MOIS |

### `Tracker de tâches`
Nom (title) · Tâches (relation) · Analyse [f]. Base de comptage/reporting.

### `Projets`
Project (title) · Statut (status : Pas commencé, En cours, Terminé) ·
Chef de projet / Equipe (person) · Date début et fin (date) ·
Jours passés sur le projet [f] · Minutes [r] · Progrès [r] · Infos / Infos dates [f] ·
Type (multi_select) · Pièce jointe (file) ·
relations → Tâches, Objectifs, Process, Contact / client, Base de connaissances,
My Brain, KPIS / MOIS.

### `Devis et factures`
| Champ | Type | Valeurs |
|---|---|---|
| N° | title | — |
| Type | select | Devis, Acompte, Facture |
| État | status | À faire, Transmis, Ouverte, Relance, Relance 1, Relance 2, Partiellement payée, Validé, Refusé, Sans retours, Payée, Mise en demeure, ANNULÉE, Recouvrement |
| Montant HT (number) → Montant TTC / TVA | [f] | — |
| TVA | select | 20 %, 10 %, 5,5 %, sans TVA |
| Date d'émission, ✓ Accepté le (devis) | date | — |
| ✓ Paiement en plusieurs fois | checkbox | — |
| Échéances de paiement, Délai | number | — |
| Montant échéance, Date d'échéance | [f] | — |
| Solde devis / Solde facture, Tot. facturé HT / TTC, Devis validé | [f] | — |
| Encaissé Fact. TTC, Date de relance, Dernier paiement, Mail | [r] | — |
| Document | file | — |
| relations | Contact, Missions clients, Produits et services, Recettes et dépenses, Mois comptabilité, Prévisionnel, Suivi des échanges, KPIS / MOIS |

> L'échelle de relance est explicite : **Transmis → Relance 1 → Relance 2 →
> Mise en demeure → Recouvrement.**

### `Recettes et dépenses`
▶︎ Dénomination (title) · Type (select : Recette / Dépense) ·
Catégorie (select : MARKETING …) · Montant TTC (number) ·
TVA (select : 20 %, 10 %, 8,8 %, MIXTE, SANS TVA) + TVA mixte (number) ·
Encaissé HT / TTC, Dépense HT / Dépensé TTC, TVA Collectée / Décaissée, Frais STRIPE [f] ·
Moyen de paiement (select : Carte bancaire, Virement, Chèque, Espèce, Stripe, Paypal) ·
Date · Rapprochée (checkbox) · Fournisseurs (select + relation) ·
Client / Mission / Produit [r] · Exercice [r] ·
relations → Mois, Devis et factures, KPIS / MOIS.

### `Comptabilité mensuelle`
Nom (title) · ✓ Date · ✓ Trimestre (select T1–T4) · ✓ Années comptabilité (relation) ·
Saisies manuelles : ✓ Solde compte bancaire, ✓ FRAIS FIXES, ✓ Mon objectif était,
✓ Nbr devis validés / en attente / refusés-ghostés, ✓ Montant devis en attente,
✓ Montant refusés ou SR, ✓ Reporting TVA négative ·
Calculs : CA Facturé HT, CA Encaissé HT, Dépenses TTC, TVA collectée / déductible /
à payer, Bénéfices, Solde trésorerie, %, Montants validés ·
**Règles d'affectation automatiques :** URSSAF + IMPÔTS (25 %) · CONGÉS (10 %) ·
TRÉSORERIE (7 %) · PROJET X/Y (5 %) · RÉMUNÉRATION (le reste) ·
relations → Recettes et dépenses, Devis et factures, Prévisionnel, KPIS.

> Ces 5 enveloppes en pourcentage sont la règle de gestion la plus structurante
> du système financier. À reprendre telle quelle ou à recalibrer explicitement.

### `Comptabilité annuelle`
Nom (title) · Mois comptabilité (relation) · CA Facturé HT, CA Encaissé HT,
Dépenses TTC, TVA collectée / décaissée, Marge avant TVA, Marge TVA, Bénéfices,
Trésorerie, %, Alerte TVA, Mon obj [f] · Objectif [r].

### `Prévisionnel`
▶︎ Nom (title) · Type (select : Recette / Dépense) · Montant (TTC) (number) ·
TVA (select : 20 %, 10 %, MIXTE, SANS) + TVA Mixte · Montant HT / Montant TVA [f] ·
Réglée (checkbox) · Solde prévisionnel [f] · Fournisseurs (select) ·
Facture (relation) · Mois comptabilité (relation) ·
Date, Échéance facture, Contact, Mission, Année [r].

### `Areas OKRS` / `Areas brain`
Nom (title) · Statistiques [f] · relations vers Objectifs (resp. Process, My Brain,
Documents, Base de connaissances).

### `Objectifs`
Nom de l'objectif (title) · État (status : En réflexion, Planifié, Actif, Terminé) ·
Période (select : Mensuel, Trimestriel, Annuel) · Mois (Janvier→Décembre) ·
Trimestre (Q1–Q4) · Date de début / de fin ·
Avancement actions [r] · Avancement Key Results [r] · Avancement temps [f] ·
Titre Temps / Actions / Key Results [f] ·
relations → Aera, KEY RESULTS, Tâches, Projet lié, Produits et services.

### `Key results`
Nom (title) · Objectif (relation) · Calcul (select : DELTA / CUMUL) ·
Valeur départ, Résultat (number) · Calcul Résultat, Moyenne du résultat [f] ·
**Paliers** : Attente « Moyen », Attente « Bien », Attente « Wow » (number)
→ Progrès Bien / Progrès Wow, Titre moyen / bien / wow, Vision [f] ·
Atteint ? (checkbox) · Area [r] · KPI liés (relation).

> Un key result n'a pas une cible unique mais **trois paliers : Moyen / Bien / Wow.**

### `KPIS` — ~200 champs, tableau de bord mensuel
Mois (title) · Date · Trimestre (T1–T4) · Mois précédent / Mois suivant (relation) ·
Mois comptable (relation).

Regroupements calculés : **FINANCIER · MARKETING - COMMERCIAL ·
MARKETING - EMAILS · RÉSEAUX SOCIAUX · OPÉRATIONNEL · RELATIONS.**

Voir le détail dans `04-kpis.md`.

---

## GESTION DES RESSOURCES

### `My Brain` — l'inbox de capture
Name (title) · lien (url) · Do Date (date) · Traitée (checkbox) ·
Tags (multi_select : Web, Notes, Inspiration, Administratif, Idea, Article) ·
Crée le (created_time) · relations → Areas brain CM, Contact, Projets, Action marketing.

### `Base de connaissances`
✓ Nom (title) · Catégorie (select : Formation, Podcast, Ressource) ·
Type (select : Workbook, Business, Notion, Interne, Guide, Outils, Templates) ·
Statut (status : En cours, Terminé !, À consommer, À acheter) ·
Note (★ à ★★★★★) · Mon step / Step au total (number) → % complété [f] ·
Coût (number) · URL / Fichier ·
**Mettre à jour tous les** (select : Année, Trimestre, Mois, Semaine) +
Dernière mise à jour (date) → **Statut de la MAJ [f]** ·
relations → Area brain, Process, Contact, Projets, Action Marketing.

### `Documents`
✓ Nom (title) · Type (select : Société / Statuts, Contrats / Externe, Courrier,
Facture / devis, Compta) · Statut (status : À traiter, En cours, Traité) ·
Date du document · Documents (file) ·
relations → Areas brain, Suivi des échanges, Recettes et dépenses.

### `Process` — les SOPs
Process - SOPs (title) · Statut (status : À créer, Phase de test, En MAJ, Actif,
Archivé) · Service interne (select : Relation client, Finances et facturation,
Marketing, Opérationnel, CEO, Équipe, Social Media) ·
Catégorie (multi_select) : Customer Care · Expérience & service client ·
Mission client · Offre · Emailing · Podcast · Blog · Youtube · Linkedin ·
Instagram · Tiktok · Facturation · Paiement / compta · Ads · Marketing ·
Visibilité · RH / Juridique · Développement - Qualité · Gestion / Production ·
Responsable - Equipe (person) · Dernière MAJ (date) → **Alerte MAJ [f]** ·
Réponse type liée (relation) · relations → Areas brain, Contact, Projet.

---

## Bases miroir — ne jamais écrire dedans
`Contenu publiée ne pas toucher` · `Portail client publiée ne pas toucher` ·
`Plateformes publiée ne pas toucher`.
Ce sont des vues techniques utilisées par les formules et rollups.
