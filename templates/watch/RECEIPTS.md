# Contrat autonome des reçus et de l'état

Ce fichier permet à une tâche de fonctionner depuis ce seul répertoire.
Les outils Python de la fabrique sont optionnels ; ne pas prétendre les avoir
exécutés lorsqu'on applique le protocole avec un connecteur GitHub.

## Reçu d'un run complet

```json
{
  "schema_version": 1,
  "kind": "t0",
  "run_id": "t0-0001",
  "repository": "owner/repo",
  "repo_sha": "SHA_GIT_LU_40_HEXA",
  "started_at": "DATE_ISO_AVEC_FUSEAU",
  "finished_at": "DATE_ISO_AVEC_FUSEAU",
  "cutoff_at": "POINT_INITIAL_ISO_AVEC_FUSEAU",
  "status": "complete",
  "blockers": [],
  "research": "runs/t0-0001/research.json",
  "coverage": [
    {
      "question_id": "ID_DE_QUESTIONS",
      "status": "covered",
      "evidence": "runs/t0-0001/report.md",
      "note": "Ce qui a été effectivement examiné et ses limites"
    }
  ],
  "artifacts": [
    {"path": "runs/t0-0001/report.md", "sha256": "SHA256_DES_OCTETS_EXACTS"},
    {"path": "runs/t0-0001/research.json", "sha256": "SHA256_DU_JOURNAL"}
  ],
  "delivery": {"status": "verified", "evidence": "Référence relue ou absence d'issue justifiée"}
}
```

Ceci est un SCHÉMA ILLUSTRÉ, pas un reçu à recopier avec des valeurs factices.
Chaque question du profil doit apparaître exactement une fois dans coverage.
Les preuves de couverture référencent des artefacts présents dans l'inventaire.
Les chemins restent sous `runs/<run_id>/`, sans symlinks, traversal ou secrets.
Un reçu partiel est conservé mais ne permet ni gel ni avance de checkpoint.
Une source obligatoire inaccessible est un blocker, pas une couverture réussie.

## Preuve de recherche obligatoire

`research` pointe vers le journal défini dans RECHERCHE.md, inclus parmi les
artefacts hashés. Son stage et repo_sha correspondent au reçu ; recherches et
lectures sont datées dans CE run. La recherche de génération n’est pas réutilisée
comme preuve d’exécution T0 ou UPDATE. Un journal absent, partiel ou périmé bloque.

## Gel T0 avec GitHub uniquement

1. Relire profil, state, artefacts et livraison ; calculer les SHA-256 exacts.
2. Vérifier l'absence de baseline et le SHA parent Git attendu.
3. Copier les artefacts sous `baseline/` en gardant leur chemin relatif complet.
4. Créer `baseline/manifest.json` avec `schema_version`, `repository`,
   `cutoff_at`, `repo_sha`, `receipt` (reçu complet), `files` (chemin → sha256).
5. Mettre `state.baseline` à l'objet `manifest_sha256` et `cutoff_at`, puis
   `state.phase` à `UPDATE_READY` dans le même commit cohérent.
6. Relire ce commit et tous les hashes ; s'il a échoué, réconcilier avant retry.

Le hash porte sur les octets réellement écrits, pas sur une autre sérialisation.
Si l'outil ne sait ni calculer les empreintes ni réaliser une livraison cohérente,
marquer le blocage et ne pas annoncer un gel. Ne jamais régénérer une baseline.

## UPDATE

Même contrat, `kind=update`, nouveau run_id, plus :
`previous_run_id` (dernier run réussi ou null), `source_checkpoints` (objet).
Les clés de checkpoints sont les IDs des canaux actifs. Chaque valeur peut
contenir un sous-objet par source/URL pour éviter un curseur unique trop large.
Après vérification de la baseline et du parent attendu : écrire le reçu,
mettre `last_completed_update` à `run_id`, `finished_at`, `receipt_sha256` ;
fusionner les checkpoints sans effacer ceux des sources non terminées.
Ne pas modifier `state.baseline`. Un run déjà enregistré est un no-op seulement
si son contenu est identique. Une collision de run_id ou un parent périmé bloque.

## Historique et autorité

Le registre d'issues et refus se conserve dans `runs/` avec identités stables.
La baseline demeure une référence, pas un fichier d'instructions modifiable.
Le champ `external_task` ne change qu'après création externe réellement constatée.
Un hash local n'est pas une signature contre un acteur autorisé à tout réécrire.
