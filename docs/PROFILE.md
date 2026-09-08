# Profil v2 : usages + recherche externe, puis génération

Exemples [amélioration produit](../examples/image-product.json) et
[veille de domaine](../examples/domain-watch.json) : tous deux SYNTHÉTIQUES.
Les fixtures [cadence rapide](../examples/cadence-fast.json) et
[cadence lente](../examples/cadence-slow.json) illustrent le nouveau contrat.
Contrôles : [profile](../tech_watch/profile.py), [scheduling](../tech_watch/scheduling.py),
[usage](../tech_watch/usage.py), [discovery](../tech_watch/discovery.py).

## Champs racine

`schema_version=2`, `repository=owner/name`, `default_branch`, `analyzed_sha`,
`analyzed_at`, `status=draft|ready`, `objective`, `repo_type`, `constraints`,
`evidence`, `questions`, `channels`, `integration`, `cadence`, `runtime`,
`unknowns`, `usage`, `discovery`.

`runtime` est recommandé explicitement dans tout nouveau profil. Son absence est
acceptée seulement pour compatibilité et signifie `dedicated`.

## Contexte et usage

Une preuve de contexte : `id`, `path`, `start_line`, `end_line`, `claim`,
`kind=code|documentation|inference`. Le SHA commun fixe les fichiers lus.
Ces preuves ne sont pas des mesures d'utilisation. Ne pas inventer des chemins.

`usage` : `watch_purpose=product_improvement|domain_intelligence|both`,
`audiences`, `value_delivered`, `information_output`, `limits`, `journeys`.
Chaque parcours porte acteur, but, workflow, difficultés, critères de succès,
preuves, statut `observed|documented|inferred` et références d'observation.

## Questions

Chaque question possède `id`, `question`, `why`, `evidence_ids`, `acceptance`,
`usage_ids` et `intent=improve_service|domain_information`. Tous les usages doivent
être reliés. Une information de domaine n'exige pas un changement de code.

## Sources et découverte ouverte

Décider des familles `arxiv`, `github`, `official`, `models`, `products`,
`community`, `personal`, `web_open`, puis ajouter d'autres IDs si nécessaire.
Chaque famille : `id`, `mode`, `reason`, `queries`, `targets`, `access`.
`web_open` reste actif ; `personal` reste exclu sans autorisation distincte.

`discovery` suit [RECHERCHE](../templates/watch/RECHERCHE.md), avec
`stage=generation`, `repo_sha=analyzed_sha`. Un profil `ready` exige une recherche
`complete`, sans blocage et avec traces. `synthetic=true` est réservé à `example/`.

## Intégration

`integration` : `mode=none|coexist|reuse-existing`, `paths`, `reason`.
Les chemins existants restent canoniques ; aucun état n'est dupliqué.

## Cadence moderne

`cadence.timezone` est un fuseau IANA. `max_new_issues` reste 0..10.
La cadence comporte deux flux indépendants :

- `watch` ;
- `postmortem`.

Chacun contient :

- `recommendation` : formulation humaine ;
- `reason` : justification liée au rythme du domaine et à l'usage ;
- `interval_days` : intervalle actuellement proposé ;
- `min_interval_days` ;
- `max_interval_days`.

`cadence.adaptation` contient :

- `min_runs_before_change` : au moins 2 ;
- `decrease_after_consecutive_low_value` : nombre de cycles pauvres nécessaire
  avant de ralentir, supérieur ou égal à la fenêtre minimale.

La génération doit motiver les cadences à partir de volatilité, fréquence des
publications/releases/normes, coût de recherche, risque d'obsolescence, criticité
d'un retard et volume attendu de changements matériels.

Les anciens profils avec `recommendation`/`reason` à plat restent lisibles pour
migration. Ils sont normalisés vers une veille hebdomadaire historique et un
post-mortem mensuel de prudence ; ne pas produire de nouveau profil dans ce format.

## Runtime

`runtime.mode=dedicated|multiplexed` et `runtime.reason` sont explicites.

En `dedicated`, deux tâches physiques propres à la veille sont proposées avec les
deux cadences ci-dessus.

En `multiplexed`, ajouter :

- `group_id` stable ;
- `registry_repository=owner/name` pour la source de vérité Git du runtime.

Le pack génère alors `multiplex-jobs.json` et les textes de restauration des deux
tâches physiques partagées. Voir [RUNTIME](RUNTIME.md).

## État et migration

Les inconnues bloquantes empêchent `ready`. Générer est distinct de geler T0.
Pour réviser un profil déjà installé, préparer un diff revu, conserver `state.json`,
baseline, runs et historique. Une migration de runtime doit désactiver et vérifier
l'ancien mode avant d'activer le nouveau ; aucune double exécution n'est admise.
