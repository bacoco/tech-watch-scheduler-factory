# Transformer les résultats en propositions utiles

## Conditions nécessaires

La source a été réellement lue ; l'intérêt pour le repo est expliqué ; un manque
ou une décision identifiable subsiste ; l'existant et les contraintes sont pris
en compte. Sinon conserver au rapport, sans issue.
La limite de `profile.json` est un plafond, pas un quota à atteindre.
Aucun label ne doit déclencher automatiquement un agent de développement.

## Informations de domaine

Une synthèse, un changement de pratique ou une information utile au public peut
constituer le résultat principal de la veille. Ne pas inventer de patch ni créer
une issue de développement pour la justifier. Écrire la synthèse dans les runs ;
aucune publication externe ni modification du produit sans autorisation.

## Déduplication et décision

Consulter le registre local, puis les issues ouvertes/fermées et les PR liées,
en paginant les résultats utiles. Identifier par repo cible + usage + sujet/décision,
pas par titre d'article seul. Plusieurs sources peuvent justifier une seule issue.
Une version plus récente d'un papier met à jour la même analyse.
Les refus sont conservés avec motif et conditions de réouverture.

Utiliser un marqueur stable `<!-- tech-watch:<sha256> -->` dans chaque proposition.
Après une panne ambiguë, rechercher ce marqueur avant de réessayer. Ce mécanisme
permet la réconciliation, pas une promesse d'exactement-une-fois distante.

## Corps attendu

Titre : `[Veille] <décision ou expérience liée à un usage>`.

- Conclusion et intérêt pour CE projet.
- Source précise, version, parties lues et limite de preuve.
- Usage et état actuel ; fichiers/lignes/SHA seulement si une intégration est proposée.
- Manque ou avantage potentiel, et raisons de ne pas adopter immédiatement.
- Plus petite expérience/modification envisageable, critères de réussite.
- Compatibilité avec les contraintes, risques, inconnues et alternatives.
- Liens des décisions existantes, identifiant stable et reçu du run.

Séparer « hypothèse à évaluer » de « amélioration mesurée ». Aucun gain de coût,
qualité ou vitesse ne doit être inventé. Ne pas recopier de secrets ni données
privées dans un repo public. Une issue créée doit être relue et référencée.
