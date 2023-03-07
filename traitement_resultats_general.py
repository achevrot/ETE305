import os
import pandas as pd

scenarii = ['log-scenario1-08-07-32','log-scenario2-09-07-5','log-scenario3-05-07-32',
            'log-scenario4-08-03-32','log-scenario5-05-03-32']

columns = ['Initial','Scénario 1 (Base)','Scénario 2 (VLT)','Scénario 3 (TNR)','Scénario 4 (SPV)','Scénario 5 (NAT)']

index = ['Passagers avions (x 1000)','Passagers train (x 1000)','CO2 vols avions (kt)',
         'CO2 construction nouveaux avions (kt)','CO2 train (kt)','Delta CO2']

df_recap_scenario = pd.DataFrame(columns=columns, index=index)
tableau_chiffres_cles = pd.DataFrame(columns=columns)

for i in range(len(scenarii)):

    nb_erreur = 0
    nb_passagers_avions_debut = 0
    CO2_debut = 0
    nb_places_train = 0

    nb_passagers_avions_fin = 0
    nb_passagers_nouv_avions = 0
    CO2_total_fin = 0
    CO2_avions = 0
    CO2_trains = 0
    CO2_nouv_avions = 0

    for file in os.listdir('log/'+scenarii[i]):
        f = open('log/'+scenarii[i]+'/'+file,'r')
        data = f.readlines()
        nb_passagers_avions_debut += float(data[2].split(':')[-1])
        CO2_debut += float(data[37].split(':')[-1])
        nb_places_train += float(data[3].split(':')[-1])

        nb_passagers_avions_fin += float(data[36].split(':')[-1])
        CO2_total_fin += float(data[38].split(':')[-1])
        CO2_avions += float(data[40].split(':')[-1])
        CO2_trains += float(data[41].split(':')[-1])
        CO2_nouv_avions += float(data[42].split(':')[-1])

        f.close()

    passagers_train = nb_passagers_avions_debut - nb_passagers_avions_fin
    delta_CO2 = CO2_debut - CO2_total_fin

    if i == 0:
        df_recap_scenario['Initial'] = [nb_passagers_avions_debut/1000,0,CO2_debut/1000,0,0,0]

    df_recap_scenario[columns[i+1]] = [nb_passagers_avions_fin/1000, passagers_train/1000,
                                      CO2_avions/1000,CO2_nouv_avions/1000,CO2_trains/1000,delta_CO2/1000]

df_recap_scenario.to_excel('resultats_generaux.xlsx')
