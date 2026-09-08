# Deux demandes courtes dans ChatGPT, prompts canoniques dans le repo

Le [README](../README.md) ne contient volontairement que deux mini-prompts. Toute la logique détaillée est versionnée dans :

- [`prompts/PREPARE.md`](../prompts/PREPARE.md) pour préparer le repo cible ;
- [`prompts/ACTIVATE.md`](../prompts/ACTIVATE.md) pour activer la veille et le website.

L'utilisateur fournit uniquement `TARGET_REPOSITORY` via le lien du repo sur lequel il travaille. Cela évite de recopier de longs prompts et garantit que les futures corrections de la factory sont lues depuis GitHub.

## Premier prompt : préparer le repo cible

ChatGPT applique `prompts/PREPARE.md`, comprend les usages, recherche réellement sur Internet, puis publie `scheduler-techno/` selon les autorisations du dépôt. Cette première demande ne lance pas T0 et ne crée aucune Scheduled Task ni repo website.

Le profil propose séparément `cadence.watch` et `cadence.postmortem`, puis choisit explicitement `runtime.mode=dedicated|multiplexed` avec justification.

## Deuxième prompt : activer ce runtime

ChatGPT applique `prompts/ACTIVATE.md` au même repo cible et relit `runtime.json` au lieu de supposer deux tâches identiques.

### dedicated

Créer ou réutiliser deux tâches distinctes :

- `Veille — repo`, avec la cadence `watch` ;
- `Post-mortem — repo`, avec la cadence `postmortem`.

La veille réalise/reprend T0 puis UPDATE. Le post-mortem lit `POST-MORTEM.md`, mesure la qualité des runs et réévalue les deux cadences séparément. Une recommandation de fréquence ne modifie pas automatiquement la vraie tâche.

### multiplexed

Ne créer aucune tâche propre au repo. Le profil fournit `group_id` et `registry_repository`. Enregistrer les jobs de `multiplex-jobs.json` dans le registre canonique puis créer/réutiliser seulement :

- `Tech Watch Orchestrator — group_id` ;
- `Tech Watch Worker — group_id`.

Les textes restaurables sont dans `MULTIPLEX-TASKS.md`. L'Orchestrator réserve un job sans exécuter le métier. Le Worker résout le `job_id` dans le registre Git et refuse tout chemin/prompt ajouté dans la queue.

## Website

Dans les deux modes, après chaque T0/UPDATE validé, `prompts/ACTIVATE.md` impose de créer ou réutiliser le repo public `*-website`, générer ou mettre à jour la home, l'archive et l'édition, pousser sur `main`, puis maintenir le site à chaque cycle suivant. GitHub Pages est activé lorsque la capacité existe.

## Migration

Avant `dedicated → multiplexed`, désactiver réellement les anciennes tâches, relire leur état et conserver la preuve. Seulement ensuite le registre peut porter `dedicated_tasks_disabled=true`. La migration inverse suit le même principe. Ne jamais laisser les deux modes exécuter la même veille en parallèle.

## Cadence

Une tâche est créée selon la recommandation du profil, pas un lundi/vendredi universel. Le post-mortem peut proposer `keep`, `increase` ou `decrease` après une fenêtre suffisante, avec preuves et rollback. Une modification réelle du calendrier nécessite l'outil de planification et les permissions correspondantes.

## Accès et création vérifiés

Vérifier dans l'environnement réel : lecture GitHub, recherche externe, écriture, issues, création de repo runtime si nécessaire, repo website et Pages. Les outils et autorisations du chat ne prouvent pas ceux de la tâche future. Respecter les approbations requises et nommer tout blocage.

Confirmer pour chaque tâche physique son identifiant, nom, calendrier, fuseau et état retournés par l'outil. Distinguer tâche créée, activée et premier passage réussi. Un prompt ou fichier ne remplace pas une tâche exécutante.

## Capacité du compte

En `dedicated`, une veille consomme deux places de tâches. En `multiplexed`, un groupe de N veilles logiques vise deux places physiques, sans contourner aucune limite produit : les jobs s'exécutent séquentiellement via le slot unique. Vérifier les places effectivement disponibles avant activation.

L'[aide officielle](https://help.openai.com/en/articles/10291617-tasks-in-chatgpt) mentionne les comptes gratuits éligibles sous réserve des fonctionnalités, quotas et permissions disponibles. Aucune gratuité illimitée n'est promise.
