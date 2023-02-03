# ETE305

## Devoirs pour vendredi 3 février

- Notations : on travaille sur les vols. 
    - $s_i$ : Statut du vol, booléen, `True`: vol maintenu, `False` : vol supprimé
    - $CO2_i$ : émissions CO2 du vol
    - $p_i$ : nombre de passagers dans le vol
    - place_train : nombre de places libres dans les trains.
- Variables de décision : vol supprimé ou non
    - Booléen $s_i$
- Contraintes :
    - $\sum_i p_i \cdot(1-s_i) <$ place_train
- Critères : min $\sum_i CO2_i \cdot s_i$
    - Hypothèse : dans un premier temps, on néglige les émissions de CO2 des trains, mais il faudra en tenir compte.

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


### Sources :

Selon l'ADEME, la construction d'un avion à un coût carbone de 40 kgCO2/kg d'avion.
https://bilans-ges.ademe.fr/documentation/UPLOAD_DOC_FR/index.htm?aerien.htm
D'après le rapport du Shift Project et Aero decarbo, un avion a une durée de vie de 15 à 25 ans. Nous prendrons donc 20 ans.
Donc, sur une année, le coût carbone de la construction d'un avion est de 2kg de CO2 par kg d'avion.

`git commit -m "message expliquant la modification"` Permet d'annoncer la modification.

`git push` Permet d'envoyer ses modifications à tout le monde.
