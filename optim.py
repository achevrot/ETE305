import pandas as pd
import numpy as np
import pulp
from time import time
from tqdm import tqdm

debut = time()

# Fonction utilitaire
def append_row(df, row):
    return pd.concat([df, pd.DataFrame([row], columns=row.index)]).reset_index(drop=True)

def optim(n, m, indice, passagers_init, place_train, avions, CO2, logfile):
    fichier_log = open("log/"+logfile,'a')

    # Futures variables de décision
    passagers = np.empty((n,m), dtype=object)
    statut_vol = np.empty((n,m), dtype=object)
    N_avions = np.empty(m, dtype=object)

    # Déclaration problème
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
            prob += passagers[i,j] <= passagers_init[i]
            prob += passagers[i,j] <= statut_vol[i,j] * avions['Capacity'][j]
            prob += statut_vol[i].sum() <= 1

    prob += (passagers_init - np.sum(passagers,axis=1)).sum() <= place_train

    for j in range(m):
        prob += N_avions[j] >= avions['N_0'][j]
        prob += np.sum(statut_vol, axis=0)[j] <= N_avions[j]

    # Fonction objectif
    print(len(CO2),"CO2")
    print(statut_vol.shape,"statut_vol")
    print(N_avions.shape,"N_avions")
    print(avions["N_0"],"avions")

    prob += pulp.lpSum(np.multiply(CO2, statut_vol)) + pulp.lpSum(np.multiply(N_avions - avions['N_0'],avions['CO2_construction (kg)']))

    # Problem solving
    status = prob.solve(pulp.GLPK(msg=True,timeLimit=72,keepFiles=True))
    fichier_log.write("Status: "+pulp.LpStatus[status]+"\n")

    fichier_log.write("Variables: \n")
    for i in range(n):
        for j in range(m):
            if pulp.value(passagers[i,j]) != 0.:
                #print(pulp.value(statut_vol[i,j]), end=' ')
                fichier_log.write("i"+str(i)+"j"+str(j)+str(pulp.value(passagers[i,j]))+'\n')
    fichier_log.write("\n")
    fichier_log.write("Création d'avions \n")

    for j in range(m):
        fichier_log.write(str(j)+str(pulp.value(N_avions[j])-avions['N_0'][j])+'\n')

    statut_vol_fin = np.empty((n,m))
    for i in range(n):
        for j in range(m):
            statut_vol_fin[i,j] = pulp.value(statut_vol[i,j])

    CO2_fin = np.multiply(CO2,statut_vol_fin).sum()

    fichier_log.write("Début : " + str(CO2_depart) + "\n")
    fichier_log.write("Fin : " + str(CO2_fin) + "\n")
    fichier_log.write("Delta CO2 économisé : " + str(CO2_depart-CO2_fin))

    return(status)

# Données

print("----- Création des données -----")

# vols notés i, de 1 à n
flights = pd.read_csv('flights_and_emissions.csv')
n = len(flights)

# Faire sur un nombre réduit de vols (décommenter si besoin)
#TAILLE = 100
#flights = flights.head(TAILLE)
#n = len(flights)

# émissions CO2 des vols avant optim
CO2_depart = np.sum(flights["Emissions_kgCO2eq"].to_numpy())

# types d'avions notés j, de 1 à m
avions = pd.read_csv('tableau_recap_avions.csv')
#avions.sort_values(by=['N_0'])
m = len(avions)

# Tableau CO2 total
CO2 = np.load("CO2.npy")

# Trains
trains = pd.read_csv('Tableau_recap_train.csv')
PLACE_TRAINS = trains['Places dispo par jour'] * 10 # Pour un mois
couples_villes = trains[['Ville_1','Ville_2']]
t = len(trains)

# Tableaux de vol par couple de ville
"""
vols_par_trains = []
CO2_par_trains = []
for indice in range(t):
    vols_par_trains.append(pd.DataFrame(columns=flights.columns))
    CO2_par_trains.append([])
df_aeroport_ville = pd.read_csv('Aéroports_villes.csv')

for i in tqdm(range(len(flights))):
    ap1 = flights['ADEP'].iloc[i]
    ap2 = flights['ADES'].iloc[i]
    v1 = df_aeroport_ville[df_aeroport_ville['icao'] == ap1]['city'].values[0]
    v2 = df_aeroport_ville[df_aeroport_ville['icao'] == ap2]['city'].values[0]
    indice = trains.index[trains['Ville_1'].eq(v1) & trains['Ville_2'].eq(v2)][0]
    vols_par_trains[indice] = append_row(vols_par_trains[indice],flights.iloc[i])
    CO2_par_trains[indice].append(CO2[i])
for i in range(t):
    print(len(CO2_par_trains[i]))

np.save("vols_par_trains",vols_par_trains)
np.save("CO2_par_trains",CO2_par_trains)
"""
vols_par_trains = np.load("vols_par_trains.npy", allow_pickle = True)
CO2_par_trains = np.load("CO2_par_trains.npy", allow_pickle = True)
for i in range(CO2_par_trains.shape[0]):
    assert len(CO2_par_trains[i])==len(vols_par_trains[i]), "Erreur, pas autant de valeur d'émissions de CO2 que de vols"

# Optim pour chaque couple de ville
print("-----  Optimisation        -----")

for indice_trajet in tqdm(range(t)):
    vols = vols_par_trains[indice_trajet]
    n = len(vols)
    logfile = 'log_trajet'+str(indice_trajet)+'.txt'

    # nombre de passagers avant optim
    passagers_init = np.empty(n)
    for i in range(n):
        passagers_init[i] = vols["capacity"][i]

    res_optim = optim(n, m, indice_trajet, passagers_init, PLACE_TRAINS[indice_trajet], avions, CO2_par_trains[indice_trajet], logfile)
    print(res_optim)
    
fin = time()

print("Temps total : ", fin-debut, " s")
