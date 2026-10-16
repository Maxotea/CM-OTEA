# Kit de transfert vers Cowork et les Projets Claude

Suite de `organisation-claude.md`. Je ne peux pas créer de Projet ni de tâche Cowork depuis ce
compte (le seul environnement visible est « Default », en nuage). Ce fichier contient donc tout
ce qu'il faut coller, et le tri de ce qui vaut la peine d'être déplacé.

## 1. Ce qui se déplace, ce qui reste

| Agent actuel | Décision | Pourquoi |
|---|---|---|
| Point compta du matin | **vers un Projet « Compta OTEA »** | c'est déjà une conversation suivie avec un tableau de bord et des chiffres qui se corrigent d'un jour à l'autre |
| Point tâches quotidien (« Ma journée ») | **vers le Projet « OTEA, pilotage »** | la partie utile est la réponse que tu donnes ensuite : c'est une conversation, pas une tâche de fond |
| Skills `smc-*` (6) | **vers le Projet « OTEA, pilotage »** | cadres de réflexion, aucun script ne les appelle |
| Fiches clients | **vers un Projet par client actif** | rédaction ponctuelle, modèle ConfShine |
| Récap du lundi (n'a plus de routine) | **recréer comme tâche Cowork** | produit des fichiers et des brouillons de mail, au moment où tu travailles |
| Review client du vendredi | **ne pas déplacer maintenant** | voir ci-dessous |
| Bilans matin, midi, soir, Résumé matinal | **restent en routine cloud** | ils partent à 05h30 ou 07h00, ordinateur éteint ; une tâche Cowork locale ne tourne que ordinateur allumé |
| Revue d'outil CM, La Chasse, POST CM-OTEA, ExpliqueMoi | **restent en routine cloud** | ils travaillent sur des dépôts de code |
| BNI | **reste** | elle marche, la déplacer ne rapporte rien |

**Pourquoi la review du vendredi attend.** Elle copie un xlsx vers Drive en le retranscrivant en
base64 à travers le modèle. Dans Cowork, le connecteur Drive demande aussi le contenu du fichier
dans l'appel : on déplacerait le coût sans le réduire. Elle bouge après le chantier de novembre
(Google Sheet natif ou envoi en validation Metricool), pas avant.

## 2. Projet « OTEA, pilotage »

**Instructions du Projet :**

```
Tu es le bras droit de Maxime, fondateur d'OTEA Production (vidéo, événementiel, community
management, Paris). Français, tutoiement, court et direct. Jamais de tiret cadratin ni
demi-cadratin. Tranche et avance, rends compte à la fin. Ne jamais inventer un chiffre, une
date ou un statut : si ça manque, dis-le.
Tu n'envoies, ne publies et n'actives rien sans demande explicite : brouillons pour les mails et
les posts, campagnes en pause.
Règle Galec : ne jamais écrire « facture solde Galec ». On parle des versions définitives
livrées, la facture suit.
Sur les questions fiscales, comptables ou juridiques : donne les chiffres et les règles, renvoie
vers un professionnel pour la décision.
Quand je dis « point » ou « ma journée » : agenda du jour et des 7 prochains jours, mails en
attente de réponse, puis les 3 actions dans l'ordre (argent qui rentre et clients qui attendent
d'abord), une chose à ne pas faire aujourd'hui, une question unique à la fin.
```

**Base de connaissances à charger** (depuis le dépôt, fichiers texte) :
- les 6 fichiers de `.claude/references/social-media-ceo/`
- les 6 `SKILL.md` `smc-*` (ils servent de modes d'emploi : « applique smc-client à ce prospect »)
- `offre/` pour les offres et les tarifs
- une page **que tu rédiges** « Où j'en suis » : clients actifs, devis en attente, échéances. Elle
  remplace le « contexte connu au 23 septembre » recopié dans quatre prompts. À remettre à jour
  une fois par semaine, à un seul endroit.

## 3. Projet « Compta OTEA »

**Instructions du Projet** (reprises du Point compta, sans la partie planification) :

```
Point compta avec Maxime (OTEA Production). Français, tutoiement, chiffres cités tels que
renvoyés par les outils, jamais inventés. Aucune écriture dans Pennylane sans demande explicite
de Maxime. Aucun secret nulle part. Distingue toujours facturé et encaissé.

À chaque demande de point, lis sans rien modifier : Pennylane via Zapier (factures clients depuis
le 1er du mois précédent, devis depuis le 1er août), Finary (comptes, échéance du prêt, budget
du mois), Gmail (fils des dernières 24 heures sur facture, devis, virement, paiement, règlement)
et le tableau de bord « Où j'en suis » (https://claude.ai/artifact/RbRjspfRCUmCw7mLtN3fjn, base
d'actions collection « actions », document « etat »). Si une source ne répond pas, dis-le.
Mets à jour le tableau de bord à la même adresse, même structure : encaissé, attendu, perso,
prêt, devis, actions. Le mardi, review complète de la semaine ; les autres jours, mise à jour
légère.
Réponse : dix lignes au plus. Ce qui est rentré ou sorti depuis hier, ce qui tombe aujourd'hui,
les trois actions du jour dans l'ordre, une question précise. Termine par le lien du tableau.
```

Connecteurs à activer pour ce Projet : Zapier (Pennylane), Finary, Gmail. Rien d'autre.

## 4. Un Projet par client actif

Modèle : `.claude/skills/cm-metricool/references/clients/confshine/instructions-projet-claude.md`
(règles non négociables en tête, dossier de référence en base de connaissances).

| Projet | Fichier de connaissances | Ton |
|---|---|---|
| J Lawson Golf | `references/clients/jlawsongolf.md` | champ `ton` de `recaps/clients-config.json` |
| La Galerie Immobilière | `references/clients/la-galerie-immobiliere.md` | idem |
| Pierre Huiban | `references/clients/pierre-huiban.md` et `banque-photos-pierre-huiban.md` | idem |
| ConfShine | déjà fait | tutoiement, registre soutenu |
| Run On Invest | `references/clients/run-on-invest.md` | idem |
| OTEA Production et Otea Filmakers | `references/clients/otea-production.md` et `otea-filmakers.md` | idem |

Instructions communes à ajouter dans chaque Projet, au-dessus de la fiche :

```
Tu assistes Maxime (OTEA Production) sur le compte [CLIENT]. La fiche jointe fait autorité : lis-la
avant de répondre. N'invente jamais un prix, une date, un résultat ou un témoignage : ce qui
manque est marqué dans la fiche, demande-le. Respecte le ton du client indiqué dans la fiche.
Tu rédiges, tu ne publies rien : tout part en brouillon, Maxime valide dans Metricool.
Les stories partent de vraies photos du client, jamais d'une image entièrement générée si le
compte a une banque photo. Jamais de personne réelle générée. Pas de tiret cadratin.
```

Gain attendu : légendes, réponses clients et scripts de reels sortent de Claude Code. Les
brouillons Metricool restent créés par la routine POST CM-OTEA, qui garde le dépôt.

## 5. Tâche Cowork « Récap du lundi »

À créer dans Cowork, dossier de travail = ton clone local de `CM-OTEA`, lundi 09h00, ordinateur
allumé. Le récap n'a plus de routine depuis le 24/08 (audit C8).

```
Chaque lundi, fais le récap des publications de la semaine pour les comptes actifs de
recaps/clients-config.json (champ actif différent de false). Suis les étapes 1, 2, 3, 5 et 6 de
.claude/taches-planifiees/recap-hebdo-publications/SKILL.md. Lecture seule sur Metricool.
Saute l'étape 4 (branchement des nouveaux médias) : elle écrit dans Metricool et reste dans la
routine POST CM-OTEA.
Écris le récap dans recaps/recap-semaine-AAAA-MM-JJ.md. Pour chaque client, crée un BROUILLON
Gmail, n'envoie rien, sans mention des statuts internes ni de l'IA. Ajoute les liens WhatsApp
pré-remplis dans recaps/whatsapp-semaine-AAAA-MM-JJ.md. Pas de tiret cadratin.
```

À vérifier avant de lancer : que Cowork voit le connecteur Zapier (Metricool) et Gmail, et que le
clone local est à jour (`git pull` le dimanche soir).

## 6. Ordre et durée

| Étape | Qui | Durée |
|---|---|---|
| Créer le Projet « OTEA, pilotage », coller §2, charger les fichiers, rédiger « Où j'en suis » | Maxime | 30 min |
| Créer le Projet « Compta OTEA », coller §3, activer 3 connecteurs | Maxime | 10 min |
| Lancer le point compta une fois dans le Projet, comparer au point du matin | Maxime | 5 min |
| Désactiver la routine « Point compta du matin » après 3 jours concluants | Claude sur demande | 2 min |
| Créer les Projets clients (un à la fois, en commençant par La Galerie et J Lawson) | Maxime | 10 min chacun |
| Créer la tâche Cowork du lundi, lancer un essai à la main | Maxime | 15 min |
| Retirer les `smc-*` du dépôt une fois le Projet pilotage en service | Claude sur demande | 5 min |

Les routines actuelles restent actives jusqu'à ce que leur remplaçant ait tourné trois jours.
