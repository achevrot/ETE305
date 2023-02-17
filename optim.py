import pandas as pd
import numpy as np
import pulp

# Données

print("-----  Création des données   -----")

TAILLE = 1000

# vols notés i, de 1 à n
flights = pd.read_csv('flights_and_emissions.csv')
flights = flights.head(TAILLE)
n = len(flights)

# types d'avions notés j, de 1 à m
avions = pd.read_csv('mass.csv')
m = len(avions)
# Provisoire, en attendant les vraies données sur les types d'avions
avions.insert(len(avions.columns),'N0', pd.Series(np.ones(m) * 10, dtype=int))
avions.insert(len(avions.columns),'Capacite', pd.Series(np.ones(m) * 200, dtype=int))
N_avions = np.empty(m, dtype=object)

# Extraction de tableaux utiles :
AC_type_vol = flights['AC Type']
lat_departs = flights['ADEP Latitude']
lon_departs = flights['ADES Longitude']
lat_arrivees = flights['ADEP Latitude']
lon_arrivees = flights['ADES Longitude']
AC_type = avions['AC Type']

# tableau contenant les s_{i,j}
statut_vol = np.empty((n,m), dtype=object)
statut_depart = np.zeros((n,m))
for i in range(n):
    for j in range(m):
        if AC_type_vol[i] == AC_type[j]:
            statut_depart[i,j] = 1

# Au debut, chaque vol doit être effectué par un et un seul avion.
assert statut_depart.sum() == len(flights), "Erreur, certains vols sont effectués par 0 ou >1 avion"

# émissions CO2 des vols avant optim
CO2_init = flights["Emissions_kgCO2eq"].to_numpy()

# nombre de passagers avant optim
passagers_init = np.ones(n) * 200 # en vrai, à aller chercher selon type d'avion

# nombre de passagers variable
passagers = np.empty((n,m), dtype=object)

# Tableau CO2 total
CO2 = np.load("CO2.npy")
CO2 = CO2[:n]

#PLACE_TRAIN = (82000000 / 0.314 - 82000000) / 12
PLACE_TRAIN = 200 * n / 2

CO2_depart = np.sum(CO2_init)

print("----- Début de l'optimisation -----")

prob = pulp.LpProblem("Optim", pulp.LpMinimize)

# Variables de décision
for i in range(n):
    for j in range(m):
        statut_vol[i,j] = pulp.LpVariable('statut_{}_{}'.format(i,j),cat=pulp.LpBinary)
        passagers[i,j] = pulp.LpVariable('passagers_{}_{}'.format(i,j), cat=pulp.LpInteger)
for j in range(m):
    N_avions[j] = pulp.LpVariable('dispo_{}'.format(j), cat=pulp.LpInteger)

# Contraintes
for i in range(n):
    for j in range(m):
        prob += passagers[i,j] >= 0
        #prob += np.sum(passagers,axis=1)[i] <= passagers_init[i]
        prob += passagers[i,j] <= statut_vol[i,j] * avions['Capacite'][j]
        prob += statut_vol[i].sum() <= 1

prob += (np.sum(passagers,axis=1) - passagers_init).sum() <= PLACE_TRAIN

for j in range(m):
    prob += N_avions[j] >= avions['N0'][j]
    prob += np.sum(statut_vol, axis=0)[j] <= N_avions[j]

# Fonction objectif
prob += pulp.lpSum(np.multiply(CO2, statut_vol))

# Problem solving
status = prob.solve()
print("Status: ",pulp.LpStatus[status])

"""
print("Variables: ", end=' ')
for i in range(n):
    print(pulp.value(statut_vol[i,j]), end=' ')
print()
"""

statut_vol_fin = np.empty((n,m))
for i in range(n):
    for j in range(m):
        statut_vol_fin[i,j] = pulp.value(statut_vol[i,j])

CO2_fin = np.multiply(CO2,statut_vol_fin).sum()

print("Début : " + str(CO2_depart))
print("Fin : " + str(CO2_fin))
print("Delta CO2 économisé : " + str(CO2_depart-CO2_fin))
