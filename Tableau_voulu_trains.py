import pandas as pd
import csv



aeroport1 = pd.read_csv('flights_and_emissions.csv', usecols=['ADEP'])
aeroport2 = pd.read_csv('flights_and_emissions.csv', usecols=['ADES'])




ville1=[]
ville2 = []
liste_villes = pd.read_csv('Aéroports_villes.csv', usecols=['city'])
liste_aeroports = pd.read_csv('Aéroports_villes.csv', usecols=['icao'])
aeroport_act1 = ""
aeroport_act2 = ""
ville_act = ""


for i in range (0, len(aeroport1)) :
    aeroport_act1 = aeroport1.iloc[i]['ADEP']
   
    for j in range (0, len(liste_aeroports)) :
         aeroport_act2 = liste_aeroports.iloc[j]['icao']

         if (aeroport_act1 == aeroport_act2) :
            ville_act = liste_villes.iloc[j]['city']
            ville1.append(ville_act)
    

for i in range (0, len(aeroport2)) :
    aeroport_act1 = aeroport2.iloc[i]['ADES']
   
    for j in range (0, len(liste_aeroports)) :
         aeroport_act2 = liste_aeroports.iloc[j]['icao']

         if (aeroport_act1 == aeroport_act2) :
            ville_act = liste_villes.iloc[j]['city']
            ville2.append(ville_act)





passagers_transportes = 82000000 / 12
taux_occupation_initial = 0.314
taux_occupation_final = 0.80
places_restantes = passagers_transportes * (taux_occupation_final-taux_occupation_initial) / taux_occupation_initial
#nb_vols = len(ville1)
#dispo_par_vol = int(places_restantes / nb_vols)
#nb_places_dispo_liste = [dispo_par_vol]*nb_vols

part_places_grand_trajet = 0.70

popular_cities = ["Berlin","Bremen","Cologne","Dresden","Frankfurt-am-Main","Hannover","Leipzig","Munich","Nuremberg"]
liste_villes_1 = pd.read_csv('Tableau_recap_train.csv', usecols=['Ville_1'])
liste_villes_2 = pd.read_csv('Tableau_recap_train.csv', usecols=['Ville_2'])
liste_places_train = pd.read_csv('Tableau_recap_train.csv', usecols=['Places_dispo_train'])

somme = 0

for i in range (0,liste_villes_1) : 
    if (liste_villes_1[i] in popular_cities) :
        somme+= 1




csv_columns = ['Ville_1','Ville_2','Places_disponibles_en_train']

liste = [ [csv_columns[0]] + ville1 ,  [csv_columns[1]] + ville2 , [csv_columns[2]] + nb_places_dispo_liste ]
liste2 = zip(*liste)

with open('tableau_voulu.csv', 'w', ) as myfile:
    wr = csv.writer(myfile, delimiter=',', quoting=csv.QUOTE_NONE)
    for word in liste2 :
        wr.writerow(word)




popular_cities = ["Berlin","Bremen","Cologne","Dresden","Frankfurt-am-Main","Hannover","Leipzig","Munich","Nuremberg"]
liste_villes = pd.read_csv('Aéroports_villes.csv', usecols=['city'])
liste_aeroports = pd.read_csv('Aéroports_villes.csv', usecols=['icao'])



