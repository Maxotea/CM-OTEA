# Routines review client — vendredi (préparation) & lundi (envoi + CR)

Le cycle hebdomadaire de la review client, en deux temps depuis le 19/08/2026 :
le **vendredi matin** tout est préparé pour la semaine suivante, le **lundi matin**
le mail part. Destinataires, tons et opt-in d'envoi : `clients-config.json`.
Dossiers et fichiers Drive : `reviews/config.json`. Modèle du mail :
`modele-mail-review.md`. Circuit technique :
`.claude/skills/cm-metricool/references/review-hebdo.md`.

Le principe côté client : **un seul lien, pour toujours** — son dossier Drive
« Validation hebdo — <Client> » (champ `drive_dossier`), partagé une fois en
« tous les utilisateurs disposant du lien : éditeur ». Chaque vendredi le tableau
de la semaine suivante y est déposé et l'ancien glisse dans `Archives/`.

## VENDREDI — routine « Review — préparation du vendredi » (8h00 Paris été)

Avant elle, tout ça a déjà tourné tout seul — vérifier, pas refaire :

| Heure (Paris, été) | Action GitHub | Quoi |
|---|---|---|
| 6h30 | « Review hebdo client », job `appliquer` | dernière relève de la semaine en cours |
| 6h30 | « Carrousels hebdo » | le carrousel du mercredi SUIVANT est planté en brouillon |
| 7h00 | « Review hebdo client », job `generer` | un fichier par compte actif pour le lundi SUIVANT, commité dans `reviews/a-envoyer/` |

La séquence de la session (toujours commencer par `git pull`) :

1. **Vérifier la génération** : les fichiers `reviews/a-envoyer/<slug>-<lundi suivant>.xlsx`
   existent pour chaque compte actif de `reviews/config.json`. Sinon, lancer le workflow
   « Review hebdo client » en mode `generer` (le déclenchement planifié vise le lundi
   suivant tout seul ; à la main, remplir `semaine`) et attendre le commit.
2. **Pour chaque client actif** :
   - Déposer son xlsx dans son dossier permanent : `create_file` avec `parentId` =
     `drive_dossier`, `base64Content` du xlsx, `contentMimeType` xlsx, conversion par
     défaut (le fichier devient un Google Sheet, éditable au téléphone). Titre :
     « Validation hebdo — <Nom> — semaine du <JJ-MM> ».
   - Déplacer l'ancien fichier (le `drive_fichier` actuel) vers `drive_archives` :
     `update_file` avec `parentId` = `drive_archives`. Ne JAMAIS le supprimer.
   - Noter le nouvel identifiant dans `reviews/config.json` → `drive_fichier`.
   - Préparer le **brouillon Gmail** depuis `modele-mail-review.md`, au ton du client
     (`clients-config.json` → `ton`). Le bouton pointe vers le **fichier de la semaine**,
     et le mail rappelle que le **dossier** est le même lien chaque semaine. Destinataire :
     uniquement si `email_confirme` est `true` ; sinon champ « À » vide.
3. **Commit + push + PR + merge de `reviews/config.json`** : les relèves (6h30 · 12h30 ·
   18h30, heure de Paris) lisent le `drive_fichier` de main plusieurs fois par jour —
   la mise à jour doit être mergée dans la foulée.
4. **Vérifier la lisibilité** : `get_file_permissions` sur le nouveau fichier doit montrer
   une permission `type: anyone` (héritée du dossier). Si elle manque, le partage du
   dossier n'est pas actif — le signaler à Maxime, c'est UN réglage à faire une fois.
5. Terminer par un rapport court : fichiers déposés, brouillons prêts, points d'attention
   (créneaux déjà passés, visuels manquants, partage à activer).

## LUNDI — routine « Review — envoi du lundi » (8h00 Paris été)

1. `git pull`, lire `reviews/config.json` et `clients-config.json`.
2. Pour chaque client actif de la review :
   - `envoi_review_auto` **et** `email_confirme` vrais → **envoyer** le mail
     (`send_message`, composé depuis `modele-mail-review.md` avec le lien du
     `drive_fichier` courant), puis supprimer le brouillon du vendredi devenu redondant.
   - Sinon → ne rien envoyer : vérifier que le brouillon du vendredi existe toujours et
     le lister dans le rapport comme « à envoyer par Maxime ».
3. C'est la SEULE exception à la règle « ne jamais envoyer automatiquement », décidée par
   Maxime le 19/08/2026 et bornée par les deux drapeaux de `clients-config.json`.

## LUNDI — routine « CR client Publi Hebdo » (9h00 Paris été)

1. **Bilan de la semaine passée** — lire `reviews/etat/*.json` : publiés, ✏️ à corriger
   (reprendre avec le commentaire → nouveau brouillon → il repartira dans la review
   suivante), ⛔ refusés (retirer à la main dans Metricool), ⏳ ✅ en attente (média ou
   placeholder à compléter — la relève publiera toute seule ensuite), lignes retouchées
   sans décision (à relancer gentiment). C'est la matière du CR.
2. Le CR habituel (`recap-semaine-*.md`, `whatsapp-semaine-*.md`) intègre ce bilan et,
   pour chaque client, le **lien de son dossier Validation hebdo** (le lien permanent) —
   aussi dans le message WhatsApp pour les clients en canal whatsapp.
3. Les mails et messages du CR partent en **brouillon** : Maxime relit et envoie
   (l'exception d'envoi automatique ne couvre que le mail de review du lundi matin).

## Ce que le client vit (pour répondre à ses questions)

Le lundi matin il reçoit le mail, ouvre son tableau (toujours le même dossier), corrige
les légendes dans les cases jaunes, choisit ✅ / ✏️ / ⛔, commente. Ses décisions sont
appliquées automatiquement aux trois relèves quotidiennes : les ✅ partent en publication
automatique (retenus ⏳ si le visuel manque, publiés dès qu'il est attaché), les ✏️ et ⛔
remontent dans le CR suivant. Une ligne sans décision ne part jamais. Le vendredi, la
semaine suivante remplace la semaine écoulée dans son dossier ; les anciennes semaines
restent consultables dans `Archives/`.

## Dépendance amont

Les brouillons de la semaine suivante doivent exister dans Metricool AVANT le vendredi
7h00 : c'est la routine « POST CM-OTEA » du lundi (qui planifie 2 semaines d'avance) qui
garantit cette avance. Si un vendredi le fichier d'un client sort vide ou trop maigre,
c'est ce maillon-là qu'il faut regarder.
