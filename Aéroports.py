import pandas as pd
import airportsdata

airports = airportsdata.load()

df_airports = pd.read_csv('airports_ICAO.csv')
df_airports_ED = df_airports.loc[df_airports['icao'].str.startswith('ED', na=False)]
df_airports_ED = df_airports_ED.filter(['icao', 'name', 'city'])

df_flights_emissions = pd.read_csv('flights_and_emissions.csv')
list_ADEP = list(df_flights_emissions['ADEP'].values)
list_ADES = list(df_flights_emissions['ADES'].values)
list_airports = list(set(list_ADES + list_ADES))

np_airports = df_airports_ED.to_numpy()

np_airports_utiles = []
for i in range(len(np_airports)):
    if np_airports[i,0] in list_airports:
        np_airports_utiles.append(np_airports[i])

df_airports_ED = pd.DataFrame(np_airports_utiles, columns = ['icao','airport name','city'])

for j in range(len(df_airports_ED.index)):
    if df_airports_ED.isna().iloc[j]['city']:
        df_airports_ED.iloc[j]['city'] = df_airports_ED.iloc[j]['airport name'].split(" ")[0]

df_airports_ED.to_csv('Aéroports_villes.csv')
