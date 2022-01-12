# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 20:07:43 2022

@author: adjou
"""
#Importer les tkinter pour l'interface 
import tkinter as tk
#from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
# Importation des Libraries
import string
## importation de re pour la recherche de mots dans le texte
import re
## Pour accéder à l'url de la page et récupérer les données
import urllib, urllib.request
import xmltodict
import datetime
## Construction de la classe Donnes
class Donnes:
    # Initialisation des variables de la classe
    def __init__(self, titre="", date="", texte=""):
        self.titre = titre #Le titre du document
        self.date = date  # La date de modification du document
        self.texte = texte # Le texte du document
        self.docs_bruts=[] #liste contenant les données d'arxiv sur deepfake
        # dictionnaire vide qui prend comme clé les trimestres des années et comme valeur une liste des ocuurences
        self.dictionnaire = {'trim1_2020':[],'trim2_2020':[],'trim3_2020':[],'trim4_2020':[],'trim1_2021':[],'trim2_2021':[],'trim3_2021':[],'trim4_2021':[]}
    # Fonction qui return le type     
    def get_type(self):
        return self.type
    
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tDate : {self.date}\tTexte : {self.texte}\t"
     # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.texte}, par {self.date}"
    
    ## Fonction pour scraper les données
    def scrapper_arxiv(self,query_terms,max_results):
        # Requête (url pour accéder à la page)
        url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
        data = urllib.request.urlopen(url)
        # Format des données en utf-8
        data = xmltodict.parse(data.read().decode('utf-8'))
        # création de liste vide pour récupérer le texte
        docs = []       
        # Parcourir les données récupérée
        for i, entry in enumerate(data["feed"]["entry"]):
            # récupérer les textes dont les dates de modifications du document sont supérieures à 2020 
            if (entry["updated"] < '2020-01-01T00:00:00-05:00'):
                pass
            else : 
                # Ajouté le texte récupéré à la liste
                docs.append(entry["summary"].replace("\n", ""))
                # Ajouté les données scrapper à docs_bruts
                self.docs_bruts.append( entry)
        ## recupération du titre, date et texte
        # création de liste vide pour récupérer les données(titre, date, texte)
        collection = []
        # parcourir docs_bruts
        for doc in self.docs_bruts:
            titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
            summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
            # Formatage de la date en année/mois/jour avec librairie datetime
            date = datetime.datetime.strptime(doc["updated"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  
            doc_classe_pro = Donnes(titre, date, summary)  # Création du document 
            collection.append(doc_classe_pro)  # Ajout du Document à la liste.
        return docs

           
    ## fonction pour joindre chaque document
    def joindre(self,docs):     
        Corpus = " ".join(docs)
        return Corpus 
    ## fonction pour le nettoyage du test
    def nettoyage(self,ligne, hist):
        self.ligne = ligne
        self.hist = hist 
        ponctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~''' 
        for char in ponctuation:
            ligne = ligne.replace(char, ' ') 
            
        #ligne = ligne.replace('-', ' ')                    
            for mot in ligne.split():
                
                mot = mot.strip(string.punctuation + string.whitespace)
                mot = mot.upper()
                hist[mot] = hist.get(mot, 0) + 1

            
    ## fonction pour parcourir chaque mot et afficher la fréquence                   
    def parcourir(self,Corpus):
        self.Corpus = Corpus
        hist = dict()
        #fp = open(Corpus)
        #fp = nom_fichier
        for ligne in Corpus.split():
            self.nettoyage(ligne, hist)
        return hist
    
    ## fonction pour compter le nombre total de mot
    def total_mots(self,hist):   
        self.hist = hist 
        return sum(hist.values())
    
    ## fonction pour compter le nombre de mot différent
    def different_mots(self,hist):  
        self.hist =hist
        return len(hist)
    
    ## fonction pour compter le mot le plus fréquent dans le texte
    def plus_frequents(self,hist,num):  
        self.hist = hist
        t = []
        for key, value in hist.items():
            t.append((value, key))

        t.sort(reverse=True)
        return t
    
    ## Création d'un dataframe des mots fréquents selon les trimstres de 2020 et 2021.
    ## La méthode prend en entrée une liste de mots les plus fréquents
    
    def Séparation(self,Listes_mots):
            ## Création d'un dictionnaire pour la fréquence des mots par trimestres
        #dictionnaire = {'trim1':[],'trim2':[],'trim3':[],'trim4':[]}
        ## Parcourir la liste des mots les plus fréquents
        for v in Listes_mots:
            #Initialiser les valeurs des trimestres à 0 à chaque nouveau mot.
            Trim1 = 0
            Trim2 = 0
            Trim3 = 0
            Trim4 = 0

            #print(v)
            # parcourir docs_bruts
            for doc in self.docs_bruts:
                # Formatage de la date en année/mois/jour avec librairie datetime
                date = datetime.datetime.strptime(doc["updated"],"%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d") 
                date = datetime.datetime.strptime(date,"%Y/%m/%d") 
                # récuperation du texte
                summary = doc["summary"].replace("\n", "").lower()
                #print(summary)
                # Traiter le document en enlévant ce qui est dans la ponctuation
                ponctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~''' 
                for char in ponctuation:
                    summary = summary.replace(char, ' ') 
                
                ## Séparation par trimestre pour l'année 2020
                
                ## Récupération des textes du 1 er trimestre
                if (date > datetime.datetime.strptime('2020-01-01',"%Y-%m-%d")) & (date <= datetime.datetime.strptime('2020-03-31',"%Y-%m-%d")):
                    ## on recherche les mots de la liste des mot dans le summary du 1 er trimestre, on compte le nombre de fois qu'il sont apprus et l'ajoute à Trim1
                    Trim1+=len(re.findall(v,summary))
                ## Récupération des textes du 1 er trimestre   
                if (date >= datetime.datetime.strptime('2020-04-01',"%Y-%m-%d")) & (date <= datetime.datetime.strptime('2020-06-30',"%Y-%m-%d")):
                    ## on recherche les mots de la liste des mot dans le summary du 2 eme trimestre, on compte le nombre de fois qu'il sont apprus et l'ajoute à Trim2 
                    Trim2+=len(re.findall(v, summary))
                   
                ## Récupération des textes du 1 er trimestre    
                if (date >= datetime.datetime.strptime('2020-07-01',"%Y-%m-%d")) & (date <= datetime.datetime.strptime('2020-09-30',"%Y-%m-%d")):
                    ## on recherche les mots de la liste des mot dans le summary du 3 eme trimestre, on compte le nombre de fois qu'il sont apprus et l'ajoute à Trim3 
                    Trim3+=len(re.findall(v, summary)) 
                ## Récupération des textes du 1 er trimestre    
                if (date >= datetime.datetime.strptime('2020-10-01',"%Y-%m-%d")) & (date <= datetime.datetime.strptime('2020-12-31',"%Y-%m-%d")):
                    ## on recherche les mots de la liste des mot dans le summary du 4 eme trimestre, on compte le nombre de fois qu'il sont apprus et l'ajoute à Trim4 
                    Trim4+=len(re.findall(v, summary)) 
                    
                    ## Séparation par trimestre pour l'année 2021
                ## Récupération des textes du 1 er trimestre    
                if (date > datetime.datetime.strptime('2021-01-01',"%Y-%m-%d")) & (date <= datetime.datetime.strptime('2021-03-31',"%Y-%m-%d")):
                    ## on recherche les mots de la liste des mot dans le summary du 1 er trimestre, on compte le nombre de fois qu'il sont apprus et l'ajoute à Trim1 
                    Trim1+=len(re.findall(v,summary))
                
                ## Récupération des textes du 1 er trimestre    
                if (date >= datetime.datetime.strptime('2021-04-01',"%Y-%m-%d")) & (date <= datetime.datetime.strptime('2021-06-30',"%Y-%m-%d")):
                    ## on recherche les mots de la liste des mot dans le summary du 2 eme trimestre, on compte le nombre de fois qu'il sont apprus et l'ajoute à Trim2
                    Trim2+=len(re.findall(v, summary))
                   
                ## Récupération des textes du 1 er trimestre    
                if (date >= datetime.datetime.strptime('2021-07-01',"%Y-%m-%d")) & (date <= datetime.datetime.strptime('2021-09-30',"%Y-%m-%d")):
                    ## on recherche les mots de la liste des mot dans le summary du 3 eme trimestre, on compte le nombre de fois qu'il sont apprus et l'ajoute à Trim3 
                    Trim3+=len(re.findall(v, summary)) 
                
                ## Récupération des textes du 1 er trimestre    
                if (date >= datetime.datetime.strptime('2021-10-01',"%Y-%m-%d")) & (date <= datetime.datetime.strptime('2021-12-31',"%Y-%m-%d")):
                    ## on recherche les mots de la liste des mot dans le summary du 4 eme trimestre, on compte le nombre de fois qu'il sont apprus et l'ajoute à Trim4
                    Trim4+=len(re.findall(v, summary))     
            # ajouter le nombre d'occurences selon les trimestres au dictionnaire        
            self.dictionnaire["trim1_2020"].append(Trim1)
            self.dictionnaire["trim2_2020"].append(Trim2)
            self.dictionnaire["trim3_2020"].append(Trim3)
            self.dictionnaire["trim4_2020"].append(Trim4)
            self.dictionnaire["trim1_2021"].append(Trim1)
            self.dictionnaire["trim2_2021"].append(Trim2)
            self.dictionnaire["trim3_2021"].append(Trim3)
            self.dictionnaire["trim4_2021"].append(Trim4)
            
         #Covertir en dataframe 
        self.dictionnaire = pd.DataFrame(self.dictionnaire)
        return self.dictionnaire
    ## pour avoir la fréquence des mots les plus fréquences des termes de la liste
    def compteTF(self,MotDict, decoupe):
        tfDict = {}
        MotCount = len(decoupe)
        for word, count in MotDict.items():
            tfDict[word] = count / float(MotCount)
        return tfDict
    
    # Méthode de l'interface Tkinter qui prend en entrée la liste des mots les plus frèquents et la datframe retourner par la fonction 
    def interfaceTkinter(self, Listes_mots, Datas) : 
        #instanciation de tkinter
        root= tk.Tk() 
        #Parcourir la liste des mots 
        for i, valeur in enumerate(Listes_mots): 
            #Configuartion de chaque graphique
            figure = plt.figure(figsize=(3,3))
            #Ajouter le graph avec subplot
            axe = figure.add_subplot(111)
            lines = FigureCanvasTkAgg(figure, root)
            #lines.show()
            lines.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            #Faire un lineplot 
            Datas.iloc[i,].plot(label = valeur, kind='line', legend=True, ax=axe,marker='o', fontsize=10)
            #Ajouter un titre
            axe.set_title("Graphique de l\'evolution du mot suivant les trimestres de l\'année 2020")
          #runner l'application 
        root.mainloop()     
           
