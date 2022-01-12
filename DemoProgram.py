# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 18:31:58 2022

@author: HP
"""
#Importer praw pour scrapper reddit
import praw
#Importer les librairies pour scrapper arxiv
import urllib, urllib.request, _collections
import xmltodict
#import les lbrairies pour le traitement des dates
import datetime
from datetime import datetime

#Importation du module 
import Classes as cl
#importation du module Interface
import Interface as inter



############################################# Appel de la classe Reddit ######################################""


#Instancié la classe
reddit = cl.Reddit()

#créer un liste qui contient les données scrapper sur reddit. La liste comprend le titre, la date et contenu
docs_reddit = []
#Instanciation de praw
praw_user = praw.Reddit(client_id ="Vtfyg1CVHm7bHIMf92b4yg", client_secret = "oeabhR2MNpphu3m-ZIf9sz9Qgu9qDg", user_agent = "WebScrapping", check_for_async=False)

#'', praw_user, 1000
#Scraper les tendances du subreddit SFWdeepfakes
tendance = praw_user.subreddit('SFWdeepfakes')
#scraper les 1000 docs les plus tendances avec "hot" 
for post in tendance.hot(limit = 1000):
    #Récuperer le contenu, la titre et la date
    contenu = post.selftext.replace('\n', ' ')#Recuperer le contenu et remplacer les retours à la ligne par espace
    titre = post.title.replace('\n', ' ')#retrieve le titre et remplacer les retours à la ligne par des spaces
    date = datetime.fromtimestamp(post.created).strftime("%Y/%m/%d")#recuperer la date 
    #Tester si le contenu est vide et la date inférieure janvier 2020 ou superieure a 2020 ne pas le prendre en compte
    if(len(contenu)==0 or (date < '2020-01-01' or date > '2022-01-01')): 
        pass
    else : 
        #Ajouter le documet dans dans la liste
        docs_reddit.append([titre, date, contenu])

#Appel de la méthode textJoinqui prend en entrée les docs de reddit et qui retourne une chaine de tous les docs.
chaine = reddit.textJoin(docs_reddit)
#La méthode textProcessing de la classe reddit prend une chaine ou un doc en entrée et fait le traitement
chaine_reddit = reddit.textProcessing(chaine)
###################################")
reddit.vocabulaire()
#findCommonWords retourne les mots les plus fréquents. Il prend en entrée le nombre de mots voulu
reddit.findCommonWords(30)
#Ici on a tester avec 5 mots féquents parmi les 30. 
motsreddit = ["deepfacelab", "question", "sample", "video", "options"]
#Retourne un dictionnaire de la fréquence d'utilisation des mots selon les trimestres.
data_reddit = reddit.dataFrameMotsFrequents(motsreddit, docs_reddit)
print(data_reddit)

############################################# Appel de la classe Arxiv ######################################""

#Instancié la classe
arxiv = cl.Arxiv()

#créer une liste qui va contenir les données scrapper sur arxiv.
docs_arxiv = []
#Mettre en place notre requete 
url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(["deepfake"])}&start=0&max_results={185}'
data = urllib.request.urlopen(url)
# Format dict (OrderedDict)
data = xmltodict.parse(data.read().decode('utf-8'))
# Récupération du texte
# Parcourir les données récupérée
for i, entry in enumerate(data["feed"]["entry"]):
        # récupérer les textes dont les dates sont supérieures à 2020 et inférieure à 2022
    if (entry["updated"] < '2020-01-01T00:00:00-05:00' or entry["updated"] > '2022-01-01T00:00:00-05:00'):
        pass
    else : 
        #Recuperer la date 
        date_arxiv = datetime.strptime(entry["updated"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")
        #On retrieve le titre
        titre_arxiv = entry["title"].replace('\n', '')  # On enlève les retours à la ligne
        #Le contenu 
        summary = entry["summary"].replace("\n", "")  # On enlève les retours à la ligne
        #Ajouter à la liste
        docs_arxiv.append([titre_arxiv, date_arxiv, summary])

      
#Appel de la méthode textJoinqui prend en entrée les docs de reddit et qui retourne une chaine de tous les docs.
chaine_arxiv = arxiv.textJoin(docs_arxiv)
#La méthode textProcessing de la classe reddit prend une chaine ou un doc en entrée et fait le traitement
chaine_arxiv = arxiv.textProcessing(chaine_arxiv)
###################################")
arxiv.vocabulaire()
#findCommonWords retourne les mots les plus fréquents. Il prend en entrée le nombre de mots voulu
arxiv.findCommonWords(30) 
#Ici on a tester avec 5 mots féquents parmi les 30. 
motsarxiv = ["videos", "detection", "faces", "videos" , "image"] 
#Retourne un dictionnaire de la fréquence d'utilisation des mots selon les trimestres.      
data_arxiv = arxiv.dataFrameMotsFrequents(motsarxiv, docs_arxiv)  
print(data_arxiv) 
 

############################################# Appel de la classe Comparaison_corpus ######################################""


#instanciation  de la classe Comparaison_corpus. La classe reçoit les deux chaines arxiv et reddit.
p = cl.Comparaison_corpus(chaine_arxiv, chaine_reddit)


## Pour trouver les mots que les deux corpus ont en commun, 
commun = p.mots_communs()
#print(diff)
c=[]
print('Mots communs aux deux corpus :')
for motc in commun.values(): 
    #print(motc, end=' ')
    c.append(motc)

chaineCommun = " ".join(c)
print(chaineCommun)

##mots_different_Reddit(), permet de trouver les mots qui sont dans reddit et qui ne sont pas arxiv
print(p.mots_different_Reddit())
##mots_different_Arxiv(), permet de trouver les mots qui sont dans arxiv et qui ne sont pas reddit
print(p.mots_different_Arxiv())


###########################################Appel de la classe interface########################################"
#Instanciation de la classe. Elle prend en entrée les dataframe retourner par la méthode findCommonWords et les chaines data_arxiv et data_reddit.
graph = inter.InterfaceTkinter(data_arxiv, data_reddit, motsarxiv, motsreddit)
graph.interface()
