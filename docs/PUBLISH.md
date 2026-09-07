# Publier ou mettre à jour la fabrique

Dépôt canonique : https://github.com/bacoco/tech-watch-scheduler-factory
Le propriétaire a créé cette destination en accès public le 7 septembre 2026.
Ne pas y publier de secrets, de snapshots privés ni de résultats de veille métier.

## Première publication dans le dépôt public existant

Depuis le dossier extrait de l'archive, avec Python 3.11 ou plus, Git et une
CLI `gh` déjà authentifiée comme `bacoco` et autorisée à pousser :

```bash
python3 tools/publish_repository.py --owner bacoco --allow-public --apply
```

Sans `--apply`, la commande ne fait qu'un aperçu sans appel réseau. Sans
`--allow-public`, elle refuse une destination publique. Le choix public est
explicite : il ne peut pas être déduit du nom de repo ou d'un fichier téléchargé.

Le script lance les tests, contrôle l'inventaire, vérifie le compte GitHub,
prépare le commit, refuse un historique distant divergent et pousse seulement
un dépôt vide ou identique. Jamais de force-push. Il relit le SHA distant et le README.
Un résultat `published-and-reread` n'est rendu qu'après ces contrôles.
Il ne crée aucune Task et n'installe aucune veille dans d'autres repos.
Une nouvelle destination absente reste créée privée, même avec `--allow-public`.

## Mettre à jour un dépôt existant non vide

Travailler depuis un checkout à jour avec une identité GitHub autorisée.
Respecter les règles de branche et de PR. L'assistant de première publication
ne réconcilie pas automatiquement deux historiques différents.

```bash
git clone https://github.com/bacoco/tech-watch-scheduler-factory.git
cd tech-watch-scheduler-factory
# Appliquer et relire les modifications prévues.
python -m unittest discover -s tests -v
python tools/check_repository.py
# Ajouter seulement les fichiers voulus, puis committer et pousser selon la politique.
```

Le manifeste `tools/publish-files.json` recense les fichiers distribués. Le mettre
à jour explicitement après un ajout ou retrait légitime ; ne pas y inclure les
répertoires `work/`, secrets, caches ou sorties privées.

Après publication, vérifier branche, SHA et fichiers distants. Une archive locale
ou un commit non relié à une branche ne constitue pas un push. Distinguer tests
locaux, contrôles CI et recherches réelles sur les projets.

## Blocage constaté pendant cette livraison

Le connecteur pouvait lire le dépôt mais les écritures `create_file` et
`create_tree` ont toutes deux reçu HTTP 403 « Resource not accessible by
integration ». Aucune écriture distante n'a abouti. L'autre accès terminal
connecté était hors ligne. Voir [le reçu](../verification/github-publication-2026-09-07.json).
