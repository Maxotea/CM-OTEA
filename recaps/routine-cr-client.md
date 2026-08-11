# Routine du lundi — compte-rendu client + review hebdo

La séquence du lundi matin, dans l'ordre, pour la session Claude (« routine hebdo » /
« CR client »). Destinataires et canaux : `clients-config.json`. Modèle du mail :
`modele-mail-review.md`. Circuit technique de la review :
`.claude/skills/cm-metricool/references/review-hebdo.md`.

## Avant 9h, tout ça a déjà tourné tout seul — vérifier, pas refaire

| Heure (Paris, été) | Action GitHub | Quoi |
|---|---|---|
| 8h00 | « Carrousels hebdo » | le carrousel du mercredi est planté en brouillon |
| 8h30 | « Review hebdo client », job `generer` | un fichier Excel par compte actif, commité dans `reviews/a-envoyer/` |

Si le job `generer` n'a pas tourné (onglet Actions), le lancer en mode `generer` avant de
continuer. Toujours commencer par `git pull`.

## La séquence de la session

1. **Bilan de la semaine passée d'abord** — lire `reviews/etat/*.json` : publiés, ✏️ à
   corriger (reprendre avec le commentaire → nouveau brouillon → il repartira dans la
   review suivante), ⛔ refusés (retirer à la main dans Metricool), ⏳ ✅ en attente
   (média ou placeholder à compléter — la relève publiera toute seule ensuite), lignes
   retouchées sans décision (à relancer gentiment). C'est la matière du CR.
2. **Pour chaque client actif de `reviews/config.json`** :
   - Déposer son fichier `reviews/a-envoyer/<slug>-<lundi>.xlsx` dans son Drive via le
     connecteur Google Drive : `create_file`, `base64Content` du xlsx, `contentMimeType`
     xlsx, conversion par défaut (le fichier devient un Google Sheet, éditable au
     téléphone). Cible : son **dossier partagé** (`photos/<slug>.json` → `drive_folder`)
     — le partage par lien s'hérite du dossier, rien d'autre à faire. Sans dossier :
     dépôt à la racine, puis partage « tous les utilisateurs disposant du lien » à
     activer sur le fichier (une fois — vérifiable par `get_file_permissions`) et
     s'assurer que le client peut **écrire**.
   - Noter l'identifiant du fichier créé dans `reviews/config.json` → `drive_fichier`.
   - Préparer le **brouillon Gmail** depuis `modele-mail-review.md`, adapté au ton du
     client (`clients-config.json` → `ton`), pièce jointe xlsx incluse. Destinataire :
     uniquement si `email_confirme` est `true` ; sinon laisser le champ « À » vide.
3. **Commit + push `reviews/config.json`** : ce sont ces `drive_fichier` que les relèves
   (6h30 · 12h30 · 18h30, heure de Paris) lisent trois fois par jour.
4. Le CR habituel (`recap-semaine-*.md`, `whatsapp-semaine-*.md`) intègre le bilan de
   l'étape 1 et, pour chaque client, le **lien de son tableau** — aussi dans le message
   WhatsApp pour les clients en canal whatsapp.
5. **Ne JAMAIS envoyer automatiquement** : mails et messages partent en brouillon,
   Maxime relit et envoie.

## Ce que le client vit ensuite (pour répondre à ses questions)

Il reçoit le mail, ouvre son tableau, corrige les légendes dans les cases jaunes, choisit
✅ / ✏️ / ⛔, commente. Ses décisions sont appliquées automatiquement aux trois relèves
quotidiennes : les ✅ partent en publication automatique (retenus ⏳ si le visuel manque,
publiés dès qu'il est attaché), les ✏️ et ⛔ remontent dans le CR suivant. Une ligne sans
décision ne part jamais.
