import pandas as pd

numero_trajet = [29, 15]  # Berlin - Baden-Baden  # Berlin - Munich

scenarii = [
    "log-scenario1-08-07-32",
    "log-scenario2-09-07-5",
    "log-scenario3-05-07-32",
    "log-scenario4-08-03-32",
    "log-scenario5-05-03-32",
]

index1 = [
    "A20N",
    "A319",
    "A320",
    "A321",
    "A332",
    "A343",
    "AT43",
    "AT72",
    "B38M",
    "B734",
    "B736",
    "B737",
    "B738",
    "B752",
    "B753",
    "B763",
    "B788",
    "C310",
    "CRJ7",
    "CRJ9",
    "CRJX",
    "D328",
    "DH8D",
    "E120",
    "E170",
    "E190",
    "E195",
    "J328",
    "JS32",
]
columns = [
    "Capacity",
    "Nb initial passagers avion",
    "Nb final passagers avion",
    "Nb initial vols",
    "Nb final vols",
    "Nb nouveaux avions",
]

with pd.ExcelWriter("resultats/resultats_par_avion.xlsx") as writer:
    for i in range(len(scenarii)):

        df_all_data = pd.DataFrame(index=index1, columns=columns)

        for j in range(len(numero_trajet)):
            f = open(
                "log/" + scenarii[i] + "/log_trajet" + str(numero_trajet[j]) + ".txt"
            )
            data = f.readlines()

            ## Infos trajet par type d'avion ##

            capa = []
            pass_init = []
            pass_fin = []
            nb_vols_init = []
            nb_vols_fin = []
            nb_avions_constr = []

            for k in range(7, 36):
                ligne = data[k].split(",")
                ligne[-1] = ligne[-1].strip()

                capa.append(float(ligne[2]))
                pass_init.append(float(ligne[3]))
                pass_fin.append(float(ligne[4]))
                nb_vols_init.append(float(ligne[5]))
                nb_vols_fin.append(float(ligne[6]))
                nb_avions_constr.append(float(ligne[7]))

            f.close()

            df_all_data["Capacity"] = capa
            df_all_data["Nb initial passagers avion"] = pass_init
            df_all_data["Nb final passagers avion"] = pass_fin
            df_all_data["Nb initial vols"] = nb_vols_init
            df_all_data["Nb final vols"] = nb_vols_fin
            df_all_data["Nb nouveaux avions"] = nb_avions_constr

            df_all_data.to_excel(writer, sheet_name=scenarii[i], startcol=12 * j)
