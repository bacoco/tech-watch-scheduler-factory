# T0 puis UPDATE

## Génération

`T0_REQUIRED` signifie « instructions prêtes, recherche initiale non faite ».
Un profil draft bloque l'exécution. `INTEGRATION_REQUIRED` réserve les repos
ayant déjà une collecte correspondante : pas de deuxième scheduler silencieux.

## T0

Au premier run, fixer une date de fin de collecte initiale, le SHA du repo et
le périmètre. Cartographier le projet, les solutions et travaux pertinents,
les techniques déjà adoptées, les refus et les pistes à tester. Couvrir le
passé sans limite d'ancienneté, dans le périmètre et budget déclarés.
Un T0 n'est pas « tout Internet a été lu ». Sa couverture et ses limites sont
explicites. Une source obligatoire bloquée empêche de déclarer la couverture
complète ; reprendre à partir du journal sans déplacer le point initial.
Ne pas produire de code métier à cette étape.

## Gel

Un reçu `t0` complet cite les questions couvertes, les artefacts, leurs SHA-256,
les dates, le repo analysé et la livraison relue. Puis :

```bash
python -m tech_watch freeze-t0 PATH/scheduler-techno --receipt PATH/t0-receipt.json
python -m tech_watch verify-t0 PATH/scheduler-techno
```

Les artefacts doivent déjà exister sous `runs/` du dossier de veille.
Le gel crée une copie dans `baseline/` avec manifest, puis change l'état en
`UPDATE_READY`. L'outil valide forme, couverture déclarée et empreintes ;
la véracité de la recherche/livraison relève des preuves de l'agent.
Un gel ne peut pas être relancé pour écraser une baseline.

## UPDATE

Revenir aux faits actuels du repo et à la baseline intacte. Recueillir les
changements amont, les corrections, régressions et nouvelles connaissances.
Les connaissances anciennes nouvelles pour nous restent recevables. Leur
publication ne change pas le T0. Catégories : `new_release`, `new_evidence`,
`newly_discovered_historical`, `repo_change`, `correction`.
Conserver `published_at`, `first_seen_at`, `source_version` et `repo_sha`.

Les reçus de runs incomplets restent en `runs/`. Ne pas avancer les curseurs
correspondants tant que collecte, analyse, déduplication et livraison ne sont
pas confirmées. Les curseurs sont propres à chaque source, avec recouvrement.
Ne pas utiliser un timestamp global comme unique filtre de découverte.

## Reçu minimal

`schema_version`, `kind`, `run_id`, `repository`, `repo_sha`, `started_at`,
`finished_at`, `status=complete`, `coverage`, `blockers=[]`, `artifacts`,
`delivery`, `research` (journal hashé selon RECHERCHE.md) et, pour T0, `cutoff_at`. Chaque couverture contient `question_id`,
`status=covered`, `evidence` (chemin d'artefact) et `note`. Chaque artefact est
un chemin relatif sous `runs/` et un `sha256`. `delivery` : `status=verified`,
`evidence` (référence relue ou justification explicite d'absence d'issues).
Le reçu de test est synthétique, pas une preuve de collecte réelle.

## Concurrence

Un verrou local évite deux gels simultanés. Sur GitHub, utiliser un parent
Git attendu et échouer si la branche a bougé. Un lock local n'est pas un verrou
distribué. Une réparation après crash requiert inspection de l'état et des
artefacts : aucun effacement automatique d'un lock ou baseline ambiguë.
