---
name: review-vendredi
description: Agent Cowork du vendredi matin : prépare la review client de la semaine suivante (tableaux déposés dans le Drive de chaque client, brouillons Gmail), sans rien envoyer. Utilise-le le vendredi vers 8h ou quand Maxime dit « prépare la review » ou « les tableaux de la semaine prochaine ».
---

# Review client du vendredi

Remplace la routine cloud « Review, préparation du vendredi ». Même séquence, mais depuis le Mac,
avec le fichier local : plus de transcription base64 à travers le modèle.

## Avant

`cd ../CM-OTEA && git pull`. Lis `recaps/routine-cr-client.md` section VENDREDI, `reviews/config.json`
(dossier Drive permanent, archives, fichier courant par compte), `recaps/clients-config.json` (ton,
email confirmé), `recaps/modele-mail-review.md`.

## Séquence

1. Vérifier que `reviews/a-envoyer/<slug>-<lundi suivant>.xlsx` existe pour chaque compte actif
   (`actif` différent de false, et pas de `validation_auto`). Sinon déclencher le workflow GitHub
   « Review hebdo client » en mode `generer` et attendre le commit, puis `git pull`.
2. Lire les PR ouvertes qui touchent `reviews/config.json` ou `recaps/clients-config.json` : une
   décision de Maxime peut dormir dans une PR.
3. Pour chaque compte : déposer le xlsx dans son dossier Drive permanent avec le connecteur Drive
   (conversion en Google Sheet, titre « Validation hebdo, <Nom>, semaine du <JJ-MM> ») après avoir
   vérifié qu'un fichier de cette semaine n'y est pas déjà. Déplacer l'ancien fichier courant vers
   Archives (jamais de suppression). Vérifier qu'une permission « tous les utilisateurs disposant du
   lien » est héritée du dossier ; sinon le signaler.
4. Mettre à jour `drive_fichier` dans `reviews/config.json`, commit, push, PR fusionnée aussitôt
   (les relèves lisent `main` trois fois par jour).
5. Un brouillon Gmail par client, au ton du client, bouton vers le nouveau fichier et rappel du
   lien permanent. Destinataire rempli seulement si `email_confirme` est vrai.

## Interdits

Aucun mail envoyé. Aucun partage vers une adresse non confirmée. Aucune suppression de contenu
client. Pas de tiret cadratin.

## Rapport

Fichiers déposés (liens), brouillons prêts, relèves rouges de la semaine avec le compte et la cause,
points d'attention (fichier vide, partage à activer, visuels manquants).
