# Capacités à vérifier dans la vraie tâche

## Obligatoires

Lecture du repo à SHA fixe ; recherche Internet ouverte et lecture effective des pages pertinentes ; création/lecture des artefacts et états dans `scheduler-techno/`. Pour une publication d'issues : création ET lecture d'issues, commentaires, recherche des propositions existantes et autorisation de destination.

## Runtime dedicated

Vérifier l'outil de planification, les places disponibles, la création/lecture de deux tâches distinctes et la capacité à modifier leur calendrier seulement avec autorisation explicite. Une recommandation de cadence n'est pas une preuve de modification de la Scheduled Task.

## Runtime multiplexed

Vérifier en plus lecture/écriture du `registry_repository`, écriture contrôlée du slot `current-action/`, lecture des repos cibles, création/réutilisation Orchestrator + Worker et possibilité de vérifier la désactivation des anciennes tâches dédiées.

## Website

La projection publique exige écriture dans le repo `*-website`; l'activation GitHub Pages peut nécessiter une permission d'administration distincte. Ne pas confondre fichiers publiés et site réellement live.

## Preuve d'accès

Conserver outil utilisé, scope exact, résultat et date. Ne pas inclure les tokens. La présence d'un connecteur, bouton ou documentation n'est pas une preuve d'exécution. Ne pas confondre lecture GitHub et écriture GitHub.

## Refus et pannes

Source manquante : noter le manque. Écriture absente : produire le rapport possible et marquer la livraison bloquée ; ne pas avancer l'état ni inventer une issue. Autorisation interactive requise : la respecter, ne pas la contourner.

Aucune tâche réelle n'est créée par ces fichiers. Les états de runtime restent `not_created` / `not_activated` tant qu'identifiants et confirmations réels manquent.
