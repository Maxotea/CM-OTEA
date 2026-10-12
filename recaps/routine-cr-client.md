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
| 7h00 | « Review hebdo client », job `generer` | un fichier par compte actif pour le lundi SUIVANT (et celui d'après pour un compte à `semaines_avance: 2`), commité dans `reviews/a-envoyer/` |

**Ne pas compter sur le cron du vendredi : il ne part pas.** Constaté le 09/10/2026 en
listant les runs — le `generer` planifié (`0 5 * * 5`) n'a pas déclenché une seule fois
depuis le 29/08, sept vendredis d'affilée ; c'est la routine qui le lance à la main chaque
semaine. Les relèves `appliquer` partent, mais 2 passages sur 3 seulement, et avec jusqu'à
cinq heures de retard. GitHub abandonne les déclenchements planifiés des dépôts peu actifs,
sans rien signaler. Donc : **la routine déclenche `generer` elle-même, dès l'étape 1, sans
attendre ni s'étonner.**

La séquence de la session (toujours commencer par `git pull`) :

1. **Lancer la génération** : déclencher « Review hebdo client » en mode `generer` (à la
   main, remplir `semaine` = le lundi visé) et attendre le commit, puis vérifier que
   `reviews/a-envoyer/<slug>-<lundi suivant>.xlsx` existe pour chaque compte actif de
   `reviews/config.json`.
   **Puis lire les PR ouvertes qui touchent `reviews/config.json` ou `recaps/clients-config.json`.**
   Leçon du 09/10/2026 : la PR #56, ouverte le 07/10 par une autre session, enregistrait
   deux décisions de Maxime (Pierre Huiban à deux semaines d'avance, OTEA Production et
   Otea Filmakers sortis du circuit des tableaux) — jamais mergée, donc absente de main, et
   la routine a préparé un tableau et un brouillon de mail pour un compte dont il avait dit
   ne plus vouloir de review. Une décision client peut dormir dans une PR ouverte ; `main`
   n'est pas la seule source de vérité le vendredi matin. Reprendre ce qui est réversible et
   ne publie rien ; laisser à Maxime ce qui lève une règle non négociable de CLAUDE.md.
   **Puis vérifier la santé des relèves de la semaine écoulée** : lister les runs de
   `review.yml` et lire les logs des jobs `appliquer` en échec. Le job sort en erreur dès
   qu'un seul compte est illisible — un compte dont le partage par lien n'est pas actif
   met donc tout le workflow au rouge à chaque passage, et personne ne regarde les Actions
   au fil de l'eau. C'est ici, une fois par semaine, que ce voyant se lit ; toute relève
   rouge va dans le rapport final avec le compte et la cause.
2. **Pour chaque client actif** :
   - Déposer son xlsx dans son dossier permanent : `create_file` avec `parentId` =
     `drive_dossier`, `base64Content` du xlsx, `contentMimeType` xlsx, conversion par
     défaut (le fichier devient un Google Sheet, éditable au téléphone). Titre :
     « Validation hebdo — <Nom> — semaine du <JJ-MM> ».
     **Avant de déposer, vérifier qu'un fichier de la semaine visée n'est pas déjà dans
     le dossier** (`search_files` sur le titre) : un tableau peut avoir été préparé à
     l'avance, à la demande de Maxime. Dans ce cas, ne pas en déposer un second —
     reprendre l'identifiant existant pour la suite de la séquence.
     **Après dépôt, relire le tableau déposé** (`read_file_content`) et compter ses lignes
     contre le xlsx source. Le base64 long se corrompt à l'émission : jusqu'ici l'API Drive
     a toujours refusé le résultat (« Invalid conversion requested »), mais une perte qui
     laisserait par chance un zip valide passerait sans bruit et déposerait un tableau
     tronqué chez le client. La relecture est le seul contrôle qui ferme ce trou.
   - Déplacer l'ancien fichier (le `drive_fichier` actuel) vers `drive_archives` :
     `update_file` avec `parentId` = `drive_archives`. Ne JAMAIS le supprimer.
   - Noter le nouvel identifiant dans `reviews/config.json` → `drive_fichier`.
   - **Compte à deux semaines d'avance** (`semaines_avance: 2`, Pierre Huiban depuis le
     05/10/2026) : deux fichiers générés, lundi suivant (S+1) et lundi d'après (S+2).
     S+1 est normalement déjà dans le dossier depuis le vendredi précédent, peut-être
     déjà coché par le client : le garder tel quel, ne déposer que S+2. Archiver
     uniquement le fichier de la semaine qui se termine. `drive_fichiers` devient
     `[id S+1, id S+2]`. Le brouillon de mail donne les deux liens.
   - Préparer le **brouillon Gmail** depuis `modele-mail-review.md`, au ton du client
     (`clients-config.json` → `ton`). Le bouton pointe vers le **fichier de la semaine**,
     et le mail rappelle que le **dossier** est le même lien chaque semaine. Destinataire :
     uniquement si `email_confirme` est `true` ; sinon champ « À » vide.
3. **Commit + push + PR + merge de `reviews/config.json`** : les relèves (6h30 · 12h30 ·
   18h30, heure de Paris) lisent le `drive_fichier` (ou les `drive_fichiers`) de main plusieurs fois par jour —
   la mise à jour doit être mergée dans la foulée.
4. **Vérifier la lisibilité** : `get_file_permissions` sur le nouveau fichier doit montrer
   une permission `type: anyone` (héritée du dossier). Si elle manque, le partage du
   dossier n'est pas actif — le signaler à Maxime, c'est UN réglage à faire une fois.
5. Terminer par un rapport court : fichiers déposés, brouillons prêts, points d'attention
   (créneaux déjà passés, visuels manquants, partage à activer).

## LUNDI — routine « Review — envoi du lundi » (8h00 Paris été)

1. `git pull`, lire `reviews/config.json` et `clients-config.json`.
2. Pour chaque client actif de la review :
   - `envoi_review_auto` **et** `email_confirme` vrais → **envoyer le brouillon du
     vendredi lui-même** : `send_message` avec son `draftId`, rien d'autre. Le client
     reçoit exactement ce qui a été relu vendredi, et le brouillon disparaît de la liste
     du même coup — pas de recomposition, pas de mise à la corbeille. Ne recomposer
     depuis `modele-mail-review.md` que si le brouillon a disparu ; contrôler alors que
     le lien pointe bien sur le `drive_fichier` courant.
   - Sinon → ne rien envoyer : **recomposer le brouillon lundi matin** et le lister dans
     le rapport comme « à envoyer par Maxime ».

**Les brouillons du vendredi ne passent pas le week-end.** Vérifié lundi 12/10/2026 :
les deux brouillons écrits le vendredi 09/10 avaient disparu de Gmail, et rien dans les
messages envoyés — ni envoyés, ni en attente. Même constat le vendredi 09/10 sur la série
du lundi 05/10 (`list_drafts` vide, `in:sent newer_than:6d` vide). C'est le sort de chaque
série depuis le 31/08. Le cycle « écrire vendredi, envoyer lundi » ne tient donc pas : c'est **lundi
matin** qu'il faut écrire le brouillon, quelques heures avant qu'il serve, et non trois
jours avant. Le vendredi reste le moment du tableau et de la config ; le mail se compose
le lundi. Un brouillon du vendredi encore présent le lundi est un bonus, pas une base.
3. C'est la SEULE exception à la règle « ne jamais envoyer automatiquement », décidée par
   Maxime le 19/08/2026 et bornée par les deux drapeaux de `clients-config.json`.

**La routine du vendredi vérifie que celle du lundi tourne encore.** Constaté le
18/09/2026 : la routine d'envoi était désactivée depuis le 31/08 sans que rien ne le
signale, et trois lundis sont passés sans qu'aucun mail parte — y compris l'envoi
automatique d'Otea Filmakers. Les brouillons s'étaient empilés, dix au total, sans que
leur nombre alerte personne. Le vendredi, donc : lister les Routines, vérifier que
« Review — envoi du lundi » est `enabled` et que son `last_fired_at` tombe bien sur le
lundi précédent. Une routine désactivée se signale à Maxime — elle ne se réactive pas
toute seule, c'est sa décision.

**Mise à jour du 12/10/2026 : le risque qui justifiait cette prudence a disparu.** La
raison invoquée jusqu'ici — « la réactiver ferait partir un mail client dès le lundi
suivant » — ne tient plus : le seul compte en `envoi_review_auto` était Otea Filmakers,
qui est passé en `validation_auto` et sorti du circuit des tableaux le 07/10. Plus aucun
compte actif n'est en opt-in d'envoi. Réactivée aujourd'hui, la routine du lundi
n'enverrait donc **rien** automatiquement : elle se contenterait d'écrire les brouillons
et de les lister pour Maxime. Son prompt est en revanche périmé sur deux points (il nomme
Otea Filmakers comme l'opt-in, et il lit `drive_fichier` sans `drive_fichiers`) : à
rafraîchir avant de la rallumer. Sept lundis sont passés sans mail au 12/10 — 31/08,
07/09, 14/09, 21/09, 28/09, 05/10, 12/10.

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
