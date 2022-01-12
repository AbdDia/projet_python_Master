
#importation des libraries pour l'interface tkinter 
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

from random import randint

class InterfaceTkinter:
    def __init__(self,data_arxiv, data_reddit, motsarxiv, motsreddit) : 
        self.data_arxiv = data_arxiv
        self.data_reddit = data_reddit
        self.motsarxiv = motsarxiv
        self.motsreddit = motsreddit
        self.colors = []
        
    

    def interface(self):
        for i in range(12):
            self.colors.append('#%06X' % randint(0, 0xFFFFFF))
                 
        #Instanciation de tkinter
        root= tk.Tk()
        #Convertir les données en dataframe
        self.data_arxiv = pd.DataFrame(self.data_arxiv)
        self.data_reddit = pd.DataFrame(self.data_reddit)

        #instancié Canvas
        canvas1 = tk.Canvas(root, width = 1200, height = 300)
        canvas1.pack() #Definir la géometrie avec pack() de tkinter
        #Le Label() de tkinter permet de faire un titre
        label1 = tk.Label(root, text='Evolution des mots selon les trimestres en 2020 et 2021')
        label1.config(font=('Arial', 20))#Le font et la taille du titre
        #Créer un fenetre canvas
        canvas1.create_window(400, 50, window=label1)
        #faire le setup de l'environnement graphique 1
        figure1 = Figure(figsize=(7,5), dpi=100)
        #Ajouter le graphique 1 avec les 
        subplot1 = figure1.add_subplot(111)
        #Ajouter le titre
        subplot1.title.set_text('Arxiv')
        #Associé la figure et le root de tkinter 
        line = FigureCanvasTkAgg(figure1, root)
        line.name='latheesh'
        #Etablissement 
        line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)


        #faire le setup de l'environnement graphique 1
        figure2 = Figure(figsize=(7,5), dpi=100)
        subplot2 = figure2.add_subplot(111)
        #Ajouter le titre
        subplot2.title.set_text('Reddit')
        line = FigureCanvasTkAgg(figure2, root)
        line.name='latheesh'
        line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        
        #Tracer la figure arxiv
        for i, valeur in enumerate(self.motsarxiv): 
            subplot1.plot(self.data_arxiv.iloc[i,],marker='o', label = valeur)
        #tracer la figure reddit
        for i, valeur in enumerate(self.motsreddit): 
            subplot2.plot(self.data_reddit.iloc[i,],marker='o')
                
        root.mainloop()