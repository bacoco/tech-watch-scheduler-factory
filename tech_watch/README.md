# Moteur déterministe

`cli.py` : interface ; `github.py` et `snapshot.py` : lecture distante.
`profile.py` : validation du profil écrit par l'agent.
`render.py` : packs spécifiques ; `install.py` : installation locale bornée.
`state.py` : gel T0 et vérification ; `common.py` : primitives sûres.
Aucun module ne crée de Task ni n'appelle un LLM.

`usage.py` : modèle d’usage ; `discovery.py` : journal de recherche ;
`usage_render.py` : vues lisibles ; `fields.py` : contrôles élémentaires.
