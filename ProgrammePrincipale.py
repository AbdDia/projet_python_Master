# -*- coding: utf-8 -*-
#Importation de la librairie Praw pour le scrapping des données 
import praw
#Importation du module 
import Classes

#Instanciation de praw
praw_user = praw.Reddit(client_id ="Vtfyg1CVHm7bHIMf92b4yg", client_secret = "oeabhR2MNpphu3m-ZIf9sz9Qgu9qDg", user_agent = "WebScrapping" )

#Instanciation de la classe
d = Classes.DeepFakeRedditTextAnalysis()

#Appel de la méthode scrapper pour 1000 docs avec SFWdeepfakes comme thème.
#Cette Méthode retourne une liste de documents avec le titre, la  date et contenu
corpus = d.redditScrapper('SFWdeepfakes', praw_user, 1000)


#Jointure des documents.
#La fonction prend en entrée deux une liste de documents et retourne une chaine de tous les fichiers documents joins.
chaine = d.textJoin(corpus)


#Cette focntion prend en entrée un chaine de caractères, fait le traitement en enlevant les mots vides(articles,...) et les ponctuations.
chaine = d.textProcessing(chaine)


#Une fonction qui prend en entrée un nombre et qui retourne le nombre de mots les plus frèquents correspondant.
d.findCommonWords(10) #retourne les 10 mots les plus fréquents

#définir une liste des mots parmi les plus frèquents que l'on veut afficher dans l'interface.
listMots = ["deepfacelab", "cuda", "face", "video", "process" ]

#Appel de la méthode dataFrameMotsFrequents qui prend en entrée une liste de mots.
#Et retourne pour chaque motle nombre d'utilisation par trimestre.
data = d.dataFrameMotsFrequents(listMots)

#Afficher l'inteface avec Tkinter
#Prend en entrée une liste de mots et la valeur retourner par la méthode dataFrameMotsFrequents()
d.interfaceTkinter(listMots, data)
 







