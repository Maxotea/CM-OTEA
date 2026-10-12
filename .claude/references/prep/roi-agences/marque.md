# R.O.I. · Run on Investment : identité visuelle retenue

Source : le deck sponsors `R.O.I._Presentation_Sponsors.pptx` (juillet 2026, Drive).
Les couleurs sont relevées directement dans les slides (le thème PowerPoint est
celui par défaut d'Office et ne sert pas). Même identité pour le deck agences et
pour la vidéo.

## Couleurs

| Rôle | Hex | Usage |
|---|---|---|
| Fond | `#0A0A0A` | fond de toutes les slides (noir profond, jamais `#000`) |
| Surface | `#161616` | cartes, encarts (variante `#1A1A1A`) |
| Filet | `#2A2A2A` | séparateurs, lignes fines |
| Rouge R.O.I. | `#DC2626` | couleur d'accent unique : sous-titre du logo, mots-clés, tracé de parcours, puces |
| Rouge profond | `#9F1414` | ombre ou dégradé du rouge, à utiliser avec parcimonie |
| Gris texte | `#6B7280` | libellés, pieds de page |
| Gris clair | `#9CA3AF` | texte courant secondaire |
| Blanc cassé | `#E5E5E5` | accroches, citations |
| Blanc | `#FFFFFF` | titres, chiffres |

Règle : un seul accent (le rouge) par écran, sur fond noir. Pas d'autre couleur.

## Typographies

Le deck sponsors utilise **Cambria** (titres, logo) et **Calibri** (texte).
Pour le web et la vidéo, on prend leurs équivalents Google Fonts, aux mêmes
métriques :

- **Caladea** (équivalent de Cambria) : titres, chiffres, logo. Gras 700 pour les
  titres, italique 400 pour les accroches.
- **Carlito** (équivalent de Calibri) : texte courant (400), libellés en
  capitales espacées (700, interlettrage 0,2 à 0,4 em).

Fichiers locaux (woff2, sous-ensemble latin) : `deck-src/fonts/`, déclarés dans
`deck-src/fonts.css`.

## Logo

Le deck sponsors ne contient **pas de logo image** : les 8 images de
`ppt/media/` sont des pictogrammes génériques noirs (diamant, réseau, cible, œil,
carte, mallette, courbe, poignée de main). Le logo est un **logotype
typographique** :

- « R.O.I. » en Caladea gras, blanc (sur fond sombre) ;
- dessous, « RUN ON INVESTMENT » en Carlito gras, rouge `#DC2626`, capitales
  très espacées (0,42 em).

Rendus PNG transparents, générés depuis `deck-src/logo.html` :

- `logo/roi-wordmark-fond-sombre.png` (R.O.I. en blanc)
- `logo/roi-wordmark-fond-clair.png` (R.O.I. en noir `#0A0A0A`)

Note : le deck sponsors écrivait « RUN ON INVEST ». Le nom retenu est désormais
**Run on Investment**.

## Motifs graphiques

- Tracé de parcours : courbe rouge `#DC2626`, trait arrondi, qui finit sur un point
  rouge cerclé, à l'intérieur de deux ellipses grises (l'Arena). Version
  pointillée (tirets de 3, espaces de 14 à 18) pour les liaisons et la suite.
- Barre verticale rouge de 14 px sur le bord gauche de la couverture.
- Pictogrammes au trait blanc dans un cercle cerclé de rouge.
- Pas de photo, pas d'image générée : typographie, formes et tracés seulement.
