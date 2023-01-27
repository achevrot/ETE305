# ETE305

## Devoirs pour vendredi 3 février

- Algo utilisé : Paired comparison method for Multicrietria Decision Making (MCDM) with discrete alternatives.
- Variables de décision : poids associé à chaque critère
- Contraintes :
    - Somme CO2 optimisé < Somme CO2 tendanciel
    - Nbre de passagers dont le vol est supprimé et qui doivent utilier le train < Nombre de places vides dans le train avant optimisation
- Critères : 
    - CO2 émis
    - Nombre de passagers
    - Distance 

## Tuto Github

1. Ouvrir votre éditeur de code (VS Code, PyCharm, ...)
2. Ouvrir le fichier ETE305 dans cet éditeur
3. Ouvrir le terminal

`git status` permet de connaître le statut, c'est-à-dire savoir si votre copie du dépôt est à jour ou pas. Si quelqu'un d'autre a fait des modifications, il va falloir les "importer" sur votre PC

### Comment récupérer les données sur le dépôt ?

`git pull` permet d'"importer" la version la plus récente, à faire avant de commencer à coder pour être sûr d'avoir la dernière version.

### Comment envoyer un fichier dans le dépôt ?

Si vous voulez partir de zéro sur un nouveau fichier, il faut d'abord créer le fichier localement sur votre PC dans le fichier ETE305. Ensuite : 

`git add [nom_fichier]` À faire pour dire quels fichiers modifiés/ajoutés doivent être pris en compte un nouveau fichier sur le github.

`git commit -m "message expliquant la modification"` Permet d'annoncer la modification.

`git push` Permet d'envoyer ses modifications à tout le monde.