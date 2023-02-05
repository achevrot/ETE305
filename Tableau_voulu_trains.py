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





passagers_transportes = 82 000 000
taux_occupation = 0,314
places_restantes = passagers_transportes / taux_occupation *(1-taux_occupation)
nb_vols = len(ville1)
dispo_par_vol = places_restantes / nb_vols



csv_columns = ['Ville_1','Ville_2']

liste = [  [csv_columns[0]] + ville1 ,  [csv_columns[1]] + ville2 ]
liste2 = zip(*liste)

with open('tableau_voulu.csv', 'w', ) as myfile:
    wr = csv.writer(myfile, delimiter=',', quoting=csv.QUOTE_NONE)
    for word in liste2 :
        wr.writerow(word)


