import pandas as pd

sortie = pd.read_csv('flights_and_emissions.csv', usecols=['AC Type'])
print(sortie)

print(len(sortie))
print(sortie.iloc[0])

dico_AC_type = dict()

for i in range (0,len(sortie)) :
    cle = sortie.iloc[i]['AC Type']
    if (cle in dico_AC_type) :
        dico_AC_type[cle] = dico_AC_type[cle] + 1
    else :
        dico_AC_type[cle] = 1

print(dico_AC_type)
print(len(dico_AC_type))

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
Masse['A320N'] = 60000
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

print('la longueur de la liste Masse est', 'len(Masse)')