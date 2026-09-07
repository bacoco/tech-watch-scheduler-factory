# Outils de maintenance

`check_repository.py` : fichiers courts, syntaxe Python, liens locaux et inventaire.
`publish_repository.py` : création et push de cette fabrique dans GitHub via
une CLI `gh` déjà authentifiée, seulement avec `--apply`. Pas de Task.
`publish-files.json` : liste fermée des fichiers autorisés à être publiés.
Ce dernier fichier est vérifié par le contrôle de dépôt.

Une destination publique existante nécessite `--allow-public` explicite ;
le mode par défaut reste privé et sans écriture. Voir [PUBLISH](../docs/PUBLISH.md).
