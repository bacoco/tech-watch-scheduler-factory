# Runtime : dedicated ou multiplexed

Le runtime décide combien de Scheduled Tasks physiques portent les veilles.
Il ne change ni les contrats métier, ni le T0, ni les permissions GitHub.

## Mode dedicated

`runtime.mode=dedicated` conserve deux tâches propres à un repo : `watch` et
`postmortem`. Leurs fréquences viennent de deux objets de cadence distincts.
C'est le mode simple pour une veille isolée ou lorsque les places de tâches ne
sont pas une contrainte.

## Mode multiplexed

`runtime.mode=multiplexed` exige :

- `group_id` : identifiant stable du groupe ;
- `registry_repository` : repo GitHub canonique du runtime ;
- deux Scheduled Tasks physiques partagées : Orchestrator et Worker ;
- N définitions de jobs logiques versionnées dans Git.

Le repo runtime doit conserver au minimum :

- `jobs/*.json` : jobs canoniques ;
- `current-action/job.json` : zéro ou un dispatch ;
- `completed/` et `failed/` : archives ;
- `receipts/` : preuves des transitions et SHAs lus.

Le repo runtime n'est pas un repo website. Sa visibilité suit les besoins de
confidentialité des projets surveillés et ne doit pas être rendue publique par
défaut.

## Définition d'un job

Schéma v1 :

- `job_id` stable et unique ;
- `repository` cible ;
- `kind=watch|postmortem` ;
- `instructions_path` sous `scheduler-techno/` ;
- `timezone` ;
- `schedule.anchor_at` et `schedule.interval_days` ;
- `priority` 0..100 ;
- `max_lateness_minutes` ;
- `max_retries` 0..10 ;
- `lease_minutes` : durée maximale d'une réservation avant récupération ;
- `guard` canonique ;
- `enabled`.

`anchor_at` généré par un pack est une proposition. Lors de l'inscription réelle
dans le registre, le remplacer par l'instant d'activation voulu pour éviter un
rattrapage historique involontaire.

## Orchestrator

Il lit le registre à un SHA, vérifie la garde de migration et sélectionne le
prochain job dû selon :

1. `due_at` le plus ancien ;
2. priorité la plus haute ;
3. `job_id` lexical.

Il écrit seulement un dispatch minimal. Il n'exécute jamais le métier.
`dispatch_id = hash(job_id | due_at)` : une occurrence garde donc une identité
stable à travers les retries.

Chaque réservation contient `reserved_at` et `lease_until`. Tant que le lease
n'est pas expiré, une seconde réservation est refusée. Si le Worker disparaît,
l'Orchestrator récupère le slot après expiration : la même occurrence repart avec
le même `dispatch_id` et un numéro de tentative supérieur. Si le budget retry est
épuisé, l'occurrence est archivée dans `failed` au lieu de bloquer le groupe.

## Worker

Il lit le dispatch réservé puis retrouve `job_id` dans le registre canonique.
Le repo, le guard et `instructions_path` exécutés proviennent exclusivement du
registre. Un dispatch contenant un chemin, repo, prompt ou permission
supplémentaire est refusé. Après exécution, le Worker archive le résultat et
libère le slot.

Un échec est retenté jusqu'à `max_retries`, puis l'occurrence passe en `failed`.
Une réussite passe en `completed`. Une occurrence archivée n'est plus redispatchée.

## Rattrapage

Plusieurs jobs dus au même instant sont consommés successivement. Le slot unique
évite le parallélisme implicite. `max_lateness_minutes` borne le rattrapage pour
ne pas exécuter indéfiniment un backlog devenu sans valeur.

## Post-mortem et T0

Le job post-mortem porte un guard : sans baseline ou runs exploitables, il est
reporté. Il ne doit pas transformer l'absence de matière en blocage du T0.

## Migration dedicated → multiplexed

La migration est volontairement fail-closed :

1. identifier les tâches dédiées encore actives ;
2. les désactiver réellement ;
3. relire leur état et conserver la preuve ;
4. inscrire les jobs logiques avec leur nouvel anchor ;
5. passer `dedicated_tasks_disabled=true` dans le registre ;
6. créer/réutiliser Orchestrator + Worker ;
7. vérifier qu'aucune double exécution n'a eu lieu.

Sans étape 3, le dispatch est bloqué. Le sens inverse suit la même règle :
désactiver d'abord les jobs multiplexés avant de recréer des tâches dédiées.

## Restauration

Le repo runtime + les repos sources suffisent à reconstruire l'état logique.
`MULTIPLEX-TASKS.md` contient les textes pour recréer les deux tâches physiques
sur un autre compte. Leur présence dans Git ne prouve jamais leur création réelle.

## Validation locale

Le module `tech_watch.multiplex` valide registre, ordre, idempotence, lease,
retry et autorité du dispatch. Le CLI fournit `multiplex-validate`,
`multiplex-reserve` et `multiplex-finish` pour simuler les transitions sans créer
de Scheduled Task.
