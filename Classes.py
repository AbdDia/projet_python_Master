#importer nltk librairie NLP. Dans ce cas on va utlisé les stopwords pour enlever les mots vides de nos données
import nltk
#importer les mots vide et instanciation
from nltk.corpus import stopwords
nltk.download('stopwords')
#Importer la librairie Regex de Python 
import re 
#Importer la librairie Opretor de python
import operator
#IMPORTER datetime 
from datetime import datetime
#importer pandas
#import pandas as pd



class PyNLP :
    def __init__(self, doctext = "", motscommuns = {}, vocabular = {}) : 
        #chaine contenant tous les documents joins
        self.doctext = doctext
        #dictionnaire des mots les plus fréquents 
        self.motscommuns = motscommuns
        #le dictionnaire des vacabulaires
        self.vocabular = vocabular
        #créer un dictionnaire vide qui prend comme clé les trimestres de l'année et comme valeur une liste des ocuurences
        self.motsfrequents = {'trim1_2020':[],'trim2_2020':[],'trim3_2020':[],'trim4_2020':[],'trim1_2021':[],'trim2_2021':[],'trim3_2021':[],'trim4_2021':[]}
        
        
    def textJoin(self, listedocs) :
        for text in listedocs : 
            #Ajout du texte à notre chaine
            self.doctext += text[2]
        return self.doctext
    
    
    #Méthode de traitement de la chaine : Enlever les ponctuations et la mattre en minuscule
    def textProcessing(self, text):#Prend une chaine en entrée
        #Mettre le texte en minuscule avec lower() de python
        self.doctext = text.lower()
        #Enlever les caractères suivant  de la chaine
        symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n,-"
        for ponctuation in symbols : 
            self.doctext = self.doctext.replace(ponctuation, " ")
        #Supprimmer les liens
        self.doctext = re.sub(r"https?://\S+", "", self.doctext)
        #Enlever les balises html de 
        self.doctext = re.sub(r"<a[^>]*>(.*?)</a>", r"\1", self.doctext)
        #Enlever les nombres
        self.doctext = re.sub(r"\b[0-9]+\b\s*", "", self.doctext)
        #motsvide prend la liste des stopwors de nltk
        motsvide = stopwords.words('english')
        #Créer une liste de mots avec split()
        listemots = self.doctext.split()
        docP = [] #Créer une liste vide 
        for mot in listemots : 
            if (mot in motsvide or len(mot)<1) :# Testet si le mot est un stopword ou sa taille est 1
                pass #exclure le mot
            else : 
                docP.append(mot)#Ajouter les mots pertinents
        self.doctext = docP.copy()#faire une copie de docP dans self.doctext
        #mettre en format txt
        self.doctext = ' '.join(str(e) for e in self.doctext)
        #Supprimer les multispaces de notre text
        self.doctext = re.sub(' +', ' ', self.doctext)
        #retourner un document traiter
        return self.doctext
    
    
    #Méthode pour trouver les mots les plus fréquents dans la chaine sef.doctext
    def vocabulaire(self) :
        #Splitter le document avec espace comme separateur
        dictionnaire = self.doctext .split()
        #determiner les valeurs unique de notre texte
        for i, mot in enumerate(dictionnaire) :
          if mot not in self.vocabular.values():
            self.vocabular[i]=mot
    
    
    #Méthode pour trouver les mots les plus fréquents et 
    def findCommonWords(self, nombre) :
        for valeur in self.vocabular.values():
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
           #Arreter le programme lorsqu'on a atteint le nombre passée en paramètre.
           if (i>nombre) : 
               break
         
           
   #Créer un dataframe des mots fréquents selon le trimstre 2020. La méthode prend en entrée une liste de mots les plus fréquents
    def dataFrameMotsFrequents(self, listeMots, corpus):
        for mots in listeMots : #Parcourir la liste des mots les plus fréquents
            #Initialiser les valeurs des trimestres à 0 à chaque nouveau mot.
            trim1_2020 = 0
            trim2_2020 = 0
            trim3_2020 = 0
            trim4_2020 = 0
            trim1_2021 = 0
            trim2_2021 = 0
            trim3_2021 = 0
            trim4_2021 = 0

            for text in corpus :#Le corpus contient le titre, la date et le contenu de chaque document
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
                            trim1_2020 +=1 #Ajouter 1  au trimestre
                    #trim1+=len(re.findall(mots, doc))#Compter le nombre de fois que le mots est apparut dans le poste et l'ajouter à trim1
                #tester si le post a été pubié au trimestre 2
                elif((date >= datetime.strptime("2020-04-01", '%Y-%m-%d')) and (date <= datetime.strptime("2020-06-30", '%Y-%m-%d'))) : 
                    #trim2+=len(re.findall(mots, doc))#Ajouter le mots 
                    liste = doc.split()
                    for occurence in liste:
                        if mots == occurence:
                            trim2_2020 += 1
                #
                elif((date >= datetime.strptime("2020-06-01", '%Y-%m-%d')) and (date <= datetime.strptime("2020-09-30", '%Y-%m-%d'))) :
                    #trim3+=len(re.findall(mots, doc))
                    liste = doc.split()
                    for occurence in liste:
                        if mots == occurence:
                            trim3_2020 += 1
                elif((date >= datetime.strptime("2020-09-01", '%Y-%m-%d')) and (date <= datetime.strptime("2021-12-31", '%Y-%m-%d'))) :
                    #trim4+=len(re.findall(mots, doc))
                    liste = doc.split()
                    for occurence in liste:
                        if mots == occurence:
                            trim4_2020 += 1
   #Selon la date de publication du post, chercher le mots et compter son nombre d'occurence dans le post et enfin l'ajouter au trimestre correspondant
            ## 2021
                if((date >= datetime.strptime("2021-01-01", '%Y-%m-%d')) and (date <= datetime.strptime("2021-03-31", '%Y-%m-%d'))) :#tester si le post a été publié au trimestre 1
            #Spliter le document en liste de mots 
                    liste = doc.split()
                    for occurence in liste: #Parcourir la liste 
                        if mots == occurence:#Si le mots choisis est égal au mot courant alors : 
                            trim1_2021 = trim1_2021 + 1 #Ajouter 1  au trimestre
                #trim1+=len(re.findall(mots, doc))#Compter le nombre de fois que le mots est apparut dans le poste et l'ajouter à trim1
            #tester si le post a été pubié au trimestre 2
                elif((date >= datetime.strptime("2021-04-01", '%Y-%m-%d')) and (date <= datetime.strptime("2021-06-30", '%Y-%m-%d'))) : 
                #trim2+=len(re.findall(mots, doc))#Ajouter le mots 
                    liste = doc.split()
                    for occurence in liste:
                        if mots == occurence:
                            trim2_2021 = trim2_2021 + 1
                #
                elif((date >= datetime.strptime("2021-06-01", '%Y-%m-%d')) and (date <= datetime.strptime("2021-09-30", '%Y-%m-%d'))) :
                    #trim3+=len(re.findall(mots, doc))
                    liste = doc.split()
                    for occurence in liste:
                        if mots == occurence:
                            trim3_2021 = trim3_2021 + 1
                elif((date >= datetime.strptime("2021-09-01", '%Y-%m-%d')) and (date <= datetime.strptime("2021-12-31", '%Y-%m-%d'))) :
                    #trim4+=len(re.findall(mots, doc))
                    liste = doc.split()
                    for occurence in liste:
                        if mots == occurence:
                            trim4_2021 = trim4_2021 + 1
            #Ajouter le nombre d'occurences selon les trimestres  
            self.motsfrequents["trim1_2020"].append(trim1_2020)
            self.motsfrequents["trim2_2020"].append(trim2_2020)
            self.motsfrequents["trim3_2020"].append(trim3_2020)
            self.motsfrequents["trim4_2020"].append(trim4_2020)
            self.motsfrequents["trim1_2021"].append(trim1_2021)
            self.motsfrequents["trim2_2021"].append(trim2_2021)
            self.motsfrequents["trim3_2021"].append(trim3_2021)
            self.motsfrequents["trim4_2021"].append(trim4_2021)
         #Covertir en dataframe 
        #self.motsfrequents = pd.DataFrame(self.motsfrequents)
        #Valeur de retour 
        return self.motsfrequents




class Reddit(PyNLP) :
    def __init__(self, doctext = "", vocabular = {}, motscommuns = {}) : 
        PyNLP.__init__(self, doctext, vocabular, motscommuns)
      
  
        
  

class Arxiv(PyNLP) : 
    def __init__(self, doctext = "", vocabular = {}, motscommuns = {}) : 
        PyNLP.__init__(self, doctext, vocabular, motscommuns)
        



# La classe Comparaison_corpus permet de voir les mots en commun et les mots diffents entre deux corpus.
#Il prend comme paramètres deux documents (string) d1 et d2.
class  Comparaison_corpus:
    
    def __init__(self,d1, d2): 
        #definir d1 et d2 qui sont des listes de mots de chaque document
        self.d1 = d1.split()
        self.d2 = d2.split()
    
    ## Pour trouver les mots que les deux corpus ont en commun,     
    def mots_communs(self):
        dictcommuns = dict()
        #self.d1 = self.d1.split()
        #self.d2 = self.d2.split()
        for i, clef in enumerate(self.d1) : 
            if clef in self.d2:
                dictcommuns[i] = clef
        return dictcommuns
    
    ## Pour trouver les mots qui sont dans Arxiv et qui ne sont pas dans Reddict ,
    def mots_different_Reddit(self):
        dictdiff1 = dict()
        for i, clef in enumerate(self.d1) : 
            if clef not in self.d2:
                dictdiff1[i] = clef
        return dictdiff1
    
    ## Pour trouver les mots qui sont dans Arxiv et qui ne sont pas dans Reddict,
    def mots_different_Arxiv(self):
        dictdiff2 = dict()#créer un dictionnaire 
        for i, clef in enumerate(self.d2) : #parcourir la liste d2
            if clef not in self.d1:#tester si le mot n'est pas dans d2
                dictdiff2[i] = clef
        return dictdiff2