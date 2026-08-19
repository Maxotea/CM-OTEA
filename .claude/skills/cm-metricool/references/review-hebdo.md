# La review hebdo client — fichier Excel ↔ Metricool

Chaque lundi, le client reçoit un fichier type Excel listant ses publications de la
semaine. Il corrige les légendes directement dans les cases, ajuste une heure, commente,
et décide ligne par ligne : ✅, ✏️ ou ⛔. Ses décisions sont relevées plusieurs fois par
jour et appliquées automatiquement dans Metricool — modifications poussées, puis passage
du brouillon à la **publication automatique**. Ce qu'il n'a pas validé ne part jamais.

## Le circuit (cycle vendredi → lundi, depuis le 19/08/2026)

| Quand (UTC) | Qui | Quoi |
|---|---|---|
| Vendredi 4h30 | Action « Carrousels hebdo » | plante le carrousel du mercredi SUIVANT |
| Vendredi 5h00 | Action « Review hebdo client » — job `generer` | lit les brouillons du lundi SUIVANT dans Metricool, écrit `reviews/a-envoyer/<client>-<lundi>.xlsx`, commit + artefact |
| Vendredi 6h00 | Routine Claude « Review — préparation du vendredi » | dépose chaque fichier dans le **dossier Drive permanent** du client (l'ancien part en `Archives/`), note l'identifiant dans `reviews/config.json`, prépare les brouillons Gmail |
| Lundi 6h00 | Routine Claude « Review — envoi du lundi » | envoie le mail (seulement si `envoi_review_auto` + `email_confirme`), sinon signale les brouillons à envoyer |
| En semaine | Le client | corrige, commente, décide — toujours au même lien (son dossier) |
| 4h30 · 10h30 · 16h30 | Action — job `appliquer` | relit chaque fichier par son export public, applique dans Metricool, journalise dans `reviews/etat/` |
| Lundi 7h00 | Routine Claude « CR client Publi Hebdo » | lit `reviews/etat/` pour le récap : parti, à corriger, refusé, bloqué |

Même partage des rôles que la chaîne photos : **la session fait la moitié authentifiée**
(connecteur Drive, récap Gmail), **l'action fait la moitié réseau** (Metricool, export
public du fichier). Aucune clé Google nulle part.

## Le fichier

Trois onglets : `Mode d'emploi` (client), `Semaine du JJ-MM` (la table), `_tech` (caché —
post_id, blog_id, horaire et texte d'origine ; c'est lui qui permet le rapprochement au
retour, ne jamais y toucher).

Colonnes de la table — seules les JAUNES sont éditables par le client :

| Colonne | Éditable | Contenu |
|---|---|---|
| Réf | non | `GBC-01`… — la clé de rapprochement affichée |
| Jour / Format / Réseaux | non | `Lun 10/08` · Post, Reel, Story, Carrousel (n visuels) · IG + FB |
| Heure | **oui** | `18:00` — tolère `18h`, `18 h 30`, une heure Sheets |
| Visuel | non | lien « voir le visuel », ou `⚠️ visuel à venir` |
| Légende | **oui** | le texte complet — le client corrige dans la case |
| Votre décision | **oui** | menu : `✅ OK pour publier` · `✏️ À corriger (voir commentaire)` · `⛔ Ne pas publier` |
| Votre commentaire | **oui** | libre |

Ce que fait `appliquer` de chaque décision :
- **✅** → légende/heure de la ligne poussées dans Metricool si modifiées, puis
  `draft: false, autoPublish: true` — le post part tout seul à l'heure dite ;
- **✏️** → aucun geste Metricool ; signalé avec le commentaire, à retravailler
  (réécrire → le brouillon corrigé repart dans la review suivante) ;
- **⛔** → aucun geste Metricool ; reste en brouillon, à retirer à la main —
  **jamais de suppression automatique** ;
- vide → rien. Un post sans décision ne part jamais.

## Côté sessions Claude — le vendredi et le lundi

La séquence opératoire complète des deux routines est dans `recaps/routine-cr-client.md`,
le modèle du mail dans `recaps/modele-mail-review.md`. Le détail technique :

1. **Vendredi** — vérifier que le job `generer` a tourné (sinon : workflow « Review hebdo
   client », mode `generer` — planifié, il vise le lundi suivant tout seul), puis
   `git pull` pour récupérer `reviews/a-envoyer/`.
2. Pour chaque client actif de `reviews/config.json` : déposer son fichier dans son
   **dossier permanent** (`drive_dossier`) via le connecteur Google Drive — `create_file`
   avec `base64Content` (le xlsx),
   `contentMimeType: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`,
   `parentId` = `drive_dossier`. Laisser la conversion par défaut : le fichier devient un
   **Google Sheet**, éditable au téléphone sans rien installer. Puis déplacer l'ancien
   `drive_fichier` vers `drive_archives` (`update_file`, champ `parentId`).
3. Le partage vit sur le **dossier**, réglé une fois pour toutes : « tous les
   utilisateurs disposant du lien : éditeur ». Tout fichier déposé dedans en hérite —
   lecture pour la relève (export public), écriture pour le client. Contrôle :
   `get_file_permissions` du nouveau fichier doit montrer une entrée `type: anyone`.
4. Écrire l'identifiant du nouveau fichier dans `reviews/config.json` → `drive_fichier`
   du client, commit + PR + merge dans la foulée. C'est **lui** que le workflow relit
   trois fois par jour ; un identifiant périmé est sans danger (semaine passée rejouée à
   vide), un identifiant absent = client non relevé.
5. Préparer le brouillon Gmail au ton du client (`recaps/clients-config.json`), sans
   pièce jointe (le client télécharge depuis le tableau : Fichier → Télécharger →
   Microsoft Excel).
6. **Lundi 6h00 UTC** — la routine d'envoi expédie le mail des comptes où
   `envoi_review_auto` ET `email_confirme` sont vrais (seule exception au « ne jamais
   envoyer automatiquement », décidée par Maxime le 19/08/2026) et liste les autres
   brouillons pour envoi manuel.
7. **Lundi 7h00 UTC** — le CR redescend `reviews/etat/*.json` : publiés, ✏️ à retravailler
   (avec les commentaires), ⛔ à retirer à la main, blocages (placeholders non complétés,
   média manquant), lignes retouchées sans décision.

## Retour par mail — la variante sans Drive

Le client préfère renvoyer le fichier par mail ? Déposer la pièce jointe telle quelle
dans `reviews/retours/` sous le nom `<slug>-<lundi>.xlsx`, commit + push : la prochaine
relève la traite exactement comme un fichier Drive. Les deux canaux cohabitent.

## Garde-fous

- Un ✅ sur un texte à placeholders (`[VAINQUEUR]`…) ou sur un post **sans média** est
  **retenu**, pas publié : l'accord du client reste acquis (`en_attente` dans le
  journal), la relève retente à chaque passage et publie dès que le texte est complété
  ou le visuel attaché dans Metricool. Rien d'autre à faire côté client.
- **La « mise à jour » de l'API Metricool crée une nouvelle entrée** (nouvel id, même
  uuid) et laisse l'ancien brouillon en place — constaté au premier test réel (OTEA,
  08/08/2026). Le script vérifie donc l'état réel du créneau avant et après chaque
  écriture : il ne ré-écrit jamais si la version publiable existe déjà (sinon double
  publication), et retire l'ancien brouillon devenu périmé une fois la nouvelle version
  confirmée. C'est le **seul** cas de suppression automatique, strictement borné à
  l'entrée périmée d'un post que le client vient de valider.
- Un post déjà validé directement dans Metricool (`autoPublish`) n'est jamais retouché —
  même règle que `publier.py` : ce que le client a validé lui appartient.
- Idempotence par `reviews/etat/<client>.json` : une décision déjà appliquée à
  l'identique n'est pas rejouée ; une décision **changée** (nouvelle légende, nouveau
  choix) est rejouée.
- Les ids Metricool changent quand un brouillon est recréé : le rapprochement retombe
  alors sur le **créneau horaire**, la même clé que `carrousels_existants` de
  `publier.py`. Un post déplacé hors de sa semaine est signalé, pas deviné.
- Première mise en route : lancer `appliquer` en `dry_run` et lire ce qui serait fait,
  comme pour les carrousels.

## Correspondance SOCIAL MEDIA CEO

Ce fichier EST l'étape `Validation client` du pipeline de contenu, côté client :
- ✅ = passage `Prêt à programmer / publier` → `Programmé / publié` ;
- ✏️ = refus de validation → retour `Rédaction` avec le commentaire ;
- ⛔ = le contenu sort du calendrier de la semaine (recyclage ou abandon, à trancher).
