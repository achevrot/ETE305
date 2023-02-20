from geopy.distance import great_circle
import pandas as pd

df_aeroport_ville = pd.read_csv('Aéroports_villes.csv')
df_all_flights = pd.read_csv('flights_and_emissions.csv')

couple_v1_v2 = []
distance = []
emissions_train = []

for i in range(len(df_all_flights)):
    ap1 = df_all_flights['ADEP'].iloc[i]
    ap2 = df_all_flights['ADES'].iloc[i]
    v1 = df_aeroport_ville[df_aeroport_ville['icao'] == ap1]['city'].values[0]
    v2 = df_aeroport_ville[df_aeroport_ville['icao'] == ap2]['city'].values[0]
    if [v1,v2] not in couple_v1_v2:
        couple_v1_v2.append([v1,v2])
        geo_ville_1 = (df_all_flights['ADEP Latitude'][i], df_all_flights['ADEP Longitude'][i])
        geo_ville_2 = (df_all_flights['ADES Latitude'][i], df_all_flights['ADES Longitude'][i])
        dgc = great_circle(geo_ville_1, geo_ville_2).km
        distance.append(round(dgc,3)) # Arrondi à 3 chiffres après la virgule
        emissions_train.append(round(dgc * 0.0445,3)) # Arrondi à 3 chiffres après la virgule

# Calcul places disponibles selon trajet populaire ou pas

taux_grands_trajets = 0.7
taux_remplissage_objectif = 0.8

taux_remplissage_actuel = 0.314
passagers_transportes = 82000000 / 12
places_restantes = passagers_transportes * (taux_remplissage_objectif / taux_remplissage_actuel - 1)

popular_cities = ["Berlin","Bremen","Cologne","Dresden","Frankfurt-am-Main","Hannover","Leipzig","Munich","Nuremberg",
                  "Hamburg","Stuttgart","Dusseldorf","Dortmund","Essen"]
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

df_recap_train.to_csv('Tableau_recap_train.csv')


