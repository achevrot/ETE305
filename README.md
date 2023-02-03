# ETE305

## Modélisation du problème

- Notations : on travaille sur les vols $i$ et les avions $j$. 
    - $s_{i,j}$ : On utilise l'avion $j$ pour effectuer le vol $i$, booléen
    - $CO2_{i,j}$ : émissions $CO_2$ du vol $i$ effectué avec l'avion $j$
    - ${p_0}_i$ : Nombre de passagers initiaux dans le vol $i$.
    - place_train : nombre de places libres dans les trains.
    - $N_j$ : Nombre d'avions de type $j$ disponibles.
    - $N0_j$ : Nombre d'avions de type $j$ initialement disponibles.
    - $C_j$ : Capacité en passagers de l'avion de type $j$.
    - $B_j = N_j-N0_j$ : Nombre d'avions de type $j$ à construire.
    - $ICO2_j$ : Impact carbone de la construction de l'avion de type $j$.
    - $p_i$ : nombre de passagers dans le vol $i$


- Variables de décision :
    - Booléen $s_{i,j}$
    - Variable entière : $p_i$, bornée entre $0$ et $p0_i$
    - Variable entière : $N_j$

- Contraintes :
    - Limite sur le nombre d'avions d'un certain type :   $\forall j \quad \sum_i s_{i,j} \leq N_j$
    - Limite sur la capacité en passagers de l'avion : $\forall i,j \quad p_i \cdot s_{i,j} \leq C_j$
    - Limite en capacité en passagers de train : $\sum_i (p0_i - p_i) \leq$ place_train
    - On ne peut pas détruire des avions : $\forall j \quad N_j \geq N0_j$
    - Plusieurs avions n'effectuent pas le même trajet : $\forall i \quad \sum_j s_{i,j} \leq 1$
   
- Critères : min $\sum_{i,j} CO2_{i,j} \cdot s_{i,j}   + \sum_j B_j \cdot ICO2_j $
    - Hypothèse : dans un premier temps, on néglige les émissions de CO2 des trains, mais il faudra en tenir compte.

## À faire

- Dans `flights_and_emissions.csv` : rajouter une colonne capacité -> Constant
- Créer un csv (ou autre) qui contient les émissions de fabrication pour chaque type d'avion -> Flo
- Créer un csv avec les colonnes : ville1, ville2, nombre de places libres pour aller de ville1 à ville 2 par jour -> Flo
    - Pour ça, besoin de beaucoup d'hypothèses !!! 
    - ville1 et ville 2 à extraire du tableau `flights_and_emissions.csv`
    - Les chiffres qu'on a :
        - 82 000 000 de passagers longue distance par an
        - 31,4% de taux d'occupation
    - trouver une manière de pondérer les places disponibles selon le trajet (yolo)

Idée du tableau attendu :
| Ville 1 | Ville 2 | Nombre de places libres par jour | CO2 émis / passager |
|--------------|-----------|------------|------------|
| | | | |
| | | | |

- Ajouter au tableau précédent les émissions de CO2 par passager sur chaque trajet ville1 - ville2 -> Constant

Si possible, ce qui est au-dessus fait max le vendredi 10 février

- Implémenter la nouvelle optimisation -> Apolline, le week-end du 11-12 février

## Tuto Github - en local

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
