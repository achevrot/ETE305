import pandas as pd
from geopy.distance import great_circle

df_all_data = pd.read_csv('Flights_20190301_20190331.csv') # Fichier trop lourd pour être ajouté sur le repo Git

# Sélection des vols intérieurs en Allemagne (codes aéroports commençant par ED)
df_all_data = df_all_data.loc[df_all_data['ADEP'].str.startswith('ED', na=False)]
df_all_data = df_all_data.loc[df_all_data['ADES'].str.startswith('ED', na=False)]

# On enlève le fret
df_all_data = df_all_data.drop(df_all_data[df_all_data['STATFOR Market Segment'] == 'All-Cargo'].index)

# On enlève les jets privés
df_all_data = df_all_data.drop(df_all_data[df_all_data['STATFOR Market Segment'] == 'Charter'].index)
df_all_data = df_all_data.drop(df_all_data[df_all_data['STATFOR Market Segment'] == 'Business Aviation'].index)

# On enlève les colonnes qu'on n'utilise pas
df_all_data.drop(columns=['ECTRL ID','FILED OFF BLOCK TIME','FILED ARRIVAL TIME','ACTUAL OFF BLOCK TIME','ACTUAL ARRIVAL TIME','AC Operator','AC Registration','Requested FL'], inplace=True)
df_all_data = df_all_data.reindex()
df_all_data = df_all_data.reset_index(drop=True)

# On ajoute les émissions de CO2
df_coeff_ac = pd.read_csv('data/ac_model_coefficients.csv')
list_emissions = []
list_avions_non_rep = []

for i in range(len(df_all_data.ADEP)):
    ac = df_all_data['AC Type'][i]

    if ac in df_coeff_ac['ac_code_icao'].values:
        coeffs = df_coeff_ac.loc[df_coeff_ac['ac_code_icao'] == ac].values
        alpha = coeffs[0][4]
        beta = coeffs[0][5]
        gamma = coeffs[0][6]

        ap_1 = (df_all_data['ADEP Latitude'][i], df_all_data['ADEP Longitude'][i])
        ap_2 = (df_all_data['ADES Latitude'][i], df_all_data['ADES Longitude'][i])
        dgc = great_circle(ap_1, ap_2).km

        fuel = alpha * dgc ** 2 + beta * dgc + gamma
        emission_kgCO2eq = fuel * 3.16
        list_emissions.append(emission_kgCO2eq)

    else:
        list_avions_non_rep.append(ac)
        list_emissions.append(0)

df_all_data['Emissions_kgCO2eq'] = list_emissions

df_flights_emissions = df_all_data.drop(df_all_data[df_all_data['Emissions_kgCO2eq'] == 0].index)

# Sauvegarde pour avoir un tableau contenant seulement les données que nous allons utiliser par la suite
df_flights_emissions.to_csv('data/flights_and_emissions.csv')
