# Publication du site public

Ce fichier autorise une sortie publique DISTINCTE du repo source. Lire aussi
`website.json`. Le repo source reste canonique pour le profil, le T0, les runs,
les reçus et les décisions. Le repo public ne contient que du contenu destiné
explicitement à être lu publiquement.

## Cible

Le nom exact est défini dans `website.json`, par défaut `owner/repo-website`.
La cible DOIT être un dépôt GitHub public séparé, branche `main`, site statique
à la racine. Ne jamais rendre public le repo source pour simplifier le déploiement.

Au premier run de veille :

1. Vérifier si le dépôt public cible existe réellement.
2. S'il n'existe pas et si les droits le permettent, le créer en PUBLIC avec
   une branche `main` initialisée.
3. S'il existe mais est privé, ne jamais changer sa visibilité silencieusement :
   bloquer la publication et demander une décision explicite.
4. Générer seulement des fichiers de site public : `index.html`, `assets/`,
   `archive/index.html`, pages d'éditions, `.nojekyll` et métadonnées publiques.
5. Publier ces fichiers sur `main`, idéalement dans un seul commit atomique.
6. Activer GitHub Pages sur `main` + `/(root)` si une capacité administrative
   réelle est disponible. Sinon publier les fichiers, donner l'URL Settings/Pages
   exacte et signaler que l'activation reste bloquée ; ne pas prétendre que le
   site est live.

## Ce qui peut être publié

Publier une version éditoriale des résultats déjà validés : synthèse, changements
matériels, analyses, implications, limites, sources publiques et archive datée.
Une source privée peut informer une analyse seulement si l'abstraction publique
est autorisée ; ne jamais publier le mail, document, extrait privé ou identifiant.
Les citations vers des sources publiques restent des liens, pas des copies.

Ne JAMAIS publier dans le repo public :

- `profile.json`, `state.json`, `generation.json`, `website.json` du repo source ;
- `T0.md`, baseline brute, reçus, checkpoints ou rapports internes de runs ;
- instructions du scheduler, prompts, permissions, tokens ou secrets ;
- code privé, fichiers produit, pièces jointes ou données utilisateur ;
- une affirmation qui n'a pas passé les contrôles de statut/source du run.

## Structure attendue

Le site est statique et navigable :

- `/index.html` : dernière édition + accès aux récentes ;
- `/archive/index.html` : archive chronologique ;
- `/<slug>/index.html` : une édition stable ;
- `/assets/style.css` : thème local sans dépendance requise ;
- `/.nojekyll` : publication directe du HTML généré.

Les liens internes sont relatifs. Le rendu doit être responsive et lisible sans
JavaScript. Les tableaux larges doivent rester consultables sur mobile.

## Idempotence, corrections et historique

Une édition existante avec le même slug et le même contenu est un no-op.
Une édition existante avec le même slug mais un contenu différent ne doit pas
être écrasée silencieusement. Une correction du même document est permise
uniquement comme remplacement explicite et traçable ; sinon utiliser un nouveau
slug selon la politique du projet. Ne jamais supprimer l'archive pour reconstruire
la home.

Après chaque T0 achevé ou UPDATE achevé, publier ou rafraîchir le site seulement
avec les éléments de ce run qui sont autorisés publiquement. Un échec du site
ne transforme pas une veille réussie en veille ratée : consigner séparément
`watch_status` et `website_status`.

## Preuves de livraison

Après écriture, relire au minimum la home, l'archive, l'édition créée et le CSS.
Vérifier que les liens Home/Archive/édition ciblent le repo public. Rapporter :
repo public exact, commit, fichiers créés/modifiés, statut Pages et URL publique
si elle répond réellement. Une URL calculée mais non vérifiée n'est pas une
preuve de publication.
