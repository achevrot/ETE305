from geopy.distance import great_circle
import numpy as np
import pandas as pd
import sys

# Paramètres de décision
SCENARIO = 4
taux_remplissage_objectif = 0.8
taux_grands_trajets = 0.3
FACTEUR_EMISSION = 0.032

# Création des liens codes aéroports - ville 
df_all_flights = pd.read_csv('data/flights_and_emissions.csv')
df_airports = pd.read_csv('data/airports_ICAO.csv')

df_airports_ED = df_airports.loc[df_airports['icao'].str.startswith('ED', na=False)]
df_airports_ED = df_airports_ED.filter(['icao', 'name', 'city'])

list_ADEP = list(df_all_flights['ADEP'].values)
list_ADES = list(df_all_flights['ADES'].values)
for j in range(len(list_ADES)):
    list_ADEP.append(list_ADES[j])
list_airports = list(set(list_ADEP))

np_airports = df_airports_ED.to_numpy()
np.set_printoptions(threshold=sys.maxsize)
np_airports_utiles = []
for i in range(len(np_airports)):
    if np_airports[i,0] in list_airports:
        np_airports_utiles.append(np_airports[i])

df_airports_ED = pd.DataFrame(np_airports_utiles, columns = ['icao','airport name','city'])

for j in range(len(df_airports_ED.index)):
    if df_airports_ED.isna().iloc[j]['city']:
        df_airports_ED.iloc[j]['city'] = df_airports_ED.iloc[j]['airport name'].split(" ")[0]

# Création des données
couple_v1_v2 = []
distance = []
emissions_train = []

for i in range(len(df_all_flights)):
    ap1 = df_all_flights['ADEP'].iloc[i]
    ap2 = df_all_flights['ADES'].iloc[i]
    v1 = df_airports_ED[df_airports_ED['icao'] == ap1]['city'].values[0]
    v2 = df_airports_ED[df_airports_ED['icao'] == ap2]['city'].values[0]
    if [v1,v2] not in couple_v1_v2:
        couple_v1_v2.append([v1,v2])
        geo_ville_1 = (df_all_flights['ADEP Latitude'][i], df_all_flights['ADEP Longitude'][i])
        geo_ville_2 = (df_all_flights['ADES Latitude'][i], df_all_flights['ADES Longitude'][i])
        dgc = great_circle(geo_ville_1, geo_ville_2).km
        distance.append(round(dgc,3)) # Arrondi à 3 chiffres après la virgule
        emissions_train.append(round(dgc * FACTEUR_EMISSION,3)) # Arrondi à 3 chiffres après la virgule

# Calcul places disponibles selon trajet populaire ou pas

taux_remplissage_actuel = 0.314 # Vient des données Deutsche Bahn
passagers_transportes = 82000000 / 12 # Vient des données Deutsche Bahn, par mois
places_restantes = passagers_transportes * (taux_remplissage_objectif / taux_remplissage_actuel - 1)

popular_cities = ["Berlin","Bremen","Cologne","Dresden","Frankfurt-am-Main","Hannover","Leipzig","Munich","Nuremberg",
                  "Hamburg","Stuttgart","Dusseldorf","Dortmund","Essen"] # Villes allemandes de plus de 500 000 habitants
nb_trajet_pop = 0
for j in range(len(couple_v1_v2)):
    if (couple_v1_v2[j][0] in popular_cities) and (couple_v1_v2[j][1] in popular_cities):
        nb_trajet_pop += 1

places_restantes_grands_trajets = places_restantes * taux_grands_trajets
places_restantes_petits_trajets = places_restantes - places_restantes_grands_trajets

places_restantes_grands_trajets_par_ligne = places_restantes_grands_trajets / nb_trajet_pop
places_restantes_petits_trajets_par_ligne = places_restantes_petits_trajets / (len(couple_v1_v2) - nb_trajet_pop)

places_dispo_train = []

for j in range(len(couple_v1_v2)):
    if (couple_v1_v2[j][0] in popular_cities) and (couple_v1_v2[j][1] in popular_cities):
        places_dispo_train.append(round(places_restantes_grands_trajets_par_ligne/31,0))
    else:
        places_dispo_train.append(round(places_restantes_petits_trajets_par_ligne/31,0))

# Création tableau final

df_recap_train = pd.DataFrame()

ville_1 = []
ville_2 = []
for k in range(len(couple_v1_v2)):
    ville_1.append(couple_v1_v2[k][0])
    ville_2.append(couple_v1_v2[k][1])
df_recap_train['Ville_1'] = ville_1
df_recap_train['Ville_2'] = ville_2

df_recap_train['Distance (km)'] = distance
df_recap_train['Places dispo par jour'] = places_dispo_train
df_recap_train['Emissions_CO2 (kg/passager)'] = emissions_train

df_recap_train.to_csv('data/Tableau_recap_train'+str(SCENARIO)+'.csv')
