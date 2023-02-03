from geopy.distance import great_circle
import pandas as pd

df_flights = pd.read_csv('201903_interieur.csv')
df_coeff_ac = pd.read_csv('ac_model_coefficients.csv')
df_corres = pd.read_csv('Correspondances.csv')

list_emissions = []
list_avions_non_rep = []

for i in range(len(df_flights.ADEP)):
    ac = df_flights['AC Type'][i]

    if ac in df_coeff_ac['ac_code_icao'].values:
        coeffs = df_coeff_ac.loc[df_coeff_ac['ac_code_icao'] == ac].values
        alpha = coeffs[0][4]
        beta = coeffs[0][5]
        gamma = coeffs[0][6]

        ap_1 = (df_flights['ADEP Latitude'][i], df_flights['ADEP Longitude'][i])
        ap_2 = (df_flights['ADES Latitude'][i], df_flights['ADES Longitude'][i])
        dgc = great_circle(ap_1, ap_2).km

        fuel = alpha * dgc ** 2 + beta * dgc + gamma
        emission_kgCO2eq = fuel * 3.16
        list_emissions.append(emission_kgCO2eq)

    else:
        list_avions_non_rep.append(ac)
        list_emissions.append(0)

df_flights['Emissions_kgCO2eq'] = list_emissions

df_flights_emissions = df_flights.drop(df_flights[df_flights['Emissions_kgCO2eq'] == 0].index)
df_flights_emissions.to_csv('flights_and_emissions.csv')

print('Emissions totales du mois (- les non rép, environ 4%) :')
print(df_flights['Emissions_kgCO2eq'].sum()/1000000, " ktCO2eq")







