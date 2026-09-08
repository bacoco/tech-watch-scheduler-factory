# Outils de maintenance

`check_repository.py` : fichiers courts, syntaxe Python, liens locaux et inventaire.
`publish_repository.py` : création et push de cette fabrique dans GitHub via
une CLI `gh` déjà authentifiée, seulement avec `--apply`. Pas de Task.
`render_public_website.py` : wrapper du renderer statique ; assemble une édition
publique dans une home, une archive et une route stable sans appel réseau.
`create_public_website_repo.py` : bootstrap GitHub explicite du repo `*-website` ;
sans `--apply`, il ne crée rien. Avec écriture, il exige `GITHUB_TOKEN` et ne
rend jamais public le repo source.
`publish-files.json` : liste fermée des fichiers autorisés à être publiés.
Ce dernier fichier est vérifié par le contrôle de dépôt.

Une destination publique existante nécessite `--allow-public` explicite pour
`publish_repository.py` ; le mode par défaut reste privé et sans écriture.
Le workflow website a son contrat propre dans [WEBSITE](../docs/WEBSITE.md).
