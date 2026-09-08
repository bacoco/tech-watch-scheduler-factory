# Prompts ChatGPT

Ces fichiers contiennent les instructions longues. Le README principal ne demande à l'utilisateur que de fournir le repo cible et de faire appliquer le prompt canonique correspondant.

- `PREPARE.md` : analyser le repo cible, rechercher, choisir cadences/runtime et installer `scheduler-techno/`. Aucun scheduler ni website n'est encore activé.
- `ACTIVATE.md` : activer le runtime déclaré, exécuter la veille et créer puis maintenir automatiquement le repo public `*-website` et son site GitHub Pages.

Le dépôt cible n'est pas écrit dans ces fichiers. Il est fourni par l'utilisateur dans son mini-prompt ; l'agent doit le traiter comme `TARGET_REPOSITORY`.
