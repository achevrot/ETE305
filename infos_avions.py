import pandas as pd

df_mass = pd.read_csv('mass.csv')
df_capacity = pd.read_csv('capacity.csv')
df_flights = pd.read_csv('flights_and_emissions.csv')

list_ac = sorted(list(set(list(df_flights['AC Type'].values))))
nb_type_ac = [0]*len(list_ac)

list_capacity = []
list_mass = []
list_CO2_construction = []

"""
# Effectif
for i in range(len(df_flights.index)):
    for j in range(len(list_ac)):
        if df_flights['AC Type'].iloc[i] == list_ac[j]:
            nb_type_ac[j] += 1
"""

# Capacity and mass
for j in range(len(list_ac)):
    capa = df_capacity[df_capacity['AC_type'] == list_ac[j]]['capacity'].values[0]
    list_capacity.append(capa)

    mass = df_mass[df_mass['AC Type'] == list_ac[j]]['Masse avion (kg)'].values[0]
    constr = df_mass[df_mass['AC Type'] == list_ac[j]]['Impact CO2 construction (kg CO2)'].values[0]
    list_mass.append(mass)
    list_CO2_construction.append(constr)

df_effectif_ac = pd.DataFrame()
df_effectif_ac['AC Type'] = list_ac
df_effectif_ac['Capacity'] = list_capacity
df_effectif_ac['Mass (kg)'] = list_mass
df_effectif_ac['CO2_construction (kg)'] = list_CO2_construction
#df_effectif_ac['N_0'] = nb_type_ac

df_effectif_ac.to_csv('tableau_recap_avions.csv')