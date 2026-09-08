---
name: generate-tech-watch
description: Comprend les usages, recherche le domaine, puis génère une veille avec cadence adaptative, runtime et site public séparé.
---

# Fabriquer une veille à partir de ce que le projet apporte aux utilisateurs

## Objectif

Pour chaque repo, comprendre qui utilise le service, pour accomplir quoi,
comment et avec quelles difficultés. Le code vérifie le fonctionnement et les
possibilités d'intégration ; il ne définit pas seul le sujet de veille.

La fabrique effectue une recherche externe DE CADRAGE avant de générer le profil ;
ce n'est pas le T0 complet. Elle produit `scheduler-techno/` avec contrats de
recherche, cadences, runtime et site public. Aucun fichier n'active une tâche,
ne crée un repo runtime ni le repo website.

## 1. Résoudre sélection et droits

Accepter une liste ou les repos autorisés. Résoudre branche par défaut et SHA.
Signaler les repos inaccessibles. Exclure la fabrique elle-même et son activité
générée seule. Sans autorisation d'installation : produire pack/diff hors repo.
Aucun cron ni Scheduled Task n'est créé à cette étape.

## 2. Comprendre les usages AVANT la stack

Lire objectif, guide utilisateur, parcours, écrans/démos, documentation métier,
décisions et retours accessibles. Chercher utilisateurs, contexte, alternatives,
difficultés, valeur produite et critères de réussite. Distinguer observation,
documentation, déclaration et inférence. L'absence de télémétrie est une limite.

Puis lire assez de code/tests pour vérifier ce qui existe. Examiner issues ouvertes
ET fermées, PR et refus pertinents. Ne jamais transmettre un extrait privé du repo
à un moteur de recherche.

## 3. Formuler ce qui mérite d'être surveillé

Construire `usage` selon [PROFILE](../../docs/PROFILE.md). Choisir
`product_improvement`, `domain_intelligence` ou `both`. Relier chaque question à
un usage ; ne pas confondre concurrence, implémentation et valeur métier.

## 4. Recherche externe approfondie OBLIGATOIRE

Appliquer [RECHERCHE](../../templates/watch/RECHERCHE.md) : initial, expansion,
challenge. Ouvrir réellement les sources. Explorer au-delà de GitHub/arXiv :
pratiques métier, services, guides, données, normes, communautés, secteurs
adjacents. Consigner requêtes, traces, URLs, dates, découvertes, limites et rejets.

Sans accès externe effectif : profil `draft`, recherche `blocked/partial`, blocage
nommé. Zéro piste nouvelle est acceptable ; inventer une découverte ne l'est pas.

## 5. Déduire DEUX cadences

Ne jamais utiliser une fréquence universelle. Générer `cadence.watch` et
`cadence.postmortem` séparément. Pour chacun :

- `recommendation` et `reason` ;
- `interval_days` ;
- `min_interval_days` et `max_interval_days`.

Fonder la justification sur : rythme observable des releases/normes/publications,
volatilité du domaine, coût de recherche, risque d'obsolescence, criticité d'un
retard et volume attendu de nouveautés actionnables.

Ajouter `cadence.adaptation.min_runs_before_change` et
`decrease_after_consecutive_low_value`. Le post-mortem doit accumuler assez de
runs pour juger le bruit ; une veille hebdomadaire n'implique donc jamais un
post-mortem hebdomadaire. Utiliser les fixtures `cadence-fast.json` et
`cadence-slow.json` comme forme de contrat, pas comme valeurs par défaut.

## 6. Choisir le runtime explicitement

Produire `runtime.mode=dedicated|multiplexed` et une justification.

Choisir `dedicated` pour une veille isolée quand deux places de tâches sont
acceptables. Choisir/proposer `multiplexed` quand plusieurs veilles doivent
partager les mêmes deux tâches physiques ou que les slots sont une contrainte.
Ne pas utiliser le multiplexage pour contourner des limites ou permissions.

En `multiplexed`, définir aussi :

- `group_id` stable ;
- `registry_repository=owner/name`, repo Git canonique du runtime.

Le pack génère `runtime.json`, `multiplex-jobs.json`, `RUNTIME.md`,
`CHATGPT-TASK.md` et `MULTIPLEX-TASKS.md`. L'Orchestrator réserve ; le Worker
résout les jobs dans le registre. Aucun contenu de queue ne gagne d'autorité.
Lire [RUNTIME](../../docs/RUNTIME.md).

## 7. Intégrer l'existant puis générer

Repérer les veilles/schedulers existants : `none`, `coexist`, `reuse-existing`.
Une veille déjà couvrante ne doit pas être lancée en parallèle. Aucun T0 d'un
autre projet n'est importé comme baseline.

Rédiger le profil v2 puis générer le pack. Le moteur local ne browse pas le web
et ne remplace pas l'agent de recherche. Sans terminal, appliquer les mêmes
contrats par connecteur sans prétendre avoir exécuté les tests locaux.
L'état commence en `T0_REQUIRED` ou `INTEGRATION_REQUIRED`.

Le pack contient aussi `WEBSITE.md` et `website.json` : cible PUBLIC séparée
`owner/repo-website`, branche main, Pages depuis la racine. Ce repo n'est jamais
la source de vérité de la veille.

## 8. Installer seulement si autorisé

Écrire uniquement dans `scheduler-techno/`. Un pack divergent, SHA différent ou
checkout modifié bloque l'installateur. Pour un dossier existant, préserver
baseline, runs, état et décisions humaines. Épingler la révision de la fabrique.

L'installation ne crée ni Scheduled Task, ni repo runtime, ni repo website.
En migration `dedicated → multiplexed`, la future activation doit désactiver et
vérifier les tâches dédiées avant `dedicated_tasks_disabled=true`.

## 9. Relire et rendre des résultats vérifiables

Pour chaque repo rendre : SHA, usages, limites, recherches externes, sources,
cadence watch, cadence postmortem, runtime et justification, intégration, fichiers
et commit/PR relu. Distinguer : `généré`, `installé`, `T0 effectué`, `runtime
activé`, `tâches physiques créées`, `repo website créé`, `site publié`, `Pages live`.

Fournir le prompt d'activation sans activer soi-même les tâches dans cette étape.
Aucun résultat inventé. L'échec d'un repo ne masque pas les autres.
