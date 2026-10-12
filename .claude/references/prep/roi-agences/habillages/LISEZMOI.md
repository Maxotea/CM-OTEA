# R.O.I. · pack d'habillages pour le teaser

Titres animés à fond transparent, 1920 × 1080, 25 i/s, à poser par-dessus le B-roll de running.
Typo sport : **Barlow Condensed Black Italic** (Google Fonts, licence OFL). Libellés en Carlito,
logo en Caladea, rouge `#DC2626` comme seul accent.

## Les fichiers

| Fichier | Durée | Le coup tombe à... |
|---|---|---|
| `00_flash-rouge.mov` | 0,52 s | image 0 (flash plein cadre, puis décroissance) |
| `01_10000.mov` | 2 s | image 2 (« 10 000 »), image 21 (« ENTREPRENEURS. ») |
| `02_ligne-depart.mov` | 1,52 s | image 0, un mot toutes les 2 à 3 images |
| `03_la-defense.mov` | 2 s | image 0 (cartouche en bas à gauche) |
| `04_5km.mov` | 1 s | image 0 |
| `05_10km.mov` | 1 s | image 0 |
| `06_arena.mov` | 2 s | image 0 (« ARRIVÉE »), image 21 (« PLÉNITUDE ARENA ») |
| `07_networking.mov` | 2,52 s | une ligne aux images 0, 9 et 19 |
| `08_compteur.mov` | 2,52 s | le compteur se pose sur 10 000 à l'image 42 |
| `09_public.mov` | 2 s | un mot aux images 0, 10, 20 et 30 |
| `10_2027.mov` | 1,52 s | image 0 |
| `11_agence.mov` | 3 s | aplat rouge « L'AGENCE » à l'image 7 |
| `12_pas-tout.mov` | 2,52 s | image 0, puis « LA SUITE, EN VISIO. » à l'image 30 |
| `13_signature.mov` | 4 s | fond noir **plein** (pas transparent), logo à l'image 3 |

Deux versions de chaque habillage :

- **à la racine** : ProRes 4444 avec alpha, la qualité master (35 à 48 Mo pièce). Ces fichiers restent
  sur le poste, ils ne vont pas dans git (voir plus bas pour les refaire).
- **dans `leger/`** : `.mov` en codec PNG avec alpha (1 à 8 Mo pièce, 56 Mo en tout), suivis dans git.
  Même animation au pixel près ; seule différence : l'ombre portée est plus serrée et le voile sombre
  diffus derrière le texte est retiré, pour tenir le poids.

`demo-habillages.mp4` (35 s) enchaîne tout sur un fond gris neutre, pour voir le rendu sans ouvrir
DaVinci. `planche-habillages.png` montre une image clé de chaque fichier.

## Poser les habillages dans DaVinci Resolve

1. Importe les `.mov` dans le Media Pool (ProRes ou version `leger/`, les deux gardent la transparence).
2. Pose chaque habillage sur la **piste V2**, au-dessus du B-roll en V1.
3. Mode composite : **Normal** (Inspecteur > Composite). L'alpha est lu automatiquement, rien à régler.
4. Si un liseré clair ou sombre se voit autour des lettres : clic droit sur le clip > Attributs du clip >
   Vidéo > Mode alpha, et choisis « Droit » (Straight).
5. Cale le **début du clip sur le temps fort** de la musique : tout entre en 2 à 6 images.
   Pour `08_compteur`, cale plutôt l'image 42 (le chiffre qui se pose) sur un temps fort.
6. Si un deuxième mot tombe à côté du temps (`01`, `06`, `12`) : coupe le clip à la lame juste avant
   ce mot et glisse la seconde moitié sur le temps suivant.
7. `09_public` change de mot toutes les 10 images, soit un mot par temps à 150 BPM. Pour un autre tempo,
   règle la vitesse du clip (clic droit > Modifier la vitesse du clip) à **BPM du morceau ÷ 150**
   (par exemple 80 % à 120 BPM).
8. `00_flash-rouge` se pose sur les coupes fortes, juste avant un habillage qui claque, ou seul.

## Découpage conseillé (environ 40 s, une mesure = 4 temps)

Vers 120 à 128 BPM, une mesure dure à peu près 2 s : le montage tient en 18 à 20 mesures.

| Mesures | Plan de B-roll | Habillage | Calage |
|---|---|---|---|
| 1 à 2 | Chaussures en gros plan, pieds sur la ligne | `02_ligne-depart` | temps 1 de la mesure 2 |
| 3 à 4 | Départ en masse | `00_flash-rouge` puis `01_10000` | flash et chiffre sur le temps 1 de la mesure 3 |
| 5 | Vue aérienne de La Défense | `03_la-defense` | temps 1 |
| 6 | Foulées rapides, coupes sèches | `04_5km` puis `05_10km` | temps 1, puis temps 3 |
| 7 à 8 | Foulées au ralenti | `08_compteur` | le 10 000 se pose sur le temps 1 de la mesure 8 |
| 9 | Coureurs qui franchissent l'arrivée | `00_flash-rouge` puis `06_arena` | temps 1 |
| 10 à 11 | Poignées de main | `07_networking` | temps 1 de la mesure 10 |
| 12 | Salle pleine | `09_public` | un mot par temps |
| 13 | Vue aérienne ou plan large du quartier | `10_2027` | temps 1 |
| 14 à 15 | Salle pleine ou poignées de main au ralenti | `11_agence` | « L'AGENCE » sur le temps 1 de la mesure 14 |
| 16 | Un coureur qui sort du champ | `12_pas-tout` | temps 1 ; « LA SUITE » arrive 1,2 s plus tard, recale-le à la lame sur le temps 3 si besoin |
| 17 à 18 | Coupe sèche au noir | `13_signature` | temps 1, laisse finir la musique dessus |

Garde des plans sans texte entre les habillages : c'est la respiration qui fait claquer les suivants.

## Regénérer les fichiers depuis `src/`

Il faut Node 22, Playwright avec son Chromium, Python 3 et un ffmpeg complet (avec `prores_ks`,
`png` et `libx264`). Les polices sont dans `src/fonts/`, rien à télécharger.

```bash
cd habillages/src
# ProRes 4444 avec alpha (master), écrits dans habillages/
FFMPEG=/chemin/vers/ffmpeg node render.cjs mov .. all
# version légère, écrite dans habillages/leger/
FFMPEG=/chemin/vers/ffmpeg node render.cjs leger ../leger all
# un seul habillage : remplace « all » par son nom, par exemple 08_compteur
# démo sur fond gris (à lancer après les ProRes)
python3 demo.py /chemin/vers/ffmpeg ..
```

Les images PNG intermédiaires sont effacées après chaque encodage. Pour vérifier une image précise
sur un fond de contrôle : `node render.cjs stills /tmp/controle 08_compteur 42 --review`.

Les textes, durées et timings se modifient dans `src/habillages.js` (un bloc par habillage, minuté en
images à 25 i/s), les couleurs et les polices dans `src/index.html`.
