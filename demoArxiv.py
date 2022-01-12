# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 20:07:42 2022

@author: adjou
"""
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


#### Frequence Mot dans le Corpus 
## affichage de l'histogramme des mots
p.hist = p.parcourir(document)
print(p.hist)
print('Nombre total de mots :', p.total_mots(p.hist))
print('Nombre de mots différents :', p.different_mots(p.hist))   
## affichage des 30 mots les plus fréquents 
num=30
t = p.plus_frequents(p.hist,num)
print('Les mots les plus fréquents sont :')
for freq, mot in t[:num]:
    print(mot, freq, sep='\t')   
    
#### Evolution du Mot au cours des années 

## Listes des mots les plus fréquents (choisi 5 mots)
Listes_mots=['detection','face','videos','image','methods']
Datas=p.Séparation(Listes_mots)
#print(Datas)
"""
#### Frequence des termes de la liste de mots 

## découpage du document par mot
decoupe=document.split(' ')
## dictionnaire de chaque mot avec leur fréquence
num_mot = dict.fromkeys(decoupe, 0)
for word in decoupe:
    num_mot[word] += 1
#print(numOfWordsA)

## dictionnaire des mots les plus fréquences avec leurs fréquences
MotDict={'detection':7160,'face':4982,'videos':4429,'image':3646,'methods':4036}
tfA=p.compteTF(MotDict,decoupe)
print(tfA)
"""
#Afficher l'inteface avec Tkinter
#Prend en entrée une liste de mots et la valeur retourner par la méthode Séparation()
p.interfaceTkinter(Listes_mots, Datas)
