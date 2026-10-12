---
name: cm-metricool
description: Workflow complet de community management multi-comptes — génère un calendrier éditorial calé sur l'actualité et la saisonnalité du secteur d'un client, écrit les légendes, et planifie les posts en brouillon dans Metricool via Zapier. Utilise ce skill dès que l'utilisateur demande de planifier, programmer ou publier du contenu, de créer/mettre à jour un calendrier éditorial, de réagir à un événement du secteur (tournoi, salon, fête, sortie produit), ou mentionne Metricool ou l'un de ses comptes clients (J Lawson Golf, Le Loft, Gossip Beauty Center, La Galerie Immobilière, Otea), même s'il ne dit pas explicitement "calendrier" ou "Metricool".
---

# CM Metricool — calendrier éditorial automatisé multi-comptes

## Étape 0 — Détection des nouveaux comptes & routine hebdomadaire

**À CHAQUE session utilisant ce skill** : commencer par `list_brands_direct` et comparer aux marques connues (tableau Étape 1). Si une marque inconnue apparaît → lancer l'ONBOARDING avant toute autre chose :
1. Poser les questions (via ask_user_input quand pertinent) : secteur/typologie du client ? saisonnalité et événements clés du secteur ? site web (pour vérifier les prix des services → ROI) ? banque photos disponible ? ton de marque ? prestation CM mensuelle facturée ?
2. Rechercher sur le web l'actu et le calendrier événementiel du secteur.
3. Générer 3 mois (~13 semaines) de posts en brouillon via `bulk_schedule_posts` (cadence lundi/mercredi/vendredi + déclencheurs événements).
4. Créer la fiche du client dans `references/clients/` en dupliquant `_template-nouveau-client.md`, la remplir, et mettre à jour la mémoire.

**Routine hebdomadaire** (déclenchée par « routine hebdo » ou équivalent — un rappel récurrent du lundi existe sur le téléphone de l'utilisateur) :
0. **Le carrousel du mercredi de chaque compte est-il écrit, rendu et planifié ?** C'est le premier point de la routine, avant l'horizon : un carrousel manquant se voit dans le fil, un trou à la semaine 12 non. Voir `references/carrousels-hebdo.md`.
1. Pour CHAQUE marque : `list_scheduled_posts` sur les 14 prochaines semaines → mesurer l'horizon couvert.
2. **Repérer les suppressions** en comparant avec ce qui avait été planifié : photo retirée d'un brouillon, ou brouillon disparu = un refus de l'utilisateur → appliquer les « Règles de recréation après suppression » ci-dessous.
3. Compléter pour revenir à ~13 semaines d'avance (générer la ou les semaines manquantes avec l'actu fraîche du secteur, vérifiée par recherche web).
4. Compléter les placeholders des événements du week-end écoulé ([VAINQUEUR], [RÉSULTAT]…) : rechercher le résultat réel, fournir le texte final, supprimer/recréer le brouillon concerné.
5. **Review client** : le cycle est automatisé depuis le 19/08/2026 — le vendredi matin, l'action « Review hebdo client » génère les fichiers de la semaine suivante et la routine « Review — préparation du vendredi » les dépose dans le dossier Drive permanent de chaque client (`reviews/config.json`) ; le mail se compose le lundi matin (les brouillons du vendredi ne passent pas le week-end) et part si opt-in ; le CR redescend `reviews/etat/` (publiés, à corriger, refusés, en attente). Séquence complète : `recaps/routine-cr-client.md` ; détail technique : `references/review-hebdo.md`.
6. Rendre compte : posts ajoutés par compte, placeholders complétés, photos à attacher, contenus recréés après suppression.
7. **Veille trends** : rechercher sur le web les trends/formats/sons de la semaine (Instagram Reels, TikTok), filtrer celles adaptables à chaque compte sans dénaturer la marque, et proposer 1-2 adaptations concrètes par compte (script via reel-script). Voir `references/bonnes-pratiques-cm.md`.

**Capture de trend à tout moment** : quand l'utilisateur signale une trend (message, vocal transcrit, lien, description), immédiatement : 1) l'évaluer avec les critères de bonnes-pratiques-cm.md, 2) proposer son adaptation pour chaque compte pertinent (script/légende prêts), 3) planifier les posts validés via bulk_schedule_posts dans la semaine (les trends se périment en jours), 4) si c'est un enseignement durable (« ce format marche »), l'ajouter à la mémoire et aux bonnes pratiques.

## Vue d'ensemble du flux

Idée / événement → actu vérifiée (web) → légende + script → photo réelle de la banque (ou IA en dernier recours) → brouillon Metricool daté → l'utilisateur attache le média et valide.

## Étape 1 — Identifier la marque

Les outils Metricool passent par Zapier. Toujours appeler `Zapier:list_enabled_zapier_actions` d'abord, puis l'action `code_action_metricoolcliapi__list_brands_direct` pour obtenir les blogId à jour. Marques connues (juillet 2026) :

| Marque | blogId | Réseaux | Secteur |
|---|---|---|---|
| jlawsongolf | 6563137 | Instagram, Facebook | Fitting de clubs de golf |
| LE LOFT | 6191921 | Instagram | Barbier |
| ~~Gossip Beauty Center~~ | ~~5733306~~ | | **DÉSACTIVÉ le 28/08/2026** : ne rien produire ni programmer sans un feu vert explicite de Maxime |
| La Galerie Immobilière | 5733302 | IG, FB, TikTok | Immobilier |
| OTEA PRODUCTION | 5733269 | IG, FB, TikTok, YT, LinkedIn | Production vidéo |
| Otea Filmakers | 4728418 | IG, FB, TikTok, LinkedIn | Production vidéo |

## Étape 2 — Actu et saisonnalité du secteur (JAMAIS de mémoire)

Toujours vérifier par recherche web avant d'écrire : dates réelles des événements, vainqueurs/gagnants récents, sorties produits. Exemples par secteur : golf → majeurs (Masters avril, PGA mai, US Open juin, The Open juillet), WITB des vainqueurs, sorties matériel janv-mars ; beauté → fêtes (Saint-Valentin, fête des mères), saisons (été/soleil, hiver/hydratation), tendances ; immobilier → rentrée, printemps (pic d'achats), taux ; barbier → Movember, fêtes, rentrée.

## Étape 3 — Structure éditoriale (commune à tous les comptes)

5 piliers : P1 pédagogie métier (30%), P2 actu secteur (25%), P3 coulisses (20%), P4 saisonnalité client (15%), P5 preuve sociale (10%). Cadence : 3 posts feed/semaine (lundi P2, **mercredi carrousel**, vendredi P5/P4) + stories. Semaine d'événement majeur : 4-5 posts.

**Le mercredi est un carrousel, sur tous les comptes, toutes les semaines.** Il remplace le post feed du mercredi, il ne s'y ajoute pas : le volume mensuel et donc le palier vendu ne bougent pas. C'est le format qui produit le plus de sauvegardes et de partages. Structure, archétypes, adaptation à la typologie et à la cible, méthode de planification : `references/carrousels-hebdo.md`. Les specs vivent dans `carrousels/<client>/`, le rendu se fait avec `scripts/carrousel.py`.

Déclencheurs automatiques :
- **J-7 avant événement** → post/reel preview
- **J+1 après événement** → post réaction (ex. WITB du vainqueur pour le golf) — créer le brouillon À L'AVANCE avec des placeholders [VAINQUEUR], [STAT] à compléter le jour J
- **J+2** → carrousel débat/stat
- **Saisonnier récurrent** → campagnes fixes (reprise, cadeaux, etc.)

## Étape 4 — Visuels : hiérarchie stricte pour chaque publication

Les **carrousels du mercredi** ne suivent pas cette hiérarchie : leurs slides sont typographiques et générées par `scripts/carrousel.py` à partir de la DA du compte (`scripts/themes.json`). Voir `references/carrousels-hebdo.md`. La banque photos reste réservée aux posts simples et aux reels — c'est aussi ce qui la préserve de l'épuisement.

Pour CHAQUE post simple non-reel, choisir le visuel dans cet ordre :

1. **Galerie du client d'abord** : photo de la banque classée par pilier (voir la fiche du client dans `references/clients/`), en rapport avec le texte. Rotation : pas de réutilisation à moins de 30 jours. Limite API : les photos locales n'ont pas d'URL publique → créer le post en brouillon et indiquer à l'utilisateur le fichier exact à attacher.
2. **Photo trouvée si la galerie ne couvre pas le sujet** (événement externe, lieu, produit) : chercher via image_search/web une photo en rapport avec le texte, en privilégiant les sources libres de droits ou officielles (banques d'images libres, communiqués/press kits des marques) — jamais de photo de presse/agence protégée (Getty, AFP) pour un compte commercial. Avantage : une photo en ligne a une URL publique → elle peut être attachée directement au `schedule_post` (post planifié complet, plus besoin de brouillon). Toujours montrer la photo choisie à l'utilisateur dans la réponse.
3. **IA (Higgsfield) en tout dernier recours** : uniquement si rien d'existant ne convient (concepts abstraits, schémas pédagogiques). Utiliser l'élément de référence de la marque (ex. J Lawson Golf : élément "JLawson-Studio", rendu tech premium moderne, PAS de bois, métal noir mat, LED avec accent chaud, bleu marine et vert, launch monitor en fond). Une photo supprimée ensuite par l'utilisateur = refusée : en recréer une plus réaliste (voir « Règles de recréation après suppression »).

Les reels restent tournés avec de vraies vidéos (script reel-script + B-roll listé depuis la banque).

**Stories : format figé.** Une story se produit toujours de la même façon, sur
tout compte qui a de vraies photos : vraie photo du client recadrée 9:16 dans
PIL, animée en i2v caméra verrouillée (`kling3_0_turbo`, 5 s, 7,5 crédits),
composée **plein cadre 1080×1920** avec le texte incrusté en ffmpeg par-dessus,
**muette**, branchée en brouillon puis vérifiée à `audit_publication_safety`.
Jamais une carte typographique seule, jamais une photo de banque, jamais une
vidéo logée dans une vignette, jamais un `zoompan` seul. Process complet et
pièges mesurés : `.claude/memories/story-video-plein-cadre.md`.

## Étape 5 — Écriture

Scripts de reels : relire d'abord `references/inspirations-montage.md` (les styles de montage repérés par Maxime, à reprendre en priorité), puis passer par le skill `reel-script` (hook chiffré, 3 étapes, cliffhanger, ≤175 mots), puis `reel-lint` avant tournage. Légendes : hook + valeur + 1 seul CTA + 4-6 hashtags niche. Toujours finir la légende par le pont vers l'offre du client (fitting, RDV, visite…).

## Étape 6 — Planification Metricool

**Carrousel** : un carrousel = un seul appel `schedule_post` avec les slides dans `media01` … `media08`, DANS L'ORDRE (l'ordre des paramètres est l'ordre d'affichage). `bulk_schedule_posts` ne gère pas les médias et ne convient donc pas. Penser à supprimer le post feed déjà planifié ce mercredi-là, que le carrousel remplace. Procédure complète : `references/carrousels-hebdo.md`.

**Création en masse (préférée dès 3+ posts)** : code action personnalisé `code_action_metricoolcliapi__bulk_schedule_posts` (params : blog_id, posts = chaîne JSON `[{"date_time":"YYYY-MM-DDTHH:mm:ss","text":"...","type":"POST|REEL"}]`) — crée directement en brouillon (draft true, autoPublish false), Instagram+Facebook, fuseau Europe/Paris natif SANS bug horaire. C'est la méthode par défaut pour un calendrier.

**Création unitaire** via `Zapier:execute_zapier_write_action`, action `schedule_post` :
- `blogId` de la marque, réseaux de la marque à true, `type` POST/REEL/STORY
- **`draft: true` + `autoPublish: false` OBLIGATOIRES** si le média n'est pas attaché (l'API exige une URL publique pour les médias — les photos locales du client ne peuvent pas être attachées par l'API, l'utilisateur les ajoute dans Metricool) ou si la légende contient des placeholders
- Horaires par défaut : reels 9h00 ou 12h00, posts feed 18h00, heure de Paris, format `YYYY-MM-DDTHH:mm:ss`
- Si Zapier renvoie une followUpQuestion demandant des URLs de médias : ré-exécuter en précisant dans instructions que le brouillon est créé SANS média (ajout manuel ensuite)
- **⚠️ Bug de fuseau horaire connu** : `schedule_post` décale les heures de plusieurs heures. Après toute création de posts, TOUJOURS vérifier avec `code_action_metricoolcliapi__list_scheduled_posts` (params blogId, start, end) puis corriger avec le code action personnalisé `code_action_metricoolcliapi__bulk_update_post_times` (params : blog_id, updates = chaîne JSON `[{"post_id":123,"date_time":"YYYY-MM-DDTHH:mm:ss"}]` en heure de Paris). ATTENTION : cette correction fait sauter le statut brouillon → enchaîner OBLIGATOIREMENT avec `code_action_metricoolcliapi__bulk_set_draft` (params : blog_id, post_ids = chaîne JSON `[123,456]`) pour re-verrouiller les brouillons. Noter que les IDs des posts changent après correction.
- Après chaque brouillon créé, lister à l'utilisateur : date, contenu, média à attacher, placeholders à compléter

## Étape 7 — Boucle post-événement

Le lendemain d'un événement : rechercher le résultat réel sur le web, donner à l'utilisateur le texte final complété. Pour éditer un brouillon existant : supprimer/recréer via schedule_post (le texte n'est pas éditable directement), ou utiliser les code actions personnalisés pour la date et le statut brouillon.

## Validation client — la review hebdo (fichier Excel ↔ Metricool)

Le client valide sa semaine dans un fichier type Excel déposé chaque vendredi dans son
dossier Drive permanent (toujours le même lien pour lui) ; le mail part le lundi matin.
Il corrige les légendes dans les cases, choisit ✅ / ✏️ / ⛔ par ligne ; ses décisions sont
relevées trois fois par jour par l'action « Review hebdo client », qui pousse les
modifications dans Metricool et passe les ✅ en publication automatique. Un post sans
décision ne part jamais ; jamais de suppression automatique. Rôle des routines du
vendredi et du lundi (dépôt Drive, `reviews/config.json`, envoi opt-in, exploitation de
`reviews/etat/` dans le récap) et garde-fous : `references/review-hebdo.md`.

## Règles de recréation après suppression — une suppression est un feedback

Les brouillons sont relus par l'utilisateur directement dans Metricool : une suppression n'est jamais un accident, c'est un refus à interpréter — pas besoin de demander pourquoi. Deux règles :

1. **La photo d'une publication a été supprimée** (le brouillon existe encore, mais son média a disparu) → la photo ne convenait pas : **en recréer une plus réaliste** pour le même brouillon. Repasser par la hiérarchie de l'Étape 4 (vraie photo de la banque d'abord) ; si le visuel refusé était généré par IA, régénérer en gommant ce qui fait artificiel — lumière naturelle, cadrage type smartphone, textures imparfaites, pas de rendu lisse « publicité » — puis indiquer le nouveau fichier à attacher (ou attacher directement si URL publique).
2. **Un post a été totalement supprimé** (il n'apparaît plus dans `list_scheduled_posts` alors qu'il avait été planifié) → le texte n'allait pas : **en réécrire un nouveau** sur le même créneau. Changer d'angle et de hook — pas une simple reformulation de la légende refusée.

Dans les deux cas : recréer sans attendre (le créneau reste dû au calendrier) et signaler dans le compte-rendu ce qui a été recréé et pourquoi.

## Étape 8 — Calcul ROI pour le client (justifier la prestation)

Objectif : montrer au client combien de ventes/prestations générées par les réseaux suffisent à rembourser la prestation CM mensuelle. À produire à chaque bilan mensuel, proposition commerciale ou renégociation.

Méthode :
1. **Trouver le prix réel des services du client** — toujours vérifier sur son site officiel ou par recherche web (voir la fiche du client dans `references/clients/` pour les tarifs déjà vérifiés). Ne jamais inventer un prix.
2. **Seuil de rentabilité** = prix de la prestation CM mensuelle ÷ prix moyen du service. Exprimer en langage client : « X séances/ventes par mois venues des réseaux et la prestation est remboursée ».
3. **Adapter à la typologie du client** :
   - Service unitaire cher, faible récurrence (fitting golf, mandat immobilier, projet vidéo) → raisonner en nombre de ventes : souvent 1 à 4 conversions suffisent. Pour l'immobilier, une seule commission de vente couvre généralement des mois de prestation.
   - Service récurrent moins cher (barbier, institut de beauté) → raisonner en **valeur vie client (LTV)** : un client acquis revient (ex. coupe tous les mois) — 1 nouveau client fidélisé = prix unitaire × 12 par an. Compter les nouveaux clients acquis, pas les tickets.
4. **Présenter toujours 2 chiffres** : le seuil de rentabilité (combien pour rembourser) et le scénario réaliste (avec les stats Metricool réelles : reach, clics, DM → estimation de conversions), pour rester honnête et crédible.
5. Format de sortie : tableau simple ou visuel carrousel « Ce que vous coûte le CM vs ce qu'il rapporte », adapté au vocabulaire du secteur du client.
