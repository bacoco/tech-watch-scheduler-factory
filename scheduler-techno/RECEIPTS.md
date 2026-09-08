# Contrat autonome des reçus et de l'état

Ce fichier permet à une tâche de fonctionner depuis ce seul répertoire. Les outils Python de la fabrique sont optionnels ; ne pas prétendre les avoir exécutés lorsqu'on applique le protocole avec un connecteur GitHub.

## Reçu d'un run complet

Un reçu contient `schema_version`, `kind`, `run_id`, `repository`, `repo_sha`, `started_at`, `finished_at`, `cutoff_at`, `status`, `blockers`, `research`, `coverage`, `artifacts` avec SHA-256 et `delivery` vérifiée.
Chaque question du profil apparaît exactement une fois dans coverage. Les chemins restent sous `runs/<run_id>/`, sans symlink, traversal ou secret. Un reçu partiel ne permet ni gel ni avance de checkpoint.

## Preuve de recherche obligatoire

`research` pointe vers le journal défini dans RECHERCHE.md, inclus parmi les artefacts hashés. Son stage et repo_sha correspondent au reçu ; recherches et lectures sont datées dans CE run. La recherche de génération n’est pas réutilisée comme preuve T0 ou UPDATE.

## Gel T0 avec GitHub uniquement

1. Relire profil, state, artefacts et livraison ; calculer les SHA-256 exacts.
2. Vérifier l'absence de baseline et le SHA parent Git attendu.
3. Copier les artefacts sous `baseline/` en gardant leur chemin relatif complet.
4. Créer `baseline/manifest.json` avec `schema_version`, `repository`, `cutoff_at`, `repo_sha`, `receipt` et `files`.
5. Mettre `state.baseline` à l'objet `manifest_sha256` et `cutoff_at`, puis `state.phase` à `UPDATE_READY` dans le même commit cohérent.
6. Relire ce commit et tous les hashes.

Le hash porte sur les octets réellement écrits. Ne jamais régénérer une baseline.

## UPDATE

Même contrat, `kind=update`, nouveau run_id, plus `previous_run_id` et `source_checkpoints`. Après vérification de la baseline et du parent attendu : écrire le reçu, mettre `last_completed_update` puis fusionner les checkpoints sans effacer les sources non terminées. Ne pas modifier `state.baseline`.

## Historique et autorité

Le registre d'issues et refus se conserve dans `runs/` avec identités stables. La baseline demeure une référence. Le champ `external_task` ne change qu'après création externe réellement constatée.
