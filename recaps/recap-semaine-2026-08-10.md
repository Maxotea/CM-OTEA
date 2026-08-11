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

---

## 🔄 Changement de règle, 11/08 : le CR passe à la semaine suivante

Décision de Maxime : **le compte rendu et son fichier de validation portent désormais sur
la semaine d'après, plus jamais sur celle qui commence.** Un client ne valide pas le lundi
matin ce qui sort le lundi midi — il répond le soir ou le lendemain, et le créneau est
passé. La semaine du 10/08 en est la démonstration : J Lawson à 10 brouillons sur 10 avec
trois créneaux perdus, La Galerie à 8 sur 9.

Désormais le client a **sept jours pleins** pour trancher, et les publications du lundi
partent à l'heure.

**Appliqué dans le code** (commit `a3cb267`) :

- `scripts/review.py` → `semaine_lundi()` sans argument vise le lundi **suivant**, quel que
  soit le jour où il tourne. Vérifié sur les sept jours de la semaine.
- `appliquer` n'est pas touché : il lit la semaine dans l'onglet `_tech` du fichier, donc il
  traite toujours la bonne, même en retard.
- `--semaine` explicite reste prioritaire, avec son recalage sur le lundi.
- Doctrine réécrite dans `review-hebdo.md`, en-têtes de `review.yml` et `reviews/config.json`.

**Fichiers de la semaine du 17/08 générés et vérifiés** (Action `review.yml`, run 17) :
six comptes, chaque ligne rattachée à son `post_id` Metricool.

| Client | Lignes à valider | Fichier |
|---|---|---|
| Gossip Beauty Center | 10 | `gossip-beauty-center-2026-08-17.xlsx` |
| Le Loft | 10 | `le-loft-2026-08-17.xlsx` |
| J Lawson Golf | 10 | `jlawsongolf-2026-08-17.xlsx` |
| Pierre Huiban | 9 | `pierre-huiban-2026-08-17.xlsx` |
| La Galerie Immobilière | 8 | `la-galerie-immobiliere-2026-08-17.xlsx` |
| Otea Filmakers (banc d'essai) | 3 | `otea-filmakers-2026-08-17.xlsx` |

### Où en est l'envoi du nouveau CR

| Client | Fichier 10/08 (semaine en cours) | Fichier 17/08 (nouvelle règle) |
|---|---|---|
| J Lawson Golf | ✅ envoyé 09h27 | ⏳ brouillon neutralisé — pièce jointe à refaire |
| La Galerie Immobilière | ✅ envoyé 09h27 | ⏳ à faire |
| Le Loft | ✅ envoyé 09h50 | ⏳ à faire |
| Gossip Beauty Center | ❌ canal WhatsApp | ❌ bloqué — même cause |
| Pierre Huiban | ❌ canal WhatsApp | ❌ bloqué — même cause |

**Incident à signaler** : le premier brouillon 17/08 de J Lawson a été créé avec une pièce
jointe corrompue — le fichier base64 s'est tronqué à la recopie. Le brouillon a été
neutralisé (objet préfixé « NE PAS ENVOYER », pièce jointe retirée) avant tout envoi.
Le fichier sain est dans `reviews/a-envoyer/jlawsongolf-2026-08-17.xlsx`.
