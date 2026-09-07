# Deux demandes dans ChatGPT, puis deux tâches distinctes

## Premier prompt : préparer le repo cible

Le [README](../README.md) contient les deux demandes en langage naturel.
L'utilisateur ouvre un chat ChatGPT et remplace le lien du repo cible.
ChatGPT lit la fabrique, comprend les usages, recherche réellement sur Internet,
puis publie le dossier scheduler-techno selon les autorisations du dépôt.
Cette première demande ne lance pas le T0 et ne crée aucune tâche.
Le parcours ne requiert ni terminal utilisateur ni passage dans Codex ou Claude.

## Deuxième prompt : activer deux tâches

Toujours dans ChatGPT, demander deux tâches distinctes pour le même repo :
la veille le lundi matin et le post-mortem le vendredi matin, Europe/Paris,
ou aux créneaux expressément choisis par l'utilisateur.

Le pack fournit CHATGPT-TASK.md comme entrée vers les instructions de veille.
La tâche de veille réalise ou reprend le T0, puis passe aux mises à jour.
Le post-mortem lit POST-MORTEM.md et les résultats observés pour améliorer les
instructions dans le cadre autorisé. Ne pas fusionner ce second travail dans
la tâche de veille. La fabrique ne crée aucun objet planifié à la génération.

Chaque tâche conserve le repo cible, sa branche réelle et son point d'entrée.
Elle relit les instructions à chaque passage et épingle un SHA pour le cycle ;
elle ne dépend pas d'une copie figée du chat ni de sa mémoire implicite.
Réutiliser les tâches équivalentes existantes au lieu de créer des doublons.

## Accès et création vérifiés

Vérifier dans l'environnement réel de chaque tâche la lecture du repo, la
recherche externe, l'écriture des résultats et les droits sur les issues.
Les outils et autorisations du chat ne prouvent pas ceux de la tâche future.
Respecter les approbations requises : elles peuvent mettre une tâche en pause.
Nommer ce blocage ; ne jamais contourner l'autorisation ni promettre l'autonomie.

Confirmer pour chaque tâche son identifiant, son nom, son calendrier, son fuseau
et son état réellement retournés par l'outil. Distinguer tâche créée, activée et
première exécution réussie. Sans outil disponible, aucune création n'est acquise.
Un simple rappel, un prompt ou un fichier ne remplace pas une tâche exécutante.

## Gratuité et capacité du compte

Le parcours utilise ChatGPT sans serveur ni clé d'API externe à configurer.
L'[aide officielle](https://help.openai.com/en/articles/10291617-tasks-in-chatgpt)
mentionne les comptes gratuits éligibles, sous réserve des fonctionnalités,
quotas et permissions disponibles. Cela ne garantit pas que tous les comptes
possèdent les accès GitHub nécessaires ou les mêmes possibilités d'écriture.

Deux tâches par repo nécessitent deux places. Vérifier la capacité effective
avant création, sans supprimer les autres tâches pour libérer des places.
Le créneau « matin » ne suppose pas une heure exacte réservée à certains plans.
Aucun nombre fixe de tâches ni aucune gratuité illimitée n'est promis ici.
