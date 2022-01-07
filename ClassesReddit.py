# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 14:47:57 2021

@author: HP
"""
#Importer les tkinter pour l'interface 
import tkinter as tk
#from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Importer pandas et numpy 
import pandas as pd
#import numpy as np
#importer la librairie datetime pour le traitement des données
from datetime import datetime
import re
import operator

#import matplotlib as plt

import spacy
#Initialisation 
nlp=spacy.load("en_core_web_sm")


class DeepFakeRedditTextAnalysis() : 
    def __init__(self) : 
        self.docs_reddit = []#liste contenant le contenu des documents, leur date de pub et leur titre
        self.contenu =  ""#Le contenu du document
        self.date = 0#La date de publication
        self.titre = ""#Le titre du document
        self.doctext = "" #chaine contenant tous les documents joins
        #le dictionnaire des vacabulaires
        self.vocabulaire = {}
        #dictionnaire des mots les plus fréquents 
        self.motscommuns = {}
        #créer un dictionnaire vide qui prend comme clé les trimestres de l'année et comme valeur une liste des ocuurences
        self.motsfrequents = {"Trim1" : [],"Trim2" : [],"Trim3"  : [],"Trim4"  : []}
        
        
        
        
    #fonction de scraping des données 
    def redditScrapper(self, sub_reddit, reddit, nombre):    #les arguments : la thématique, le nombre de documents et le subreddit
    #############"
        tendance = reddit.subreddit(sub_reddit)
        #scraper le docs les plus tendances avec "hot"
        for post in tendance.hot(limit = nombre):
            #Récuperer le contenu, la titre et la date
            self.contenu = post.selftext.replace('\n', ' ')
            self.titre = post.title.replace('\n', ' ')#remplacer les retours à la ligne par des spaces
            self.date = datetime.fromtimestamp(post.created).strftime("%Y/%m/%d")
            #si le contenu à moins de 100 lettres et la date inférieure janvier 2020 ne pas le prendre en compte
            if(len(self.contenu)==0 or self.date < '2020-01-01'): 
                pass
            else : #Ajouter le documet dans dans la liste
                self.docs_reddit.append([self.titre, self.date, self.contenu])
        return self.docs_reddit
    
    
    #Convertir en format dataframe la liste 
    def dataframe(self) :  
        return pd.DataFrame(self.docs_reddit, columns=['titre', 'date', 'contenu'])
    
    
    #Méthode pour joindre les documents Reddit
    def textJoin(self, docs) :
        for text in docs : 
            #Ajout du texte à notre chaine
            self.doctext += text[2]
        return self.doctext
    
    
    #Méthode de traitement de la chaine : Enlever les ponctuations et la mattre en minuscule
    def textProcessing(self, text):#Prend une chaine en entrée
        #Mettre le texte en minuscule avec lower() de python
        self.doctext = text.lower()
        #Enlever les caractères suivant  de la chaine
        ponctuations = "\_=/#<>"
        for ponctuation in ponctuations : 
            self.doctext = self.doctext.replace(ponctuation, " ")
        #Supprimer les multispaces de notre text
        self.doctext = re.sub(' +', ' ', self.doctext)
        #Supprimmer les liens
        self.doctext = re.sub(r"https?://\S+", "", self.doctext)
        #Enlever les balises html de 
        self.doctext = re.sub(r"<a[^>]*>(.*?)</a>", r"\1", self.doctext)
        #Enlever les nombres
        self.doctext = re.sub(r"\b[0-9]+\b\s*", "", self.doctext)
        
        #instanciaton de l'objet
        self.doctext = nlp(self.doctext)
        #enlver les ponctuations et les mots inutiles de notre text
        self.doctext = [token for token in self.doctext if not token.is_stop and not token.is_punct and len(token)>1]
        #Jointure
        self.doctext = ' '.join(str(e) for e in self.doctext)
        return self.doctext
    
        
    #Méthode pour trouver les mots les plus fréquents dans la chaine sef.doctext
    def vocabular(self, document) :
        #Splitter le document avec espace comme separateur
        document = document.split()
        #determiner les valeurs unique de notre texte
        for i, mot in enumerate(document) :
          if mot not in self.vocabulaire.values():
            self.vocabulaire[i]=mot
    
    
    #Méthode pour trouver les mots les plus fréquents et 
    def findCommonWords(self, nombre) :
        for valeur in self.vocabulaire.values():
          count = 0              # Initialiser le compteur à zero
          for word in self.doctext.split():     # Iterer sur les mots.
            if word == valeur:   # Test si le mot est egal au vocabulaire courant?
              count += 1     # incrementer de 1 si "True"
          if count>0 : #Test si le mot a au moins une occurence
              self.motscommuns[valeur]=count #Ajouter du mots
          else : #Au cas contraire rien faire
              pass
        #trier par mots les plus fréquents 
        self.motscommuns = dict( sorted(self.motscommuns.items(), key=operator.itemgetter(1),reverse=True))
        i = 1
        for key, valeur in self.motscommuns.items() :
           print(i, ": ", key," - ", valeur)
           i+=1
           #Arreter le programme lorsqu'o a atteint le nombre passée en paramètre.
           if (i>nombre) : 
               break
     
   #Créer un dataframe des mots fréquents selon le trimstre 2020. La méthode prend en entrée une liste de mots les plus fréquents
    def dataFrameMotsFrequents(self, listeMots):
        for mots in listeMots : #Parcourir la liste des mots les plus fréquents
            #Initialiser les valeurs des trimestres à 0 à chaque nouveau mot.
            trim1 = 0
            trim2 = 0
            trim3 = 0
            trim4 = 0
            for text in self.docs_reddit :#Le corpus contient le titre, la date et le contenu de chaque document
                #recuperer le contenu du document
                doc = text[2].lower()
                #Convertir en date 
                date = datetime.strptime(text[1], '%Y/%m/%d')
                #Traiter le document avec la méthode textProcessing
                doc = self.textProcessing(doc)
                #Selon la date de publication du post, chercher le mots et compter son nombre d'occurence dans le post et enfin l'ajouter au trimestre correspondant
                if(date <= datetime.strptime("2020-03-31", '%Y-%m-%d')) :#tester si le post a été publié au trimestre 1
                #Spliter le document en liste de mots 
                    liste = doc.split()
                    for occurence in liste: #Parcourir la liste 
                        if mots == occurence:#Si le mots choisis est égal au mot courant alors : 
                            trim1 = trim1 + 1 #Ajouter 1  au trimestre
                    #trim1+=len(re.findall(mots, doc))#Compter le nombre de fois que le mots est apparut dans le poste et l'ajouter à trim1
                #tester si le post a été pubié au trimestre 2
                elif((date >= datetime.strptime("2020-04-01", '%Y-%m-%d')) and (date <= datetime.strptime("2020-06-30", '%Y-%m-%d'))) : 
                    #trim2+=len(re.findall(mots, doc))#Ajouter le mots 
                    liste = doc.split()
                    for occurence in liste:
                        if mots == occurence:
                            trim2 = trim2 + 1
                #
                elif((date >= datetime.strptime("2020-06-01", '%Y-%m-%d')) and (date <= datetime.strptime("2020-09-30", '%Y-%m-%d'))) :
                    #trim3+=len(re.findall(mots, doc))
                    liste = doc.split()
                    for occurence in liste:
                        if mots == occurence:
                            trim3 = trim3 + 1
                elif((date >= datetime.strptime("2020-09-01", '%Y-%m-%d')) and (date <= datetime.strptime("2021-12-31", '%Y-%m-%d'))) :
                    #trim4+=len(re.findall(mots, doc))
                    liste = doc.split()
                    for occurence in liste:
                        if mots == occurence:
                            trim4 = trim4 + 1
            #Ajouter le nombre d'occurences selon les trimestres  
            self.motsfrequents["Trim1"].append(trim1)
            self.motsfrequents["Trim2"].append(trim2)
            self.motsfrequents["Trim3"].append(trim3)
            self.motsfrequents["Trim4"].append(trim4)
         #Covertir en dataframe 
        self.motsfrequents = pd.DataFrame(self.motsfrequents)
        #Valeur de retour 
        return self.motsfrequents
    
    
    #Méthode de l'interface Tkinter qui prend en entrée la liste des mots les plus frèquents et la datframe retourner par la fonction 
    def interfaceTkinter(self, listMots, data) : 
        #instanciation de tkinter
        root= tk.Tk() 
        #Parcourir la liste des mots 
        for i, valeur in enumerate(listMots): 
            #Configuartion de chaque graphique
            figure = plt.figure(figsize=(3,3))
            #Ajouter le graph avec subplot
            axe = figure.add_subplot(111)
            lines = FigureCanvasTkAgg(figure, root)
            lines.show()
            lines.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            #Faire un lineplot 
            data.iloc[i,].plot(label = valeur, kind='line', legend=True, ax=axe,marker='o', fontsize=10)
            #Ajouter un titre
            axe.set_title("Graphique de l\'evolution du mot suivant les trimestres de l\'année 2020")
          #runner l'application 
        root.mainloop()     
        
    
        
        
        
        
