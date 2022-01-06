# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 20:07:42 2022

@author: adjou
"""

# Importation des Libraries

import Classes_pro
## Importation de la classe
from Classes_pro import Donnes
#instanciation  de la classe
p = Classes_pro.Donnes()
## appel de la fonction de scrapping
Entre=p.scrapper_arxiv(["deepfake"],185)
#print(Entre)
## appel de la fonction pour joindre les documents
document=p.joindre(Entre)
#print(document)


######################## Frequence Mot dans le Corpus #########################""
## affichage de l'histogramme des mots
p.hist = p.process_file(document)
print(p.hist)
print('Nombre total de mots :', p.total_mots(p.hist))
print('Nombre de mots différents :', p.different_mots(p.hist))   
## affichage des 30 mots les plus fréquents 
num=30
t = p.les_plus_frequents(p.hist,num)
print('Les mots les plus fréquents sont :')
for freq, mot in t[:num]:
    print(mot, freq, sep='\t')   
    
######################## Evolution du Mot au cours des années #########################

## Listes des mots les plus fréquents (choisi 5 mots)
Listes_mots=['detection','face','videos','image','methods']
Datas=p.Séparation(Listes_mots)
#print(Datas)

#############"" Frequence des termes de la liste de mots ################

decoupe=document.split(' ')

numOfWordsA = dict.fromkeys(decoupe, 0)
for word in decoupe:
    numOfWordsA[word] += 1
#print(numOfWordsA)

## dictionnaire des mots les plus fréquences avec leurs fréquences
wordDict={'detection':7160,'face':4982,'videos':4429,'image':3646,'methods':4036}
tfA=p.computeTF(wordDict,decoupe)
print(tfA)