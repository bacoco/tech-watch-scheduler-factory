# T0 — Tech Watch Scheduler Factory self-watch

## Conclusion

Le design actuel tient face à un test réel : deux mini-prompts, vérification des capacités, repo website public séparé, GitHub Pages à la racine, et runtime avec reprise bornée. Aucun correctif source immédiat n'est requis par ce T0.

Le principal enseignement opérationnel est de laisser la tâche créer `*-website` lorsqu'elle en a le droit plutôt que de le précréer manuellement : GitHub indique qu'un repo créé par l'App reçoit automatiquement son accès, tandis qu'un repo manuel peut rester hors de la sélection de l'installation.

## q1 — ChatGPT Scheduled Tasks

La documentation OpenAI actuelle confirme les tâches ponctuelles/récurrentes, le monitoring, l'usage d'apps connectées dont GitHub lorsqu'elles sont disponibles, et le fait qu'une action externe peut nécessiter une approbation qui met la tâche en pause.

**Décision : retain.** Le contrat CAPABILITIES/ACTIVATE qui exige une vérification réelle des outils, permissions et états est justifié. La veille hebdomadaire reste appropriée.

## q2 — GitHub Apps et Pages

GitHub documente séparément les permissions d'une App et les repositories sélectionnés pour l'installation. Le test a reproduit ce risque : `tech-watch-scheduler-factory-website`, créé manuellement, a d'abord renvoyé `403 Resource not accessible by integration` jusqu'à son ajout à l'installation.

GitHub Pages confirme la publication depuis une branche, avec `/(root)` ou `/docs`, et `.nojekyll` pour une publication statique directe sans build Jekyll demandé.

**Décision : retain.** Garder `main` + `/(root)` et la vérification de Pages. Préférer la création du repo website par l'agent quand elle est autorisée.

## q3 — Fiabilité du runtime

AWS SQS documente le visibility timeout : un travail non terminé après crash redevient disponible, mais l'at-least-once impose de prévoir les doublons. Google Cloud recommande retries et jobs idempotents pour supporter les redémarrages.

**Décision : retain.** `dispatch_id` déterministe + `lease_minutes` + retry borné + archive failed est cohérent avec ces patterns. Continuer à tester le crash après réservation et les effets distants idempotents.

## q4 — Friction utilisateur et projection publique

Le passage aux deux mini-prompts réduit la charge du README sans perdre l'autorité du repo : PREPARE et ACTIVATE restent versionnés. La séparation repo source / repo website évite d'exposer le T0, les reçus et les instructions internes.

**Décision : retain.** Le premier website du factory sera produit à partir de ce T0 pour tester la projection de bout en bout.

## Cadence initiale

- Watch : 7 jours — conserver.
- Post-mortem : 30 jours — conserver jusqu'à au moins 3 runs exploitables.
- Issues nouvelles : aucune pour ce T0 ; les constats sont déjà couverts par les contrats actuels.

## Limites

Ce T0 couvre le produit public et les docs officielles utiles au chemin d'activation. Il ne prétend pas couvrir toute la littérature sur les schedulers distribués ni l'expérience de tous les utilisateurs.
