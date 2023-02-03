# ETE305

## Devoirs pour vendredi 3 février

- Notations : on travaille sur les vols. 
    - $s_{i,j}$ : On utilise l'avion de type j pour effectuer le vol i
    - $CO2_{i,j}$ : émissions CO2 du vol i, effectué avec l'avion j
    - $p_i$ : nombre de passagers dans le vol i
    - $p0_i$ : Nombre de passagers initiaux dans le vol j.
    - place_train : nombre de places libres dans les trains.
    - $N_j$ : Nombre d'avions de type j disponibles.
    - $N0_j$ : Nombre d'avions de type j initialement disponibles.
    - $C_j$ : Capacité en passagers de l'avion de type j.
    - $B_j$ : Nombre d'avions de type j à construire.
    - $ICO2_j$ : Impact carbone de la construction de l'avion de type j.

- Variables de décision :
    - Booléen $s_{i,j}$
    - Variable entière : $p_i$ : Nombre de passagers présents en avion dans le vol i.
    - Variable entière : $N_j$ : Nombre d'avions de type j conservés.


- Contraintes :
    - Limite sur le nombre d'avions d'un certain type :   $\sum_i s_{i,j} < N_j $
    - Limite sur la capacité en passagers de l'avion : $ p_i \cdot s_{i,j} < C_j $
    - Limite en capacité en passagers de train : $\sum_i (p0_i - p_i) < $ place_train
    - Impact carbone de la construction d'un nouvel avion : $ N_j - N0_j = B_j \cdot(ICO2_j) $
    - On ne peut pas détruire des avions : $ N_j >= N0_j $
    - Plusieurs avions n'effectuent pas le même trajet : $ \sum_j s_{i,j} <= 1 $
   
- Critères : min $\sum_{i,j} CO2_{i,j} \cdot s_{i,j}   + \sum_j B_j \cdot ICO2_j $
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

`git commit -m "message expliquant la modification"` Permet d'annoncer la modification.

`git push` Permet d'envoyer ses modifications à tout le monde.


### Sources :

Selon l'ADEME, la construction d'un avion à un coût carbone de 40 kgCO2/kg d'avion.
https://bilans-ges.ademe.fr/documentation/UPLOAD_DOC_FR/index.htm?aerien.htm
D'après le rapport du Shift Project et Aero decarbo, un avion a une durée de vie de 15 à 25 ans. Nous prendrons donc 20 ans.
Donc, sur une année, le coût carbone de la construction d'un avion est de 2kg de CO2 par kg d'avion.
