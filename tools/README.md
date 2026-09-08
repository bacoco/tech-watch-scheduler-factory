# Outils de maintenance

`check_repository.py` : fichiers courts, syntaxe Python, liens locaux et inventaire.
`publish_repository.py` : création et push de cette fabrique dans GitHub via
une CLI `gh` déjà authentifiée, seulement avec `--apply`. Pas de Task.
`render_public_website.py` : wrapper du renderer statique ; assemble une édition
publique dans une home, une archive et une route stable sans appel réseau.
`create_public_website_repo.py` : bootstrap GitHub explicite du repo `*-website` ;
sans `--apply`, il ne crée rien. Avec écriture, il exige `GITHUB_TOKEN`, crée le
repo public avec une branche `main` initialisée et ne rend jamais public le repo source.
`publish_public_website.py` : vérifie un site rendu puis publie tous ses fichiers
textuels en un commit Git atomique sur `main`, sans supprimer les anciennes pages.
Il peut activer GitHub Pages après le commit avec `--enable-pages`.
`publish-files.json` : liste fermée des fichiers autorisés à être publiés.
Ce dernier fichier est vérifié par le contrôle de dépôt.

Une destination publique existante nécessite `--allow-public` explicite pour
`publish_repository.py` ; le mode par défaut reste privé et sans écriture.
Le workflow website a son contrat propre dans [WEBSITE](../docs/WEBSITE.md).
