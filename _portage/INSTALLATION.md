# Portage du projet CM OTEA — état de la migration

Copie complète du projet au **02/08/2026**, puis **migration effectuée le
02/08/2026** dans l'environnement Claude Code (Linux). Ce fichier est le
compte rendu de ce qui a été réinstallé, de ce qui restait faux dans la note
d'origine, et de ce qui reste à faire à la main.

---

## 1. Ce qui a été réinstallé dans le repo ✅

| Élément | Où | Note |
|---|---|---|
| Fiches clients (11) + références transverses | `.claude/skills/cm-metricool/references/` | l'archive était **plus récente** que le git : 7 fiches mises à jour, 4 fichiers ajoutés (`confshine-game`, `compte-rendu-hebdo-clients`, `roi-clients`, `banques-photos`) |
| `PASSATION.md` | racine | état réel des 9 brands Metricool |
| `scripts/` | `carte-story.py`, `scan-medias.py` | **corrigé** (voir §4) |
| `recaps/medias-index.json` | `recaps/` | 240 médias indexés (4 clients) |
| `recaps/clients-config.json` | `recaps/` | la version du git avait perdu les blocs `medias_auto` |
| **Mémoires (7)** | `.claude/memories/` | **déplacées dans le repo** (voir §2) |
| **Tâche du lundi** | `.claude/taches-planifiees/recap-hebdo-publications/SKILL.md` | **chemins macOS corrigés** (voir §4) |
| `assets/fonts/` | `assets/fonts/README.md` | emplacement de repli des polices |

**Non inclus : le dossier `medias/` (1,5 Go).** Exclu par `.gitignore`. Voir §5.

---

## 2. Les mémoires — changement de méthode

La note d'origine demandait de copier `_portage/memoires/` vers
`~/.claude/projects/<projet>/memory/`. **C'est le mauvais endroit dans cet
environnement** : le conteneur est éphémère et remis à zéro entre les
sessions — les mémoires seraient reperdues au prochain démarrage, exactement
comme lors de cette migration.

Elles sont donc **versionnées dans le repo**, à `.claude/memories/`, et les
deux règles non négociables (brouillon obligatoire, zéro IA dans les stories)
sont rappelées directement dans `CLAUDE.md`, qui se charge à chaque session.

Les 7 mémoires :

| Fichier | Ce qu'il protège |
|---|---|
| `stories-vraies-photos-sans-ia.md` | **Règle n°1** : vraies photos animées, jamais de visuel IA, et le prompt i2v qui préserve les visages |
| `autonomie-decisions-cm.md` | Trancher sans demander, mais **toujours en brouillon** |
| `hebergement-photos-reelles-metricool.md` | Pipeline d'hébergement photo/vidéo + pièges |
| `bulk-schedule-stories-metricool.md` | Les code actions Metricool + le piège du PUT |
| `recap-hebdo-lundi.md` | La tâche du lundi 9h (interne + clients) |
| `detection-nouveaux-medias.md` | Scan SHA1 des dossiers clients |
| `otea-brand-identity.md` | Charte OTEA (#FF5800, Forma DJR, koru) |

---

## 3. Zapier, connecteurs et tâche planifiée

### 3a. Code actions Metricool — ✅ **elles ont survécu, rien à recréer**

La note d'origine annonçait qu'il fallait les réécrire. **C'est faux** : elles
vivent sur le compte Zapier, qui n'est pas lié au poste. Vérifié le 02/08/2026,
**21 actions Metricool actives**, dont les 5 annoncées manquantes :

| Action | Rôle | État |
|---|---|---|
| `bulk_schedule_stories` | stories en masse (brouillon, média, heure Paris) | ✅ |
| `bulk_replace_posts` | remplacer un post feed (crée en brouillon vérifié puis supprime) | ✅ |
| `bulk_delete_posts` | suppression en masse | ✅ |
| `list_brands` / `list_brands_direct` | autodécouverte des comptes | ✅ |
| `get_post_raw` | JSON brut d'un post (source de vérité) | ✅ |

Également présentes : `bulk_schedule_posts`, `bulk_set_draft`,
`bulk_update_post_times`, `list_scheduled_posts`, `schedule_post`…

⚠️ **`bulk_update_post_media` est toujours active alors qu'elle a été retirée
de la méthode** (le PUT `/scheduler/posts` répond 200 sans remplacer le média
et crée des doublons fantômes). Ne jamais l'appeler — passer par
`bulk_replace_posts` (créer + supprimer).

⚠️ **Reste à revalider par un test réel** : que `bulk_replace_posts` crée bien
en `draft:true` (le correctif `draft_verified` du 29/07). Le code s'exécute
côté Zapier et n'est pas lisible depuis ici — un post de test suffit à trancher.

### 3b. Connecteurs — ✅ branchés

Zapier MCP (Metricool) ✅ · Higgsfield ✅ (plan pro, 3 128 crédits) · Gmail ✅.

### 3c. Tâche hebdomadaire — ❌ toujours à créer

`.claude/taches-planifiees/recap-hebdo-publications/SKILL.md` est le prompt
complet de la tâche du lundi 9h. **Aucune Routine n'existe** (vérifié :
0 trigger). À créer en Routine serveur, cron `0 7 * * 1` (UTC = lundi 9h Paris
en été ; `0 8 * * 1` en heure d'hiver), connecteurs Zapier + Gmail.

Avantage de la Routine serveur sur l'ancienne tâche desktop : elle tourne même
application fermée — la note d'origine signalait cette limite.

---

## 4. Compatibilité multi-plateforme — corrigée

| Sujet | État |
|---|---|
| `ffmpeg` | ✅ installé (6.1.1) — testé : upscale 1080×1920 + overlay du calque texte + extraction de la dernière frame |
| Python + Pillow | ✅ installé (Pillow 12.3) — `carte-story.py` et `scan-medias.py` testés OK |
| Polices | ✅ DejaVu/Liberation présentes. Repli : déposer un `.ttf` dans `assets/fonts/titre.ttf` |
| **Bug police corrigé** | `carte-story.py` demandait `index=1` (le gras d'un `.ttc` macOS) — sur un `.ttf` Linux/Windows cela lève `OSError: invalid argument` et **le script plantait à chaque appel**. Un helper `charger_police()` tente l'index gras puis retombe sur l'index unique. |
| **Chemins macOS corrigés** | le prompt de la tâche du lundi contenait 5 chemins `/Users/oteaproduction/CM-OTEA/…` — passés en chemins relatifs au repo |
| `clients-config.json` | ✅ chemins déjà relatifs (`medias/<client>`) |

⚠️ Les cartes Gossip et Le Loft utilisaient **Didot** et **Baskerville**
(polices macOS). Ici elles retombent sur DejaVu : le rendu est correct mais
pas identique à l'original. Pour retrouver la DA exacte, déposer
Playfair Display / Libre Baskerville dans `assets/fonts/`.

---

## 5. Les médias (1,5 Go, non inclus)

Exclus du git par `.gitignore`. À copier séparément (disque externe, cloud) :

| Client | Poids |
|---|---|
| jlawson-golf | 568 Mo |
| pierre-huiban | 450 Mo |
| le-loft | 208 Mo |
| otea-production | 161 Mo |
| gossip-beauty-center | 104 Mo |
| la-galerie-immobiliere | 29 Mo |

`recaps/medias-index.json` référence **240 médias** (le-loft 21, jlawson-golf
107, otea-production 31, pierre-huiban 81), dont **128 en réserve**
(Le Loft 21 + J Lawson 107) = le vivier dans lequel la tâche du lundi puise.
**Sans le dossier `medias/`, l'étape 4 de la tâche du lundi ne peut rien
brancher** : c'est le prérequis n°1 pour relancer l'automatisation.

Les stories déjà produites sont hébergées publiquement (CloudFront) et
référencées dans Metricool : elles restent en ligne même sans le dossier local.
