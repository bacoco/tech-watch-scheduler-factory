# Publication du site public

Ce fichier autorise une sortie publique DISTINCTE du repo source. Lire aussi `website.json`. Le repo source reste canonique pour le profil, le T0, les runs, les reçus et les décisions. Le repo public ne contient que du contenu destiné explicitement à être lu publiquement.

## Cible

Le nom exact est défini dans `website.json`, par défaut `owner/repo-website`. La cible DOIT être un dépôt GitHub public séparé, branche `main`, site statique à la racine. Ne jamais rendre public le repo source pour simplifier le déploiement.

Au premier run de veille :
1. Vérifier si le dépôt public cible existe réellement.
2. S'il n'existe pas et si les droits le permettent, le créer en PUBLIC avec une branche `main` initialisée.
3. S'il existe mais est privé, bloquer la publication et demander une décision explicite.
4. Générer seulement des fichiers de site public : `index.html`, `assets/`, `archive/index.html`, pages d'éditions, `.nojekyll` et métadonnées publiques.
5. Publier ces fichiers sur `main`, idéalement dans un seul commit atomique.
6. Activer GitHub Pages sur `main` + `/(root)` si une capacité administrative réelle est disponible. Sinon publier les fichiers, donner l'URL Settings/Pages exacte et signaler le blocage.

## Ce qui peut être publié

Publier une version éditoriale des résultats déjà validés : synthèse, changements matériels, analyses, implications, limites, sources publiques et archive datée. Les citations vers des sources publiques restent des liens, pas des copies.

Ne JAMAIS publier dans le repo public : profil/state/generation du repo source, T0 brut, baseline brute, reçus, instructions du scheduler, code privé, mails, pièces jointes, secrets ou données utilisateur.

## Structure attendue

- `/index.html` : dernière édition + accès aux récentes ;
- `/archive/index.html` : archive chronologique ;
- `/<slug>/index.html` : une édition stable ;
- `/assets/style.css` : thème local ;
- `/.nojekyll` : publication directe du HTML généré.

Une édition identique est un no-op. Un même slug avec contenu différent ne doit pas être écrasé silencieusement. Après chaque T0/UPDATE achevé, publier ou rafraîchir le site seulement avec les éléments autorisés publiquement.

## Preuves de livraison

Après écriture, relire au minimum la home, l'archive, l'édition créée et le CSS. Rapporter repo public exact, commit, fichiers créés/modifiés, statut Pages et URL publique seulement si vérifiée.
