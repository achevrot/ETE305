import pandas as pd
import numpy as np
import pulp
from time import time

debut = time()

# Données

print("-----  Création des données   -----")


# vols notés i, de 1 à n
flights = pd.read_csv('flights_and_emissions.csv')
n = len(flights)

# Faire sur un nombre réduit de vols (décommenter si besoin)
TAILLE = 100*2
# flights = flights.head(TAILLE)
# n = len(flights)

# types d'avions notés j, de 1 à m
avions = pd.read_csv('tableau_recap_avions.csv')
#avions.sort_values(by=['N_0'])
m = len(avions)
#N_avions = np.empty(m, dtype=object)

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
passagers_init = np.empty(n)
for i in range(n):
    passagers_init[i] = flights["capacity"][i]

# nombre de passagers variable
passagers = np.empty((n,m), dtype=object)

# Tableau CO2 total
CO2 = np.load("CO2.npy")
CO2 = CO2[:n]

#PLACE_TRAIN = (82000000 / 0.314 - 82000000) / 12
PLACE_TRAIN = 100 * n

CO2_depart = np.sum(CO2_init)

print("----- Début de l'optimisation -----")

prob = pulp.LpProblem("Optim", pulp.LpMinimize)

# Variables de décision
for i in range(n):
    for j in range(m):
        statut_vol[i,j] = pulp.LpVariable('statut_{}_{}'.format(i,j),cat=pulp.LpBinary)
        passagers[i,j] = pulp.LpVariable('passagers_{}_{}'.format(i,j), cat=pulp.LpInteger)
#for j in range(m):
    #N_avions[j] = pulp.LpVariable('dispo_{}'.format(j), cat=pulp.LpInteger)

# Contraintes
for i in range(n):
    for j in range(m):
        prob += passagers[i,j] >= 0
        #prob += np.sum(passagers,axis=1)[i] <= passagers_init[i]
        prob += passagers[i,j] <= passagers_init[i]
        prob += passagers[i,j] <= statut_vol[i,j] * avions['Capacity'][j]
        prob += statut_vol[i].sum() <= 1

prob += (passagers_init - np.sum(passagers,axis=1)).sum() <= PLACE_TRAIN

#for j in range(m):
    #prob += N_avions[j] >= avions['N_0'][j]
    #prob += np.sum(statut_vol, axis=0)[j] <= N_avions[j]

# Fonction objectif
prob += pulp.lpSum(np.multiply(CO2, statut_vol)) + pulp.lpSum(np.multiply(N_avions- avions['N_0'],avions['CO2_construction (kg)']))

# Problem solving
status = prob.solve(pulp.GLPK())
print("Status: ",pulp.LpStatus[status])

print("Variables: ", end=' ')
for i in range(n):
    for j in range(m):
        if pulp.value(passagers[i,j]) != 0.:
            #print(pulp.value(statut_vol[i,j]), end=' ')
            print("i",i,"j",j,pulp.value(passagers[i,j]), end =' ')
    print('\n')
print()

print("Création d'avions")

for j in range(m):
    print(j,pulp.value(N_avions[j])-avions['N_0'][j],end=' ')
    print('\n')

statut_vol_fin = np.empty((n,m))
for i in range(n):
    for j in range(m):
        statut_vol_fin[i,j] = pulp.value(statut_vol[i,j])

CO2_fin = np.multiply(CO2,statut_vol_fin).sum()

print("Début : " + str(CO2_depart))
print("Fin : " + str(CO2_fin))
print("Delta CO2 économisé : " + str(CO2_depart-CO2_fin))

fin = time()

print("Temps total : ", fin-debut, " s")