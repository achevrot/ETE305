import pandas as pd

numero_trajet = [29, # Berlin - Baden-Baden
                 15] # Berlin - Munich


scenarii = ['log-scenario1-08-07-32','log-scenario2-09-07-5','log-scenario3-05-07-32','log-scenario4-08-03-32','log-scenario5-05-03-32']

index1 = ['A20N','A319','A320','A321','A332','A343','AT43','AT72','B38M','B734','B736','B737','B738','B752',
          'B753','B763','B788','C310','CRJ7','CRJ9','CRJX','D328','DH8D','E120','E170','E190','E195','J328','JS32']

columns = ['Initial','Scénario 1 (Base)','Scénario 2 (VLT)','Scénario 3 (TNR)','Scénario 4 (SPV)','Scénario 5 (NAT)']

index2 = ['Passagers avions (x 1000)','Passagers train (x 1000)','CO2 vols avions (kt)',
         'CO2 construction nouveaux avions (kt)','CO2 train (kt)','Delta CO2']

with pd.ExcelWriter("/ETE_305/ETE305/resultats_par_trajet.xlsx") as writer:

    for j in range(len(numero_trajet)):

        df_trajet_par_avion = pd.DataFrame(columns=columns, index=index1)
        df_trajet_general = pd.DataFrame(columns=columns, index=index2)

        for i in range(len(scenarii)):

            f = open('log/'+scenarii[i]+'/log_trajet'+str(numero_trajet[j])+'.txt')
            data = f.readlines()

            ## Infos générales ##
            nb_passagers_avions_debut = float(data[2].split(':')[-1])
            CO2_debut = float(data[37].split(':')[-1])
            nb_places_train = float(data[3].split(':')[-1])

            nb_passagers_avions_fin = float(data[36].split(':')[-1])
            CO2_total_fin = float(data[38].split(':')[-1])
            CO2_avions = float(data[40].split(':')[-1])
            CO2_trains = float(data[41].split(':')[-1])
            CO2_nouv_avions = float(data[42].split(':')[-1])

            ## Infos trajet par type d'avion ##
            pass_init = []
            pass_fin = []

            for k in range(7,36):
                ligne = data[k].split(',')
                ligne[-1] = ligne[-1].strip()
                pass_init.append(float(ligne[3]))
                pass_fin.append(float(ligne[4]))


            ## Infos trajet générales ##
            passagers_train = nb_passagers_avions_debut - nb_passagers_avions_fin
            delta_CO2 = CO2_debut - CO2_total_fin

            f.close()

            ## On remplit les tableaux ##
            if i == 0:
                df_trajet_general['Initial'] = [nb_passagers_avions_debut / 1000, 0, CO2_debut / 1000, 0, 0, 0]
                df_trajet_par_avion['Initial'] = pass_init

            df_trajet_general[columns[i+1]] = [nb_passagers_avions_fin / 1000, passagers_train / 1000,
                                              CO2_avions / 1000, CO2_nouv_avions / 1000, CO2_trains / 1000, delta_CO2/1000]
            df_trajet_par_avion[columns[i+1]] = pass_fin

        df_trajet_par_avion.to_excel(writer, sheet_name='trajet'+str(numero_trajet[j]))
        df_trajet_general.to_excel(writer, sheet_name='trajet'+str(numero_trajet[j]), startcol=10)

