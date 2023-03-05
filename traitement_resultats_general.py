import os
import numpy as np
import pandas as pd
# from openpyxl import WorkBook

scenarii = ['log-scenario1-08-07-32','log-scenario2-08-07-5','log-scenario3-05-07-32','log-scenario4-08-03-32','log-scenario5-05-03-32']

columns = ['Initial', 'Final']

index = ['Passagers_avion_init', 'CO2_init (t)', 'Places_train', 'Passagers_avion_fin', 'Passagers_train', 'CO2_total_fin (t)',
         'CO2_avions (t)', 'CO2_trains (t)', 'CO2_constr_nouv_avions (t)', 'Delta_CO2 (t)']
tableaux_recap = pd.DataFrame(index=index)

for scenario in scenarii:

    nb_erreur = 0
    nb_passagers_avions_debut = 0
    CO2_debut = 0
    nb_places_train = 0

    nb_passagers_avions_fin = 0
    CO2_total_fin = 0
    CO2_avions = 0
    CO2_trains = 0
    CO2_nouv_avions = 0

    for file in os.listdir(scenario):
        if file.endswith('.txt'):
            f = open(scenario+'/'+file,'r')
            data = f.readlines()

            if 'Optimal' in data[4]:

                nb_passagers_avions_debut += float(data[2].split(':')[-1])
                CO2_debut += float(data[60].split(':')[-1])
                nb_places_train += float(data[3].split(':')[-1])

                nb_passagers_avions_fin += float(data[59].split(':')[-1])
                CO2_total_fin += float(data[61].split(':')[-1])
                CO2_avions += float(data[63].split(':')[-1])
                CO2_trains += float(data[64].split(':')[-1])
                CO2_nouv_avions += float(data[65].split(':')[-1])

            else:
                nb_erreur += 1
            f.close()

    passagers_train = nb_passagers_avions_debut - nb_passagers_avions_fin
    delta_CO2 = CO2_debut - CO2_total_fin

    tableaux_recap[scenario] = [nb_passagers_avions_debut, CO2_debut, nb_places_train, nb_passagers_avions_fin,
                                passagers_train, CO2_total_fin, CO2_avions, CO2_trains, CO2_nouv_avions, delta_CO2]


pd.set_option('display.max_columns', None)
print(tableaux_recap)
tableaux_recap.to_excel('Résultats_scenarii.xlsx')

