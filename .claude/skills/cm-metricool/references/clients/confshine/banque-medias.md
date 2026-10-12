# ConfShine — banque médias

État au 04/08/2026. Inventaire relevé via le connecteur Google Drive.

## Le dossier de référence

**`Mon Drive / CM-OTEA / medias / CONFSHINE RS`**
→ https://drive.google.com/drive/folders/1ZAotuUDLNSUPW5QlrlGNTChoofttUX6K
Créé le 04/08/2026 par contact@oteaproduction.com. C'est le point d'entrée médias
ConfShine pour les réseaux sociaux.

Il ne contient pas de fichiers en propre : **deux raccourcis** vers les dossiers
sources. ⚠️ L'API Drive n'expose pas la cible d'un raccourci — les rattachements
ci-dessous sont déduits des noms et restent **à vérifier d'un clic** dans Drive.

| Raccourci | Cible probable |
|---|---|
| `CONFSHINE` | dossier partagé par **contact@podmax.fr** — les rushes de tournage |
| `CONFSHINE GBO Gatsby 28 juin 26` | dossier partagé par **confshine@gmail.com** — événement du 28/06/2026 |

## 1. Rushes de tournage (partagé par PodMax)

https://drive.google.com/drive/folders/12Or0dYjm9_giZEIfyoOOrdUUCVSFJbQy

Trois sessions, même arborescence `tournage / b-roll / audio` :

| Session | Date des rushes | Contenu relevé |
|---|---|---|
| `01` | 28/07/2026 | tournage : 3 caméras `.mp4` (9,4 à 9,7 Go chacune) + `MIC 1 .wav` · b-roll · audio |
| `02` | 28/07/2026 | tournage : 3 caméras `.mp4` (7,2 à 7,4 Go) · b-roll · audio |
| `03` | 03/08/2026 | tournage : 3 caméras `.mp4` (12,6 à 13 Go) · b-roll : ~10 `.MP4` C72xx (0,1 à 2,5 Go) · audio : `Track2-Combo`, `Track3-Combo` `.wav` |

Tous les fichiers caméra sont nommés **« Hermann Deckous [date] CAM 1/2/3 01 »**.
⚠️ À confirmer : Hermann Deckous est bien l'intervenant / le porteur de ConfShine,
et ces rushes sont exploitables sur les réseaux (droit à l'image, accord PodMax).

`BROLL IPHONE` (https://drive.google.com/drive/folders/1tZmxUYDctaNRlcDNlYpqxcQ7CbwOpv8z)
— une soixantaine de fichiers iPhone bruts (`.HEIC` 1,3–3,3 Mo et `.MOV` 19–354 Mo),
captés les 28/07 et 03/08. C'est le seul lot directement **photographique** utilisable.

## 2. Charte et assets de marque

Dossier OTEA `CONFSHINE` (hors `CONFSHINE RS`, à ne pas confondre) :
https://drive.google.com/drive/folders/1_AxHXeoeQ633psEMd7qWI73lsQLVBvlw

- `Confshine_Game_Univers_Mentors_charte2026` — charte 2026 (Slides + PDF, plusieurs versions, la plus récente au 28/07 09:45)
- `Confshine_Game_Gabarits_reseaux.pdf` — **gabarits réseaux sociaux** : à lire avant tout visuel
- `CONFSHINE WEB- PISTE GRAPHIQUE.pdf` — piste graphique web
- `planche illustrations ConfShine.ai` + logos PNG (violet, blanc), `trefle vert Confshine.png`
- `Confshine_Game_Kit_de_collecte_mentors` (Doc), `Confshine_Univers_Mentors` (Slides)

## 3. Événement Gatsby du 28/06/2026

https://drive.google.com/drive/folders/1y-RC5C81tFfTfJKoPg3XmtSFEn0rntw-
Partagé par confshine@gmail.com. **Le contenu ne remonte pas via le connecteur**
(restriction de partage probable) — à ouvrir manuellement pour inventaire.

## Ce que ça veut dire pour la production

- **Rien n'est prêt à publier en l'état.** Les rushes sont des masters multi-caméras
  de 7 à 13 Go : ils passent par un dérushage et un export vertical avant tout post.
- Le b-roll iPhone (`.HEIC` / `.MOV`) doit être **converti** (HEIC → JPG, MOV → MP4)
  et redimensionné avant envoi : Metricool ne prend pas le HEIC.
- Pour attacher un média à un post Metricool, même méthode que Pierre Huiban :
  redimensionner en local → héberger (media_upload → PUT → media_confirm) → URL dans
  `media01`. Pas d'URL publique directe depuis Drive.
- **Trous à combler** : aucune photo posée exploitable en visuel de post (portrait,
  scène, public), aucun visuel déjà décliné aux gabarits réseaux, pas de vertical
  exporté. À demander avant de lancer un trimestre.

## Règles

- Toujours partir des **gabarits réseaux** et de la charte 2026 pour un visuel.
- Vraies images uniquement : pas de génération IA sur un compte qui vend de
  l'incarnation et de l'authenticité.
- Ne rien publier tiré des rushes tant que l'accord sur les droits n'est pas confirmé.
