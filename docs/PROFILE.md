# Profil v2 : usages + recherche externe, puis génération

Exemples [amélioration produit](../examples/image-product.json) et
[veille de domaine](../examples/domain-watch.json) : tous deux SYNTHÉTIQUES.
Contrôles : [profile](../tech_watch/profile.py), [usage](../tech_watch/usage.py),
[discovery](../tech_watch/discovery.py). Vue métier : [USAGE](USAGE.md).

## Champs racine

`schema_version=2`, `repository=owner/name`, `default_branch`, `analyzed_sha`
(SHA Git), `analyzed_at` (ISO avec fuseau), `status=draft|ready`, `objective`,
`repo_type`, `constraints`, `evidence`, `questions`, `channels`, `integration`,
`cadence`, `unknowns`, `usage`, `discovery`. Aucun profil v1 n'est accepté par v2.
`analyzed_at` suit la recherche de cadrage ; celle-ci n'est pas le T0.

## Contexte et usage

Une preuve de contexte : `id`, `path`, `start_line`, `end_line`, `claim`,
`kind=code|documentation|inference`. Le SHA commun fixe les fichiers lus.
Ces preuves ne sont pas des mesures d'utilisation. Ne pas inventer des chemins.

`usage` : `watch_purpose=product_improvement|domain_intelligence|both`,
`audiences` (liste), `value_delivered`, `information_output`, `limits` (liste),
`journeys` (1 à 10 parcours).
Chaque parcours : `id`, `actor`, `goal`, `workflow`, `pain_points` (liste),
`success_criteria` (liste), `evidence_ids` (contexte),
`status=observed|documented|inferred`, `observation_refs` (liste de références
aux observations réelles autorisées). `observed` nécessite ces références.
Les références doivent rester désensibilisées ; le validateur ne les authentifie pas.

## Questions

`id`, `question`, `why`, `evidence_ids` (contexte), `acceptance`,
`usage_ids` (non vide), `intent=improve_service|domain_information`.
Tous les usages déclarés doivent être reliés aux questions. Leur intention
correspond à la finalité. Les informations de domaine n'exigent pas de patch.
`acceptance` est un critère d'intérêt ou d'évaluation, pas un ordre de coder.

## Sources et découverte ouverte

Décider des familles `arxiv`, `github`, `official`, `models`, `products`,
`community`, `personal`, `web_open`. Ce sont des amorces, pas une liste fermée :
ajouter d'autres IDs (minuscules, chiffres, `_`, `-`) selon les besoins.
Chaque famille : `id`, `mode=primary|secondary|excluded`, `reason`, `queries`,
`targets`, `access=unknown|verified|blocked`. Une famille active a requêtes et cibles.
`web_open` reste actif ; les sujets recherchés dépendent des usages, pas des outils.
`personal` reste exclu sans autorisation explicite distincte et bornée.
Un accès constaté pendant la génération ne prouve pas l'accès de la tâche future.

`discovery` suit [RECHERCHE](../templates/watch/RECHERCHE.md), avec
`stage=generation`, `repo_sha=analyzed_sha`. Un profil `ready` exige une
recherche `complete`, sans blocage et avec traces réelles. `synthetic=true`
n'est admis que sous `example/`, jamais pour un repo utilisateur.
Sans navigation : conserver un journal `blocked/partial` et un profil `draft`.
Deux éditeurs et trois phases ne suffisent pas à prouver une recherche approfondie.

## Intégration, cadence et état

`integration` : `mode=none|coexist|reuse-existing`, `paths`, `reason`.
Les chemins de l'existant sont canoniques ; aucun état n'est dupliqué.
`cadence` : `timezone` IANA, `recommendation`, `reason`, `max_new_issues` (0 à 10).
Le plafond est une proposition, pas un quota ni une Task créée.
Les inconnues bloquantes empêchent `ready`. Les limites non bloquantes restent
visibles dans les usages et les sources. Générer est distinct de geler le T0.

## Migration

Réaliser l'analyse d'usage et la recherche externe manquantes. Préparer un diff
revu des instructions et du profil ; conserver `state.json`, baseline, runs et
historiques. Ne pas utiliser l'installation neuve pour écraser une veille existante.
