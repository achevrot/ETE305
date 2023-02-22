# ETE305

Slides : 
https://docs.google.com/presentation/d/1PPGJkFX__X4g9yJG4p3WRMIzL1cTqfYSVBUSeDgx-1M/edit?usp=sharing

## Abstract : Impact de la gestion du trafic ferroviaire sur le bilan carbone du trafic aérien en Allemagne

Notre étude s’intéresse à la minimisation du bilan carbone de la mobilité collective intérieure à l’Allemagne, et plus particulièrement aux trafics aériens et ferroviaires. Tout en conservant le même nombre de passagers entre la situation initiale et la situation finale (pas de sobriété), nous proposons d’activer 2 leviers :

1)	Le report modal de l’avion vers le train
2)	Le remplacement d’avions fortement émetteurs de GES vers d’autres moins émetteurs (par exemple des avions plus petits)

Et ce, sachant qu’il est possible de construire de nouveaux avions, mais au prix d’un certain coût carbone.
Les décisions prises par notre algorithme dépendent de l’arbitrage fait sur 2 paramètres :

1)	Le taux de remplissage maximal des trains   
2)	La répartition des places de train entre les axes reliant 2 villes de plus de 500 000 habitants, et ceux qui n’en relie pas.

Nos principaux résultats sont les suivants :

## Notes

- Faire un titre + abstract en 120 mots : qu'est-ce qu'on a fait, comment on s'y est pris et le résultat. Pour la veille. + lien git
- Présentation de 15 minutes.
- Mail : xavier.olive@onera.fr ; antoine.chevrot@onera.fr ; olivier.poitou@onera.fr

## Nouvelle modélisation

On s'intéresse aux vols intérieurs en Allemagne. Nous travaillons sur chaque couple de ville, défini comme un trajet possible. Par exemple, tous les vols effectuant Berlin -> Munich seront traités ensemble. Les vols Munich -> Berlin seront traités séparément. Cette décision a été prise car elle facilite la prise en comtpe du report modal : la contrainte sur le nombre de places disponibles en train est en effet propre à chaque trajet : un passagers sur le vol Berlin -> munich occupera une place train disponible sur Berlin -> Munich, et pas sur Hambourg -> Cologne, chaque trajet est donc indépendant des autres (les correspondances ne sont pas prises en compte, car nous n'avons pas d'information à ce sujet).

Nous avons ainsi dénombré 368 trajets. La modédlisation expliquée par la suite est faite indépendamment pour chaque trajet allant d'une ville `v1` à une ville `v2`.

Période sélectionnée : mars 2019.

### Notations
- $passagers_{init}$: nombre entier, nombre de passagers sur les vols initiaux de `v1` à `v2` pendant la période sélectionnée.
- $place_{train}$ : nombre entier, nombre de places disponbibles dans les trains entre `v1` et `v2` pendant la période sélectionnée.
- $n$ : nombre entier, nombre de vols entre `v1` et `v2` pendant la période sélectionnée.
- $m = 52$ : nombre entier, nombre de type d'avions répertoriés dans notre analyse.
- $j$ : nombre entier, indice utilisé pour parler d'un type d'avions, $j$ va de $0$ à $m-1$.
- $N_0$ : tableau d'entiers, de taille $m$, contenant le nombre d'avions de type $j$ faisant le trajet de `v1` à `v2` pendant la période sélectionnée.
- $CO_2$ : tableau de taille $m$, contenant les émissions de CO$_2$ (en kg) d'un avion de type $j$ faisant le trajet de `v1` à `v2`.
- $capacite$ : tableau d'entiers, de taille $m$, contenant le nombre de passagers pouvant monter à bord d'un avion de type $j$.
- ${CO_2}_{train}$ : valeur représentant les émissions de CO$_2$ (en kg) par passager pour un trajet en train entre `v1` et `v2`.
- ${CO_2}_{constr}$ : tableau de taille $m$ contenant les émissions de CO$_2$ pour la construction d'un nouvel avion de type $j$.

### Variables de décision

- `nb_passagers[j]`, $j\in [0,m-1]$ : indique le nombre de passagers prenant un vol de `v1` à `v2` dans un type d'avion $j$ pendant la période sélectionnée. Cette variable compte donc seulement les personnes prenant l'avion, et pas le train (le nombre de personnes prenant le train est $passagers_{init} - \sum_j$ `nb_passagers[j]`).
- `nb_avions[j]`, $j\in [0,m-1]$ : nombre de vols d'un avion de type $j$ de `v1` à `v2` pendant la période sélectionnée. C'est bien le nombre de vols, et pas le nombre d'appareils : si un même appareil réalise 2 fois le trajet, il compte pour 2 et pas 1.
- `nb_nouv_avions[j]`, $j\in [0,m-1]$ : quantité de nouveaux avions de type $j$ à construire.

Il y a donc 52x3 = 156 variables de décisions pour chaque trajet.

### Contraintes

- Le nombre de passagers doit être positif ou nul : $\forall j\quad$ `nb_passagers[j]` $\geq 0$
- On ne crée pas de nouveaux passagers : $\sum_j$ `nb_passagers[j]` $\leq passagers_{init}\quad\Rightarrow\quad 0\leq passagers_{init}-\sum_j$ `nb_passagers[j]`
- Le nombre de personnes prenant le train ne doit pas excéder le nombre de places libres en train : $passagers_{init}-\sum_j$ `nb_passagers[j]` $\leq place_{train}$
- Le nombre de vols doit être positif ou nul : $\forall j\quad$ `nb_avions[j]` $\geq 0$
- Le nombre de nouveaux avions doit être positif ou nul : $\forall j\quad$ `nb_nouv_avions[j]` $\geq 0$
- Le nombre d'avions de type $j$ doit être égal au rapport entre le nombre de passagers empruntant un avion de type $j$ et la capacité de l'avion. Comme ce dernier n'est pas forcément un nombre entier, cette contrainte est définie comme étant élastique, afin d'avoir une tolérance sur l'égalité : $\forall j\quad$ `nb_passagers[j]` - `nb_avions[j]` $\times capacite_j = 0$
- Le nombre de passagers ne peut pas excéder la capacité maximale de tous les vols disponibles : $\forall j \quad$ `nb_passagers[j]` $\leq capacite_j \times({N_0}_j-$ `nb_nouv_avions[j]`)

### Fonction objectif
On veut minimiser : $(\sum_j {CO_2}_j\times nb_avions[j]$ 

Les valeurs sont divisées par 1000, pour passer en tonnes de CO$_2$ et éviter d'avoir des valeurs trop élevées, plus compliquées à traiter informatiquement.

### Remarques

- Le report ne prend pas en compte les horaires précis des vols et des trains, mais seulement un décompte global sur le mois de mars 2019.
- Ne prends pas en compte le fait que créer un nouvel avion permet de faire plusieurs vols avec.
- On pourrait essayer de faire les calculs avec les émissions CO$_2$ de train pour la France, pour voir l'impact du facteur d'émission du mix électrique.
- On pourrait essayer de prendre en compte plusieurs mois (pour l'instant, seuls les vols de mars 2019 sont pris en compte).

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

## Notes

- Faire un titre + abstract en 120 mots : qu'est-ce qu'on a fait, comment on s'y est pris et le résultat. Pour la veille. + lien git
- Présentation de 15 minutes.
- Mail : xavier.olive@onera.fr ; antoine.chevrot@onera.fr ; olivier.poitou@onera.fr

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
