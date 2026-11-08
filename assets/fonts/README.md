# Polices

Déposer ici une police `.ttf` nommée **`titre.ttf`** si la machine n'a ni
Helvetica (macOS), ni Arial (Windows), ni DejaVu/Liberation (Linux).
`scripts/carte-story.py` la trouvera automatiquement en dernier recours.

Équivalents libres recommandés pour retrouver le rendu des cartes :
- OTEA (sans-serif) : Inter, Archivo, Helvetica Now
- Gossip / Le Loft (serif) : Playfair Display, Libre Baskerville, Prata

## Inter Display (stories de jeu concours)

`InterDisplay-Black.otf` et `InterDisplay-Medium.otf` servent à
`scripts/concours-bandeau.py` et `scripts/concours-story.py`. Elles sont
versionnées ici pour que les outils et les tests tournent sur n'importe quelle
machine, y compris le serveur de tests. Licence libre SIL Open Font License 1.1
(projet Inter de Rasmus Andersson), redistribution autorisée.
