# Metricool en direct : quel chemin pour quelle action

Décision de Maxime du 18/11/2026 : on sort Metricool de Zapier pour arrêter de payer à
l'action. Zapier compte 2 tâches par appel, même pour une simple lecture, et un mois de
dépassement a coûté 116,14 € à l'été 2026 (remboursés une fois, pas deux).

## Les trois chemins, dans l'ordre de préférence

| Chemin | Coût | Pour quoi |
|---|---|---|
| **1. Connecteur Metricool direct** (outils `Metricool_Social_Media_Management`) | gratuit | lister les marques, lire les posts programmés, créer un post, modifier un post |
| **2. `scripts/publier.py`** (API Metricool, lancé par l'action GitHub) | gratuit | les carrousels du mercredi, voir `carrousels-hebdo.md` : rien ne change |
| **3. Zapier** (actions `MetricoolCLIAPI`) | 2 tâches par appel | seulement ce que les deux premiers ne savent pas faire, liste ci-dessous |

Règle : on essaie toujours le chemin 1. On ne passe par Zapier que pour une action de la liste
« Ce qui reste sur Zapier », et on le dit dans le compte rendu.

## Chemin 1 : les quatre outils

| Besoin | Outil direct | Remplace sur Zapier |
|---|---|---|
| Lister les marques et leurs blogId | `getBrandSettings` | `list_brands_direct`, `list_brands` |
| Lire les posts programmés d'une marque | `getScheduledPosts` (brandId, fromDate, toDate, timezone `Europe/Paris`) | `list_scheduled_posts`, `summarize_scheduled_posts`, `dump_post_texts`, `get_post_raw` |
| Créer un post, un reel ou une story | `createScheduledPost` | `schedule_post`, `schedule_post_direct`, `bulk_schedule_posts`, `bulk_schedule_stories`, `bulk_schedule_posts_media` |
| Modifier la légende ou l'heure d'un post | `updateScheduledPost` | `update_post_text_only`, `retext_posts`, `update_post_datetime`, `bulk_update_post_times`, `bulk_set_draft` |

### Gabarit de création (toujours en brouillon)

`createScheduledPost` prend `blogId`, `date` (ISO avec décalage, ex. `2026-12-30T10:00:00+01:00`)
et `info`, une chaîne JSON :

```json
{
  "autoPublish": false,
  "draft": true,
  "descendants": [],
  "firstCommentText": "",
  "hasNotReadNotes": false,
  "media": ["https://URL-publique-du-visuel.jpg"],
  "mediaAltText": [],
  "providers": [{"network": "instagram"}],
  "publicationDate": {"dateTime": "2026-12-30T10:00:00", "timezone": "Europe/Paris"},
  "shortener": false,
  "smartLinkData": {"ids": []},
  "text": "",
  "instagramData": {"type": "STORY"}
}
```

- `providers` : un bloc par réseau de la marque, et le bloc de données correspondant
  (`instagramData`, `facebookData`, `tiktokData`, `linkedinData`), vide si rien à préciser.
- `instagramData.type` : `POST`, `REEL` ou `STORY`. `facebookData.type` : `POST`, `REEL` ou `STORY`.
- `media` : des adresses publiques. Metricool recopie le fichier chez lui à la création.
- Une story n'a pas de légende : `text` vide quand le post ne contient que des stories.
- Pas de bug de fuseau : demandé 10h00 à Paris, planifié 10h00 à Paris.

### Les règles qui ne bougent pas

1. **`draft: true` et `autoPublish: false` à chaque création.** Les exceptions de relève
   automatique décrites dans `.claude/memories/autonomie-decisions-cm.md` restent celles de ce
   fichier, pas d'autres. Seul cas à part : le reel Instagram, programmé en notification selon
   `.claude/memories/reels-musique-instagram.md`.
2. **Relire après chaque création** avec `getScheduledPosts` sur le jour concerné et vérifier
   trois choses : `draft` vaut `true`, l'heure est la bonne, le nombre de médias est le bon. Un
   post qui n'est pas en brouillon se corrige tout de suite avec `updateScheduledPost` et se
   signale à Maxime.
3. **`updateScheduledPost` remplace le post entier** : repartir du contenu relu par
   `getScheduledPosts`, ne changer que le champ voulu. L'`id` change après la mise à jour,
   l'`uuid` reste.
4. **Changer un visuel ne passe jamais par une mise à jour** : Metricool garde l'ancien média ou
   recrée un doublon. On remplace puis on supprime, voir Zapier ci-dessous et
   `.claude/memories/bulk-schedule-stories-metricool.md`.
5. **Pas de création par lot en direct** : un appel par post. C'est plus lent que le lot Zapier,
   mais gratuit. Créer le premier, le relire, puis enchaîner.

### Ce qui est vérifié, ce qui ne l'est pas encore

- Vérifié le 18/11/2026 sur Otea Filmakers : story Instagram en brouillon avec une image,
  heure de Paris exacte, média recopié par Metricool, relecture `draft: true`, puis suppression.
- Pas encore vérifié en direct : un reel vidéo, un post sur plusieurs réseaux à la fois, un
  carrousel de plusieurs visuels, une modification de légende. Au premier usage de chacun :
  créer un seul post, le relire en entier, et seulement ensuite continuer. En cas d'échec,
  revenir à l'action Zapier habituelle et noter ici ce qui a cassé.

## Ce qui reste sur Zapier (en attendant Make)

Le connecteur direct ne sait ni supprimer ni contrôler. Ces actions restent donc sur Zapier,
2 tâches par appel :

| Besoin | Action Zapier |
|---|---|
| Supprimer un ou plusieurs posts | `delete_post`, `bulk_delete_posts` |
| Changer le visuel d'un post (créer le remplaçant en brouillon, supprimer l'ancien) | `bulk_replace_posts` |
| Contrôle de sécurité : rien en publication automatique, rien sans média | `audit_publication_safety` |
| Envoyer une image qui n'a pas d'adresse publique | `schedule_story_b64`, `upload_image_attach_post`, `attach_image_from_url` |
| Passer un lot de brouillons en notification | `bulk_set_autopublish` |

Pour limiter la dépense : regrouper les suppressions dans un seul `bulk_delete_posts`, et faire
un seul `audit_publication_safety` à la fin d'une session, sur tous les comptes à la fois.

Ces actions sont de simples appels à Metricool. La suite du chantier est de les refaire dans
Make (abonnement gardé, 54 $ par an), puis de repasser Zapier en gratuit. Tant que ce n'est pas
fait, Zapier reste branché : ne pas supprimer ses actions.
