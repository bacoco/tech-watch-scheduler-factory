# Preuves de vérification

[Publication confirmée](publication-confirmed-2026-09-07.json) : commit de code
relu sur main, arbre Git identique à la version locale, 105 tests locaux réussis
et limite de la CI distante, qui n'a exécuté aucune étape sur le premier run.

[Contrôles locaux initiaux](local-2026-09-07.json) : les 102 tests et contrôles
de l'étape précédente, avant les trois tests supplémentaires du README.
[Ancien refus de publication](github-publication-2026-09-07.json) : HTTP 403
avant la mise à jour des autorisations ; conservé uniquement comme historique.

Les tests utilisent des recherches synthétiques et des réponses réseau simulées.
Ils contrôlent la mécanique, pas la qualité d'une recherche réelle. Une réussite
locale ne vaut pas réussite du workflow GitHub Actions.

Aucune tâche n'a été activée, aucun profil installé dans un repo cible, aucun T0
réel effectué. Voir [la livraison](../DELIVERY.md) pour les frontières exactes.
