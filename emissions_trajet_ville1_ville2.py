from geopy.distance import great_circle
import pandas as pd

df_dispo_train = pd.read_csv('tableau_voulu.csv')
df_aeroport_ville = pd.read_csv('Aéroports_villes.csv')
df_all_flights = pd.read_csv('flights_emissions_capacity.csv')

ville_1 = []
ville_2 = []
distance = []
emissions_train = []

for i in range(len(df_all_flights)):
    ap1 = df_all_flights['ADEP'].iloc[i]
    ap2 = df_all_flights['ADES'].iloc[i]
    v1 = df_aeroport_ville[df_aeroport_ville['icao'] == ap1]['city'].values[0]
    v2 = df_aeroport_ville[df_aeroport_ville['icao'] == ap2]['city'].values[0]
    ville_1.append(v1)
    ville_2.append(v2)
    geo_ville_1 = (df_all_flights['ADEP Latitude'][i], df_all_flights['ADEP Longitude'][i])
    geo_ville_2 = (df_all_flights['ADES Latitude'][i], df_all_flights['ADES Longitude'][i])
    dgc = great_circle(geo_ville_1, geo_ville_2).km
    distance.append(dgc)
    emissions_train.append(dgc * 0.0445)

passagers_transportes = 82000000 / 12
taux_occupation = 0.314
places_restantes = passagers_transportes * (1-taux_occupation) / taux_occupation
nb_vols = len(df_all_flights.index)
dispo_par_vol = int(places_restantes / nb_vols)
places_dispo_train = [dispo_par_vol]*nb_vols

df_recap_train = pd.DataFrame()
df_recap_train['Ville_1'] = ville_1
df_recap_train['Ville_2'] = ville_2
df_recap_train['Distance (km)'] = distance
df_recap_train['Places_dispo_train'] = places_dispo_train
df_recap_train['Emissions_CO2 (kg/passager)'] = emissions_train

df_recap_train.to_csv('Tableau_recap_train.csv')


