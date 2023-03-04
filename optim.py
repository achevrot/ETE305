import pandas as pd
import numpy as np
import pulp
from time import time
from tqdm import tqdm
from geopy.distance import great_circle
import warnings
warnings.filterwarnings("ignore")

SCENARIO = 5

debut = time()

DF_COEFF_AC = pd.read_csv('data/ac_model_coefficients.csv')

# Fonctions utilitaires
def append_row(df, row):
    return pd.concat([df, pd.DataFrame([row], columns=row.index)]).reset_index(drop=True)

def CO2_vol(lat_depart, lon_depart, lat_arrivee, lon_arrivee, ac):
    if ac in DF_COEFF_AC['ac_code_icao'].values:
        coeffs = DF_COEFF_AC.loc[DF_COEFF_AC['ac_code_icao'] == ac].values
        alpha = coeffs[0][4]
        beta = coeffs[0][5]
        gamma = coeffs[0][6]

        ap_1 = (lat_depart, lon_depart)
        ap_2 = (lat_arrivee, lon_arrivee)
        dgc = great_circle(ap_1, ap_2).km
        fuel = alpha * dgc ** 2 + beta * dgc + gamma
        CO2 = fuel * 3.16
    else:
        CO2 = 7000 # valeur arbitraire si le type d'avion n'est pas connu
    return CO2

def optim(m, passagers_init, CO2_depart, place_train, avions, CO2_avions, CO2_train, logfile):
    inv_capacity = np.divide(np.ones(m),avions['Capacity'])
    # Futures variables de décision
    nb_passagers   = np.empty(m, dtype=object)
    nb_vols = np.empty(m, dtype=object)
    nb_nouv_avions = np.empty(m, dtype=object)

    # Déclaration problème
    prob = pulp.LpProblem("Optim", pulp.LpMinimize)

    # Variables de décision
    for j in range(m):
        nb_passagers[j]   = pulp.LpVariable('nb_passagers_{}'.format(j), 0, None, cat=pulp.LpInteger)
        nb_vols[j]        = pulp.LpVariable('nb_vols_{}'.format(j), 0, None, cat=pulp.LpInteger)
        nb_nouv_avions[j] = pulp.LpVariable('nb_nouv_avions_{}'.format(j), 0, None, cat=pulp.LpInteger)

    # Contraintes
    prob += np.sum(nb_passagers) <= passagers_init.sum()
    prob += passagers_init.sum() - np.sum(nb_passagers) <= place_train
    for j in range(m):
        #prob.extend(pulp.LpConstraint(nb_passagers[j]-nb_vols[j]*avions['Capacity'][j],sense=0,name="Contrainte_{}".format(j),rhs=0).makeElasticSubProblem())
        prob += nb_passagers[j] <= avions['Capacity'][j] * (avions['N_0'][j] + 60*nb_nouv_avions[j])
        prob += nb_passagers[j] <= avions['Capacity'][j] * nb_vols[j]
        prob += nb_vols[j] <= avions['N_0'][j] + 60*nb_nouv_avions[j]
        prob += 0 <= (pulp.lpSum(np.multiply(CO2_avions, nb_vols)) +\
            pulp.lpSum(CO2_train * (np.sum(passagers_init) - np.sum(nb_passagers))) +\
            pulp.lpSum(np.multiply(nb_nouv_avions, avions['CO2_construction (kg)'])))/1000

    # Fonction objectif
    prob += (pulp.lpSum(np.multiply(CO2_avions, nb_vols)) +\
            pulp.lpSum(CO2_train * (np.sum(passagers_init) - np.sum(nb_passagers))) +\
            pulp.lpSum(np.multiply(nb_nouv_avions, avions['CO2_construction (kg)'])))/1000 # en tonnes pour éviter les trop gros nombres

    # Problem solving
    status = prob.solve(pulp.GLPK(msg=False)) #msg=True,timeLimit=72))

    # Writing log to logfile
    fichier_log = open(logfile,'a')
    fichier_log.write("Status: "+pulp.LpStatus[status]+"\n")
    fichier_log.write("Valeurs finales des variables de décision: \n")
    fichier_log.write("j,AC Type,Capacity,passagers_init,nb_passagers,N_0,nb_vols,nb_nouv_avions\n")
    nb_passagers_finaux = 0
    passagers_finaux = np.empty(m)
    nb_vols_final = np.empty(m)
    nb_nouv_avions_final = np.empty(m)
    for j in range(m):
        passagers_courant = pulp.value(nb_passagers[j])
        passagers_finaux[j] = passagers_courant
        nb_vols_final[j] = pulp.value(nb_vols[j])
        nb_nouv_avions_final[j] = pulp.value(nb_nouv_avions[j])
        fichier_log.write(str(j)+","+\
                        avions['AC Type'][j]+","+\
                        str(avions['Capacity'][j])+","+\
                        str(passagers_init[j])+","+\
                        str(passagers_courant)+","+\
                        str(avions['N_0'][j])+","+\
                        str(pulp.value(nb_vols[j]))+","+\
                        str(pulp.value(nb_nouv_avions[j]))+'\n')
        nb_passagers_finaux += passagers_courant
    fichier_log.write("Nombre de passagers finaux : "+str(nb_passagers_finaux)+"\n")
    
    CO2_fin_avions = np.sum(np.multiply(CO2_avions, nb_vols_final))
    CO2_fin_trains = np.sum(CO2_train * (np.sum(passagers_init) - np.sum(passagers_finaux)))
    CO2_fin_constr = np.sum(np.multiply(nb_nouv_avions_final,avions['CO2_construction (kg)']))
    CO2_fin = CO2_fin_avions + CO2_fin_trains + CO2_fin_constr
    fichier_log.write("Emissions de CO2 totales, en tonnes : ")
    fichier_log.write("Début : " + str(CO2_depart/1000) + "\n")
    fichier_log.write("Fin : " + str(CO2_fin/1000) + "\n")
    fichier_log.write("Résultat optim : "+str(prob.objective.value())+"\n")
    fichier_log.write("CO2 venant des avions : "+str(CO2_fin_avions/1000)+"\n")
    fichier_log.write("CO2 venant des trains : "+str(CO2_fin_trains/1000)+"\n")
    fichier_log.write("CO2 venant de la construction de nouveaux avions : "+str(CO2_fin_constr/1000)+"\n")
    fichier_log.write("Delta CO2 économisé : " + str(CO2_depart/1000-CO2_fin/1000)+"\n")
    fichier_log.close()

# Données

print("----- Création des données -----")

# Vols notés i, de 1 à n
flights = pd.read_csv('data/flights_and_emissions.csv')
n = len(flights)
CO2_flights = round(flights["Emissions_kgCO2eq"])

# Types d'avions notés j, de 1 à m
avions = pd.read_csv('data/Tableau_recap_avions.csv')
m = len(avions)
"""
for j in range(m):
    avions['CO2_construction (kg)'] = 0
"""
# Trains
trains = pd.read_csv('data/Tableau_recap_train'+str(SCENARIO)+'.csv')
PLACE_TRAINS = trains['Places dispo par jour'] * 10 # Pour un mois
CO2_trains = round(trains['Emissions_CO2 (kg/passager)'])
t = len(trains)

# Collecte des données par couple de villes
"""
df_aeroport_ville = pd.read_csv('data/airports_ICAO.csv',usecols=["icao","city"])
CO2_debut = np.zeros(t)
passagers_init = np.zeros((t,m))
N_0 = np.zeros((t,m))
CO2_avions = np.zeros((t,m))
for i in tqdm(range(n)): # itération sur tous les vols
    # Trouver l'indice correspondant au couple (ville1,ville2) :
    ap1 = flights['ADEP'].iloc[i]
    ap2 = flights['ADES'].iloc[i]
    v1 = df_aeroport_ville[df_aeroport_ville['icao'] == ap1]['city'].values[0]
    v2 = df_aeroport_ville[df_aeroport_ville['icao'] == ap2]['city'].values[0]
    print(v1,v2,i)
    indice_trajet = trains.index[trains['Ville_1'].eq(v1) & trains['Ville_2'].eq(v2)][0]
    # Sauvegarde des données par couple de villes :
    CO2_debut[indice_trajet] += CO2_flights[i]
    AC_Type = flights['AC Type'].iloc[i]
    j = avions.index[avions['AC Type'].eq(AC_Type)][0]
    passagers_init[indice_trajet][j] += flights['capacity'].iloc[i]
    N_0[indice_trajet][j] += 1
    if CO2_avions[indice_trajet][j] == 0:
        lat_depart = flights['ADEP Latitude'].iloc[i]
        lon_depart = flights['ADEP Longitude'].iloc[i]
        lat_arrivee = flights['ADES Latitude'].iloc[i]
        lon_arrivee = flights['ADES Longitude'].iloc[i]
        for j_avions in range(m):
            CO2_avions[indice_trajet,j_avions] = CO2_vol(lat_depart, lon_depart, lat_arrivee, lon_arrivee, avions['AC Type'].iloc[j_avions])
np.save("data/CO2_debut",CO2_debut)
np.save("data/passagers_init",passagers_init)
np.save("data/N_0",N_0)
np.save("data/CO2_avions",CO2_avions)
"""
CO2_debut = np.load("data/CO2_debut.npy")
passagers_init = np.load("data/passagers_init.npy")
N_0 = np.load("data/N_0.npy")
CO2_avions = np.load("data/CO2_avions.npy")

print("-----  Optimisation        -----")

for indice_trajet in tqdm(range(t)):
    avions['N_0'] = N_0[indice_trajet]
    logfile = 'log/log-scenario5-05-03-32/log_trajet'+str(indice_trajet)+'.txt'
    f = open(logfile,'a')
    f.write("Ville_1 : "+str(trains['Ville_1'].iloc[indice_trajet])+'\n')
    f.write("Ville_2 : "+str(trains['Ville_2'].iloc[indice_trajet])+'\n')
    f.write("Nombre de passagers initiaux : "+str(passagers_init[indice_trajet].sum())+'\n')
    f.write("Nombre de places dans les trains : "+str(PLACE_TRAINS[indice_trajet])+'\n')
    f.close()
    optim(m, passagers_init[indice_trajet], CO2_debut[indice_trajet], PLACE_TRAINS[indice_trajet], avions, CO2_avions[indice_trajet], CO2_trains[indice_trajet], logfile)
    
fin = time()

print("Temps total : ", fin-debut, " s")
