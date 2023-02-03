import pandas as pd
import numpy as np
import pulp

 # Données

flights = pd.read_csv('flights_and_emissions.csv')
n = len(flights)
print(n)

statut_vol = np.empty(n, dtype=object)
CO2 = flights["Emissions_kgCO2eq"].to_numpy()
passagers = np.ones(n) * 200
place_train = (82000000 / 0.314 - 82000000) / 12
#place_train = 200 * n / 2

CO2_depart = np.sum(CO2)

prob = pulp.LpProblem("Optim", pulp.LpMinimize)

# Variables de décision
for i in range(n):
    statut_vol[i] = pulp.LpVariable('statut_{}'.format(i),cat=pulp.LpBinary)

# Contraintes
prob += np.multiply(passagers,(1-statut_vol)).sum() <= place_train

# Fonction objectif
prob += pulp.lpSum(np.multiply(CO2, statut_vol))

# Problem solving
status = prob.solve()
print("Status: ",pulp.LpStatus[status])

"""
print("Variables: ", end=' ')
for i in range(n):
    print(pulp.value(statut_vol[i]), end=' ')
print()
"""

statut_vol_fin = np.empty(n)
for i in range(n):
    statut_vol_fin[i] = pulp.value(statut_vol[i])

CO2_fin = np.multiply(CO2,statut_vol_fin).sum()

print("Début : " + str(CO2_depart))
print("Fin : " + str(CO2_fin))
print("Delta CO2 économisé : " + str(CO2_depart-CO2_fin))