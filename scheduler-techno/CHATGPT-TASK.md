# Activation manuelle — runtime dédié

Aucune tâche n'a été créée par la génération.

## Veille
Créer ou réutiliser `Veille — bacoco/tech-watch-scheduler-factory` selon : une fois par semaine, lundi matin (Europe/Paris).
À chaque exécution, relire `https://github.com/bacoco/tech-watch-scheduler-factory/blob/main/scheduler-techno/INSTRUCTIONS.md`, épingler un SHA, appliquer `USAGES.md`, `RECHERCHE.md`, puis T0/UPDATE.
Après un run validé, appliquer `WEBSITE.md` vers `bacoco/tech-watch-scheduler-factory-website`.

## Reprise
Créer ou réutiliser `Reprise — bacoco/tech-watch-scheduler-factory` toutes les 6 heures.
Relire le repo à chaque passage et n'agir que si la dernière occurrence de veille est non terminale et récupérable. Reprendre exactement cette occurrence depuis ses reçus/checkpoints ; ne jamais démarrer un nouveau cycle hors cadence. Une réservation ancienne n'est pas une preuve de concurrence : `CONCURRENT_RUN_ACTIVE` exige une preuve positive d'un writer/lease encore actif. Si rien n'est à reprendre, ne rien faire.

## Post-mortem
Créer ou réutiliser `Post-mortem — bacoco/tech-watch-scheduler-factory` selon : une fois par mois (Europe/Paris).
Lire `POST-MORTEM.md`, accumuler assez de runs et réévaluer séparément les deux cadences sans modifier silencieusement une vraie tâche.
