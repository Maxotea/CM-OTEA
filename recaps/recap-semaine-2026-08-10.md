# 📅 Semaine du lundi 10/08 au dimanche 16/08 — comptes rendus clients

*Généré le mardi 11/08/2026 — avec les upgrades du CR (fichier de validation `reviews/`).
Le CR est parti avec un jour de retard : la routine du lundi n'a pas tourné.*

## Ce qui a été produit

| Client | Canal | Fichier de validation | État |
|---|---|---|---|
| J Lawson Golf | email | ✅ joint | envoyé le 11/08 à 09h27 |
| La Galerie Immobilière | email | ✅ joint | envoyé le 11/08 à 09h27 |
| Le Loft | email | ✅ joint (2ᵉ mail correctif) | 1ᵉʳ mail envoyé, correctif en brouillon |
| Gossip Beauty Center | WhatsApp | ❌ **non livré** | message envoyé, fichier manquant |
| Pierre Huiban | WhatsApp | ❌ **non livré** | message envoyé, fichier manquant |

## 🔴 Erreur constatée le 11/08 : 3 clients sur 5 n'ont pas reçu le fichier

Le CR est parti sans le fichier de validation pour trois clients. Deux causes distinctes :

1. **Le Loft — erreur de jugement de ma part.** J'avais volontairement écarté le fichier
   au motif qu'une seule ligne était à valider, et le mail annonçait même l'envoi « à
   partir de lundi prochain ». C'était une mauvaise décision : le fichier doit partir
   pour tous les clients, chaque semaine. **Corrigé** — un second mail avec la pièce
   jointe attend en brouillon.

2. **Gossip et Pierre — limite structurelle, non corrigée.** Ces deux clients passent par
   WhatsApp faute d'adresse email, et un lien `wa.me` ne peut pas porter de pièce jointe.
   Deux tentatives de contournement ont échoué :
   - le dépôt Drive via le connecteur renvoie `Invalid conversion requested` sur un xlsx ;
   - même en cas de succès, les dossiers Drive des deux clients sont partagés en
     `anyone: reader`. Le client pourrait ouvrir le fichier mais **pas le remplir**, ce
     qui casse la boucle de validation. Je n'ai pas d'outil pour passer un partage en
     éditeur.

   **Ce qu'il faut pour débloquer, par ordre de préférence :**
   a. **Leur adresse email** — le fichier part alors en pièce jointe comme pour les
      autres. C'est la solution propre, et elle prend une minute.
   b. À défaut : passer leurs dossiers Drive en « tous les utilisateurs disposant du
      lien : éditeur », puis déposer le fichier à la main et noter son identifiant dans
      `reviews/config.json` → `drive_fichier`.

   En attendant, leurs fichiers sont prêts dans `reviews/a-envoyer/`.

## 🔴 Le vrai sujet de la semaine : les brouillons qui bloquent

État réel relevé dans Metricool le 11/08, pas au fichier généré lundi :

| Client | Contenus | Validés | Brouillons | Créneaux déjà perdus |
|---|---|---|---|---|
| Gossip Beauty Center | 10 | 10 | 0 | 0 |
| Le Loft | 10 | 9 | 1 | 0 |
| Pierre Huiban | 9 | 5 | 4 | 1 |
| La Galerie Immobilière | 9 | 1 | 8 | 2 |
| **J Lawson Golf** | 10 | **0** | **10** | **3** |

**J Lawson Golf ne publie rien depuis lundi.** Les dix contenus de la semaine sont en
brouillon, trois créneaux sont passés à vide (story + post de lundi, story de mardi). John
a prévenu le 05/08 qu'il était en Suisse pour sa course et peu disponible — la validation
n'a donc jamais eu lieu. C'est exactement le trou que le circuit `reviews/` doit boucher.

**La Galerie Immobilière** est dans le même cas à un post près : 8 brouillons sur 9, deux
stories perdues. Seul le post du mercredi 12/08 est validé.

À l'inverse, **Gossip est à 10/10 validé** et **Le Loft à 9/10** — pour eux le système
tourne.

## Les upgrades appliqués à ce CR

1. **Fichier de validation joint au mail** (`reviews/a-envoyer/*.xlsx`) pour les deux
   clients à fort volume de brouillons. Le client coche ✅ / ✏️ / ⛔ ligne par ligne,
   corrige les légendes dans les cases, renvoie le fichier par mail. C'est la variante
   « sans Drive » documentée dans `review-hebdo.md` : au retour, déposer la pièce jointe
   dans `reviews/retours/<slug>-2026-08-10.xlsx`, commit + push, et la relève l'applique.
2. **Canal par client** : email pour les trois clients à adresse confirmée, WhatsApp pour
   les deux dont on n'a que le numéro. Plus de destinataire en `[À RENSEIGNER]`.
3. **Transparence sur les créneaux perdus** : chaque CR nomme les publications qui ne sont
   pas parties, avec leur date. C'est le point qui fait comprendre au client pourquoi sa
   validation compte.

**Règle à ne plus enfreindre** : le fichier de validation part pour **tous** les clients
actifs de `reviews/config.json`, chaque semaine, quel que soit le nombre de lignes à
valider. Pas d'arbitrage au cas par cas — c'est le rituel qui crée l'habitude côté client,
et un client qui ne le reçoit pas une semaine ne le cherchera pas la suivante.

## ⚠️ À trancher

- **Le Loft — adresse non re-confirmée.** `lestudio92800@gmail.com` est marquée confirmée
  dans la config *par l'usage* : tu y as envoyé toi-même le CR de juillet le 05/08. Tu ne
  l'as pas citée le 11/08 (tu n'as confirmé que John et La Galerie). Corrige la config si
  ce n'est pas la bonne boîte.
- **Le fichier de validation est daté de lundi.** Il liste des créneaux déjà passés
  (lundi, mardi). Le client verra des lignes qu'il ne peut plus sauver. C'est assumé et
  expliqué dans les mails, mais si tu préfères, je régénère les fichiers sur les seuls
  créneaux restants avant envoi.
- **Colonne « Format » erronée dans les fichiers générés.** Les stories y apparaissent
  comme `Post` (la légende dit bien « Story lundi… », mais le format affiché est faux).
  Bug côté `scripts/review.py` à corriger avant lundi prochain.
- **Reel Sabrina non tourné.** Le face-cam « marché immo de l'été » traîne depuis la
  semaine du 03/08. Le mail lui pose la question : tourner cette semaine ou remplacer.

## Prochaine échéance

Les stories de tous les comptes s'arrêtent au **31/08** → reconduction septembre à prévoir
avant la mi-août (~15 min en bulk).
