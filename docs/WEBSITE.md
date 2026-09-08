# Site public associé à une veille

## Principe

Le repo surveillé reste la source de vérité. Le site est publié dans un dépôt
GitHub public séparé nommé par défaut `owner/repo-website`. Cette séparation est
obligatoire : elle permet d'utiliser GitHub Pages sans rendre public le code,
les instructions, le T0, les runs ni les preuves privées du repo source.

Chaque pack `scheduler-techno/` contient `WEBSITE.md` et `website.json`.
Le premier décrit le contrat de publication ; le second donne la cible exacte.
La génération du pack ne crée aucun repo et ne publie rien. Le scheduler créé
ensuite par ChatGPT réalise ce bootstrap au premier passage s'il possède les
droits nécessaires.

## Premier passage du scheduler

La tâche de veille doit :

1. relire `INSTRUCTIONS.md`, `WEBSITE.md` et `website.json` au SHA épinglé ;
2. vérifier l'existence du repo public cible ;
3. le créer en PUBLIC s'il n'existe pas et si l'outil GitHub l'autorise ;
4. s'assurer que la branche `main` existe ;
5. publier le site statique à la racine de `main` ;
6. activer GitHub Pages sur `main` + `/(root)` si cette capacité existe ;
7. relire home, archive et édition avant d'annoncer la publication.

Si l'outil GitHub peut écrire mais pas administrer Pages, la tâche conserve les
fichiers publiés et rend l'URL directe `https://github.com/OWNER/REPO/settings/pages`
comme blocage explicite. Elle ne déclare pas le site live avant vérification.
Si la création du repo elle-même est impossible, la veille peut continuer dans
le repo source mais `website_status` reste bloqué.

## Format d'une édition pour le renderer local

Le renderer attend un JSON contenant :

- `slug` : chemin stable de l'édition, en minuscules et tirets ;
- `date` : date ISO `YYYY-MM-DD` ;
- `title` : titre public ;
- `excerpt` : résumé court public ;
- `body_html` : corps HTML déjà construit par l'agent.

Le HTML actif est refusé : scripts, iframes, objets, formulaires, base/meta,
URL `javascript:`, `srcdoc` et attributs d'événements. Le renderer ne récupère
aucune donnée et n'appelle aucun modèle ; il assemble uniquement une sortie
publique déterministe.

Le helper `tools/render_public_website.py` expose la commande `website-render`
du package. Il écrit `index.html`, `archive/index.html`, la page d'édition,
`assets/style.css`, `.nojekyll` et `site.json`. Une édition identique est un
no-op. Un slug existant avec un contenu différent est refusé par défaut ; une
correction volontaire doit utiliser `--replace-existing`.

Le helper `tools/create_public_website_repo.py` est un fallback local explicite.
Sans `--apply`, il ne fait qu'afficher le plan. Avec `--apply`, il nécessite
`GITHUB_TOKEN`, crée ou vérifie le repo public séparé et initialise `main`.

Le helper `tools/publish_public_website.py` vérifie ensuite la sortie rendue et
la publie en un seul commit Git atomique sur `main`. Il préserve les anciennes
pages déjà présentes dans le repo public et peut activer Pages avec
`--enable-pages`. Sans `--apply`, il ne fait qu'afficher le plan de publication.

## Structure publique

Le site produit est volontairement simple : HTML/CSS statique, sans backend et
sans dépendance JavaScript obligatoire.

- `/index.html` : dernière édition et cartes récentes ;
- `/archive/index.html` : toutes les éditions ;
- `/<slug>/index.html` : édition complète ;
- `/assets/style.css` : thème responsive ;
- `/.nojekyll` : empêche une transformation Jekyll non demandée ;
- `/site.json` : métadonnées publiques d'archive uniquement.

Le scheduler peut enrichir le design pour un projet donné, mais doit préserver
ces routes et la compatibilité GitHub Pages.

## Confidentialité

Le site public ne reçoit jamais les fichiers de `scheduler-techno/`, la baseline,
les reçus, les checkpoints, le code privé, les mails ou pièces jointes. Une
information privée ne peut être publiée que sous forme d'abstraction explicitement
autorisée. L'absence de secret détecté n'est pas une autorisation de publication.

Les sources publiques peuvent être liées. Les contenus tiers ne sont pas copiés
intégralement. Le repo website ne devient jamais la source de vérité pour la
veille : il est une projection éditoriale reproductible du contenu validé.
