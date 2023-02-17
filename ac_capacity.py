import pandas as pd

df_flights_emissions = pd.read_csv('flights_and_emissions.csv')
list_ac = list(set(df_flights_emissions['AC Type'].values))

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

new_dict = {}
new_dict['AC_type'] = list(AC_type)
new_dict['capacity'] = list(capacity)

df_capacity = pd.DataFrame(data=new_dict)

list_capa = []
for i in range(len(df_flights_emissions.index)):
    avion = df_flights_emissions['AC Type'].iloc[i]
    capa = df_capacity[df_capacity['AC_type'] == avion]['capacity'].values[0]
    list_capa.append(capa)

df_flights_emissions['capacity'] = list_capa

df_flights_emissions.to_csv('flights_and_emissions.csv')
