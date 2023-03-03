import os
import numpy as np


nb_erreur = 0
CO2_fin = 0.
CO2_debut = 0.
for file in os.listdir('log'):
    if file.endswith('.txt'):
        f = open('log/'+file,'r')
        premiere_ligne = f.readline().split(':')
        if "Optimal" in premiere_ligne[-1]:
            for ligne in f:
                if "Début" in ligne:
                    CO2_debut += float(ligne.split(':')[-1])
                if "Fin" in ligne:
                    CO2_fin += float(ligne.split(':')[-1])
        else:
            nb_erreur += 1
        f.close()

# CO2 intital pour fichier "log"
CO2_debut = 0.
f = open('log/log_trajet0.txt')
for ligne in f:
    if "Début" in ligne:
        CO2_debut = float(ligne.split(':')[-1])
f.close()
print("CO2 initial   : "+str(round(CO2_debut)/1000)+" tCO2")
print("CO2 économisé : "+str(round(CO2_debut-CO2)/1000)+" tCO2")
print("Nombe de cas pour lesquels l'optim n'a pas fonctionné : "+str(nb_erreur))

