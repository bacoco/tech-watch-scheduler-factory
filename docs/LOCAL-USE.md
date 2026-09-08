# Usage local pour les mainteneurs

L'entrée destinée aux utilisateurs reste [le README](../README.md), entièrement
en langage naturel. Les commandes ci-dessous sont des outils de maintenance,
pas un préalable à copier par l'utilisateur dans sa demande à un assistant.

## Vérifier et essayer sans réseau

Depuis un checkout complet, avec Python 3.11 ou plus :

```bash
python -m unittest discover -s tests -v
python tools/check_repository.py
python -m tech_watch generate --profile examples/image-product.json --out work
python -m tech_watch validate work/example--image-product/scheduler-techno
python -m tech_watch generate --profile examples/domain-watch.json --out work/domain
python -m tech_watch multiplex-validate examples/multiplex-registry.json
```

Les profils, cadences et registres d'exemple sont synthétiques. Ces commandes
testent la fabrique ; elles ne font pas une recherche Internet et n'activent
aucune Scheduled Task.

## Simuler le multiplexage

La réservation et la fin d'un dispatch peuvent être simulées sans effet distant :

```bash
python -m tech_watch multiplex-reserve examples/multiplex-registry.json --now 2026-09-08T09:00:00+02:00
python -m tech_watch multiplex-reserve examples/multiplex-registry.json --state work/runtime-state.json --now 2026-09-08T09:00:00+02:00
python -m tech_watch multiplex-finish examples/multiplex-registry.json work/runtime-state.json --success
```

Ces commandes rendent le nouvel état en sortie ; elles n'écrivent pas la queue
GitHub. Le runtime réel suit [RUNTIME](RUNTIME.md) et ses contrôles d'autorité.

## Collecter, puis faire travailler l'agent

Avec les accès GitHub réellement nécessaires :

```bash
python -m tech_watch discover --owner bacoco --limit 10 --out work/repos.json
python -m tech_watch snapshot --repo owner/project --out work/project-snapshot
```

L'agent lit ensuite les sources du projet, étudie les usages et mène la recherche
externe. Il rédige les profils selon [PROFILE](PROFILE.md). Ces étapes ne sont
pas remplacées par la collecte du snapshot.

```bash
python -m tech_watch generate --profile-dir work/profiles --out work/packs
python -m tech_watch install work/packs/owner--project/scheduler-techno /chemin/project
```

L'installation est un aperçu par défaut. L'option `--apply` n'est utilisée
qu'après autorisation des écritures bornées. Sans terminal, l'agent utilise ses
connecteurs conformément aux mêmes contrats et ne prétend pas exécuter les tests.
