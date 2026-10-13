# Polices versionnées

Polices libres (SIL Open Font License 1.1, licence `OFL.txt` dans chaque dossier) lues par
`scripts/story-photo.py` (qui indexe ce dossier directement) et par `scripts/carrousel.py`
(qui ne lit que les polices système et `~/.fonts` : le job `carrousels.yml` copie ce dossier
dans `~/.fonts` avant le rendu ; sur le Mac, faire de même ou installer les fichiers).

Une graisse par fichier : les polices variables ne sont pas reconnues par la recherche par nom
de `carrousel.py`. Instances produites le 12/10/2026 avec fontTools (`varLib.instancer`) depuis
les fichiers variables de github.com/google/fonts (`ofl/inter`, `ofl/archivo`), Space Mono
copiée telle quelle de `ofl/spacemono`.

| Dossier | Fichier | Instance | Compte |
| - | - | - | - |
| `inter-display/` | `InterDisplay-Medium.ttf` | Inter, opsz 32, wght 500 | OTEA Production (labels), Otea Filmakers (phrase et labels) |
| `inter-display/` | `InterDisplay-Bold.ttf` | Inter, opsz 32, wght 700 | OTEA Production (phrase, titres) |
| `archivo/` | `Archivo_Expanded-Black.ttf` | Archivo, wdth 125, wght 900 | Run On Invest (nom R.O.I., phrase, titres) |
| `archivo/` | `Archivo-Regular.ttf` | Archivo, wdth 100, wght 400 | Run On Invest (corps des carrousels) |
| `space-mono/` | `SpaceMono-Regular.ttf`, `SpaceMono-Bold.ttf` | statiques d'origine | Run On Invest (mention, registre, pied) |
| `fraunces/` | `Fraunces-SemiBold.ttf` | Fraunces, opsz 100, wght 600, SOFT 0, WONK 0 | Pierre Huiban (sous-titres du gabarit `monologue` de `pierre-reel-ralenti.py`) |
| `fraunces/` | `Fraunces-Regular.ttf` | Fraunces, opsz 100, wght 400, SOFT 0, WONK 0 | Pierre Huiban (phrases du gabarit `reel` de `pierre-reel-ralenti.py`, à défaut d'une Fraunces-Regular dans `--polices`) |

Fraunces : instances produites le 13/10/2026 avec fontTools (`varLib.instancer`) depuis le
fichier variable `Fraunces[SOFT,WONK,opsz,wght].ttf` (famille Google Fonts `ofl/fraunces`). Taille
optique 100 : c'est elle qui rend les largeurs mesurées sur la référence @rundadlift ; WONK 0 :
sans les lettres penchées de la coupe par défaut. `pierre-carousel-v2.py` ne lit pas ce dossier
(il charge `Fraunces-SemiBold.ttf` à plat dans `--polices`) : les titres de la DA de Pierre ne
changent pas.

Inter Display est le repli DÉCLARÉ des deux comptes OTEA tant que la licence de Forma DJR
Display (police payante de la charte, fichiers « Testing » sur le Mac) n'est pas confirmée par
Maxime. Aucun fichier Forma DJR ne doit entrer dans ce dépôt, licence ou non : sur le Mac, les
déposer dans `~/Library/Fonts` sous les noms `FormaDJRDisplay-Bold.ttf` et
`FormaDJRDisplay-Medium.ttf`, puis seulement alors remettre « Forma DJR Display » en tête des
listes de `scripts/themes.json`.

Ne pas ajouter `Archivo_Expanded-Regular.ttf` : le corps R.O.I. est en Archivo 400 normal (kit
V2.1), et sa présence ferait choisir l'Expanded Regular au corps des carrousels.
