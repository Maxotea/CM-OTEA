---
name: smc-veille
description: Veille concurrentielle SOCIAL MEDIA CEO — grille d'analyse d'un concurrent (présence par plateforme, fréquence, formats, gamme de prix, newsletter, mots-clés), suivi de ses offres et lancements (type, durée, lead magnet, notation), et exploitation des enseignements. Utilise ce skill quand l'utilisateur veut analyser un concurrent, comprendre ce que fait quelqu'un d'autre sur les réseaux, décortiquer un lancement ou une offre du marché, ou mettre à jour sa veille.
---

# Veille concurrentielle — SOCIAL MEDIA CEO

Référentiel : `.claude/references/social-media-ceo/01-bases-de-donnees.md` (Concurrents, Offres et lancements).

## Grille d'analyse d'un concurrent

Une fiche `Concurrents` complète comporte :

**Identité** — nom, site, gamme de prix, produits/services proposés,
thématiques, mots-clés / placement Google.

**Par plateforme** (Instagram, LinkedIn, Facebook, X, Podcast) — trois champs
systématiquement :
- nombre d'abonnés
- fréquence des publications
- formats / types de contenus

**Newsletter** — fréquence (`1x / mois`, `1x / 2 semaines`, `1x / semaine`,
`Plusieurs fois / semaine`).

**Communication média** — `Publications`, `Journaux`, `Magazines`,
`Présence sur des Salons`, `Conférences`.

**Publicités / offres spéciales**, `Objectifs de comparaison visés`.

**État** — `À faire` → `En cours` → `Tout est ok` → `À mettre à jour`
(+ date de dernière mise à jour, qui déclenche l'alerte).

Un contact peut être rattaché à un concurrent (type de contact : `Concurrent`).

## Analyser une offre ou un lancement

Base `Offres et lancements concurrents` :

| Champ | À renseigner |
|---|---|
| Offre | nom |
| Tarif | prix affiché |
| Page de vente | URL |
| Type de lancement | `Hybride` · `Orchestré` · `Evergreen` |
| Durée du lancement en jours | — |
| LeadMagnet | `Challenge` · `E-book` · `MasterClass Live` · `MasterClass Evergreen` · `Template` |
| Lien / Doc LeadMagnet | archiver le document |
| Stratégie | la séquence observée, en texte |
| Note de l'offre | ⭐ à ⭐⭐⭐⭐⭐ |
| Note du lancement | ⭐ à ⭐⭐⭐⭐⭐ |

Noter séparément **l'offre** (est-elle bonne ?) et **le lancement** (est-il bien
exécuté ?). Une offre médiocre bien lancée et une bonne offre mal lancée
n'appellent pas les mêmes conclusions.

## Comment conduire une veille

1. Collecter les faits observables uniquement : ce qui est publié, affiché,
   annoncé. Pas de spéculation sur les chiffres d'affaires ou les résultats.
2. Renseigner la fiche plateforme par plateforme.
3. Pour un lancement : reconstituer la séquence dans l'ordre (lead magnet →
   contenus de chauffe → ouverture → relances → fermeture) avec les dates.
4. Conclure sur **ce qui est transposable** et **ce qui ne l'est pas** compte tenu
   de la taille d'audience et du positionnement.

Ce qu'il ne faut pas faire : copier une stratégie sans regarder l'audience de
départ. Un lancement orchestré sur 30 000 abonnés ne se réplique pas sur 2 000.

## Rythme

Revue trimestrielle. Le champ `État` = `À mettre à jour` sert de file d'attente.
Entre deux revues, ne consigner que les nouveaux lancements observés — pas les
métriques, qui bougent trop pour valoir un relevé continu.

## Ce que la veille doit produire

Une veille qui ne débouche sur rien est du temps perdu. Chaque revue doit sortir
au moins un élément vers une autre base :
- une idée de contenu → `Contenu` (statut `Idée`)
- une idée d'offre → `Produits et services` (statut `Idée`)
- une action marketing → `Actions Marketing`
- un enseignement à garder → `Base de connaissances`
