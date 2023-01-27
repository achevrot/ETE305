#!/bin/python3

import os
import pandas as pd

directory="./"
data = pd.DataFrame()

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        data = pd.concat([data, pd.read_csv(directory + filename, sep=",")])

data = data.loc[data['ADEP'].str.startswith('ED', na=False)]
data = data.loc[data['ADES'].str.startswith('ED', na=False)]

print(len(data))

data.to_csv("201903_interieur.csv")