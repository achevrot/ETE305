import pandas as pd

df_flights = pd.read_csv('data/flights_and_emissions.csv')

list_ac = sorted(list(set(list(df_flights['AC Type'].values))))

list_capacity = []
list_mass = []
list_CO2_construction = []

# Capacité
Capacity = dict()
Capacity['PC12'] = 9
Capacity['A333'] = 335
Capacity['E55P'] = 9
Capacity['B462'] = 100
Capacity['B752'] = 228
Capacity['B737'] = 149
Capacity['A319'] = 142
Capacity['A320'] = 180
Capacity['B748'] = 467
Capacity['J328'] = 32
Capacity['A332'] = 293
Capacity['CRJ7'] = 70
Capacity['B744'] = 524
Capacity['B763'] = 351
Capacity['CRJ2'] = 50
Capacity['D328'] = 39
Capacity['F406'] = 8
Capacity['A20N'] = 194
Capacity['E190'] = 114
Capacity['E120'] = 30
Capacity['C680'] = 12
Capacity['C25A'] = 9
Capacity['D228'] = 19
Capacity['E195'] = 124
Capacity['GLF5'] = 19
Capacity['B38M'] = 178
Capacity['B788'] = 250
Capacity['B733'] = 149
Capacity['SF34'] = 34
Capacity['AT43'] = 50
Capacity['BE40'] = 8
Capacity['JS32'] = 19
Capacity['B738'] = 167
Capacity['B77L'] = 440
Capacity['B772'] = 440
Capacity['B753'] = 280
Capacity['BE20'] = 13
Capacity['A343'] = 335
Capacity['A306'] = 298
Capacity['A388'] = 853
Capacity['CRJX'] = 104
Capacity['B734'] = 168
Capacity['A321'] = 220
Capacity['A346'] = 419
Capacity['E170'] = 80
Capacity['CRJ9'] = 90
Capacity['B762'] = 255
Capacity['C310'] = 5
Capacity['DH8D'] = 78
Capacity['C208'] = 14
Capacity['AT72'] = 72
Capacity['B736'] = 132

AC_type = Capacity.keys()
capacity = Capacity.values()

dict_capacity = {}
dict_capacity['AC_type'] = list(AC_type)
dict_capacity['capacity'] = list(capacity)
df_capacity = pd.DataFrame(data=dict_capacity)

for j in range(len(list_ac)):
    capa = df_capacity[df_capacity['AC_type'] == list_ac[j]]['capacity'].values[0]
    list_capacity.append(capa)



    constr = df_mass[df_mass['AC Type'] == list_ac[j]]['Impact CO2 construction (kg CO2)'].values[0]
    list_CO2_construction.append(constr)

# Masse
Masse = dict()
Masse['B734'] = 60000
Masse['B733'] = 60000
Masse['A332'] = 200000
Masse['B77L'] = 300000
Masse['B762'] = 170000
Masse['A306'] = 150000
Masse['B738'] = 60000
Masse['A320'] = 60000
Masse['B752'] = 100000
Masse['E190'] = 40000
Masse['A319'] = 60000
Masse['CRJ9'] = 30000
Masse['A20N'] = 60000 # C'est l'A320N mais son code c'est A20N !
Masse['A321'] = 60000
Masse['DH8D'] = 25000
Masse['CRJ7'] = 25000
Masse['D328'] = 10000
Masse['J328'] = 10000
Masse['E55P'] = 9000
Masse['C25A'] = 4000
Masse['E195'] = 50000
Masse['C680'] = 10000
Masse['JS32'] = 5000
Masse['B744'] = 380000
Masse['AT72'] = 20000
Masse['D228'] = 5000
Masse['B788'] = 200000
Masse['BE20'] = 5000
Masse['B737'] = 60000
Masse['E170'] = 40000
Masse['B38M'] = 60000
Masse['BE40'] = 6000
Masse['B763'] = 60000
Masse['AT43'] = 10000
Masse['C208'] = 3000
Masse['E120'] = 10000
Masse['B748'] = 380000
Masse['F406'] = 4000
Masse['B462'] = 30000
Masse['A388'] = 400000
Masse['A343'] = 260000
Masse['SF34'] = 10000
Masse['B753'] = 100000
Masse['B736'] = 70000
Masse['CRJ2'] = 20000
Masse['GLF5'] = 30000
Masse['B772'] = 300000
Masse['A333'] = 180000
Masse['PC12'] = 4000
Masse['C310'] = 2000
Masse['A346'] = 300000
Masse['CRJX'] = 20000

AC_type = Masse.keys()
mass = Masse.values()

dict_mass = {}
dict_mass['AC_type'] = list(AC_type)
dict_mass['Masse avion (kg)'] = list(mass)
df_mass = pd.DataFrame(data=dict_mass)

for j in range(len(list_ac)):
    mass = df_mass[df_mass['AC Type'] == list_ac[j]]['Masse avion (kg)'].values[0]
    list_mass.append(mass)

# Émissions CO2 lors de la construction
impact_co2_par_kilo_avion = 2
co2_build = dict()
for keys in Masse :
    co2_build[keys] = impact_co2_par_kilo_avion * Masse[keys]

AC_type = co2_build.keys()
CO2_values = co2_build.values()

dict_CO2 = {}
dict_CO2['AC_type'] = list(AC_type)
dict_CO2['Impact CO2 construction (kg CO2)'] = list(CO2_values)
df_CO2 = pd.DataFrame(data=dict_CO2)

for j in range(len(list_ac)):
    constr = df_CO2[df_CO2['AC Type'] == list_ac[j]]['Impact CO2 construction (kg CO2)'].values[0]
    list_CO2_construction.append(constr)

# Sauvegarde 
df_effectif_ac = pd.DataFrame()
df_effectif_ac['AC Type'] = list_ac
df_effectif_ac['Capacity'] = list_capacity
df_effectif_ac['Mass (kg)'] = list_mass
df_effectif_ac['CO2_construction (kg)'] = list_CO2_construction
df_effectif_ac.to_csv('data/Tableau_recap_avions.csv')

# Ajout de la capacité pour les vols
list_capa = []

for i in range(len(df_flights.index)):
    avion = df_flights['AC Type'].iloc[i]
    capa = df_capacity[df_capacity['AC_type'] == avion]['capacity'].values[0]
    list_capa.append(capa)

df_flights['capacity'] = list_capa
df_flights.to_csv('data/flights_and_emissions.csv')
