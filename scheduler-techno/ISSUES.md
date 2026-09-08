# Transformer les résultats en propositions utiles

## Conditions nécessaires

La source a été réellement lue ; l'intérêt pour le repo est expliqué ; un manque ou une décision identifiable subsiste ; l'existant et les contraintes sont pris en compte. Sinon conserver au rapport, sans issue. La limite de `profile.json` est un plafond, pas un quota.

## Déduplication et décision

Consulter le registre local, puis les issues ouvertes/fermées et les PR liées. Identifier par repo cible + usage + sujet/décision, pas par titre d'article seul. Plusieurs sources peuvent justifier une seule issue. Les refus sont conservés avec motif et conditions de réouverture.

Utiliser un marqueur stable `<!-- tech-watch:<sha256> -->` dans chaque proposition. Après une panne ambiguë, rechercher ce marqueur avant de réessayer.

## Corps attendu

Titre : `[Veille] <décision ou expérience liée à un usage>`.
- Conclusion et intérêt pour CE projet.
- Source précise, version, parties lues et limite de preuve.
- Usage et état actuel.
- Manque ou avantage potentiel, raisons de ne pas adopter immédiatement.
- Plus petite expérience/modification envisageable, critères de réussite.
- Compatibilité avec contraintes, risques, inconnues et alternatives.
- Liens des décisions existantes, identifiant stable et reçu du run.

Séparer « hypothèse à évaluer » de « amélioration mesurée ». Aucun gain de coût, qualité ou vitesse ne doit être inventé. Une issue créée doit être relue et référencée.
