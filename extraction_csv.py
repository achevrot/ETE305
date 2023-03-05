import pandas as pd

df_all_data = pd.read_csv('..\Données EuroControl 2019\Mars 2019.csv')

df_all_data = df_all_data.loc[df_all_data['ADEP'].str.startswith('ED', na=False)]
df_all_data = df_all_data.loc[df_all_data['ADES'].str.startswith('ED', na=False)]
df_all_data = df_all_data.drop(df_all_data[df_all_data['STATFOR Market Segment'] == 'All-Cargo'].index)
# A commenter si on veut finalement prendre en compte les jets
####
df_all_data = df_all_data.drop(df_all_data[df_all_data['STATFOR Market Segment'] == 'Charter'].index)
df_all_data = df_all_data.drop(df_all_data[df_all_data['STATFOR Market Segment'] == 'Business Aviation'].index)
####
# Suppression des colonnes inutiles
df_all_data.drop(columns=['ECTRL ID','FILED OFF BLOCK TIME','FILED ARRIVAL TIME','ACTUAL OFF BLOCK TIME','ACTUAL ARRIVAL TIME','AC Operator','AC Registration','Requested FL'], inplace=True)
df_all_data = df_all_data.reset_index(drop=True)

df_all_data.to_csv('201903_interieur.csv')