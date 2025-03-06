# -*- coding: utf-8 -*- 
"""
Created on Sun Dec  1 20:03:01 2024

@author: mathf
"""

## Liste des choses à ajouter
# Démolir bâtiment


from tkinter import *
import math
import random
import numpy as np
from scipy.optimize import fsolve
from PIL import Image, ImageTk
import time
import tkinter.messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

TEMPS_ABSOLU = 0

def reinit_fenetre():
    
    Batiment.bat = {}
    Batiment.LISTE_ID = []
    Batiment.liste_Batiment = []
    
    Surface_d_eau.surface = {}
    
    Arbre.arbre = {}
    Arbre.LISTE_ID = []

def maj_FONCTION_ACTUELLE(fct):
    global FONCTION_ACTUELLE
    FONCTION_ACTUELLE = fct
    INTERFACE.m.reinit_couleur()

LISTE_PARAMETRES = [("KET",30)]
BASE_DE_DONNEES = []
BASE_DE_DONNEES_VEGE = []
IRR_SOL = 0
OMBRAGE_BATIMENT  = 0.1
MATERIAU = {}
NOM_PARAM =[]
TEMP_VALEUR = {}
TEMP_VALEUR_EAU = {}
TEMP_VALEUR_MAT = {}
PRECIPITATION_ = {}
AUTRE_ENTREE_EAU_ = {}
EVAPORATION_ = {}
HR_VALEUR = {}
RESULTATS_SIMULATION= {}
FORMULE = "Variables physiques : \n EVAPOTRANSPIRATION(x,y,z) en mm/jour \n HUMIDITE(x,y,z) en % \n PRESSION(x,y,z) en Pa \n TEMPERATURE(x,y,z) en K \n VENT(x,y,z) en m/s \n IRRADIANCE_OMBRAGE(x,y,z) en W/m² \n SURFACE_EAU(x,y,z) en m² \n \n Paramètres sur les matériaux : \n ALBEDO(x,y,z) \n DIFFUSIVITE_THERMIQUE(x,y,z) \n CONDUCTIVITE_THERMIQUE(x,y,z) \n EMISSIVITE_THERMIQUE(x,y,z) \n POROSITE(x,y,z) \n PERMEABILITE(x,y,z) \n \n Fonctions spéciales : \n SURFACE_MAILLE(x,y,z) : surface d'une maille en m² \n RESULTATS_SIMU(x,y,z) : Résultats de la dernière simulation"

DESCRIPTION = {"PRESSION":"en Pa, vous donne la pression statique présent en chaque point de la maille.",
               "RECHAUFFEMENT":'En °C, renseigne sur comment les différents éléments du quadrillage participent à une élévation de température.',
               "RAFRAICHISSEMENT":'En °C, renseigne sur comment les différents éléments du quadrillage participent à une diminution de température.',
               "TEMPERATURE":'En K, renseigne sur la valeur de la température, avant de tenir compte des différents éléments du quadrillage.',
               "TEMPERATURE_CELSIUS":'En °C, renseigne sur la valeur de la température, avant de tenir compte des différents éléments du quadrillage.'
               ,"IRRADIANCE" : "En W/m² renseigne la valeur d'irradiance entrée dans l'onglet IRRADIANCE."
               ,"IRRADIANCE_OMBRAGE" : "En W/m², renseigne sur la valeur d'irradiance, en considérant les possibles ombrages"
               ,"TEMPERATURE_EAU":'En K, renseigne sur la valeur de la température de l\'eau en un point du maillage.'
               ,"EVAPOTRANSPIRATION":'en mm/jour, renseigne sur la quantité d\'évapotranspiration présente sur un maillage'
               ,'VENT':'en m/s, renseigne sur la vitesse du vent en un point du maillage'
               ,'HUMIDITE': 'en %, renseigne sur l\'humidité relative en un point du maillage'
               ,'ALBEDO':'sans unité, renseigne la quantité de rayonnement solaire réfléchi.'
               ,'SURFACE_EAU':'m², renseigne la surface d\'eau présente sur une maille.'
               ,'DIFFUSIVITE_THERMIQUE':'En m²/s, renseigne sur la diffisuvité thermique du matériau présent à la maille sélectionnée'
               ,'CONDUCTIVITE_THERMIQUE':'renseigne sur la conductivité thermique du matériau présent à la maille sélectionnée'
               ,'EMMISIVITE_THERMIQUE':'renseigne sur la émissivité thermique du matériau présent à la maille sélectionnée'
               ,'MASSE_VOLUMIQUE':'renseigne sur la masse volumique du revêtement présent à la maille sélectionnée'
, 'POROSITE': 'renseigne sur la porosité du matériau présent à la maille sélectionnée'
, 'EVAPOTRANSPIRATION_MATERIAU': 'renseigne sur l\'évapotranspiration d\'1 m² de matériau présent à la maille sélectionnée'
               ,'cp':'en J.K/kg, capacité thermique massique du revêtement'
                   ,"TEMPERATURE_MATERIAU":'en K'
                   , "TEMPERATURE_MATERIAU_CELSIUS":"en °C"
                   ,"RESULTATS_SIMU":"affiche le résultat de la dernière simulation. La grandeur et les unités sont \ncelles de la grandeur entrée avant de lancer la simulation."
                   ,"PENTE_TVS":"pente de vapeur saturante (en Pa/°C)"
                   ,"EVAPOTRANSPIRATION_LITRE":"en L/jour, quantité d'eau lachée dans l'atmosphère par évapotranspiration en L/jour"}
cos = math.cos
sin = math.sin
pi = math.pi
exp = math.exp
CST_e = exp(1)
floor = math.floor
sqrt = math.sqrt


class Interface(Tk):
    TOUCHE_ZOOM = ['s','<Up>']
    TOUCHE_DEZOOM = ['w','<Down>']
    TOUCHE_ROTA_DROITE = ['<Right>']
    TOUCHE_ROTA_GAUCHE = ['<Left>']
    TOUCHE_DECAL_X = ['2']
    TOUCHE_DECAL_Y = ['5']
    TOUCHE_DECAL_Xneg = ['1']
    TOUCHE_DECAL_Yneg = ['4']
    TOUCHE_DECAL_REINIT = ['6']
    FONT = "Arial"
    TAILLE_FONT = 10
    font_label = "Arial"
    taille_font = 8
    def __init__(self,N=40,M=50,t=10,ouvrir_fichier = 'RessourceLogiciel/defaut.txt', temps_actualisation=50,to_destroy=None, BD = None, BDV = None):
        reinit_fenetre()
        global INTERFACE, RESULTATS_SIMULATION,IRR_SOL,BASE_DE_DONNEES_VEGE, NOM_PARAM,NOM_PARAM_VEGE, TEMP_VALEUR, HR_VALEUR, BASE_DE_DONNEES, BASE_DE_DONNEES_VEGE
        IRR_SOL = 200
        INTERFACE = self
        TEMP_VALEUR = {}
        HR_VALEUR = {}
        RESULTATS_SIMULATION = {}
        
        if to_destroy != None:
            to_destroy.destroy()
        
        Tk.__init__(self)
    
        self.title('Logiciel UrbanWater')
        self.N, self.M = N,M
        self.block_interface = False
        self.timing_note = [0,0,0]
        self.timing_prenote = [0,0,0]
        self.mainPaned = PanedWindow(self, orient=HORIZONTAL, height = 700)
        # Lancement Simulation
        self.listes_Simu = []
        self.liste_arbres = []
        self.liste_batiments = []
        self.taille_maillage_reel = t #1 m/pixels
        self.simu_run = False
        self.tare = {}
        self.fonctionTare = None
        self.save_time_scale = 0
        self.launch_interface_irr = False
        self.temps_actualisation = temps_actualisation
        self.stop_simulation = False
        self.valeur_simu_temporelle_save_temperature = {}
        violet = '#e4b0fb'
        #Paramètres iniitiaux
        if BD == None:
            BASE_DE_DONNEES = []
        else:
            BASE_DE_DONNEES = BD
        NOM_PARAM = ['NOM','ALBEDO','DIFFUSIVITE_THERMIQUE','COULEUR','FONCTION_SELECTION','CONDUCTIVITE_THERMIQUE','MASSE_VOLUMIQUE',"POROSITE","PERMEABILITE","EVAPOTRANSPIRATION","EMISSIVITE_THERMIQUE", "FACTEUR_RUGOSITE_SURFACE",'CP']
        if BDV == None:
            BASE_DE_DONNEES_VEGE = [['Sapin', 3, 20, 5, self.select_vegetation_sapin, 'TEMPERATURE(x,y,z)','HUMIDITE(x,y,z)','#228B22']]
        else:
            BASE_DE_DONNEES_VEGE = BDV
        NOM_PARAM_VEGE = ['NOM','KET','HAUTEUR','RAYON', "FONCTION_SELECTION",'TEMPERATURE','HUMIDITE','COULEUR','PSYCHROMETRIQUE']
        self.select_case = (None,None)
        self.coord = (0,0)
        self.VIEW_ARBRE = True
        self.select_materiau = None
        self.select_vege = None
        self.VIEW_BATIMENT = True
        
        #Paned Paramètres
        self.buttonPaned = PanedWindow(self.mainPaned,orient = VERTICAL)
        self.element = {}
        self.buttonPaned.add(Label(self,text="1. Définir les données :", fg='blue',anchor="w"))
        self.buttonPaned.add(Label(self,text="1.1 Définir la carte :", fg='blue',anchor="w"))

        b = Button(self,text="Maillage", command = self.souspar_affiche_Maillage, fg='white', bg='grey')
        self.buttonPaned.add(b)
        
        b = Button(self,text = "Bâtiment", command = self.souspar_affiche_Batiment, fg='brown', bg='#e8e6a6')
        self.buttonPaned.add(b)
        
        b = Button(self,text = "Définir:Revêtement", command = self.souspar_affiche_Terrain, fg='brown', bg='#D6B699')
        self.buttonPaned.add(b)
        
        b = Button(self,text = "Base de données:Revêtement", command = self.souspar_affiche_TerrainApplique, fg='brown', bg='#D6B699')
        self.buttonPaned.add(b)
        
        b = Button(self,text="Définir:Végétation ", command = self.souspar_affiche_Vegetalisation, fg='brown', bg='#9de6ab')
        self.buttonPaned.add(b)
        
        b = Button(self,text="Base de données:Végétation ", command = self.souspar_affiche_BDVegetation, fg='brown', bg='#9de6ab')
        self.buttonPaned.add(b)
        
        b = Button(self,text="Eau", command = self.souspar_affiche_Eau, fg='#0000FF', bg='cyan')
        self.buttonPaned.add(b)
        
        self.buttonPaned.add(Label(self,text="1.2 Définir le cadre :", fg='blue',anchor="w"))
        
        b = Button(self,text="Irradiance", command = self.souspar_affiche_Irradiance, bg='yellow', fg='orange')
        self.buttonPaned.add(b)
        
        #b = Button(self,text="Albédo", command = self.souspar_affiche_Albedo, fg = 'white',bg='black')
        #self.buttonPaned.add(b)
        
        self.buttonPaned.add(Button(self,text="Ventilation", bg="#d1e7e9", fg="#18a5b2",command = self.souspar_affiche_Ventilation))
        
        self.buttonPaned.add(Button(self,text="Variables thermodynamiques", bg="#f9e0b0", fg="#ecaa2e",command = self.souspar_affiche_VarThermo))
        
        
        self.buttonPaned.add(Label(self,text="2. Modélisation :", fg='blue',anchor="w"))
        
        b = Button(self,text="Évapotranspiration", command = self.souspar_affiche_Evapotranspiration, fg='#1623bd', bg='#a3f0db')
        self.buttonPaned.add(b)
        self.buttonPaned.add(Button(self,text="[Statique]\nSource d'ilôt de chaleur", bg='#f07a75',fg='#b6281a', command = self.souspar_affiche_Temperature))
        self.buttonPaned.add(Button(self,text="[Statique]\nCritère de rafraichissement", command = self.souspar_affiche_Rafraichissement, bg='#d4cdf8', fg="#29197a"))
        self.buttonPaned.add(Button(self,text="Puissance",command = self.souspar_affiche_Puissance, bg="#e3caff", fg="#be84ff"))

        self.buttonPaned.add(Label(self,text="3. Simulation :", fg='blue',anchor="w"))
        #self.buttonPaned.add(Label(self,text="Simulation instantannée: ", fg='black', anchor='w'))
        self.buttonPaned.add(Button(self, text="Visualiser les données statiques",bg='#f7dffc',fg="#e47bfa",command = self.commande_simulation))
        self.buttonPaned.add(Button(self,text="Simulation des puissances",bg="#e3caff", fg="#be84ff", command = self.souspar_affiche_SimuTemp))
        #self.buttonPaned.add(Button(self,text="Visualiser les données", bg="#e3caff", fg="#be84ff", command = self.souspar_affiche_SimuVisu))
        self.buttonPaned.add(Label(self,text="Traitement du fichier", fg='blue', anchor='w'))
        self.entree_save = Entry(self)
        self.entree_save.insert(0,'save.txt')
        self.buttonPaned.add(self.entree_save)
        self.buttonPaned.add(Button(self,text="Sauvegarder",command=self.save_to_file))
        self.buttonPaned.add(Button(self,text="Ouvir une sauvegarde", command = self.save_open))
        self.buttonPaned.add(Button(self,text="Rafraichir", command = self.rafraichir))
        #Paned Sous-paramètres
        self.sousparPaned = PanedWindow(self.mainPaned, orient = HORIZONTAL, width=400)
        self.liste_souspar = []
       
        #Maillage
        self.souspar_Maillage = PanedWindow(self.sousparPaned,orient = VERTICAL)
        self.souspar_Maillage.add(Label(self, text = "Paramètres du Maillage : ",anchor="w",fg='red'))
        self.souspar_Maillage.add(Label(self,text="Taille du maillage (en m/pixel)", anchor="w",fg='blue'))
        self.entree_Maillage = Entry(self)
        self.entree_Maillage.insert(0,str(t))
        self.souspar_Maillage.add(self.entree_Maillage)
        self.souspar_Maillage.add(Label(self,text="Dimensions actuelles du maillage : \n{0}m*{1}m \n {2}unités*{3}unités".format(self.N*self.taille_maillage_reel ,self.M*self.taille_maillage_reel, self.N,self.M), anchor="w"))
        self.souspar_Maillage.add(Label(self,text="Nombre de maillage selon x", anchor="w",fg='blue'))
        self.entree_Maillage_x = Entry(self)
        self.entree_Maillage_x.insert(0,str(self.N))
        self.souspar_Maillage.add(self.entree_Maillage_x)
        self.souspar_Maillage.add(Label(self,text="Nombre de maillage selon y", anchor="w",fg='blue'))
        self.entree_Maillage_y = Entry(self)
        self.entree_Maillage_y.insert(0,str(self.M))
        self.souspar_Maillage.add(self.entree_Maillage_y)
        self.souspar_Maillage.add(Label(self,text="Temps d'actualisation (en ms) :", anchor="w",fg='blue'))
        self.entree_temps_actu = Entry(self)
        self.entree_temps_actu.insert(0,str(self.temps_actualisation))
        self.souspar_Maillage.add(self.entree_temps_actu)
        self.souspar_Maillage.add(Button(self,text="Réinitialiser le maillage \n Attention \nVeuillez sauvegarder votre fichier au préalable.", command = self.reinit_maillage))
        
        self.liste_souspar.append(self.souspar_Maillage)
        
        #Batiment
        self.souspar_Batiment = PanedWindow(self.sousparPaned,orient = VERTICAL)
        self.souspar_Batiment.add(Label(self,text="Paramètres du terrain :", fg = 'red', anchor = "w"))
        self.souspar_Batiment.add(Label(self,text="Paramètres des bâtiments : ", fg='blue',anchor="w"))
        self.souspar_Batiment.add(Label(self,text="Hauteur du bâtiment : ",anchor="w"))

        self.entree_hauteur_bat = Entry(self)
        self.entree_hauteur_bat.insert(0,"2")
        self.souspar_Batiment.add(self.entree_hauteur_bat)
        self.souspar_Batiment.add(Label(self,text="Couleur du bâtiment : ",anchor="w"))
        self.entree_couleur_bat = Entry(self)
        self.entree_couleur_bat.insert(0,"#e8e6a6")
        self.souspar_Batiment.add(self.entree_couleur_bat)
        self.souspar_Batiment.add(Button(self,text="Ajouter le bâtiment", command = self.ajout_batiment))
        self.liste_souspar.append(self.souspar_Batiment)
        #Terrain       
        self.paned_terrain = PanedWindow(self.sousparPaned, orient = VERTICAL)
        self.souspar_Terrain = PanedWindowDefilant(self.sousparPaned,paned_gen=self.paned_terrain,orient = VERTICAL)
        self.paned_terrain.add(self.souspar_Terrain)
        self.liste_souspar.append(self.paned_terrain)
       
        self.souspar_Terrain.add(Label(self,text = "Ajout d'un matériau dans la base de données", fg='red',anchor="w"))
        self.ENT_MAT = {}
        self.souspar_Terrain.add(Label(self,text = "Nom du matériau :",anchor="w"))
        self.entree_nom_mat = Entry(self)
        self.ENT_MAT['NOM'] = self.entree_nom_mat
        self.souspar_Terrain.add(self.entree_nom_mat)
        self.souspar_Terrain.add(Label(self,text = "Propriétés optiques", fg='blue',anchor="w"))
        self.souspar_Terrain.add(Label(self,text="Albédo (de 0 à 1)",anchor="w"))
        self.entree_albedo_terrain = Entry(self)
        self.entree_albedo_terrain.insert(0,"0")
        self.ENT_MAT['ALBEDO'] = self.entree_albedo_terrain
        self.souspar_Terrain.add(self.entree_albedo_terrain)
        self.souspar_Terrain.add(Label(self,text="Couleur du matériau :"))
        self.entree_couleur_mat = Entry(self)
        self.entree_couleur_mat.insert(0,"#303030")
        self.ENT_MAT['COULEUR'] = self.entree_couleur_mat
        self.souspar_Terrain.add(self.entree_couleur_mat)
        self.souspar_Terrain.add(Label(self,text = "Propriétés thermiques", fg='blue',anchor="w"))
        self.souspar_Terrain.add(Label(self,text="Diffusivité thermique (en m²/s) :", anchor="w"))
        self.entree_diffusivite = Entry(self)
        self.entree_diffusivite.insert(0,"0")
        self.ENT_MAT['DIFFUSIVITE_THERMIQUE'] = self.entree_diffusivite
        self.souspar_Terrain.add(self.entree_diffusivite)
        self.souspar_Terrain.add(Label(self,text="Émissivité thermique :", anchor="w"))
        self.entree_emissivite = Entry(self)
        self.entree_emissivite.insert(0,"0")
        self.ENT_MAT['EMISSIVITE_THERMIQUE'] = self.entree_emissivite
        self.souspar_Terrain.add(self.entree_emissivite)
        self.souspar_Terrain.add(Label(self,text="Conductivité thermique (en W/m.K) :", anchor="w"))
        self.entree_conductivite = Entry(self)
        self.entree_conductivite.insert(0,"0")
        self.souspar_Terrain.add(self.entree_conductivite)
        self.ENT_MAT['CONDUCTIVITE_THERMIQUE'] = self.entree_conductivite
        self.souspar_Terrain.add(Label(self,text="cp, capacité thermique (en J/(kg.K)):", anchor="w"))
        self.entree_cp = Entry(self)
        self.entree_cp.insert(0,"0")
        self.ENT_MAT['CP'] = self.entree_cp
        self.souspar_Terrain.add(self.entree_cp)
        self.souspar_Terrain.add(Label(self,text = "Propriétés hydriques :", fg='blue',anchor="w"))
        self.souspar_Terrain.add(Label(self,text="Porosité (en %) :", anchor="w"))
        self.entree_porosite = Entry(self)
        self.entree_porosite.insert(0,"0")
        self.ENT_MAT['POROSITE'] = self.entree_porosite
        self.souspar_Terrain.add(self.entree_porosite)
        self.souspar_Terrain.add(Label(self,text="Perméabilité à l'eau (en m/s) :", anchor="w"))
        self.entree_permeabiliteEau = Entry(self)
        self.entree_permeabiliteEau.insert(0,"0")
        self.ENT_MAT['PERMEABILITE'] = self.entree_permeabiliteEau
        self.souspar_Terrain.add(self.entree_permeabiliteEau)
        self.souspar_Terrain.add(Label(self,text="Évapotranspiration due au matériau (en mm/jour/m²) :", anchor="w"))
        self.entree_evapMat = Entry(self)
        self.entree_evapMat.insert(0,"0")
        self.souspar_Terrain.add(self.entree_evapMat)
        self.ENT_MAT['EVAPOTRANSPIRATION'] = self.entree_evapMat
        self.souspar_Terrain.add(Label(self,text = "Propriétés due à la forme du matériau :", fg='blue',anchor="w"))
        self.souspar_Terrain.add(Label(self,text="Facteur de rugosité surfacique :", anchor="w"))
        self.entree_factRug = Entry(self)
        self.entree_factRug.insert(0,"0")
        self.souspar_Terrain.add(self.entree_factRug)
        self.ENT_MAT['FACTEUR_RUGOSITE_SURFACE'] = self.entree_factRug
        self.souspar_Terrain.add(Label(self,text="Densité (en kg/m^3) :", anchor="w"))
        self.entree_densite = Entry(self)
        self.entree_densite.insert(0,"0")
        self.ENT_MAT['MASSE_VOLUMIQUE'] = self.entree_densite
        self.souspar_Terrain.add(self.entree_densite)
        self.souspar_Terrain.add(Label(self,text = "Propriétés environnementales :", fg='blue',anchor="w"))
        self.souspar_Terrain.add(Button(self,text="Ajouter le matériau dans la base",command=self.ajout_materiau_Base))
        
        #TerrainApplique
        self.souspar_TerrainApplique = PanedWindow(self.sousparPaned,orient = VERTICAL)
        self.souspar_TerrainApplique.add(Label(self,text="Choix du matériau :", fg='blue',anchor ="w"))
        self.paned_paned_mat = PanedWindow(self.souspar_TerrainApplique, orient=VERTICAL)
        self.paned_mat = PanedWindowDefilant(self.sousparPaned, orient=VERTICAL, paned_gen = self.paned_paned_mat)
        #for i in BASE_DE_DONNEES:
        #    self.paned_mat.add(Button(self,command = i[4],fg=i[3],text="{0} \n Alb={1} \n Diffu={2}m²/s, Cond={3}W/m.K, Dens={4}kg/m^3 \n Por={5}%, Perm={6} Evap={7}mm/jour".format(i[0],i[1],i[2],i[5],i[6],i[7],i[8],i[9])))
        self.paned_paned_mat.add(self.paned_mat)
        self.souspar_TerrainApplique.add(self.paned_paned_mat)
        self.souspar_TerrainApplique.add(Button(self,text = "Appliquer au maillage sélectionné", command = self.appliquer_materiau))
        self.liste_souspar.append(self.souspar_TerrainApplique)
        #Albédo
        self.souspar_Albedo = PanedWindow(self.sousparPaned,orient = VERTICAL)
        
        self.souspar_Albedo.add(Label(self.sousparPaned, text = "Paramètres de l'albédo :",anchor="w"))
        self.entree_albedo = Entry(self.sousparPaned)
        self.entree_albedo.insert(0,"0")
        self.souspar_Albedo.add(self.entree_albedo)
        self.souspar_Albedo.add(Button(self.sousparPaned,command=self.appliquer_albedo,text="Appliquer aux cases sélectionnées"))
        self.entree_albedo_bis = Entry(self.sousparPaned)
        self.entree_albedo_bis.insert(0,"math.exp(-(x**2+y**2)**0.5/400)")
        self.souspar_Albedo.add(self.entree_albedo_bis)
        self.souspar_Albedo.add(Button(self.sousparPaned,command=self.appliquer_albedo_bis, text="Appliquer la fonction aux cases sélectionnées"))
        self.liste_souspar.append(self.souspar_Albedo)
        #Végétalisation
        self.souspar_VG = PanedWindow(self.sousparPaned, orient = VERTICAL)
        self.souspar_Vegetalisation = PanedWindowDefilant(self.sousparPaned,paned_gen=self.souspar_VG,bg='#9de6ab',orient=VERTICAL)
        self.souspar_Vegetalisation.add(Label(self,bg='#9de6ab', text = "Paramètres de végétation : ",fg ='red',anchor="w"))
        
        self.souspar_Vegetalisation.add(Label(self,bg='#9de6ab',text="Paramètres d'ajout d'un arbre : ", fg = 'blue',anchor="w"))
        l = Label(self,text="Kcbmid : ",anchor="w",bg='#9de6ab')
        self.souspar_Vegetalisation.add(l)        
        self.ajouter_texte_passant(l, "Coefficient d'évapotranspiration (Kcbmid)")
        self.entree_KET = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_KET.insert("1.0","0.2+(Kcbfull-0.2)*min([1.2*fc, fceff**(1/1+h)])")
        
        self.souspar_Vegetalisation.add(self.entree_KET)
        self.souspar_Vegetalisation.add(Label(self, text="Kcbfull", anchor="w"))
        self.entree_Kcbfull =Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Kcbfull.insert("1.0","1+0.1*h+(0.04*(VENT(x,y,z)-2)-0.004*(HUMIDITE_RELATIVE_MIN(x,y,z) - 45))*(h/3)**0.3")
        
        self.souspar_Vegetalisation.add(self.entree_Kcbfull)
        
        #self.souspar_Vegetalisation.add(Label(self, text="gamma(x,y,z) = coefficients psychrométriques (en Pa/°C)", anchor="w"))
        #self.entree_gamma = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        #self.entree_gamma.insert('1.0','1')
        #self.souspar_Vegetalisation.add(self.entree_gamma)
        
        self.souspar_Vegetalisation.add(Label(self,bg='#9de6ab',text="Hauteur de l'arbre (en m) : " ,anchor="w"))        
        self.entree_hauteur = Entry(self)
        self.entree_hauteur.insert(0,'2')
        self.souspar_Vegetalisation.add(self.entree_hauteur)
        
        self.souspar_Vegetalisation.add(Label(self,bg='#9de6ab',text="Rayon du houpier (en m) : " ,anchor="w"))        
        self.entree_rayon = Entry(self)
        self.entree_rayon.insert(0,'1')
        self.souspar_Vegetalisation.add(self.entree_rayon)
    
        self.souspar_Vegetalisation.add(Label(self,bg='#9de6ab',text="Température de l'air autour de l'arbre (en K) : " ,anchor="w"))        
        self.entree_Temp = Entry(self)
        self.entree_Temp.insert(0,'TEMPERATURE(x,y,z)')
        self.souspar_Vegetalisation.add(self.entree_Temp)
        
        self.souspar_Vegetalisation.add(Label(self,bg='#9de6ab',text="Humidité relative de l'air autour de l'arbre (en %) : " ,anchor="w"))        
        self.entree_HR = Entry(self)
        self.entree_HR.insert(0,'HUMIDITE(x,y,z)')
        self.souspar_Vegetalisation.add(self.entree_HR)
    
        self.label_position_vegetalisation = Label(self,bg='#9de6ab',text="Position de l'arbre : ")
        self.label_position_vegeta = Label(self,bg='#9de6ab',text="Position de l'arbre : ")
        self.souspar_Vegetalisation.add(Button(self,text = "Ajouter un arbre", command = self.ajout_arbre))
        self.souspar_Vegetalisation.add(Label(self,bg='#9de6ab',text="Paramètres de suppression d'un arbre : ", fg = 'blue',anchor="w"))
        self.souspar_Vegetalisation.add(self.label_position_vegetalisation)
        self.souspar_Vegetalisation.add(self.label_position_vegeta)
        self.souspar_Vegetalisation.add(Button(self,text = "Supprimer un arbre",command = self.suppr_arbre))
        self.liste_souspar.append(self.souspar_VG)
        self.souspar_VG.add(self.souspar_Vegetalisation)

        # Base de données : Végétation
        self.souspar_BDVegetation= PanedWindow(self.sousparPaned,orient=VERTICAL)
        self.paned_Veg_Veg = PanedWindow(self.sousparPaned)
        self.paned_VEGEbd = PanedWindowDefilant(self.sousparPaned, orient=VERTICAL, paned_gen = self.paned_Veg_Veg)
        #for i in BASE_DE_DONNEES_VEGE:
        #    self.paned_VEGEbd.add(Button(self,command=i[4],text="{0} \n KET={1}mm/jour \n h={2}m, R={3}m \n Tair={4}K \nHR={5}".format(i[0],i[1],i[2],i[3],i[5],i[6])))
        self.souspar_BDVegetation.add(self.paned_Veg_Veg)
        self.paned_Veg_Veg.add(self.paned_VEGEbd)
        self.souspar_BDVegetation.add(Button(self,command =self.ajout_arbre_select,text="Ajouter l'arbre"))
        self.liste_souspar.append(self.souspar_BDVegetation)
        
        # Evapotranspiration
        self.souspar_Evapo = PanedWindow(self.sousparPaned,orient=VERTICAL)
        self.souspar_Evapo.add(Label(self,text="Définition de l'évapotranspiration : ", fg = 'red',anchor="w"))
        self.souspar_Evapo.add(Label(self, anchor = 'w', fg = 'blue',text="Δ = PENTE_TVS = pente de vapeur saturante (en Pa/°C) :"))
        self.entree_Formule_DELTA=Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Formule_DELTA.insert("1.0", "4098*0.6108*exp(17.27*TEMPERATURE_CELSIUS(x,y,z)/TEMPERATURE(x,y,z))/(TEMPERATURE(x,y,z))**2")
        self.souspar_Evapo.add(self.entree_Formule_DELTA)
        self.souspar_Evapo.add(Label(self,text="Évapotranspiration liée aux végétaux : ", fg = 'red',anchor="w"))
        self.souspar_Evapo.add(Label(self,text="Formule de l'évapotranspiration pour un arbre : ",fg='blue',anchor="w"))        
        self.entree_Formule_eva=Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=6)
        self.entree_Formule_eva.insert("1.0",'(pi*R**2/SURFACE_MAILLE(x,y,z))*Kcbmid*(0.408*PENTE_TVS(x,y,z)*IRRADIANCE(x,y,z)*0.0864+gamma(x,y,z)*900*VENT(x,y,z)*(tvps_ew(x,y,z)-tvps_e(x,y,z))/TEMPERATURE(x,y,z))/(PENTE_TVS(x,y,z)+gamma(x,y,z)*(1+0.34*VENT(x,y,z)))')
        self.souspar_Evapo.add(self.entree_Formule_eva)
        
        self.souspar_Evapo.add(Label(self,fg = 'blue',text="Portée de l'évapotranspiration (fonction de r la distance à l'arbre) : ",anchor="w"))        
        self.souspar_Evapo.add(Label(self,text="Est ce que l'évapotranspiration d'un arbre a lieu sur les mailles voisines ?",anchor="w"))        
        self.entree_Formule_portee = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Formule_portee.insert("1.0",'exp(-r/R)/(2*R**3)')
        self.souspar_Evapo.add(self.entree_Formule_portee)
        
        self.souspar_Evapo.add(Label(self,text="Évaporation liée à l'eau' : ", fg = 'blue',anchor="w"))
        self.entree_Formule_eva_eau = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Formule_eva_eau.insert("1.0","0")
        self.souspar_Evapo.add(self.entree_Formule_eva_eau)
        
        self.souspar_Evapo.add(Label(self,text="Évapotranspiration liée au materiau : ", fg = 'blue',anchor="w"))
        self.souspar_Evapo.add(Label(self,text="Formule de l'évapotranspiration pour le revêtement : ",anchor="w"))        
        self.entree_Formule_eva_mat = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Formule_eva_mat.insert("1.0","EVAPOTRANSPIRATION_MATERIAU(x,y,z)")
        self.souspar_Evapo.add(self.entree_Formule_eva_mat)
        self.souspar_Evapo.add(Label(self,text=""))
        self.liste_souspar.append(self.souspar_Evapo)
        #Irradiance
        self.souspar_Irradiance = PanedWindow(self.sousparPaned,orient = VERTICAL)
        self.souspar_Irradiance.add(Label(self, text = "Paramètres d'irradiance : ",anchor="w", fg='red'))
        self.souspar_Irradiance.add(Label(self, text = "Paramètres d'orientation des rayons : ",anchor="w", fg='blue'))
        self.souspar_Irradiance.add(Label(self, text = "Vecteur de direction des rayons : ",anchor="w"))
        self.entree_Irradiance = Entry(self)
        self.entree_Irradiance.insert(0,"(10*(cos(pi*t/86400)),7*(sin(pi*t/86400)) ,1+(sin(pi*t/86400)))")
        self.souspar_Irradiance.add(self.entree_Irradiance)   
        self.souspar_Irradiance.add(Button(self, text="Caculer l'ombrage", command = self.calculer_ombrage))
        self.souspar_Irradiance.add(Label(self, text = "Rayonnement solaire : ",fg='blue',anchor="w"))
        self.souspar_Irradiance.add(Label(self, text = "Irradiance solaire (en W/m²) : ",fg='black',anchor="w"))
        self.entree_IrradianceSol = Entry(self)
        self.entree_IrradianceSol.insert(0,"200*INDICATRICE(7*3600,t,20*3600)*sin(pi*t/86400)")

        self.souspar_Irradiance.add(self.entree_IrradianceSol) 
        
        frame_graph = Frame(self.souspar_Irradiance)
        self.souspar_Irradiance.add(frame_graph)
        t_values = [86400*t for t in range(100)]
        y_values = [sin(t) for t in t_values]
        
        fig, ax = plt.subplots()
        ax.plot(t_values, y_values, label='f(t) = sin(t)')
        ax.set_xlabel('t')
        ax.set_ylabel('f(t)')
        ax.legend()
        
        canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
        self.fig_save_irradiance = fig, ax, canvas

        self.souspar_Irradiance.add(Label(self, text = "Ombrage d'un bâtiment (0: complétement ombré, \n1:batiment transparent) : ",fg='black',anchor="w"))
        self.entree_IrradianceOmbreBatiment = Entry(self)
        self.entree_IrradianceOmbreBatiment.insert(0,"0.1")
        self.souspar_Irradiance.add(self.entree_IrradianceOmbreBatiment)
        
        #self.souspar_Irradiance.add(Label(self, text = "Rayonnement terrestre : ",fg='blue',anchor="w"))
        self.souspar_Irradiance.add(Button(self,text="Appliquer les paramètres",command=self.appliquer_irradiance))
        
        self.liste_souspar.append(self.souspar_Irradiance)
        #Eau
        self.souspar_Eau = PanedWindow(self.sousparPaned,orient = VERTICAL)
        self.souspar_Eau.add(Label(self, text = "Surface eau : ",fg='red',anchor="w"))
        self.souspar_Eau.add(Label(self, text = "Paramètres sur l'eau : ",fg='blue',anchor="w"))
        l = Label(self, text = "Surface d'eau (en m²) : ",anchor="w")
        self.ajouter_texte_passant(l,"Dans chaque maille sélectionnée, il y a une surface d'eau de ... m²")
        self.souspar_Eau.add(l)
        self.entree_Eau = Entry(self)
        self.entree_Eau.insert(0,'0')
        self.souspar_Eau.add(self.entree_Eau)
        self.souspar_Eau.add(Label(self,text="Température de l'eau (en K) :", anchor="w"))
        self.entree_T_eau = Entry(self)
        self.entree_T_eau.insert(0,'TEMPERATURE(x,y,z)')
        self.souspar_Eau.add(self.entree_T_eau)
        self.bouton_Eau = Button(self,text="Appliquer à la sélection",command = self.ajout_eau)
        self.souspar_Eau.add(self.bouton_Eau)
        self.souspar_Eau.add(Label(self,text="Propriétés de l'eau (choix de modèle) :", anchor="w", fg='blue'))
        self.souspar_Eau.add(Label(self,text="h_e (en kg/m².s.Pa) : coeff transf mass vap :", anchor="w"))
        self.entree_he_eau = Entry(self)
        self.entree_he_eau.insert(0,'0.0025*(1+0.004*VENT(x,y,z))')
        self.souspar_Eau.add(self.entree_he_eau)
        self.souspar_Eau.add(Label(self,text="h_c (en W/m².K) : coeff transf therm par convection :", anchor="w"))
        self.entree_hc_eau = Entry(self)
        self.entree_hc_eau.insert(0,'10+10*VENT(x,y,z)')
        self.souspar_Eau.add(self.entree_hc_eau)
        self.souspar_Eau.add(Label(self,text="PRESSION_SATURATION_EAU (en Pa) :", anchor="w"))
        self.entree_P_sat_eau = Entry(self)
        self.entree_P_sat_eau.insert(0,"610.78*exp(17.27*TEMPERATURE(x,y,z)/(TEMPERATURE(x,y,z)+273.15)) # équation d'Antoine")
        self.souspar_Eau.add(self.entree_P_sat_eau)
        self.souspar_Hydrique = PanedWindowDefilant(self.souspar_Eau, paned_gen=self.souspar_Eau, orient = VERTICAL, taille_paned = 300)
        self.souspar_Eau.add(Label(self, text = "Bilan hydrique des revêtements : ",fg='red',anchor="w"))
        self.souspar_Hydrique.add(Label(self, text = "Entrée d'eau :",fg='blue',anchor="w"))
        self.souspar_Hydrique.add(Label(self, text="Précipitations (en mm/jour)", anchor="w"))
        self.entree_precipitations = Entry(self)
        self.entree_precipitations.insert(0,'5')
        self.souspar_Hydrique.add(self.entree_precipitations)
        self.souspar_Hydrique.add(Label(self, text="Autres entrées d'eau (en mm/jour)", anchor="w"))
        self.entree_entreeEau = Entry(self)
        self.entree_entreeEau.insert(0,'0')
        self.souspar_Hydrique.add(self.entree_entreeEau)
        self.souspar_Hydrique.add(Label(self, text = "Sortie d'eau :",fg='blue',anchor="w"))
        self.entree_SortieEau = Entry(self)
        self.entree_SortieEau.insert(0,'EVAPOTRANSPIRATION(x,y,z) + EVAPORATION(x,y,z)')
        self.souspar_Hydrique.add(self.entree_SortieEau)
        self.souspar_Hydrique.add(Label(self,text="Évaporation (en mm/jour) :", anchor = 'w'))
        self.entree_Evaporation = Entry(self)
        self.entree_Evaporation.insert(0,'0')
        self.souspar_Hydrique.add(self.entree_Evaporation)
        self.souspar_Hydrique.add(Label(self,text="Teneur en eau (en %)", anchor="w"))
        self.entree_Teneur = Text(self,font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Teneur.insert("1.0",'min(POROSITE(x,y,z), (PRECIPITATION(x,y,z)+ENTREE_EAU(x,y,z)-SORTIE_EAU(x,y,z)))')
        self.souspar_Hydrique.add(self.entree_Teneur)
        self.souspar_Hydrique.add(Label(self, text = "Ruissellement (en mm/jour) :",anchor="w"))
        self.entree_Ruissellement = Text(self,font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Ruissellement.insert("1.0",'max(0,(PRECIPITATION(x,y,z)+ENTREE_EAU(x,y,z)-SORTIE_EAU(x,y,z))-TENEUR_EAU(x,y,z))')
        self.souspar_Hydrique.add(self.entree_Ruissellement)
        self.souspar_Hydrique.add(Label(self,text=""))
        self.souspar_Hydrique.add(Button(self,text="Appliquer les règles de bilan à la sélection", command = self.appliquer_hydrique))
        self.souspar_Eau.add(self.souspar_Hydrique)
        self.liste_souspar.append(self.souspar_Eau)
        #Ventilation
        self.souspar_Ventilation = PanedWindow(self.sousparPaned, orient=VERTICAL)
        
        self.souspar_Ventilation.add(Label(self,anchor="w",fg='green',text="VECTEUR_VENT(x,y,z) : valeur du vent à 2m au dessus du sol en m/s"))
        self.entree_Valeur_Vent = Entry(self)
        self.entree_Valeur_Vent.insert(0,'(0,0,0)')
        self.souspar_Ventilation.add(self.entree_Valeur_Vent)
        
        self.souspar_Ventilation.add(Label(self,anchor="w",fg='green',text="h : Coefficient de convection"))
        self.entree_h_coeff = Entry(self)
        self.entree_h_coeff.insert(0,'10')
        self.souspar_Ventilation.add(self.entree_h_coeff)
        
        
        
        self.souspar_Ventilation.add(Button(self,text="Appliquer la formule", command = self.appliquer_formule_h))
        self.liste_souspar.append(self.souspar_Ventilation)
        #Variables thermodynamiques
        self.souspar_VarThermo = PanedWindow(self.sousparPaned,bg="#f9e0b0",orient = VERTICAL)
        #self.souspar_VarThermo.add(Label(self,text="Attention, ces réglages ne s'appliquent \nqu'à une simulation instantannée : ",bg="#f9e0b0",anchor="w"))
        self.souspar_VarThermo.add(Label(self,text="Température (en K, fonction de x et y) : ",bg="#f9e0b0",anchor="w", fg='red'))
        self.entree_temperature = Entry(self)
        self.entree_temperature.insert(0,"280 +30*sin(pi*t/86400)")
        self.souspar_VarThermo.add(self.entree_temperature)
        self.souspar_VarThermo.add(Button(self, text="Appliquer à la sélection", command = self.appliquer_temperature))
        self.souspar_VarThermo.add(Label(self,text="Pression : ",bg="#f9e0b0",anchor="w", fg='red'))
        
        self.liste_souspar.append(self.souspar_VarThermo)
        #Réchauffement
        self.souspar_Rechauffement = PanedWindow(self.sousparPaned, orient=VERTICAL)
        self.souspar_Rechauffement.add(Label(self, text = "Une élévation de la température peut être due à : ",fg='red',anchor="w"))
        self.souspar_Rechauffement.add(Label(self, text = "- Rayonnement absorbée par le matériau : ",fg='black',anchor="w"))
        self.entree_Rechauffement_Rayo = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rechauffement_Rayo.insert("1.0",'0')
        self.souspar_Rechauffement.add(self.entree_Rechauffement_Rayo)
        
        self.souspar_Rechauffement.add(Label(self, text = "- Pollution urbaine : ",anchor="w"))
        self.entree_Rechauffement_urbain = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rechauffement_urbain.insert("1.0",'0')
        self.souspar_Rechauffement.add(self.entree_Rechauffement_urbain)
        self.souspar_Rechauffement.add(Label(self, text = "- Consommation énergétique : ",anchor="w"))
        self.entree_Rechauffement_conso = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rechauffement_conso.insert("1.0",'0')
        self.souspar_Rechauffement.add(self.entree_Rechauffement_conso)
        self.souspar_Rechauffement.add(Label(self, text = "- Agencement des bâtiments : ",anchor="w"))
        self.entree_Rechauffement_agen = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rechauffement_agen.insert("1.0",'0')
        self.souspar_Rechauffement.add(self.entree_Rechauffement_agen)
        self.liste_entree_rechauffement = [self.entree_Rechauffement_Rayo, self.entree_Rechauffement_agen, self.entree_Rechauffement_urbain, self.entree_Rechauffement_conso]

        self.liste_souspar.append(self.souspar_Rechauffement)
        #Rafraichissement
        self.paned_rafrai = PanedWindow(self.sousparPaned)
        self.souspar_Rafraichissement = PanedWindowDefilant(self.sousparPaned,paned_gen=self.paned_rafrai, orient=VERTICAL)
    
        self.souspar_Rafraichissement.add(Label(self, text = "Une diminution de température peut être due à : ",fg='red',anchor="w"))
        self.souspar_Rafraichissement.add(Label(self, text = "- Le choix du revêtement : ",fg='blue',anchor="w"))
        self.souspar_Rafraichissement.add(Label(self, anchor='w',text = "Inertie thermique : restitution de chaleur stockée par le matériau"))
        self.entree_Rafraichissement_Inertie = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rafraichissement_Inertie.insert("1.0","0")
        self.souspar_Rafraichissement.add(self.entree_Rafraichissement_Inertie)
        self.souspar_Rafraichissement.add(Label(self, anchor='w',text = "Diffusion thermique au sein du matériau : "))
        self.entree_Rafraichissement_Diff = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rafraichissement_Diff.insert("1.0","0")
        self.souspar_Rafraichissement.add(self.entree_Rafraichissement_Diff)
        self.souspar_Rafraichissement.add(Label(self, anchor='w',text = "Déperdition thermique vers le sous-sol : "))
        self.entree_Rafraichissement_SousSol = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rafraichissement_SousSol.insert("1.0","0")
        self.souspar_Rafraichissement.add(self.entree_Rafraichissement_SousSol)
        self.souspar_Rafraichissement.add(Label(self, text = "Le choix de la végétation : ' : ",fg='blue',anchor="w"))
        self.souspar_Rafraichissement.add(Label(self, anchor='w',text = "Evapotranspiration : "))
        self.entree_Rafraichissement_evapo = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rafraichissement_evapo.insert("1.0","SURFACE_MAILLE(x,y,z)*L_Vap_air()*EVAPOTRANSPIRATION(x,y,z)*10**-3/(3600*24)/(DENSITE_AIR()*cp_AIR())")
        self.souspar_Rafraichissement.add(self.entree_Rafraichissement_evapo)
        
        self.souspar_Rafraichissement.add(Label(self, text = "L'environnement : ",fg='blue',anchor="w"))
        
        
        self.souspar_Rafraichissement.add(Label(self, text = "Ventilation naturelle : ",anchor="w"))
        self.entree_Rafraichissement_Ventilation = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rafraichissement_Ventilation.insert("1.0","0")
        self.souspar_Rafraichissement.add(self.entree_Rafraichissement_Ventilation)
        
        self.souspar_Rafraichissement.add(Label(self, text = "La présence d'eau : ",fg='blue',anchor="w"))
        self.entree_Rafraichissement_Humidite = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rafraichissement_Humidite.insert("1.0","0")
        self.souspar_Rafraichissement.add(self.entree_Rafraichissement_Humidite)
        
        self.souspar_Rafraichissement.add(Label(self, text = "Évaporation des surfaces d'eau : ",anchor="w"))
        self.entree_Rafraichissement_EAU = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rafraichissement_EAU.insert("1.0","SURFACE_EAU(x,y,z)*h_e(x,y,z)*(TEMPERATURE_EAU(x,y,z)-HUMIDITE_RELATIVE(x,y,z)/100*TEMPERATURE(x,y,z))*L_Vap_eau()/(1.2*cp_eau()*h_c(x,y,z))")
        self.souspar_Rafraichissement.add(self.entree_Rafraichissement_EAU)
        
        self.souspar_Rafraichissement.add(Label(self, text = "Brumatisation : ",anchor="w"))
        self.entree_Rafraichissement_Brumatisation = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rafraichissement_Brumatisation.insert("1.0","0")
        self.souspar_Rafraichissement.add(self.entree_Rafraichissement_Brumatisation)
        
        self.souspar_Rafraichissement.add(Label(self, text = "Échanges hygrométriques entre le matériau et l'air : ",anchor="w"))
        self.entree_Rafraichissement_Hygro = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rafraichissement_Hygro.insert("1.0","0")
        self.souspar_Rafraichissement.add(self.entree_Rafraichissement_Hygro)
        
        self.souspar_Rafraichissement.add(Label(self, text = "Condensation de l'eau sur le matériau : ",anchor="w"))
        self.entree_Rafraichissement_Condens = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Rafraichissement_Condens.insert("1.0","0")
        self.souspar_Rafraichissement.add(self.entree_Rafraichissement_Condens)
        
        self.souspar_Rafraichissement.add(Label(self,text=" ",anchor="w"))
        self.liste_entree_rafraichissement = [self.entree_Rafraichissement_Hygro,self.entree_Rafraichissement_Condens,self.entree_Rafraichissement_Diff,self.entree_Rafraichissement_SousSol,INTERFACE.entree_Rafraichissement_evapo, INTERFACE.entree_Rafraichissement_Inertie, self.entree_Rafraichissement_Ventilation, self.entree_Rafraichissement_Humidite, self.entree_Rafraichissement_Brumatisation, self.entree_Rafraichissement_EAU]
        self.paned_rafrai.add(self.souspar_Rafraichissement)
        self.liste_souspar.append(self.paned_rafrai)
        
        
        #
        #Ecran
        self.ecranPaned = PanedWindow(self.mainPaned,orient=VERTICAL)
        self.ecranCanvas = Canvas3D(self, width = 900, height = 500, bg='white')

        TAILLE_CASE = 30
        ptitPaned = PanedWindow(self.mainPaned,orient = HORIZONTAL, height = TAILLE_CASE+5)
        
        l = Label(self,text="Voir Formules")
        self.ajouter_texte_passant(l,FORMULE)
        ptitPaned.add(l)
        #Bouton Stopper_Actualisation_Interface
        def show_tooltip(event):
            # Placer le label de l'info-bulle juste en dessous du curseur
            tooltip.place(x=event.x_root - self.winfo_rootx() + 10,y=event.y_root - self.winfo_rooty() + 10)
            tooltip.config(text="Activer/Désactiver l'actualisation de l'interface")  # Texte à afficher
            tooltip.lift()
        def hide_tooltip(event):
            tooltip.place_forget()
        tooltip = Label(self, text="", bg="white", fg="black", relief="solid", borderwidth=1)
        tooltip.place_forget() 
        im = Image.open("RessourceLogiciel/LogoActualisationInterface.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logo11 = ImageTk.PhotoImage(im)
        self.btn_rafraich_interface = Button(self,width=TAILLE_CASE, height=TAILLE_CASE,image=logo11, command = self.clic_Rafraich_Interface)
        self.btn_rafraich_interface.bind("<Enter>", show_tooltip)  # Quand on survole
        self.btn_rafraich_interface.bind("<Leave>", hide_tooltip) 
        ptitPaned.add(self.btn_rafraich_interface)
        
        #Bouton Stopper_Actualisation_Canvas
        def show_tooltip_canvas(event):
            # Placer le label de l'info-bulle juste en dessous du curseur
            tooltip.place(x=event.x_root - self.winfo_rootx() + 10,y=event.y_root - self.winfo_rooty() + 10)
            tooltip.config(text="Activer/Désactiver l'actualisation du canvas")  # Texte à afficher
            tooltip.lift()
        def hide_tooltip_canvas(event):
            tooltip.place_forget()
        tooltip = Label(self, text="", bg="white", fg="black", relief="solid", borderwidth=1)
        tooltip.place_forget() 
        im = Image.open("RessourceLogiciel/LogoActualisationCanvas.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logoBI = ImageTk.PhotoImage(im)
        self.btn_rafraich_canvas = Button(self,image=logoBI, command = self.clic_Rafraich_Canvas)
        self.btn_rafraich_canvas.bind("<Enter>", show_tooltip_canvas)  # Quand on survole
        self.btn_rafraich_canvas.bind("<Leave>", hide_tooltip_canvas) 
        ptitPaned.add(self.btn_rafraich_canvas)
        
        #Bouton Stopper Actualisation Graphisme
        def show_tooltip_tri(event):
            # Placer le label de l'info-bulle juste en dessous du curseur
            tooltip.place(x=event.x_root - self.winfo_rootx() + 10,y=event.y_root - self.winfo_rooty() + 10)
            tooltip.config(text="Activer/Désactiver l'actualisation des éléments")  # Texte à afficher
            tooltip.lift()
        def hide_tooltip_tri(event):
            tooltip.place_forget()
        tooltip = Label(self, text="", bg="white", fg="black", relief="solid", borderwidth=1)
        tooltip.place_forget() 
        im = Image.open("RessourceLogiciel/LogoActualisationTri.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logo22 = ImageTk.PhotoImage(im)
        self.btn_rafraich_tri = Button(self,image=logo22, command = self.clic_Rafraich_Tri)
        self.btn_rafraich_tri.bind('<Enter>', show_tooltip_tri)
        self.btn_rafraich_tri.bind('<Leave>', hide_tooltip_tri)
        ptitPaned.add(self.btn_rafraich_tri)
        
        #Bouton déplacement
        im = Image.open("RessourceLogiciel/PivotementIndirect.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logoantipivot = ImageTk.PhotoImage(im)
        ptitPaned.add(Button(self,image=logoantipivot, command = self.ecranCanvas.pivoter_gauche))
        
        im = Image.open("RessourceLogiciel/PivotementDirect.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logopivot = ImageTk.PhotoImage(im)
        ptitPaned.add(Button(self,image=logopivot, command = self.ecranCanvas.pivoter_droite))
        
        im = Image.open("RessourceLogiciel/LogoReinitVue.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logoReinit = ImageTk.PhotoImage(im)
        ptitPaned.add(Button(self,image = logoReinit, command = self.ecranCanvas.decal0))
        im = Image.open("RessourceLogiciel/Logo3D.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logo3D = ImageTk.PhotoImage(im)
        self.btn_3D = Button(self,width=TAILLE_CASE, image=logo3D, command = self.passer_en_3D)
        im = Image.open("RessourceLogiciel/Logo2D.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logo2D = ImageTk.PhotoImage(im)
        self.btn_2D = Button(self,width=TAILLE_CASE, image = logo2D, command = self.passer_en_2D)
        ptitPaned.add(self.btn_3D)
        ptitPaned.add(self.btn_2D)
        im = Image.open("RessourceLogiciel/LogoCacherArbre.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logoARBRE = ImageTk.PhotoImage(im)
        self.btn_cacher_arbre = Button(self,width = TAILLE_CASE, command = self.voir_arbre, image = logoARBRE)
        ptitPaned.add(self.btn_cacher_arbre)
        im = Image.open("RessourceLogiciel/LogoCacherArbreBis.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logoOARBRE = ImageTk.PhotoImage(im)
        self.btn_cacher_arbre = Button(self,width = TAILLE_CASE, command = self.cacher_arbre, image = logoOARBRE)
        ptitPaned.add(self.btn_cacher_arbre)
        im = Image.open("RessourceLogiciel/LogoCacherBatiment.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logoBAT = ImageTk.PhotoImage(im)
        self.btn_cacher_batiment = Button(self,width = TAILLE_CASE, command = self.voir_batiment, image = logoBAT)
        ptitPaned.add(self.btn_cacher_batiment)
        im = Image.open("RessourceLogiciel/LogoCacherBatimentBis.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logoBAT2 = ImageTk.PhotoImage(im)
        self.btn_cacher_batiment_bis = Button(self,width = TAILLE_CASE, command = self.cacher_batiment, image = logoBAT2)
        ptitPaned.add(self.btn_cacher_batiment_bis)
        im = Image.open("RessourceLogiciel/LogoCouleur1.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logo = ImageTk.PhotoImage(im)
        ptitPaned.add(Button(self,width = TAILLE_CASE, image=logo, command = self.definir_couleur1))
        im = Image.open("RessourceLogiciel/LogoCouleur2.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logo2 = ImageTk.PhotoImage(im)
        ptitPaned.add(Button(self,width = TAILLE_CASE, image=logo2, command = self.definir_couleur2))
        im = Image.open("RessourceLogiciel/LogoCouleur3.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        log03 = ImageTk.PhotoImage(im)
        ptitPaned.add(Button(self,width = TAILLE_CASE, image=log03, command = self.definir_couleur3))
        im = Image.open("RessourceLogiciel/LogoCouleur4.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logO2 = ImageTk.PhotoImage(im)
        ptitPaned.add(Button(self,width = TAILLE_CASE, image=logO2, command = self.definir_couleur4))
        im = Image.open("RessourceLogiciel/LogoCouleur5.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logO5 = ImageTk.PhotoImage(im)
        ptitPaned.add(Button(self,width = TAILLE_CASE, image=logO5, command = self.definir_couleur5))
        im = Image.open("RessourceLogiciel/LogoCouleur6.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logO6 = ImageTk.PhotoImage(im)
        ptitPaned.add(Button(self,width = TAILLE_CASE, image=logO6, command = self.definir_couleur6))
        im = Image.open("RessourceLogiciel/LogoCouleur7.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logO7 = ImageTk.PhotoImage(im)
        ptitPaned.add(Button(self,width = TAILLE_CASE, image=logO7, command = self.definir_couleur7))
        im = Image.open("RessourceLogiciel/LogoCouleur8.png")
        im = im.resize((TAILLE_CASE,TAILLE_CASE))
        logO8 = ImageTk.PhotoImage(im)
        ptitPaned.add(Button(self,width = TAILLE_CASE, image=logO8, command = self.definir_couleur8))

        ptitPaned.add(Button(self,width = TAILLE_CASE, text='Choisir', command = self.choisir_fonction))
        self.ecranPaned.add(ptitPaned)
        #ECRAN CANVAS
        self.ecranPaned.add(self.ecranCanvas)
        self.m=Maillages(-N//2,-M//2,1,0,N,M, couleur_test, self.ecranCanvas)
        self.m.afficher(self.ecranCanvas)
        self.ecranCanvas.create_parallelepipede(0, 0, 0, 0.25, 0.25, 0.25)
        # Sélection
        self.canvasSelectionInfo = Canvas(self,width = self.ecranCanvas['width'], height = 50, bg='white')
        self.txtSelect = self.canvasSelectionInfo.create_text(10,int(self.canvasSelectionInfo['height'])//3, anchor='w', text = "Sélection")
        self.txtValueSelect = self.canvasSelectionInfo.create_text(10,2*int(self.canvasSelectionInfo['height'])//3, anchor='w', text = "Sélection")
        self.txtTemps = self.canvasSelectionInfo.create_text(int(self.canvasSelectionInfo['width'])-10, int(self.canvasSelectionInfo['height'])//3, anchor = 'e',text="(0,0,0)")
        self.ecranPaned.add(self.canvasSelectionInfo)
        # Echelle
        self.canvasEchelle = Canvas(self,width = self.ecranCanvas['width'], height=70, bg='white')
        
        
        self.EchelleCanvasCouleur = []
        
        N = 10
        for i in range(N):
            case = self.canvasEchelle.create_rectangle(i*int(self.ecranCanvas['width'])//N,0,(i+1)*int(self.ecranCanvas['width'])//N, int(self.canvasEchelle['height'])-40, fill = 'red', width=0)
            self.EchelleCanvasCouleur.append(case)
            
        self.texteVmin = self.canvasEchelle.create_text(10,int(self.canvasEchelle['height'])-30,anchor="w",text="0")
        self.texteVmax = self.canvasEchelle.create_text(int(self.ecranCanvas['width'])-10,int(self.canvasEchelle['height'])-30,anchor="e",text="0")
        self.textefonction = self.canvasEchelle.create_text(int(self.ecranCanvas['width'])//2, int(self.canvasEchelle['height'])-23, text="Pression")
        self.texteFonctionDescription = self.canvasEchelle.create_text(10,int(self.canvasEchelle['height'])-10, anchor='w')
        self.ecranPaned.add(self.canvasEchelle)       
        
        w = int(self.ecranCanvas['width'])//3
        
        # Puissance
        self.formulePuissance = ["IRRADIANCE_OMBRAGE(x,y,z)*(1-ALBEDO(x,y,z))*SURFACE_MAILLE(x,y,z)"
                                 ,"(5.67*10**-8)*EMISSIVITE_THERMIQUE(x,y,z)*SURFACE_MAILLE(x,y,z)*(-TEMPERATURE_MATERIAU(x,y,z)**4 + TEMPERATURE(x,y,z)**4)",
                                 "h_COEFF(x,y,z)*FACTEUR_RUGOSITE_SURFACE(x,y,z)*SURFACE_MAILLE(x,y,z)*(-TEMPERATURE_MATERIAU(x,y,z)+TEMPERATURE(x,y,z))",
                                 "ECHANGE_PUISSANCE_MAILLE(x,y,z)"
                                 ,"PUISSANCE_ABSORBEE(x,y,z) + PUISSANCE_RAYONNEMENT_THERMIQUE(x,y,z) + PUISSANCE_CONVECTION(x,y,z) + PUISSANCE_CONDUCTION(x,y,z) + PUISSANCE_EVAPOTRANSPIRATION(x,y,z)"
                                 ,"(TEMPERATURE(x,y,z)-TEMPERATURE(x+1,y,z))/(R1+R2)"
                                 ,"(TEMPERATURE(x,y,z)-TEMPERATURE(x,y+1,z))/(R1+R3)",
                                 "-EVAPOTRANSPIRATION(x,y,z)/(1000*24*3600)*SURFACE_MAILLE(x,y,z)*MASSE_VOLUMIQUE_EAU()*L_Vap_eau()"]
        self.souspar_Puissance = PanedWindow(self.mainPaned, orient = VERTICAL)
        self.puissancePaned = PanedWindowDefilant(self.mainPaned, paned_gen = self.souspar_Puissance,orient=VERTICAL)
        self.puissancePaned.add(Label(self,fg='blue',text = "Échange de puissance ", anchor = "w"))
        
        self.puissancePaned.add(Label(self,text = "PUISSANCE_ABSORBEE(x,y,z,t) ", anchor = "w"))
        self.formulePuissance_Entree0 = Text(self,font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.formulePuissance_Entree0.insert("1.0",self.formulePuissance[0])
        self.puissancePaned.add(self.formulePuissance_Entree0)
        self.puissancePaned.add(Label(self,text = "PUISSANCE_RAYONNEMENT_THERMIQUE(x,y,z,t) ", anchor = "w"))
        self.formulePuissance_Entree1 = Text(self,font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.formulePuissance_Entree1.insert("1.0",self.formulePuissance[1])
        self.puissancePaned.add(self.formulePuissance_Entree1)
        self.puissancePaned.add(Label(self,text = "PUISSANCE_CONVECTION(x,y,z,t) ", anchor = "w"))
        self.formulePuissance_Entree2 = Text(self,font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.formulePuissance_Entree2.insert("1.0",self.formulePuissance[2])
        self.puissancePaned.add(self.formulePuissance_Entree2)
        self.puissancePaned.add(Label(self,text = "PUISSANCE_CONDUCTION(x,y,z,t) ", anchor = "w"))
        self.formulePuissance_Entree3 = Text(self,font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.formulePuissance_Entree3.insert("1.0",self.formulePuissance[3])
        self.puissancePaned.add(self.formulePuissance_Entree3)
        self.puissancePaned.add(Label(self,text = "SOMME_PUISSANCE(x,y,z,t) ", anchor = "w"))
        self.formulePuissance_Entree4 = Text(self,font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.formulePuissance_Entree4.insert("1.0",self.formulePuissance[4])
        self.puissancePaned.add(self.formulePuissance_Entree4)
        self.puissancePaned.add(Label(self,text = "PUISSANCE_ECHANGE(x,y,z,x+1,y,z,t) ", anchor = "w"))
        self.formulePuissance_Entree5 = Text(self,font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.formulePuissance_Entree5.insert("1.0",self.formulePuissance[5])
        self.puissancePaned.add(self.formulePuissance_Entree5)
        self.puissancePaned.add(Label(self,text = "PUISSANCE_ECHANGE(x,y,z,x,y+1,z,t) ", anchor = "w"))
        self.formulePuissance_Entree6 = Text(self,font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.formulePuissance_Entree6.insert("1.0",self.formulePuissance[6])
        self.puissancePaned.add(self.formulePuissance_Entree6)
        self.puissancePaned.add(Label(self,text = "PUISSANCE_EVAPOTRANSPIRATION(x,y,z) ", anchor = "w"))
        self.formulePuissance_Entree7 = Text(self,font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.formulePuissance_Entree7.insert("1.0",self.formulePuissance[7])
        self.puissancePaned.add(self.formulePuissance_Entree7)
        self.puissancePaned.add(Button(self,text="Mettre à jour les formules de puissance", command = self.maj_puissance))
        self.puissancePaned.add(Label(self,text = "dT = ", anchor = "w"))
        self.entree_Formule_Var = Text(self, font=(INTERFACE.FONT, INTERFACE.TAILLE_FONT),wrap="word", height=3)
        self.entree_Formule_Var.insert("1.0","SOMME_PUISSANCE(x,y,z)*dt/(cp(x,y,z)*MASSE_VOLUMIQUE(x,y,z))")
        self.puissancePaned.add(self.entree_Formule_Var)
        
        self.formulePuissance_Entrees = [self.formulePuissance_Entree0,self.formulePuissance_Entree1, self.formulePuissance_Entree2,self.formulePuissance_Entree3, self.formulePuissance_Entree4, self.formulePuissance_Entree5, self.formulePuissance_Entree6, self.formulePuissance_Entree7]
        self.souspar_Puissance.add(self.puissancePaned)
        self.liste_souspar.append(self.souspar_Puissance)
        
        #Résultats
        self.resultatsPaned = PanedWindow(self.mainPaned, orient=VERTICAL)
        self.resultatsPaned.add(Label(self,text="Choisir la mesure à visualiser :", anchor="w", fg='blue'))
        self.resultatsPaned.add(Button(self,text="Rafraichissement",bg='#d4cdf8', fg="#29197a", command = self.definir_rafraichissement))
        self.resultatsPaned.add(Button(self,text="Réchauffement", bg='#f07a75',fg='#b6281a', command = self.definir_rechauffement))
        self.resultatsPaned.add(Button(self,text = 'Evapotranspiration', command = self.definir_evapotranspiration, fg='#1623bd', bg='#a3f0db'))
        self.entree_Mesure = Entry(self)
        self.entree_Mesure.insert(0,"TEMPERATURE_CELSIUS")
        self.resultatsPaned.add(self.entree_Mesure)
        self.resultatsPaned.add(Button(self,text = "Définir la mesure", command = self.def_mesure))
        self.resultatsPaned.add(Label(self,text="Options TARE :", anchor="w", fg='blue'))
        
        self.boutonTare = Button(self,text="Tare", command = self.faireTare)
        self.resultatsPaned.add(self.boutonTare)
        self.boutonCalculeTare = (Button(self,text="Comparer à la Tare", command = self.calcule_tare))
        self.resultatsPaned.add(self.boutonCalculeTare)
        self.boutonReinitTare = Button(self,text="Réinitialiser la Tare", command = self.reinitialiser_tare)
        self.resultatsPaned.add(self.boutonReinitTare)
        self.resultatsPaned.add(Label(self,text="Temporalité :", anchor="w", fg='red'))
        self.liste_souspar.append(self.resultatsPaned)
        
        def command_scale_2(e):
            global TEMPS_ABSOLU
            TEMPS_ABSOLU = self.scale_temps_2.get()
            self.scale_temps.set(TEMPS_ABSOLU)
            self.actualiser_temps()
        def command_scale_1(e):
            global TEMPS_ABSOLU
            TEMPS_ABSOLU = self.scale_temps.get()
            self.scale_temps_2.set(TEMPS_ABSOLU)
            self.actualiser_temps()
        self.scale_temps_2 = Scale(self, from_ = 0, to_ = 86400, command = command_scale_2,bg=violet, orient=HORIZONTAL)
        self.resultatsPaned.add(self.scale_temps_2)
        
        
        # Simulation temporelle des puissances
        self.souspar_SimuTemp = PanedWindow(self.sousparPaned,orient=VERTICAL)
        
        self.liste_souspar.append(self.souspar_SimuTemp)
        
        self.souspar_SimuVisu = PanedWindowDefilant(self.souspar_SimuTemp,bg = violet,taille_paned=600,paned_gen=self.souspar_SimuTemp,orient=VERTICAL) 
        self.souspar_SimuVisu.add(Label(self,bg = violet,text="Choix de la mesure à visualiser :",anchor="w", fg="blue"))
        
        self.souspar_SimuVisu.add(Button(self,text="Température du revêtement (Recommandé)", command = lambda :maj_FONCTION_ACTUELLE(TEMPERATURE_MATERIAU_CELSIUS)))
        self.souspar_SimuVisu.add(Button(self,text="Puissance d'évapotranspiration", command = lambda :maj_FONCTION_ACTUELLE(PUISSANCE_EVAPOTRANSPIRATION)))
        
        self.souspar_SimuVisu.add(Label(self,bg = violet,text="Trame temporelle (en s) :",anchor="w", fg="blue"))
        
        self.scale_temps = Scale(self, from_ = 0, command=command_scale_1,to_ = 86400, bg=violet, orient=HORIZONTAL)
        self.souspar_SimuVisu.add(self.scale_temps)
        self.texte_temps = Label(self,text = "",bg = violet)
        self.texte_temps_bis = Label(self,text = "",bg = violet)
        self.souspar_SimuVisu.add(self.texte_temps)
        self.resultatsPaned.add(self.texte_temps_bis)
        self.souspar_SimuVisu.add(Label(self,bg = violet,text="Description d'un cycle dans la simulation :", fg='blue',anchor="w"))
        self.souspar_SimuVisu.add(Label(self,bg = violet,anchor="w",text="Nombre de points temporels :"))
        self.entree_Nb_points_temp = Entry(self)
        self.entree_Nb_points_temp.insert(0,"500")
        self.souspar_SimuVisu.add(self.entree_Nb_points_temp)
        self.souspar_SimuVisu.add(Label(self,bg = violet,anchor="w",text="Débuter le temps à (0 <= t < 86400):"))
        self.entree_temps_debut = Entry(self)
        self.entree_temps_debut.insert(0,"25000")
        self.souspar_SimuVisu.add(self.entree_temps_debut)
        self.souspar_SimuVisu.add(Label(self,bg = violet,anchor="w",text="Terminer le temps à (0 <= t < 86400):"))
        self.entree_temps_fin = Entry(self)
        self.entree_temps_fin.insert(0,"86400")
        self.souspar_SimuVisu.add(self.entree_temps_fin)
        self.souspar_SimuVisu.add(Label(self,bg = violet,anchor="w",text="[Animation] : Temps entre les points pendant la simulation (en s) :"))
        self.entree_T_points_temp = Entry(self)
        self.entree_T_points_temp.insert(0,"0.5")
        self.souspar_SimuVisu.add(self.entree_T_points_temp)
        self.souspar_SimuVisu.add(Label(self,bg = violet,anchor="w",text="Conditions initiales :", fg = 'blue'))
        self.souspar_SimuVisu.add(Label(self,bg = violet,anchor="w",text="Température du matériau (en °C) :"))
        self.entree_CI_temp_mat = Entry(self)
        self.entree_CI_temp_mat.insert(0,"20")
        self.souspar_SimuVisu.add(self.entree_CI_temp_mat)
        self.souspar_SimuVisu.add(Button(self,command = self.appliquer_CI,text='Appliquer les conditions initiales'))
        
        
        self.souspar_SimuVisu.add(Label(self,bg = violet,text="Mode de simulation :", anchor="w", fg='blue'))
        self.mode_simu = "MOYENNE"
        self.bouton_SIMU_MOYENNE = Button(self,bg = violet,text="Moyenne temporelle sur la journée.\n Ce mode prend les valeurs de FONCTION_ACTUELLE en n points\n de la journée et fait une moyenne. Cependant, ce mode\n ne tient pas compte de l'élévation de température\n du revêtement liée aux variations de puissance.", command = self.def_mode_moyenne)
        self.souspar_SimuVisu.add(self.bouton_SIMU_MOYENNE)
        self.bouton_SIMU_PROGRESSION = Button(self,text="Progression temporelle animée sur la journée\n La température du revêtement évolue selon son bilan de puissance.\n Une animation permet de voir le résultat évoluer en temps réel.", command = self.def_mode_progression)
        self.souspar_SimuVisu.add(self.bouton_SIMU_PROGRESSION)
        self.bouton_SIMU_PROGRESSION2 = Button(self,text="Progression temporelle instantannée sur la journée\n La température du revêtement évolue selon son bilan de puissance.", command = self.def_mode_progression_instant)
        self.souspar_SimuVisu.add(self.bouton_SIMU_PROGRESSION2)
        self.bouton_simu = Button(self,text="Lancer la simulation", command = self.lancer_simulation_temporelle)
        self.souspar_SimuVisu.add(self.bouton_simu)
        self.souspar_SimuVisu.add(Button(self,command = self.stopper_simulation, text="Stopper la simulation"))
        self.souspar_SimuVisu.add(Label(self,text="Analyse du résultat :", fg = 'blue',anchor='w', bg=violet))
        
        self.scale_resultat = Scale(self,from_ = 0,command=self.point_temporel, to_ = 10, bg=violet, orient=HORIZONTAL)
        self.souspar_SimuVisu.add(self.scale_resultat)     
        self.souspar_SimuVisu.add(Button(self,text="Revenir à ce point temporel", command=self.point_temporel))
        self.souspar_SimuVisu.add(Button(self,text="Afficher le graphe associé (Progression)", command = self.graphe_))
        self.save_simu = Entry(self, bg = violet)
        self.save_simu.insert(0,'simulation0.txt')
        self.souspar_SimuVisu.add(self.save_simu)
        self.souspar_SimuVisu.add(Button(self,command = self.save_simu_write,text="Enregistrer le résultat d'une simulation"))
        self.souspar_SimuVisu.add(Button(self,command = self.open_simu,text="Ouvrir une simulation"))

        self.souspar_SimuVisu.add(Label(self,text=" ", bg=violet))
        self.souspar_SimuTemp.add(self.souspar_SimuVisu)
        
        
        self.texteAvancement = self.ecranCanvas.create_text(10,int(self.ecranCanvas['height'])-10, text = '', anchor = 'sw')
        
        self.mainPaned.add(self.buttonPaned)
        self.mainPaned.add(self.sousparPaned)
        self.mainPaned.add(self.ecranPaned)
        self.mainPaned.pack(fill="both", expand=True)
        
        self.appliquer_irradiance()
        
        # Commandes
        for i in Interface.TOUCHE_ZOOM:
            self.bind(i, self.ecranCanvas.zoom)
        for _ in Interface.TOUCHE_DEZOOM:
            self.bind(_, self.ecranCanvas.dezoom)
        for _ in Interface.TOUCHE_ROTA_DROITE:
            self.bind(_, self.ecranCanvas.pivoter_droite)
        for _ in Interface.TOUCHE_ROTA_GAUCHE:
            self.bind(_, self.ecranCanvas.pivoter_gauche)
        for _ in Interface.TOUCHE_DECAL_X:
            self.bind(_, self.ecranCanvas.decalX0)
        for _ in Interface.TOUCHE_DECAL_Xneg:
            self.bind(_, self.ecranCanvas.decalX1)
        for _ in Interface.TOUCHE_DECAL_Y:
            self.bind(_, self.ecranCanvas.decalY0)
        for _ in Interface.TOUCHE_DECAL_Yneg:
            self.bind(_, self.ecranCanvas.decalY1)
        for _ in Interface.TOUCHE_DECAL_REINIT:
            self.bind(_, self.ecranCanvas.decal0)
            
        # Fonctions paramétrées
        global ALBEDO
        #ALBEDO = self.m.get_albedo
        
        #Sauvegarde
        self.ouvrir_fichier = ouvrir_fichier
        if self.ouvrir_fichier != None:
            self.load_save(self.ouvrir_fichier)
        
        self._after_fenetre()
        #self.rafraichir()
        print('Lancement de la fenêtre')
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", self.quitter_fullscreen)
        self.maj_graph_irradiance()
        self.mainloop()
    def get_description(self, fct):
        fonction = fct.__name__
        global DESCRIPTION
        try:
            return DESCRIPTION[fonction]
        except:
            DESCRIPTION[fonction] = "Aucune description n'a été renseignée à propos de cette fonction"
        return DESCRIPTION[fonction]
    def cacher_arbre(self):
        self.VIEW_ARBRE = False
    def voir_arbre(self):
        self.VIEW_ARBRE = True
    def cacher_batiment(self):
        self.VIEW_BATIMENT = False
    def voir_batiment(self):
        self.VIEW_BATIMENT = True
    def save_simu_write(self):
        link = self.save_simu.get()
        with open(link, 'w') as fichier:
            fichier.write(str(self.tramet))
            fichier.write(str(self.valeur_simu_temporelle_save_temps))
            fichier.write(str(self.valeur_simu_temporelle_save_temperature))
    def open_simu(self):
        global FONCTION_ACTUELLE
        link = self.save_simu.get()
        print(' \nOuverture du fichier {0}'.format(link))
        with open(link, "r", encoding="utf-8") as fichier:
            for ligne in fichier:
                print(ligne)
            print(lignes)
            self.valeur_simu_temporelle_save_temps = eval(lignes[1])
            self.valeur_simu_temporelle_save_temperature = eval(lignes[2])
            self.tramet = eval(lignes[0])
        FONCTION_ACTUELLE = RESULTATS_SIMU
    def appliquer_CI(self):
        t = TEMPS_ABSOLU
        FONCTION_ACT(0,0,0,True,True)
        for x,y in self.m.listeXY:
            TEMP_VALEUR_MAT[(x,y,0)] = eval(self.entree_CI_temp_mat.get())+273.15
    def choisir_fonction(self):
        fenetre = Tk()
        paned_global = PanedWindow(fenetre, orient=VERTICAL)
        paned_bouton = PanedWindowDefilant(fenetre,orient=VERTICAL,paned_gen = paned_global)
        L = list(DESCRIPTION.keys())
        L.sort()
        for i in L:
            texte = "{0}\n{1}".format(i, DESCRIPTION[i])
            b = Button(fenetre, text=texte, command = lambda valeur=i: (
    set_fonction_actuelle(eval(valeur)), FONCTION_ACT(0,0,0,True,True),fenetre.destroy()
))
            paned_bouton.add(b)
        paned_global.add(paned_bouton)
        paned_global.pack()
        Button(fenetre,text="Fermer la fenêtre", command = fenetre.destroy)
        fenetre.mainloop()
    def quitter_fullscreen(self,event):
        self.attributes("-fullscreen", False)
    def create_scrollable_paned(self):
        """Crée un PanedWindow avec une barre de défilement verticale placée à gauche."""
        container = PanedWindow(self.sousparPaned, orient=VERTICAL)
        scrollbar = Scrollbar(self.mainPaned, orient=VERTICAL)
        canvas = Canvas(container, yscrollcommand=scrollbar.set)
        scrollable_frame = Frame(canvas)
    
        # Configurer le défilement
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
    
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
        # Ajouter les widgets dans l'ordre (scrollbar à gauche, canvas à droite)
        container.add(scrollbar)
        container.add(canvas)
    
        # Associer la scrollbar au canvas
        scrollbar.config(command=canvas.yview)
    
        return container, scrollable_frame, scrollbar
    def appliquer_formule_h(self):
        global FORMULE_H, VECTEUR_VENT_VALEUR
        try:
            eval(self.entree_h_coeff.get())
            FORMULE_H = self.entree_h_coeff.get()
        except:
            self.message_erreur("Erreur dans l'expression de h")
        try:
            z = 0
            print('Modification de la valeur du vent')
            for x in range(self.select_case[0][0], self.select_case[1][0]+1):
                for y in range(self.select_case[0][1], self.select_case[1][1]+1):
                    VECTEUR_VENT_VALEUR[(x,y,z)] = self.entree_Valeur_Vent.get()     
        except:
            self.message_erreur("Erreur dans l'expression de VENT")
            
    def maj_graph_irradiance(self):
        if self.launch_interface_irr:
            try:
                fig,ax,canvas = self.fig_save_irradiance
                ax.clear()
                N = 10000
                t_values = [86400*t/N for t in range(N)]
                y_values = []
                for t in t_values:
                    y_values.append(eval(IRR_SOL))
                ax.plot(t_values,y_values, label='Rayonnement solaire')
                ax.plot([TEMPS_ABSOLU for i in range(N)],y_values, label='Temps actuel')

                ax.set_xlabel('t')
                ax.set_ylabel('IRRADIANCE_OMBRAGE')
                ax.legend()
                canvas.draw()
            except:
                pass
        self.after(1000,self.maj_graph_irradiance)
    def maj_puissance(self):
        liste = self.formulePuissance_Entrees
        for i in range(len(liste)):
            self.formulePuissance[i] = liste[i].get()
    def stopper_simulation(self):
        self.stop_simulation = True
        self.simu_run = False
    def lancer_simulation_temporelle(self,z=0):
        global RESULTATS_SIMULATION, TEMP_VALEUR, FONCTION_ACTUELLE, TEMPS_ABSOLU
        print('Lancement de la simulation temporelle')
        self.valeur_simu_temporelle_save_temps = {}
        self.stop_simulation = False
        self.simu_run = True
        conduction = True
        if self.mode_simu == "MOYENNE":
            N = eval(self.entree_Nb_points_temp.get())
            fin = int(self.entree_temps_fin.get())
            debut = int(self.entree_temps_debut.get())
            self.tramet = [debut+(fin-debut)*i/(N-1) for i in range(N)]
            self.tramet_N = -1
            for t in self.tramet :
                self.tramet_N += 1
                av = self.tramet[self.tramet_N]/(self.tramet[-1])
                print('Trame temporelle ',av,'%')
                self.ecranCanvas.itemconfig(self.texteAvancement,text="{0}%".format(100*av))
                self.scale_temps.set(t)

                TEMPS_ABSOLU = t
                self.calculer_ombrage(message=False)
                # calcul des forces de conduction
                if conduction:
                    print('Calcul de la puissance de conduction')
                    calcule_puissance_echange()
                for x,y in self.m.listeXY:
                    #Resultats
                    if (x,y,z) not in RESULTATS_SIMULATION.keys():
                        RESULTATS_SIMULATION[(x,y,z)] = 0
                    val = FONCTION_ACT(x,y,z,True, True)
                    RESULTATS_SIMULATION[(x,y,z)] += val/N
                    self.valeur_simu_temporelle_save_temps[(x,y,z,int(t))] = val
                if self.stop_simulation:
                    self.stop_simulation = False
                    break
            self.simu_run = False
        
        if self.mode_simu == "PROGRESSION":
            
            N = eval(self.entree_Nb_points_temp.get())
            self.scale_resultat['to_'] = N
            fin = int(self.entree_temps_fin.get())
            debut = int(self.entree_temps_debut.get())
            self.tramet = [debut+(fin-debut)*i/(N-1) for i in range(N)]
            self.tramet_N = 0
            temps_inter = int(1000*eval(self.entree_T_points_temp.get()))
            self.tramefonction = FONCTION_ACTUELLE
            self.start_save_time = time.time()
            def simu_t():
                if self.stop_simulation:
                    self.stop_simulation = False
                    return None
                global TEMPS_ABSOLU, FONCTION_ACTUELLE, RESULTATS_SIMU
                if self.tramet_N == len(self.tramet):
                    self.message_texte('Fin de la simulation')
                    self.simu_run = False
                    return None
                self.scale_resultat.set(self.tramet_N)
                t = self.tramet[self.tramet_N]
                av = (t-self.tramet[0])/(self.tramet[-1])
                self.ecranCanvas.itemconfig(self.texteAvancement,text="{0}%".format(100*av))
                print('Lancement de la simulation pour le temps \n{0}/{1}'.format(t,self.tramet[-1]))
                self.scale_temps.set(t)
                TEMPS_ABSOLU = t
                print('Ombrage')
                self.calculer_ombrage(message=False)
                FONCTION_ACTUELLE = self.tramefonction
                z=0
                if self.tramet_N !=0:
                    # Actualisation de la température des matériaux
                    dt = t-self.tramet[self.tramet_N-1]
                    print('Mise à jour des températures dans le sol... ')
                    for x,y in self.m.listeXY:
                        grandeur = eval(self.entree_Formule_Var.get()) 
                        if grandeur >= 10:
                            self.stop_simulation = True
                            self.message_erreur("La simulation s'est arrêtée car il y a eu une hausse de température de 10°C entre deux points temporels, il est conseillé de prendre plus de points")
                            return None
                        TEMP_VALEUR_MAT[(x,y,z)] += grandeur
                        self.valeur_simu_temporelle_save_temperature[(x,y,z,int(t))] = TEMP_VALEUR_MAT[(x,y,z)]
                self.tramet_N += 1
                print('Calcul des valeurs...')
                calcule_puissance_echange()
                for x,y in self.m.listeXY:
                    #Resultats
                    if FONCTION_ACTUELLE == TEMPERATURE_MATERIAU:
                        val = TEMP_VALEUR_MAT[(x,y,z)]
                    else:
                        val = FONCTION_ACT(x,y,z)
                    RESULTATS_SIMULATION[(x,y,z)] = val
                    self.valeur_simu_temporelle_save_temps[(x,y,z,int(t))] = val
                print('Calcul terminé, attente de la suite')
                temps_inter = int(1000*eval(self.entree_T_points_temp.get()))
                if time.time()-self.start_save_time>10:
                    temps_inter = max(temps_inter,1000)
                    self.start_save_time = time.time()
                self.after(temps_inter,simu_t) 
                FONCTION_ACTUELLE = RESULTATS_SIMU
                FONCTION_ACT(0,0,0,True,True)
            self.after(1,simu_t)
        if self.mode_simu == "PROGRESSION INSTANTANNEE":
            
            N = eval(self.entree_Nb_points_temp.get())
            self.scale_resultat['to_'] = N
            fin = int(self.entree_temps_fin.get())
            debut = int(self.entree_temps_debut.get())
            self.tramet = [debut+(fin-debut)*i/(N-1) for i in range(N)]
            self.tramet_N = 0
            temps_inter = int(1000*eval(self.entree_T_points_temp.get()))
            self.tramefonction = FONCTION_ACTUELLE
            def simu_t():
                if self.stop_simulation:
                    self.stop_simulation = False
                    return None
                global TEMPS_ABSOLU, FONCTION_ACTUELLE, RESULTATS_SIMU
                if self.tramet_N == len(self.tramet):
                    self.simu_run = False
                    return None
                self.scale_resultat.set(self.tramet_N)
                t = self.tramet[self.tramet_N]
                av = (t-self.tramet[0])/(self.tramet[-1])
                self.ecranCanvas.itemconfig(self.texteAvancement,text="{0}%".format(100*av))
                print('Lancement de la simulation pour le temps \n{0}/{1}'.format(t,self.tramet[-1]))
                
                self.calculer_ombrage(message=False)
                FONCTION_ACTUELLE = self.tramefonction
                z=0
                if self.tramet_N !=0:
                    # Actualisation de la température des matériaux
                    dt = t-self.tramet[self.tramet_N-1]
                    print('Mise à jour des températures dans le sol... ')
                    for x,y in self.m.listeXY:
                        grandeur = eval(self.entree_Formule_Var.get()) 
                        if grandeur >= 10:
                            self.stop_simulation = True
                            self.message_erreur("La simulation s'est arrêtée car il y a eu une hausse de température de 10°C entre deux points temporels, il est conseillé de prendre plus de points")
                            return None
                        TEMP_VALEUR_MAT[(x,y,z)] += grandeur
                        self.valeur_simu_temporelle_save_temperature[(x,y,z,int(t))] = TEMP_VALEUR_MAT[(x,y,z)]
                self.tramet_N += 1
                print('Calcul des valeurs...')
                calcule_puissance_echange()
                for x,y in self.m.listeXY:
                    #Resultats
                    if FONCTION_ACTUELLE == TEMPERATURE_MATERIAU:
                        val = TEMP_VALEUR_MAT[(x,y,z)]
                    else:
                        val = FONCTION_ACT(x,y,z)
                    RESULTATS_SIMULATION[(x,y,z)] = val
                    self.valeur_simu_temporelle_save_temps[(x,y,z,int(t))] = val
                print('Calcul terminé, attente de la suite')
                self.after(1,simu_t) 
                FONCTION_ACTUELLE = RESULTATS_SIMU
                FONCTION_ACT(0,0,0,True,True)
            self.after(1,simu_t)
        self.mode_simu = 'A redefinir'
        FONCTION_ACTUELLE = RESULTATS_SIMU
        self.ecranCanvas.clic(Nonee())
    def def_mode_moyenne(self):
        self.mode_simu = "MOYENNE"
    def def_mode_progression(self):
        self.mode_simu = "PROGRESSION"
    def def_mode_progression_instant(self):
        self.mode_simu = "PROGRESSION INSTANTANNEE"
    def def_mesure(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = eval(self.entree_Mesure.get())
        self.m.reinit_couleur()
    def clic_Rafraich_Interface(self):
        self.block_interface = not self.block_interface
        txt_stop = "Stopper Actualisation Interface"
        txt_remettre = "Remettre Actualisation Interface"
        if not self.block_interface: #reactivation de l'interface
            self._after_fenetre()
            self.btn_rafraich_interface['text'] = txt_stop
            self.btn_rafraich_interface['bg'] = 'green'
        else:
            self.btn_rafraich_interface['text'] = txt_remettre
            self.btn_rafraich_interface['bg']  = 'red'
    
    def clic_Rafraich_Tri(self):
        self.ecranCanvas.block_interface_tri = not self.ecranCanvas.block_interface_tri
        txt_stop = "Stopper Actualisation Graphisme"
        txt_remettre = "Remettre Actualisation Graphisme"
        if not self.ecranCanvas.block_interface_tri: #reactivation de l'interface
            self.ecranCanvas.tri_objet()
            self.btn_rafraich_tri['text'] = txt_stop
            self.btn_rafraich_tri['bg'] = 'green'
        else:
            self.btn_rafraich_tri['text'] = txt_remettre
            self.btn_rafraich_tri['bg']  = 'red'
            
    def clic_Rafraich_Canvas(self):
        self.ecranCanvas.block_interface = not self.ecranCanvas.block_interface
        txt_stop = "Stopper Actualisation Canvas"
        txt_remettre = "Remettre Actualisation Canvas"
        if not self.ecranCanvas.block_interface: #reactivation de l'interface
            self.ecranCanvas._after() 
            self.btn_rafraich_canvas['text'] = txt_stop
            self.btn_rafraich_canvas['bg'] = 'green'
            self.ecranCanvas['bg'] = 'white'
        else:
            self.btn_rafraich_canvas['text'] = txt_remettre
            self.btn_rafraich_canvas['bg']  = 'red'
            self.ecranCanvas['bg'] = 'red'
    def graphe_(self):
        x,y = self.coord
        z = 0
        self.afficher_graphe_simulation(floor(x),floor(y),z)
    def afficher_graphe_simulation(self,x,y,z):
        abscisse = [i[3] for i in self.valeur_simu_temporelle_save_temps.keys()]
        ordonnee = [self.valeur_simu_temporelle_save_temps[(x,y,z,temp)] for temp in abscisse]
        #abscisse = [i[3] for i in self.valeur_simu_temporelle_save_temps.keys()]

        #ordonnee2 = [self.valeur_simu_temporelle_save_temperature [(x,y,z,temp)] for temp in abscisse]
        plt.plot(abscisse, ordonnee, linestyle='-', color='b', label="Courbe")
       # plt.plot(abscisse, ordonnee2, linestyle='-', color='b', label="Courbe")
        plt.title('{0}({1},{2},{3}) en fonction du temps t'.format(FONCTION_ACTUELLE.__name__,x,y,z))
        plt.show()
    def def_mesure2(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = eval(self.entree_Mesure2.get())
        self.m.reinit_couleur()
    def select_materiau_beton(self):
        self.select_materiau = "Béton ordinaire"
    def select_materiau_gazon(self):
        self.select_materiau = "Gazon"
    def select_vegetation_sapin(self):
        self.select_vege = "Sapin"
    def passer_en_3D(self):
        self.ecranCanvas.mode_ = "3D"
    def passer_en_2D(self):
        self.ecranCanvas.mode_ = "2D"
    def point_temporel(self,e=None):
        if not self.simu_run:
            N = int(self.scale_resultat.get())
            z=0
            t = self.tramet[N]
            self.ecranCanvas.itemconfig(self.texteAvancement, text="{0}s".format(t))
            for x,y in self.m.listeXY:
                RESULTATS_SIMULATION[(x,y,z)] = self.valeur_simu_temporelle_save_temps[(x,y,z,int(t))] 
            FONCTION_ACTUELLE = RESULTATS_SIMU
            FONCTION_ACT(0,0,0,True,True)
            self.m.reinit_couleur()
    def reinit_maillage(self):
        t = float(self.entree_Maillage.get())
        
        # Réinitialisation du maillage
        m_to_suppr = self.m
        N=int(self.entree_Maillage_x.get())
        M=int(self.entree_Maillage_y.get())
        
        self.destroy()
        Interface(N,M,t)
    def rafraichir(self):
        if self.ecranCanvas.block_interface:
            print('Rafraichissement')
            self.ecranCanvas._after()
        FONCTION_ACT(0,0,0,True,True)
        
    def definir_couleur1(self):
        global ECHELLE_COULEUR
        ECHELLE_COULEUR = valeur_vers_couleur
        self.m.reinit_couleur()
    def definir_couleur2(self):
        global ECHELLE_COULEUR
        ECHELLE_COULEUR = couleur_test
        self.m.reinit_couleur()
    def definir_couleur3(self):
        global ECHELLE_COULEUR
        ECHELLE_COULEUR = couleur_albedo
        self.m.reinit_couleur()
    def definir_couleur4(self):
        global ECHELLE_COULEUR
        ECHELLE_COULEUR = ECHELLE_VEGE
        self.m.reinit_couleur()
    def definir_couleur5(self):
        global ECHELLE_COULEUR
        ECHELLE_COULEUR = couleur_ombre
        self.m.reinit_couleur()
    def definir_couleur6(self):
        global ECHELLE_COULEUR
        ECHELLE_COULEUR= ECHELLE_EAU
        self.m.reinit_couleur()
    def definir_couleur7(self):
        global ECHELLE_COULEUR
        ECHELLE_COULEUR = couleur_longueur_onde
        self.m.reinit_couleur()
    def definir_couleur8(self):
        global ECHELLE_COULEUR
        ECHELLE_COULEUR = couleur_longueur_onde_inv
        self.m.reinit_couleur()
    def definir_pression(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = PRESSION
        self.m.reinit_couleur()
    def definir_evapotranspiration(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = EVAPOTRANSPIRATION
        self.m.reinit_couleur()
    def definir_rafraichissement(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = RAFRAICHISSEMENT
        self.m.reinit_couleur()
        self.definir_couleur8()
    def definir_rafraichissement_inertie(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = RAFRAICHISSEMENT_INERTIE
        self.m.reinit_couleur()
        self.definir_couleur8()
    def definir_rafraichissement_diffusion(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = RAFRAICHISSEMENT_DIFFUSION
        self.m.reinit_couleur()
        self.definir_couleur8()
    def definir_rafraichissement_evapo(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = RAFRAICHISSEMENT_EVAPO
        self.m.reinit_couleur()
        self.definir_couleur8()
    def definir_rafraichissement_soussol(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = RAFRAICHISSEMENT_SOUSSOL
        self.m.reinit_couleur()
        self.definir_couleur8()
    def definir_rechauffement(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = RECHAUFFEMENT
        self.m.reinit_couleur()
        self.definir_couleur7()
    def definir_humidite(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = HUMIDITE
        self.m.reinit_couleur()
        self.definir_couleur8()
    def forget_souspar(self):
        self.VIEW_ARBRE = True
        self.VIEW_BATIMENT = True
        for i in self.liste_souspar:
            self.sousparPaned.forget(i)
        self.paned_mat.tout_cacher()
        self.launch_interface_irr = False
        FONCTION_ACT(0,0,0,True,True)
    def souspar_affiche_Albedo(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = ALBEDO
        self.definir_couleur3()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.VIEW_ARBRE = False
        self.VIEW_BATIMENT = False
        self.sousparPaned.add(self.souspar_Albedo)
    def souspar_affiche_Batiment(self):
        global FONCTION_ACTUELLE, ECHELLE_COULEUR
        FONCTION_ACTUELLE = MATERIAU_COULEUR
        ECHELLE_COULEUR = couleur_mat
        self.m.reinit_couleur()
        self.forget_souspar()
        self.sousparPaned.add(self.souspar_Batiment)
    def souspar_affiche_Terrain(self):
        global FONCTION_ACTUELLE, ECHELLE_COULEUR
        FONCTION_ACTUELLE = MATERIAU_COULEUR
        ECHELLE_COULEUR = couleur_mat
        self.m.reinit_couleur()
        self.forget_souspar()
        self.sousparPaned.add(self.paned_terrain)
    def souspar_affiche_TerrainApplique(self):
        global FONCTION_ACTUELLE, ECHELLE_COULEUR, VIEW_BATIMENT
        FONCTION_ACTUELLE = MATERIAU_COULEUR
        ECHELLE_COULEUR = couleur_mat
        self.m.reinit_couleur()
        self.forget_souspar()
        VIEW_BATIMENT = False
        self.sousparPaned.add(self.souspar_TerrainApplique)
    def souspar_affiche_Vegetalisation(self):
        global FONCTION_ACTUELLE, ECHELLE_COULEUR
        FONCTION_ACTUELLE = ARBRE
        self.definir_couleur4()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.sousparPaned.add(self.souspar_VG)
    def souspar_affiche_BDVegetation(self):
        global FONCTION_ACTUELLE, ECHELLE_COULEUR
        FONCTION_ACTUELLE = ARBRE
        self.definir_couleur4()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.sousparPaned.add(self.souspar_BDVegetation)
    def ajouter_texte_passant(self, widget, texte):
        def show_tooltip_canvas(event):
            # Placer le label de l'info-bulle juste en dessous du curseur
            tooltip.place(x=event.x_root - self.winfo_rootx() + 10,y=event.y_root - self.winfo_rooty() + 10)
            tooltip.config(text=texte)  # Texte à afficher
            tooltip.lift()
        def hide_tooltip_canvas(event):
            tooltip.place_forget()
        tooltip = Label(self, text="", bg="white", fg="black", relief="solid", borderwidth=1)
        tooltip.place_forget() 
        widget.bind('<Enter>', show_tooltip_canvas)
        widget.bind('<Leave>', hide_tooltip_canvas)
    def souspar_affiche_Evapotranspiration(self):
        global FONCTION_ACTUELLE, ECHELLE_COULEUR
        FONCTION_ACTUELLE = ARBRE
        self.definir_couleur4()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.sousparPaned.add(self.souspar_Evapo)
    def souspar_affiche_Irradiance(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = IRRADIANCE_OMBRAGE
        self.definir_couleur5()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.launch_interface_irr = True
        self.sousparPaned.add(self.souspar_Irradiance)
    def souspar_affiche_SimuTemp(self):
        global FONCTION_ACTUELE
        FONCTION_ACTUELLE = TEMPERATURE
        self.definir_couleur7()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.sousparPaned.add(self.souspar_SimuTemp)
    def souspar_affiche_SimuVisu(self):
        global FONCTION_ACTUELE
        FONCTION_ACTUELLE = TEMPERATURE
        self.definir_couleur7()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.sousparPaned.add(self.souspar_SimuVisu)
    def souspar_affiche_Eau(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = SURFACE_EAU
        self.definir_couleur6()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.VIEW_BATIMENT = False
        self.sousparPaned.add(self.souspar_Eau)
    
    def souspar_affiche_Ventilation(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = SURFACE_EAU
        self.definir_couleur2()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.sousparPaned.add(self.souspar_Ventilation)
        
    def souspar_affiche_VarThermo(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = TEMPERATURE
        self.definir_couleur1()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.sousparPaned.add(self.souspar_VarThermo)
    def souspar_affiche_Rafraichissement(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = RAFRAICHISSEMENT
        self.definir_couleur2()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.VIEW_BATIMENT = False
        self.sousparPaned.add(self.paned_rafrai)
    def souspar_affiche_Temperature(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = TEMPERATURE
        self.definir_couleur1()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.VIEW_BATIMENT = False
        self.sousparPaned.add(self.souspar_Rechauffement)
    def souspar_affiche_Maillage(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = SURFACE_EAU
        self.definir_couleur4()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.sousparPaned.add(self.souspar_Maillage)
    def souspar_affiche_Puissance(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = SOMME_PUISSANCE
        self.definir_couleur4()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.sousparPaned.add(self.souspar_Puissance)
    def commande_simulation(self):
        global FONCTION_ACTUELLE
        if FONCTION_ACTUELLE == MATERIAU_COULEUR:
            FONCTION_ACTUELLE = RAFRAICHISSEMENT
        for x,y in self.m.listeXY:
            if (x,y,0) not in MATERIAU.keys():
                self.message_alerte("Attention, le revêtement n'a pas été renseigné partout")
                break
        self.definir_couleur5()
        self.m.reinit_couleur()
        self.forget_souspar()
        self.sousparPaned.add(self.resultatsPaned)
        self.listes_Simu.append(Simulation(self))
    def faireTare(self):
        global FONCTION_ACTUELLE
        self.fonctionTare = FONCTION_ACTUELLE
        for i in self.m.liste_maillage:
            x,y=i.x,i.y
            self.tare[(x,y)] = FONCTION_ACTUELLE(x,y,0)
    def calcule_tare(self):
        global FONCTION_ACTUELLE
        if self.fonctionTare == FONCTION_ACTUELLE:
            H = FONCTION_ACTUELLE
            def f(x,y,z=0):
                return H(x,y,z) - self.tare[(x,y)]
            FONCTION_ACTUELLE = f
    def reinitialiser_tare(self):
        global FONCTION_ACTUELLE
        FONCTION_ACTUELLE = RAFRAICHISSEMENT
        self.fonctionTare = None
    def ajout_materiau_Base(self):
        global BASE_DE_DONNEES, NOM_PARAM
        l=[]
        texte_fin = 'Ajout du matériau\n'
        for i in NOM_PARAM:
            if i =='FONCTION_SELECTION':
            
                def fct_None():
                    INTERFACE.select_materiau = valeur
                l.append(fct_None)
            else:
                try:
                    l.append(float(self.ENT_MAT[i].get()))
                except:
                    l.append(self.ENT_MAT[i].get())
            texte_fin+=('\n{0} : {1}'.format(i, l[-1]))
        i=l
        self.paned_mat.add(Button(self,command = i[4],fg=i[3], bg=couleur_luminosite_complementaire(i[3]),text="{0} \n Alb={1} \n Diffu={2}m²/s, Cond={3}W/m.K, Dens={4}kg/m^3 \n Por={5}%, Perm={6} Evap={7}mm/jour".format(i[0],i[1],i[2],i[5],i[6],i[7],i[8],i[9])))
        BASE_DE_DONNEES.append(l)
        self.message_texte(texte_fin)
    def appliquer_temperature(self, temperature = None):
        
        if temperature == None:
            temperature = (self.entree_temperature.get())
        if self.select_case[0] != None:
            x,y = self.select_case[0]
            z = 0
            TEMP_VALEUR[(x,y,z)] = temperature
        if self.select_case[1] != None:
            x0,y0 = self.select_case[0]
            x1,y1 = self.select_case[1]
            z = 0
            for x in range(min(int(x0),int(x1)),max(int(x0),int(x1))+1):
                for y in range(min(int(y0),int(y1)),max(int(y0),int(y1))+1):        
                    TEMP_VALEUR[(x,y,z)] = temperature
        TEMPERATURE_MAX(0,0,0,True)
        FONCTION_ACT(0,0,0, True, True)
    def ajout_batiment(self,c0=None,d0 = None, z0 = None, c1 = None, d1 = None, z1 = None,couleur = None, h = None):
        if c0 == None:
            c0,c1 = min([self.select_case[0][0],self.select_case[1][0]]), max([self.select_case[0][0],self.select_case[1][0]])+1
            d0,d1 = min([self.select_case[0][1],self.select_case[1][1]]),max([self.select_case[0][1],self.select_case[1][1]])+1
            z0 = 0
        if couleur == None:
            couleur = self.entree_couleur_bat.get()
        x0,y0 = int(c0), int(d0)
        x1,y1 = int(c1), int(d1)
        if h == None:
            h = float(self.entree_hauteur_bat.get())
        if z1 == None:
            z1 = h
        in_bat = False
        for (x,y,z) in Batiment.bat.keys():
            in_bat = in_bat or (min(x0,x1)<= x <= max(x0,x1) and min(y0,y1) <= y <= max(y0,y1) and min(z0,z1)<= z <= max(z0,z1))
            if in_bat:
                break
        battt = Batiment(c0,d0,0,c1,d1,h, couleur)
        z1/= INTERFACE.taille_maillage_reel
        self.liste_batiments.append(battt)
        self.ecranCanvas.create_parallelepipede(c0,d0,z0,c1,d1,z1,fill = couleur,batiment = True)
        for x in range(min(int(x0),int(x1)),max(int(x0),int(x1))+1):
            for y in range(min(int(y0),int(y1)),max(int(y0),int(y1))+1):
                for z in range(min(int(z0),int(z1)),max(int(z0),int(z1))+1):
                    Batiment.bat[(x,y,z)] = battt
        self.m.reinit_couleur()
    def ajout_arbre_select(self):
        for i in BASE_DE_DONNEES_VEGE:
            if i[0]==self.select_vege:
                g = {}
                for j in range(len(i)):
                    g[NOM_PARAM_VEGE[j]] = i[j]    
                self.ajout_arbre(float(self.coord[0]), float(self.coord[1]),0,g['KET'],g['TEMPERATURE'],g['HUMIDITE'],g['HAUTEUR'],g['RAYON'])
    def ajout_arbre(self,x=None,y=None,z=None,KET=None,Tair=None,HR=None,h=None,R=None):
        FONCTION_ACT(0,0,0,True,True)
        if self.select_case[1] == None or R != None:
            if R ==None:
                x,y = float(self.coord[0]),float(self.coord[1])
                KET = (self.entree_KET.get())
                z=0
                HR = self.entree_HR.get()
                Tair = self.entree_Temp.get()
                h = float(self.entree_hauteur.get())
                R = float(self.entree_rayon.get())
            x,y = floor(x),floor(y)
            if (x,y,z) not in Arbre.arbre.keys():
                self.liste_arbres.append(Arbre(x,y,z,KET,Tair,HR,h,R))
                #Graphisme 
                R /= INTERFACE.taille_maillage_reel
                h /= INTERFACE.taille_maillage_reel
                r=R/5 #☺rayon tronc
                a=self.ecranCanvas.create_parallelepipede(x+0.5-r,y+0.5-r,z,x+0.5+r,y+0.5+r,z+h*0.5, '#6d5d4c', arbre =True)
                b=self.ecranCanvas.create_parallelepipede(x+0.5-R,y+0.5-R,z+h*0.5,x+0.5+R,y+0.5+R,z+h*1, '#459870', arbre = True)
                Arbre.arbre[(x,y,z)].liste_dessin = a+b
        else:
            z=0
            for x in range(self.select_case[0][0], self.select_case[1][0]+1):
                for y in range(self.select_case[0][1], self.select_case[1][1]+1):
                    KET = (self.entree_KET.get())
                    HR = self.entree_HR.get()
                    Tair = self.entree_Temp.get()
                    h = float(self.entree_hauteur.get())
                    R = float(self.entree_rayon.get())
                    if (x,y,z) not in Arbre.arbre.keys():
                        self.liste_arbres.append(Arbre(x,y,z,KET,Tair,HR,h,R))
                        #Graphisme 
                        R /= INTERFACE.taille_maillage_reel
                        h /= INTERFACE.taille_maillage_reel
                        r=R/5 #☺rayon tronc
                        a=self.ecranCanvas.create_parallelepipede(x+0.5-r,y+0.5-r,z,x+0.5+r,y+0.5+r,z+h*0.5, '#6d5d4c', arbre =True)
                        b=self.ecranCanvas.create_parallelepipede(x+0.5-R,y+0.5-R,z+h*0.5,x+0.5+R,y+0.5+R,z+h*1, '#459870', arbre = True)
                        Arbre.arbre[(x,y,z)].liste_dessin = a+b
        self.m.reinit_couleur()
    def ajout_eau(self,x=None,y=None,z=None,S=None):
        if self.select_case[1] == None or S != None:
            if S ==None:
                x,y = floor(self.coord[0]),floor(self.coord[1])
                t = TEMPS_ABSOLU
                z = 0
                S = eval(self.entree_Eau.get())
            Surface_d_eau.surface[(x,y,z)] = S
            TEMP_VALEUR_EAU[(x,y,z)] = (self.entree_T_eau.get())
        else:
            z=0
            for x in range(self.select_case[0][0], self.select_case[1][0]+1):
                for y in range(self.select_case[0][1], self.select_case[1][1]+1): 
                    S = eval(self.entree_Eau.get())
                    try:
                        Surface_d_eau.surface[(x,y,z)] = S
                        TEMP_VALEUR_EAU[(x,y,z)] = (self.entree_T_eau.get())
                    except KeyError:
                        pass
        self.m.reinit_couleur()
        FONCTION_ACT(0,0,0,True,True)
        self.message_texte("L'eau a bien été ajouté sur la sélection.")
    def suppr_arbre(self):
        x,y = floor(self.coord[0]),floor(self.coord[1])
        
        z=0
        if (x,y,z) in Arbre.arbre.keys():
            for i in Arbre.arbre[(x,y,z)].liste_dessin:
                self.ecranCanvas.supprimer_id(i)
            self.liste_arbres.remove(Arbre.arbre[(x,y,z)])
            del Arbre.arbre[(x,y,z)]
    def actualiser_temps(self):
        FONCTION_ACT(0,0,0,True,True)
        self.calculer_ombrage(message=False)
        self.texte_temps.config(text='{0}h{1}'.format(TEMPS_ABSOLU//(3600),(TEMPS_ABSOLU%3600)//60))
        self.texte_temps_bis.config(text='{0}h{1}'.format(TEMPS_ABSOLU//(3600),(TEMPS_ABSOLU%3600)//60))

        self.ecranCanvas.clic()
    def _after_fenetre(self):
        global TEMPS_ABSOLU
        
        if self.save_time_scale != TEMPS_ABSOLU:
            self.actualiser_temps()
        self.save_time_scale = TEMPS_ABSOLU
        self.timing_note[0] = round(time.time()-self.timing_prenote[0],3) 
        self.timing_prenote[0] = time.time()
        x,y,z = floor(self.coord[0]),floor(self.coord[1]),0
        self.label_position_vegetalisation.config(anchor="w", text="Position de l'arbre sélectionné : {0},{1}".format(x,y))
        if not (x,y,z) in Arbre.arbre.keys():
            self.label_position_vegeta.config(anchor="w", text="")
        else:
            self.label_position_vegeta.config(anchor="w", text="{0}".format(str(Arbre.arbre[(x,y,z)])))
        #self.labelResultats.config(anchor='w',text = "Résultats de la simulation : \n\tRafraîchissement : {1}\n\tÉvapotranspiration : {0}mm/jour".format(EVAPOTRANSPIRATION(x,y,z), RAFRAICHISSEMENT(x,y,z)))
        #boutonSTOP
        
        k = len(self.EchelleCanvasCouleur)
        for i in range(k) :
            j = self.EchelleCanvasCouleur[i]
            try:
                self.canvasEchelle.itemconfig(j, fill=ECHELLE_COULEUR(i/(k-1)))
            except:
                pass
        try:
            self.canvasEchelle.itemconfig(self.texteVmax, text=str(self.VMAX))
            self.canvasEchelle.itemconfig(self.texteVmin, text=str(self.VMIN))
        except AttributeError:
            pass
        
        if self.select_case[1] == None or self.select_case[0] == self.select_case[1]:
            self.canvasSelectionInfo.itemconfig(self.txtSelect, text = "Sélection [Maillage : {0},{1},{2}] [Métriques : {3}m,{4}m,{5}m]".format(x,y,z,x*self.taille_maillage_reel,y*self.taille_maillage_reel, z*self.taille_maillage_reel))
            self.canvasSelectionInfo.itemconfig(self.txtValueSelect, text = "{0}({1},{2},{3}) = {4}, TEMPERATURE_CELSIUS({1},{2},{3}) = {5}°C".format(FONCTION_ACTUELLE.__name__,x,y,z,FONCTION_ACTUELLE(x,y,z), TEMPERATURE_CELSIUS(x,y,z)))
            self.canvasSelectionInfo.itemconfig(self.txtTemps, text = str(self.timing_note))
        else:
            x1,y1 = self.select_case[1]
            x0,y0 = self.select_case[0]
            z1 = 0
            z0 = 0
            self.canvasSelectionInfo.itemconfig(self.txtSelect, text = "Sélection [Maillage : {0},{1},{2} jusqu'à {3},{4},{5}] [Métriques : {6}m,{7}m,{8}m jusqu'à {9}m,{10}m,{11}m] ({12}m*{13}m)".format(x0,y0,z0,x1,y1,z1, x0*self.taille_maillage_reel, y0*self.taille_maillage_reel, z0*self.taille_maillage_reel, x1*self.taille_maillage_reel, y1*self.taille_maillage_reel, z1*self.taille_maillage_reel,abs(x0-x1)*self.taille_maillage_reel,abs(y0-y1)*self.taille_maillage_reel))

        self.canvasEchelle.itemconfig(self.textefonction, text=str(FONCTION_ACTUELLE.__name__))
        self.canvasEchelle.itemconfig(self.texteFonctionDescription, text=self.get_description(FONCTION_ACTUELLE))

        if FONCTION_ACTUELLE.__name__ != "RESULTATS_SIMU":
            txt = "Lancer la simulation \n avec la fonction {0} \n et le mode {1}".format(FONCTION_ACTUELLE.__name__, self.mode_simu)
        else:
            txt = "Redéfinir une mesure avant de relancer la simulation"
        if self.bouton_simu['text'] != txt:
            self.bouton_simu['text'] = txt
        
        ROUGE = '#fe9797'
        VERT = '#a3e4d7'
        if self.mode_simu == "MOYENNE" and self.bouton_SIMU_MOYENNE['bg'] != VERT:
            self.bouton_SIMU_MOYENNE['bg'] = VERT
        elif self.mode_simu != "MOYENNE" and self.bouton_SIMU_MOYENNE['bg'] != ROUGE:
            self.bouton_SIMU_MOYENNE['bg'] = ROUGE
        #boutonTare
        if self.fonctionTare == None:
            if self.boutonTare['bg'] != VERT:
                self.boutonTare['bg'] = VERT
                self.boutonCalculeTare['bg'] = ROUGE
                self.boutonReinitTare['bg'] = ROUGE
        elif self.fonctionTare == FONCTION_ACTUELLE:
            if self.boutonTare['bg'] != ROUGE:
                self.boutonTare['bg'] = ROUGE
                self.boutonCalculeTare['bg'] = VERT
                self.boutonReinitTare['bg'] = VERT
        else:
            if self.boutonTare['bg'] != VERT:
                self.boutonTare['bg'] = VERT
                self.boutonCalculeTare['bg'] = ROUGE
                self.boutonReinitTare['bg'] = VERT
        
        if not self.block_interface:
            self.after(5,self._after_fenetre)
    def calculer_ombrage(self, vec=None, message=True):
        global OMBRAGE, TEMPS_ABSOLU
        t = TEMPS_ABSOLU
    
        if vec is None:
            xombr, yombr, zombr = eval(self.entree_Irradiance.get())
        else:
            xombr, yombr, zombr = vec
    
        for (x, y) in self.m.listeXY:
            OMBRAGE[(x, y, 0)] = 0 if zombr > 0 else 1
    
        if zombr <= 0:
            return None
    
        def update_ombrage(L, taillex, tailley, ombre_value):
            x0 = min(L[0][0], L[0][2])
            x1 = min(L[1][0], L[1][2])
            y0 = min(L[0][1], L[0][3])
            y1 = min(L[1][1], L[1][3])
            already_in = set()
            if not L[0][3] >= L[1][3] and L[0][2] >= L[1][2]:
                x0,x1 = x1,x0
                y0,y1 = y1,y0
            if not L[0][3] >= L[1][3] and not L[0][2] >= L[1][2]:
                pass
                
            if L[0][2] >= L[1][2] and L[0][3] >= L[1][3] or x0 == x1 or y0 == y1:
                x0,x1 = min(x0,x1),max(x0,x1)
                y0,y1 = min(y0,y1),max(y0,y1)
    
            for i in range(x0, x1):
                for k0 in range(taillex + 1):
                    for k1 in range(tailley + 1):
                        j = y0 + (i - x0) * (y1 - y0) // (x1 - x0) + k1
                        if (i+k0,j,0) not in already_in:    
                            already_in.add((i+k0,j,0))
                            if (i+k0,j,0) in OMBRAGE.keys() :
                                if OMBRAGE[(i+k0,j,0)] == 0:
                                    OMBRAGE[(i + k0, j, 0)] = ombre_value
                                else :
                                    OMBRAGE[(i+k0,j,0)] = 1 - (1-OMBRAGE[(i+k0,j,0)])*(1-ombre_value)
                        
        for bat in self.liste_batiments:
            L = []
            for z in [bat.z0 / self.taille_maillage_reel, bat.z1 / self.taille_maillage_reel]:
                newx = [x - xombr * z / zombr for x in [bat.x0, bat.x1]]
                newy = [y - yombr * z / zombr for y in [bat.y0, bat.y1]]
                newx0, newx1 = floor(newx[0]), floor(newx[1])
                newy0, newy1 = floor(newy[0]), floor(newy[1])
                L.append([newx0, newy0, newx1, newy1])
                taillex = abs(newx1 - newx0)
                tailley = abs(newy1 - newy0)
    
                #for i in range(min(newx0, newx1), max(newx0, newx1)):
                    #for j in range(min(newy0, newy1), max(newy0, newy1)):
                        #OMBRAGE[(i, j, 0)] = 1-OMBRAGE_BATIMENT
    
            update_ombrage(L, taillex, tailley, 1-OMBRAGE_BATIMENT)
    
        for arbre in self.liste_arbres:
            L = []
            Z0, Z1 = 0, arbre.h / self.taille_maillage_reel
            X0, X1 = arbre.x - arbre.R / self.taille_maillage_reel, arbre.x + arbre.R / self.taille_maillage_reel
            Y0, Y1 = arbre.y - arbre.R / self.taille_maillage_reel, arbre.y + arbre.R / self.taille_maillage_reel
            already_in = set()
            for z in [Z0, Z1]:
                newx = [x - xombr * z / zombr for x in [X0, X1]]
                newy = [y - yombr * z / zombr for y in [Y0, Y1]]
                newx0, newx1 = floor(newx[0]), floor(newx[1])
                newy0, newy1 = floor(newy[0]), floor(newy[1])
                L.append([newx0, newy0, newx1, newy1])
                taillex = abs(newx1 - newx0)
                tailley = abs(newy1 - newy0)
    
                for i in range(min(newx0, newx1), max(newx0, newx1) + 1):
                    for j in range(min(newy0, newy1), max(newy0, newy1) + 1):
                        if (i, j, 0) not in already_in:
                            #OMBRAGE[(i, j, 0)] = 0.3 #max(OMBRAGE.get((i, j, 0), 0) * (1 + Arbre.TAUX_OMBRE), 1)
                            #already_in.add((i, j, 0))
                            pass
    
            update_ombrage(L, taillex, tailley, 1-Arbre.TAUX_OMBRE)
    
        self.ecranCanvas.clic()
        if message:
            FONCTION_ACT(0, 0, 0, True, True)
            messagebox.showinfo("Information", "Le calcul de l'ombre est terminé")
    def message_texte(self,texte):
        messagebox.showinfo("Information", texte)
    def message_alerte(self,texte):
        messagebox.showwarning("Attention", texte)
    def message_erreur(self,texte):
        messagebox.showerror("Erreur", texte)
    def appliquer_irradiance(self):
        global IRR_SOL, OMBRAGE_BATIMENT
        m = float(self.entree_IrradianceOmbreBatiment.get())
        if m<0 or m>1:
            self.message_erreur('La valeur d\'ombrage pour les bâtiments n\'est pas correcte.')
        else:
            OMBRAGE_BATIMENT = m
        IRR_SOL = (self.entree_IrradianceSol.get())
    def appliquer_albedo(self):
        al = self.select_materiau
        if self.select_case[0] != None:
            x,y = self.select_case[0]
            self.m.set_albedo(int(x),int(y),al)
        if self.select_case[1] != None:
            x0,y0 = self.select_case[0]
            x1,y1 = self.select_case[1]
            for i in range(min(int(x0),int(x1)),max(int(x0),int(x1))+1):
                for j in range(min(int(y0),int(y1)),max(int(y0),int(y1))+1):
                    self.m.set_albedo(i,j,al)
    def appliquer_materiau(self):
        al = self.select_materiau
        print(al)
        if self.select_materiau == None:
            return None
        if self.select_case[0] != None:
            x,y = self.select_case[0]
            self.m.set_albedo(int(x),int(y),al)
            MATERIAU[(x,y,0)] = al
        if self.select_case[1] != None:
            x0,y0 = self.select_case[0]
            x1,y1 = self.select_case[1]
            for i in range(min(int(x0),int(x1)),max(int(x0),int(x1))+1):
                for j in range(min(int(y0),int(y1)),max(int(y0),int(y1))+1):
                    self.m.set_albedo(int(i),int(j),al)
                    MATERIAU[(i,j,0)] = al
        FONCTION_ACT(0,0,0,True,True)
        self.message_texte("Le matériau {0} a été appliqué à la sélection.".format(al))
    def appliquer_hydrique(self):
        
        if self.select_case[0] != None:
            x,y = self.select_case[0]
            x,y = int(x),int(y)
            EVAPORATION_[(x,y,0)] = self.entree_Evaporation.get()
            AUTRE_ENTREE_EAU_[(x,y,0)] = self.entree_entreeEau.get()
            PRECIPITATION_[(x,y,0)] = self.entree_precipitations.get()
        if self.select_case[1] != None:
            x0,y0 = self.select_case[0]
            x1,y1 = self.select_case[1]
            for i in range(min(int(x0),int(x1)),max(int(x0),int(x1))+1):
                for j in range(min(int(y0),int(y1)),max(int(y0),int(y1))+1):  
                    EVAPORATION_[(i,j,0)] = self.entree_Evaporation.get()
                    AUTRE_ENTREE_EAU_[(i,j,0)] = self.entree_entreeEau.get()
                    PRECIPITATION_[(i,j,0)] = self.entree_precipitations.get()
        FONCTION_ACT(0,0,0,True,True)
        self.message_texte("Le bilan hydrique a été effectué.")
    
    def appliquer_albedo_bis(self):
        if self.select_case[0] != None:
            x,y = self.select_case[0]
            self.m.set_albedo(int(x),int(y),eval(self.entree_albedo_bis.get()))
            
        if self.select_case[1] != None:
            x0,y0 = self.select_case[0]
            x1,y1 = self.select_case[1]
            for i in range(min(int(x0),int(x1)),max(int(x0),int(x1))+1):
                for j in range(min(int(y0),int(y1)),max(int(y0),int(y1))+1):
                    x,y = i,j
                    self.m.set_albedo(i,j,eval(self.entree_albedo_bis.get()))
    def save_to_file(self, filename=None):
        global BASE_DE_DONNEES, MATERIAU, BASE_DE_DONNEES_VEGE
        if filename == None:
            filename = INTERFACE.entree_save.get()
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write('[\'format\',[{0},{1},{2}]]\n'.format(str(self.M),str(self.N),str(self.taille_maillage_reel)))

                for i in Arbre.arbre:
                    file.write('[{0},{1}] \n'.format("'arbre'",[Arbre.arbre[i].x,Arbre.arbre[i].y,Arbre.arbre[i].z,Arbre.arbre[i].KET,Arbre.arbre[i].Tair,Arbre.arbre[i].HR,Arbre.arbre[i].h,Arbre.arbre[i].R]))
                for i in Batiment.liste_Batiment:
                    file.write('[{0},{1}] \n'.format("'batiment'",i))                    
                BASE_DE_DONNEES_ADAPTEE = []
                for i in BASE_DE_DONNEES:
                    j = i.copy()
                    j[4] = None
                    BASE_DE_DONNEES_ADAPTEE.append(j)
                file.write('[{0},{1}] \n'.format("'BD'",BASE_DE_DONNEES_ADAPTEE))                    
                BASE_DE_DONNEES_ADAPTEE_VEGE = []
                for i in BASE_DE_DONNEES_VEGE:
                    j = i.copy()
                    j[4] = None
                    BASE_DE_DONNEES_ADAPTEE_VEGE.append(j)
                file.write('[{0},{1}] \n'.format("'BDV'",BASE_DE_DONNEES_ADAPTEE_VEGE))                    
                file.write('[{0},{1}] \n'.format("'MAT'",MATERIAU))                    
            self.message_texte('Le fichier a bien été sauvegardé dans {0}'.format(filename))
        except Exception as e:
            self.message_erreur('Une erreur est survenue lors de la sauvegarde : {0}'.format(e))
    def save_open(self):
        t = self.taille_maillage_reel
        N=self.N
        M=self.M
        Interface(N,M,t, INTERFACE.entree_save.get(), to_destroy = self)
        
    def load_save(self,text):
        global LISTE_PARAMETRES, BASE_DE_DONNEES, MATERIAU, BASE_DE_DONNEES_VEGE
        LISTE_PARAMETRES = [("KET",30)]
        BASE_DE_DONNEES = []
        MATERIAU = {}
        print('\nLoad de la save')
        with open(text, "r", encoding="utf-8") as fichier:
            for lg in fichier:
                ligne = lg.strip()
                lst = eval(ligne)
                print(lst)
                if lst[0] == 'arbre':
                    par = lst[1]
                    self.ajout_arbre(*par)
                if lst[0] == 'batiment':
                    par = lst[1]
                    self.ajout_batiment(*par)
                if lst[0] == 'BD':
                    base_a_traiter = lst[1]
                    bs = []
                    print('Chargement de la base de donnée')
                    for i in base_a_traiter:
                        print(i)
                        j = i.copy()
                        if j[4]==None:
                            valeur = j[0]
                            j[4] = lambda valeur=valeur: (
            print('Nouveau matériau ', valeur),
            setattr(INTERFACE, 'select_materiau', valeur)
        )
                        else:
                            try:
                                j[4] = eval(j[4])
                            except:
                                pass
                        bs.append(j)
                    BASE_DE_DONNEES = bs
                    for i in BASE_DE_DONNEES:
                        self.paned_mat.add(Button(self,command = i[4],fg=i[3], bg=couleur_luminosite_complementaire(i[3]),text="{0} \n Alb={1} \n Diffu={2}m²/s, Cond={3}W/m.K, Dens={4}kg/m^3 \n Por={5}%, Perm={6} Evap={7}mm/jour".format(i[0],i[1],i[2],i[5],i[6],i[7],i[8],i[9])))
                if lst[0] == 'BDV':
                    base_a_traiter = lst[1]
                    bs = []
                    for i in base_a_traiter:
                        j = i.copy()
                        if j[4]==None:
                            j[4] = lambda valeur=valeur: (
            print('Nouvelle végétation ', valeur),
            setattr(INTERFACE, 'select_vege', valeur)
        )
                        else:
                            j[4] = eval(j[4])
                        bs.append(j)
                    BASE_DE_DONNEES_VEGE = bs
                    for i in BASE_DE_DONNEES_VEGE:
                        self.paned_VEGEbd.add(Button(self,command=i[4],fg=i[7],bg=couleur_luminosite_complementaire(i[7]),text="{0} \n KET={1}mm/jour \n h={2}m, R={3}m \n Tair={4}K \nHR={5}".format(i[0],i[1],i[2],i[3],i[5],i[6])))
                if lst[0] == 'MAT':
                    MATERIAU = lst[1]
        print('\nBase de données après chargement : ')
        print(BASE_DE_DONNEES)

def is_point_in_polygon(point, polygon):
    """Vérifie si un point est dans un polygone (convexe ou concave)."""
    x, y = point
    n = len(polygon)
    inside = False

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        # Vérifie si le point est dans la bande verticale de l'arête
        if min(y1, y2) < y <= max(y1, y2) and x <= max(x1, x2):
            # Calcule l'intersection de l'arête avec la ligne horizontale passant par le point
            if y1 != y2:  # Pas d'arête horizontale
                xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
            if x1 == x2 or x <= xinters:  # Si l'intersection est à droite
                inside = not inside

    return inside

def cst_couleur(x,y):
    return 'grey'

def cst_couleur_cl(couleur):
    def cl(x,y):
        return couleur
    return cl

def couleur_albedo(r):
    _1 = hex(int(255*r))[2:]
    _2 = hex(int(255*r))[2:]
    _3 = hex(int(255*r))[2:]
    if len(_1) == 1:
        _1 = '0'+_1
    if len(_2) == 1:
        _2 = '0'+_2
    if len(_3) == 1:
        _3 = '0'+_3
    return '#{0}{1}{2}'.format(_1, _2, _3)

def couleur_ombre(r):
    valeur = max(0, min(1, r))
    r_froid, g_froid, b_froid = 50, 50, 50 
    r_chaud, g_chaud, b_chaud = 255, 255, 230 

    # Interpolation linéaire
    r = int(r_froid + (r_chaud - r_froid) * valeur)
    g = int(g_froid + (g_chaud - g_froid) * valeur)
    b = int(b_froid + (b_chaud - b_froid) * valeur)
    
    # Convertir en format hexadécimal
    return f"#{r:02x}{g:02x}{b:02x}"
    _1 = hex(int(255*r))[2:]
    _2 = hex(int(255*r))[2:]
    _3 = hex(int(255*r))[2:]
    if len(_1) == 1:
        _1 = '0'+_1
    if len(_2) == 1:
        _2 = '0'+_2
    if len(_3) == 1:
        _3 = '0'+_3
    return '#{0}{1}{2}'.format(_1, _2, _3)

def couleur_test(x,y=None):
    u = 1/(1+(x)**2)
    _1 = hex(int(255))[2:]
    _2 = hex(int(255*(1-u)))[2:]
    _3 = hex(int(255*u))[2:]
    if len(_1) !=2:
        _1 = '0'+_1
    if len(_2) != 2:
        _2 = '0'+_2
    if len(_3) !=2:
        _3 = '0'+_3
    return '#{0}{1}{2}'.format(_1, _2, _3)

def couleur_mat(x,y=None):
    return x

def valeur_vers_couleur(valeur):
    valeur = max(0, min(1, valeur))
    r_froid, g_froid, b_froid = 100, 0, 255 
    r_chaud, g_chaud, b_chaud = 255, 0, 100  

    # Interpolation linéaire
    r = int(r_froid + (r_chaud - r_froid) * valeur)
    g = int(g_froid + (g_chaud - g_froid) * valeur)
    b = int(b_froid + (b_chaud - b_froid) * valeur)
    
    # Convertir en format hexadécimal
    return f"#{r:02x}{g:02x}{b:02x}"

def violet_vers_bleu(valeur):
    valeur = max(0, min(1, valeur))
    r_froid, g_froid, b_froid = 157, 128, 229 
    r_chaud, g_chaud, b_chaud = 128, 211, 229  

    # Interpolation linéaire
    r = int(r_froid + (r_chaud - r_froid) * valeur)
    g = int(g_froid + (g_chaud - g_froid) * valeur)
    b = int(b_froid + (b_chaud - b_froid) * valeur)
    
    # Convertir en format hexadécimal
    return f"#{r:02x}{g:02x}{b:02x}"

def bleu_vers_vert(valeur):
    valeur = max(0, min(1, valeur))
    r_froid, g_froid, b_froid = 128, 211, 229
    r_chaud, g_chaud, b_chaud = 100, 243, 58  

    # Interpolation linéaire
    r = int(r_froid + (r_chaud - r_froid) * valeur)
    g = int(g_froid + (g_chaud - g_froid) * valeur)
    b = int(b_froid + (b_chaud - b_froid) * valeur)
    
    # Convertir en format hexadécimal
    return f"#{r:02x}{g:02x}{b:02x}"

def vert_vers_jaune(valeur):
    valeur = max(0, min(1, valeur))
    r_froid, g_froid, b_froid = 100, 243, 58 
    r_chaud, g_chaud, b_chaud = 243, 229, 58  

    # Interpolation linéaire
    r = int(r_froid + (r_chaud - r_froid) * valeur)
    g = int(g_froid + (g_chaud - g_froid) * valeur)
    b = int(b_froid + (b_chaud - b_froid) * valeur)
    
    # Convertir en format hexadécimal
    return f"#{r:02x}{g:02x}{b:02x}"



def jaune_vers_rouge(valeur):
    valeur = max(0, min(1, valeur))
    r_froid, g_froid, b_froid = 243, 229, 58 
    r_chaud, g_chaud, b_chaud = 242, 66, 38  

    # Interpolation linéaire
    r = int(r_froid + (r_chaud - r_froid) * valeur)
    g = int(g_froid + (g_chaud - g_froid) * valeur)
    b = int(b_froid + (b_chaud - b_froid) * valeur)
    
    # Convertir en format hexadécimal
    return f"#{r:02x}{g:02x}{b:02x}"

def couleur_longueur_onde(valeur):
    if valeur<0.1:
        return violet_vers_bleu(valeur/0.1)
    if valeur<0.5:
        return bleu_vers_vert((valeur-0.1)/(0.5-0.1))
    if valeur<0.6 :
        return vert_vers_jaune((valeur-0.5)/(0.6-0.5))
    return jaune_vers_rouge((valeur-0.6)/(1-0.6))

def couleur_longueur_onde_inv(valeur):
    return couleur_longueur_onde(1-valeur)


def ECHELLE_VEGE(valeur):
    valeur = max(0, min(1, valeur))
    r_froid, g_froid, b_froid = 0, 100, 255 
    r_chaud, g_chaud, b_chaud = 0, 255, 100  

    # Interpolation linéaire
    r = int(r_froid + (r_chaud - r_froid) * valeur)
    g = int(g_froid + (g_chaud - g_froid) * valeur)
    b = int(b_froid + (b_chaud - b_froid) * valeur)
    
    # Convertir en format hexadécimal
    return f"#{r:02x}{g:02x}{b:02x}"

def ECHELLE_EAU(valeur):
    valeur = max(0, min(1, valeur))
    r_froid, g_froid, b_froid = 168, 166, 163 
    r_chaud, g_chaud, b_chaud = 115, 111, 255  

    # Interpolation linéaire
    r = int(r_froid + (r_chaud - r_froid) * valeur)
    g = int(g_froid + (g_chaud - g_froid) * valeur)
    b = int(b_froid + (b_chaud - b_froid) * valeur)
    
    # Convertir en format hexadécimal
    return f"#{r:02x}{g:02x}{b:02x}"

def MATERIAU_COULEUR(x,y,z=0):
    if (x,y,z) in MATERIAU.keys():
        mat = MATERIAU[(x,y,z)]
        for i in BASE_DE_DONNEES:
            if i[0] == mat:
                return i[3]
    return '#FF0000'

def PRESSION(x,y,z=None):
    return 1013*10**5

def RAFRAICHISSEMENT(x,y,z=0):
    return RAFRAICHISSEMENT1(x,y,z) - RAFRAICHISSEMENT2(x,y,z)

def RAFRAICHISSEMENT_INERTIE(x,y,z=0):
    return eval(INTERFACE.entree_Rafraichissement_Inertie.get())

def RAFRAICHISSEMENT_SOUSSOL(x,y,z=0):
    return eval(INTERFACE.entree_Rafraichissement_SousSol.get())

def RAFRAICHISSEMENT_DIFFUSION(x,y,z=0):
    return eval(INTERFACE.entree_Rafraichissement_Diff.get())

def RAFRAICHISSEMENT_EVAPO(x,y,z=0):
    return eval(INTERFACE.entree_Rafraichissement_evapo.get())

def RAFRAICHISSEMENT1(x,y,z=0):
    r = 0
    for i in INTERFACE.liste_entree_rafraichissement:
        try:
            r += eval(i.get())
        except Exception as e:
            pass
    return r

def RAFRAICHISSEMENT2(x,y,z=0):
    r = 0
    for i in INTERFACE.liste_entree_rechauffement:
        try:
            r += eval(i.get())
        except Exception as e:
            pass
    return r

def RECHAUFFEMENT(x,y,z=0):
    return -RAFRAICHISSEMENT(x,y,z)

def DENSITE_AIR():
    return 1.2 

def cp_AIR(temperature = 25):
    if temperature == 25:
        return 1005
    
def cp_eau(temperature = 25):
    '1005 J/kg·K'
    return 1005
    
def L_Vap_air(temperature = 25,y=None,z=None):
    return 2.45 *10**6

def L_Vap_eau(temperature = 25,y=None,z=None):
    return 2.5 *10**6

PAR_save_nom_x_y_z = {}
PAR_save_materiau = None

def PARAMETRE(nom,x,y,z):
    global PAR_save_nom_x_y_z, PAR_save_materiau, MATERIAU
    if (nom,x,y,z) in PAR_save_nom_x_y_z.keys():
        if PAR_save_materiau != MATERIAU:
            PAR_save_materiau = MATERIAU
            PAR_save_nom_x_y_z = {}
        else:
            return PAR_save_nom_x_y_z[(nom,x,y,z)]
    elif PAR_save_materiau != MATERIAU and PAR_save_nom_x_y_z == {}:
        PAR_save_materiau = MATERIAU
    indicek = 0
    for i in NOM_PARAM:
        if i == nom:
            break
        indicek += 1
    if (x,y,z) in MATERIAU.keys():
        for j in BASE_DE_DONNEES:
            if j[0]==MATERIAU[(x,y,z)]:
                PAR_save_nom_x_y_z[(nom,x,y,z)] = j[indicek]
                return j[indicek]
    return 0

def RESULTATS_SIMU(x,y,z=0):
    if (x,y,z) in RESULTATS_SIMULATION.keys():
        return RESULTATS_SIMULATION[(x,y,z)]
    return 0

def DIFFUSIVITE_THERMIQUE(x,y,z=0):
    return PARAMETRE('DIFFUSIVITE_THERMIQUE',x,y,z)

def CONDUCTIVITE_THERMIQUE(x,y,z=0):
    return PARAMETRE('CONDUCTIVITE_THERMIQUE',x,y,z)

def EMISSIVITE_THERMIQUE(x,y,z=0):
    return PARAMETRE('CONDUCTIVITE_THERMIQUE',x,y,z)

def POROSITE(x,y,z=0):
    return PARAMETRE('POROSITE',x,y,z)

def PERMEABILITE(x,y,z=0):
    return PARAMETRE('PERMEABILITE',x,y,z)

def FACTEUR_RUGOSITE_SURFACE(x,y,z=0):
    try:
        return PARAMETRE('FACTEUR_RUGOSITE_SURFACE',x,y,z)
    except:
        return 1

def MASSE_VOLUMIQUE(x,y,z=0):
    return PARAMETRE('MASSE_VOLUMIQUE',x,y,z)

def MASSE_VOLUMIQUE_EAU():
    return 1000

def IRRADIANCE_OMBRAGE(x,y,z=0):
    return IRRADIANCE(x,y,z)*(1-OMBRE(x,y,z))

def EVAPOTRANSPIRATION_MATERIAU(x,y,z=0):
    return PARAMETRE('EVAPOTRANSPIRATION',x,y,z)

def EVAPOTRANSPIRATION_LITRE(x,y,z):
    return EVAPOTRANSPIRATION(x,y,z)*SURFACE_MAILLE(x,y,z)

def COEFF_TRANSFERT(x,y,z=0):
    return 1

def HUMIDITE(x,y,z=0,t=None):
    
    if t == None:
        t = TEMPS_ABSOLU
    if (x,y,z) in HR_VALEUR.keys():
        return HR_VALEUR[(x,y,z)]
    HR_VALEUR[(x,y,z)] = 10
    return 10

fc = 0.1
fceff = 0.4

hrmin_save = {}
def HUMIDITE_RELATIVE_MIN(x,y,z=0):
    return 10
    global TEMPS_ABSOLU,  hrmin_save
    if (x,y,z) in HR_VALEUR.keys() and (x,y,z,HR_VALEUR[(x,y,z)]) in hrmin_save.keys():
        return hrmin_save[(x,y,z,HR_VALEUR[(x,y,z)])]
    
    tactu = TEMPS_ABSOLU
    hrmin = math.inf
    hrmin = min([HUMIDITE_RELATIVE(x,y,z,t) for t in range(24*3600)])
    hrmin_save[(x,y,z,HR_VALEUR[x,y,z])] = hrmin
    TEMPS_ABSOLU = tactu
    return hrmin
    
def HUMIDITE_RELATIVE(x,y,z=0,t=None):
    
    return HUMIDITE(x,y,z,t)

def ECHELLE_COULEUR(r):
    return 'grey'

def REDUCTION(v,vMax,vMin):
    return (v-vMin)/(vMax-vMin)

def gamma(x,y,z=0):
    return 0.665*10**-3*PRESSION(x,y,z)

def EVAPOTRANSPIRATION(x,y,z=0):
    evapotranspi = 0 
    #Apport par les arbres 
    for i in INTERFACE.liste_arbres:
        Tair = eval(i.Tair)
        HR = eval(i.HR)
        R = i.R
        h = i.h
        r = ((x-i.x)**2 + (y-i.y)**2 + (z-i.z)**2)**0.5 #taille en pixels
        r *= INTERFACE.taille_maillage_reel
        Kcbfull = eval(INTERFACE.entree_Kcbfull.get())
        KET = eval(i.KET)
        Kcbmid = eval(i.KET)
        PORTEE = eval(INTERFACE.entree_Formule_portee.get())
        pass
        FORMULE = INTERFACE.entree_Formule_eva.get()
        FORMULE = eval(FORMULE)
        evapotranspi += FORMULE*PORTEE
    evapotranspi+=eval(INTERFACE.entree_Formule_eva_mat.get())
    evapotranspi+=eval(INTERFACE.entree_Formule_eva_eau.get())
    #Apport par l'eau
    return evapotranspi

def ALBEDO(x,y,z=0):
    try:
        return PARAMETRE('ALBEDO',x,y,z)
    except:
        pass
    return 0

def gamma(x,y,z=0):
    return 0

def ABSORPTIVITE(x,y,z=0):
    return 1-ALBEDO(x,y,z)


def ARBRE(x,y,z=0):
    value = 0
    for i in INTERFACE.liste_arbres:
        h = i.h
        #value += h*exp(-((x-i.x)**2 + (y-i.y)**2)**0.5)
        Kcbfull = eval(INTERFACE.entree_Kcbfull.get())
        KET = eval(i.KET)
        value += KET*exp(-((x-i.x)**2 + (y-i.y)**2)**0.5)
    return value

def SURFACE_MAILLE(x,y,z=0):
    return INTERFACE.taille_maillage_reel**2

def IRRADIANCE(x,y,z=0):
    t = TEMPS_ABSOLU
    return eval(IRR_SOL)

def PUISSANCE_ABSORBEE(x,y,z=0):
    return eval(INTERFACE.formulePuissance[0])
def PUISSANCE_REFLECHIE(x,y,z=0):
    return IRRADIANCE_OMBRAGE(x,y,z)*SURFACE_MAILLE(x,y,z)-PUISSANCE_ABSORBEE(x,y,z)
def SOMME_PUISSANCE(x,y,z=0):
    return eval(INTERFACE.formulePuissance[4])
def PUISSANCE_RAYONNEMENT_THERMIQUE(x,y,z=0):
    return eval(INTERFACE.formulePuissance[1])

def PUISSANCE_CONDUCTION(x,y,z=0):
    return eval(INTERFACE.formulePuissance[3])


def PUISSANCE_CONDUCTION_AIR(x,y,z=0):
    return 0

def PUISSANCE_EVAPOTRANSPIRATION(x,y,z=0):
    return eval(INTERFACE.formulePuissance[7])

FORMULE_H = "10"

def h_COEFF(x,y,z=0):
    global FORMULE_H
    return eval(FORMULE_H)

def PUISSANCE_CONVECTION(x,y,z=0):
    return eval(INTERFACE.formulePuissance[2])
    return h_COEFF(x,y,z)*SURFACE_MAILLE(x,y,z)*(-TEMPERATURE_MATERIAU(x,y,z)+TEMPERATURE(x,y,z))

def PUISSANCE_STOCKEE(x,y,z=0):
    return 0

PROFONDEUR_SOUSSOL = 10
def PUISSANCE_SOUSSOL(x,y,z=0):
    return 0 

PUISSANCE_ECHANGE = {}

def calcule_puissance_echange():
    z=0
    e = INTERFACE.taille_maillage_reel//2
    S = INTERFACE.taille_maillage_reel*PROFONDEUR_SOUSSOL
    for x,y in INTERFACE.m.listeXY:
        try:
            R1 = e/(CONDUCTIVITE_THERMIQUE(x,y,z)*S)
            R2 = e/(CONDUCTIVITE_THERMIQUE(x+1,y,z)*S)
            R3 = e/(CONDUCTIVITE_THERMIQUE(x,y+1,z)*S)
            PUISSANCE_ECHANGE[(x,y,z,x+1,y,z)] = eval(INTERFACE.formulePuissance[5])
            PUISSANCE_ECHANGE[(x,y,z,x,y+1,z)] = eval(INTERFACE.formulePuissance[6]) #(TEMPERATURE(x,y,z)-TEMPERATURE(x,y+1,z))/(R1+R3)
            PUISSANCE_ECHANGE[(x+1,y,z,x,y,z)] = - PUISSANCE_ECHANGE[(x,y,z,x+1,y,z)]
            PUISSANCE_ECHANGE[(x,y+1,z,x,y,z)] = - PUISSANCE_ECHANGE[(x,y,z,x,y+1,z)]
        except:
            pass
        
def ECHANGE_PUISSANCE_MAILLE(x,y,z=0):
    try:
        return sum([PUISSANCE_ECHANGE[(x,y,z,x+1,y,z)], PUISSANCE_ECHANGE[(x,y,z,x,y+1,z)],PUISSANCE_ECHANGE[(x,y,z,x,y-1,z)],PUISSANCE_ECHANGE[(x,y,z,x-1,y,z)]])
    except:
        return 0

def ECHANGE_PUISSANCE_MAILLE_(x,y,z,x0,y0,z0):
    try:
        return PUISSANCE_ECHANGE[(x,y,z,x0,y0,z0)]
    except:
        PUISSANCE_ECHANGE[(x,y,z,x0,y0,z0)] = 0
        return 0

def PRESSION_SATURATION_EAU(x,y,z=0):
    '''Utilise l'équation d'Antoine'''
    T = TEMPERATURE_CELSIUS(x,y,z)
    t = TEMPS_ABSOLU
    return eval(INTERFACE.entree_P_sat_eau.get())

def h_e(x,y,z=0):
    t = TEMPS_ABSOLU
    return eval(INTERFACE.entree_he_eau.get())

def h_c(x,y,z=0):
    t = TEMPS_ABSOLU
    return eval(INTERFACE.entree_hc_eau.get())

def cp(x,y,z=0):
    a = PARAMETRE('CP',x,y,z)
    #if a!=None:
     #   return a
    return CONDUCTIVITE_THERMIQUE(x,y,z)/(MASSE_VOLUMIQUE(x,y,z)*DIFFUSIVITE_THERMIQUE(x,y,z))

def OMBRE(x,y,z=0):
    if (x,y,z) in OMBRAGE.keys():
        return OMBRAGE[(x,y,z)]
    return 0

def SURFACE_EAU(x,y,z=0):
    try:
        return Surface_d_eau.surface[(x,y,z)]
    except KeyError:
        return 0
    
def SORTIE_EAU(x,y,z=0):
    return eval(INTERFACE.entree_SortieEau.get())

def TENEUR_EAU(x,y,z=0):
    return eval(INTERFACE.entree_Teneur.get())

VECTEUR_VENT_VALEUR = {}

def VECTEUR_VENT(x,y,z=0):
    global VECTEUR_VENT_VALEUR
    try:
        return eval(VECTEUR_VENT_VALEUR[(x,y,z)])
    except:
        pass
    VECTEUR_VENT_VALEUR[(x,y,z)] = '(0,0,0)'
    return (0,0,0)

def VENT(x,y,z=0):
    v = VECTEUR_VENT(x,y,z)
    return (v[0]**2 + v[1]**2 + v[2]**2)**0.5

def tvps_ew(x,y,z=0):
    return (tvps_e(x,y,z,TEMPERATURE_MAX_CELSIUS(x,y,z)) + tvps_e(x,y,z,TEMPERATURE_MIN_CELSIUS(x,y,z)))/2

def tvps_e(x,y,z=0,T_CELSIUS=None):
    if T_CELSIUS==None:
        T = TEMPERATURE_CELSIUS(x,y,z)
    else:
        T = T_CELSIUS
    return 0.6108*exp(17.27*T/(T+237.3))

def TEMPERATURE(x, y, z=0,t = None):
    ''' en Kelvin'''
    global TEMP_VALEUR
    if t==None:
        t = TEMPS_ABSOLU
    if (x,y,z) in TEMP_VALEUR.keys():
        try:
            return eval(TEMP_VALEUR[(x,y,z)])
        except Exception as e:
            INTERFACE.message_erreur('Problème dans la définition de la température : {0}'.format(e))
    return 273.15+20
def TEMPERATURE_CELSIUS(x,y,z=0):
    return TEMPERATURE(x,y,z) - 273.15


temps_max_min_save = {}
def TEMPERATURE_MAX(x,y,z=0, actualisation = False):
    global temps_max_min_save
    if actualisation:
        temps_max_min_save = {}
    if (x,y,z) in temps_max_min_save.keys():
        return temps_max_min_save[(x,y,z)][0]
    ma = max([TEMPERATURE(x,y,z,t) for t in range(0,24*3600,1000)])
    mi = min([TEMPERATURE(x,y,z,t) for t in range(0,24*3600,1000)])
    temps_max_min_save[(x,y,z)] = [ma,mi]
    
    return temps_max_min_save[(x,y,z)][0]

def TEMPERATURE_MAX_CELSIUS(x,y,z=0):
    return TEMPERATURE_MAX(x,y,z) - 273.15

def TEMPERATURE_MIN(x,y,z=0):
    global temps_max_min_save
    if (x,y,z) in temps_max_min_save.keys():
        return temps_max_min_save[(x,y,z)][1]
    ma = max([TEMPERATURE(x,y,z,t) for t in range(0,24*3600,1000)])
    mi = min([TEMPERATURE(x,y,z,t) for t in range(0,24*3600,1000)])
    temps_max_min_save[(x,y,z)] = [ma,mi]
    return temps_max_min_save[(x,y,z)][1]

def TEMPERATURE_MIN_CELSIUS(x,y,z=0):
    return TEMPERATURE_MIN(x,y,z) - 273.15

def TEMPERATURE_EAU(x, y, z=0):
    ''' en Kelvin'''
    global TEMP_VALEUR_EAU
    t = TEMPS_ABSOLU
    if (x,y,z) in TEMP_VALEUR_EAU.keys():
        return eval(TEMP_VALEUR_EAU[(x,y,z)])

def TEMPERATURE_MATERIAU(x,y,z=0):
    try:
        return TEMP_VALEUR_MAT[(x,y,z)]
    except:
        TEMP_VALEUR_MAT[(x,y,z)] = TEMPERATURE(x,y,z)
    return TEMPERATURE(x,y,z)

def TEMPERATURE_MATERIAU_CELSIUS(x,y,z=0):
    return TEMPERATURE_MATERIAU(x,y,z) - 273.15

def PRECIPITATION(x,y,z=0):
    try:
        return eval(PRECIPITATION_[(x,y,z)])
    except:
        return 0
    
pente_tvs_save = {}
def PENTE_TVS(x,y,z=0):
    f=INTERFACE.entree_Formule_DELTA.get()
    if (x,y,z,f) in pente_tvs_save.keys():
        return pente_tvs_save[(x,y,z,f)]
    valeur = eval(f)
    pente_tvs_save[(x,y,z,f)] = valeur
    return valeur

def AUTRE_ENTREE_EAU(x,y,z=0):
    try:
        return eval(AUTRE_ENTREE_EAU_[(x,y,z)])
    except:
        return 0

def EVAPORATION(x,y,z=0):
    try:
        return eval(EVAPORATION_[(x,y,z)])
    except:
        return 0

OMBRAGE = {}
ECHELLE_COULEUR = couleur_test
FONCTION_ACTUELLE = TEMPERATURE
COULEUR_ACTUELLE = couleur_test
FONCTION_ACTUELLE_SAVE = {'Name':0}

def FONCTION_ACT(x,y,z=0, maj = False, maj_force = False):
    global FONCTION_ACTUELLE_SAVE
    if maj_force or FONCTION_ACTUELLE_SAVE['Name'] != FONCTION_ACTUELLE.__name__:
        FONCTION_ACTUELLE_SAVE = {'Name':FONCTION_ACTUELLE.__name__}
    if not maj:
        try:
            return FONCTION_ACTUELLE_SAVE[(x,y,z)]
        except:
            pass
    FONCTION_ACTUELLE_SAVE[(x,y,z)] = FONCTION_ACTUELLE(x,y,z)
    return FONCTION_ACTUELLE_SAVE[(x,y,z)]

def set_fonction_actuelle(valeur):
    global FONCTION_ACTUELLE
    FONCTION_ACTUELLE = valeur

class CanvasAnime(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.args=  args
        self.kwargs = kwargs
        self._liste_objets = []
        self.commandes_dessins = [self.dessin]
        self._after()
    def dessin(self):
        pass
    def _after(self):
        for i in self._liste_objets:
            self.delete(self.master,i)
        self._liste_objets = []
        for i in self.commandes_dessins:
            i()
        
        temps_actu = INTERFACE.temps_actualisation
        self.master.after(temps_actu,self._after)
        
class Canvas3D(CanvasAnime):
    MAXIMUM_ZOOM = 1000
    MINIMUM_ZOOM = 1
    PAS_ZOOM = 2
    ZOOM_INITIAL = 2
    MAX_ANGLE = 2*math.pi/3 - pi/16
    MIN_ANGLE = math.pi/2 - (2*math.pi/3-math.pi/2) + pi/16
    PAS_ROTATION = math.pi/16
    ELLIPSE_ROTA_a = 1
    ELLIPSE_ROTA_b = 0.5
    def __init__(self,*args,**kwargs):
        x0,x1 = 20,0
        y0,y1 = -10.5,17
        z0,z1 = 0,-13
        self.a = Canvas3D.ELLIPSE_ROTA_a
        self.b = Canvas3D.ELLIPSE_ROTA_b
        self.difference_angle = -Canvas3D.MAX_ANGLE
        self.open_interface_thermique = False
        self.open_interface_hydrique = False
        self.avancement = 0
        self.cache_valeur = {}
        self.echelle = Canvas3D.ZOOM_INITIAL
        alphax, alphay,alphaz = (x0**2+x1**2),(y0**2+y1**2),(z0**2+z1**2)
        self.vecteurx = (self.echelle*x0/alphax,self.echelle*x1/alphax)
        self.vecteury = (self.echelle*y0/alphay,self.echelle*y1/alphay)
        self.vecteurz = (self.echelle*z0/alphaz,self.echelle*z1/alphaz)
        self.idx = None
        self.idy = None
        self.idz = None
        self.mode_ = "3D"
        self.reinit_vecteur()
        self.liste_dessin = []
        self.block_interface = False
        self.block_interface_tri = False
        if INTERFACE.M*INTERFACE.N >= 3000:
            self.block_interface_tri = True
            def cmd():
                INTERFACE.message_alerte("Le rafraîchissement des éléments a été désactivé à cause du trop haut nombre de mailles. Appuyez sur le bouton Rafraîchir pour actualiser l'interface.")
            if INTERFACE.M*INTERFACE.N >= 5000:
                self.block_interface = True

            INTERFACE.after(1000, cmd)
        self.id = 0
        self.id_vue = None
        self.decalageX = 0
        self.decalageY = 0
        CanvasAnime.__init__(self,*args,**kwargs)
        self.commandes_dessins.append(self.dessin_vecteur)
        self.tri_objet(start=True)
        #INTERFACE.update()
        self.actualise_interface()
        self.bind('<Button-1>',self.clic)
        self.bind('<ButtonPress-1>',self.clic_press)
        self.bind('<B1-Motion>',self.clic_relacher)
        self.bind('<ButtonRelease-1>',self.clic_relacher)
        self.bind('<Motion>', self.check_visualisation)
        self.bind('<Double-Button-1>',self.double_clic)
        self.bind('<Button-3>',self.double_clic)
    def decalX0(self,e=0):
        self.decalageX += 100
    def decalX1(self,e=0):
        self.decalageX -= 100
    def decalY0(self,e=0):
        self.decalageY += 100
        
    def decal0(self,e=0):
        self.decalageX = 0
        self.decalageY = 0
        self.avancement = 0
        self.echelle = Canvas3D.ZOOM_INITIAL
    def decalY1(self,e=None):
        self.decalageY -= 100
        
    def check_visualisation(self,e):
        x,y = e.x, e.y
        if x < 10:
            self.decalageX += 20
        if y < 10:
            self.decalageY += 20
        if y > int(self['height'])-10:
            self.decalageY -= 20
        if x > int(self['width']) - 10:
            self.decalageX -= 20
    def actualise_interface(self):
        #INTERFACE.update()
        pass
        #self.master.after(1,self.actualise_interface)
    def tri_objet(self,start = False):
        
        INTERFACE.timing_note[2] = round(time.time()-INTERFACE.timing_prenote[2],3) 
        INTERFACE.timing_prenote[2] = time.time()
        """
        Trie les objets en fonction de leur profondeur et met à jour leur affichage.
        """
        #INTERFACE.update()
        self.initialize_u()
        self.liste_dessin = self.tri_fusion(self.liste_dessin)

        # Application des filtres
        arbre_filtre = INTERFACE.VIEW_ARBRE
        batiment_filtre = INTERFACE.VIEW_BATIMENT

        # Mise à jour graphique
        if not self.block_interface:
            for i in [
                i for i in self.liste_dessin
                if (arbre_filtre or i[0][1] not in Arbre.LISTE_ID) and
                   (batiment_filtre or i[0][1] not in Batiment.LISTE_ID)]:
                if i[-1] is not None:
                    self.tag_raise(i[-1])

        # Boucle périodique
        temps_actu = INTERFACE.temps_actualisation
        if not self.block_interface_tri:
            if start:
                self.master.after(10**3, self.tri_objet)
            else:
                self.master.after(10*temps_actu,self.tri_objet)
            
    def estDevans(self, x0, y0, z0, x1, y1, z1):
        """
        Vérifie si un point (x0, y0, z0) est devant un autre point (x1, y1, z1).
        """
        u = self._cached_u  # Pré-calculé dans tri_objet
        v = self._cached_v
        if (x0,y0,z0,x1,y1,z1,v) in self.cache_valeur.keys():
            return self.cache_valeur[(x0,y0,z0,x1,y1,z1,v)]
        #condition=(z0, x0 * u[0] + y0 * u[1]) >= (z1, x1 * u[0] + y1 * u[1])
        condition = x0*v[0] + y0*v[1] + z0*v[2] >= x1*v[0] + y1*v[1] + z1*v[2]
        self.cache_valeur[(x0,y0,z0,x1,y1,z1,v)] = condition
        return condition

    def estDevansF(self, f1, f2, recurrence = False):
        """
        Vérifie si l'objet f1 est constamment devant l'objet f2.
        """
        # Extraction des points pour les deux objets
        def extract_points(f):
            if f[0][0] == 'ligne':
                return [(f[1], f[2], f[3]), (f[4], f[5], f[6])]
            if f[0][0] == 'quad':
                return [
                    (f[1], f[2], f[3]),
                    (f[4], f[5], f[6]),
                    (f[7], f[8], f[9]),
                    (f[10], f[11], f[12])
                ]
            return []

        liste_point_1 = extract_points(f1)
        liste_point_2 = extract_points(f2)

        # Calcul des intervalles z pour une élimination rapide
        z1_min = min(p[2] for p in liste_point_1)
        z1_max = max(p[2] for p in liste_point_1)
        z2_min = min(p[2] for p in liste_point_2)
        z2_max = max(p[2] for p in liste_point_2)

        if z1_max < z2_min :  # f1 est entièrement derrière f2
            return False
        if z2_max < z1_min :  # f1 est entièrement devant f2
            return True
        
        if z1_max == z2_min and z2_min != z2_max:
            return False
        
        if z1_max == z2_min and z1_max != z1_min:
            return False
        
        if z2_max == z1_min and z1_min != z1_max:
            return True

        # Comparaison point par point uniquement si nécessaire
        for x0, y0, z0 in liste_point_1:
            if all(self.estDevans(x0, y0, z0, x1, y1, z1) for x1, y1, z1 in liste_point_2):
                return True
        if not recurrence:
            return not self.estDevansF(f2,f1, True)
        return False
    
    def tri_fusion(self, liste):
        """
        Tri fusion optimisé pour les objets graphiques.
        """
        if len(liste) <= 1:
            return liste
        milieu = len(liste) // 2
        gauche = self.tri_fusion(liste[:milieu])
        droite = self.tri_fusion(liste[milieu:])
        return self.fusion(gauche, droite)

    def fusion(self, gauche, droite):
        """
        Fusionne deux listes triées.
        """
        resultat = []
        i, j = 0, 0
        while i < len(gauche) and j < len(droite):
            if self.estDevansF(droite[j], gauche[i]):
                resultat.append(gauche[i])
                i += 1
            else:
                resultat.append(droite[j])
                j += 1
        resultat.extend(gauche[i:])
        resultat.extend(droite[j:])
        return resultat
    def initialize_v(self):
        
        c = tuple(solve_system(self.vecteurx[0],self.vecteury[0],self.vecteurz[0],self.vecteurx[1],self.vecteury[1],self.vecteurz[1]))
        return c
            
    def initialize_u(self):
        """
        Pré-calcul les constantes nécessaires pour les comparaisons.
        """
        self._cached_u = self.inverse_z_zero(0, 1)
        self._cached_v = self.initialize_v()
        
    def _after(self):
        INTERFACE.timing_note[1] = round(time.time()-INTERFACE.timing_prenote[1],3) 
        INTERFACE.timing_prenote[1] = time.time()
        for i in self.commandes_dessins:
            i()
        temps_actu = INTERFACE.temps_actualisation
        if not self.block_interface:
            self.master.after(temps_actu,self._after)
            
    def clic(self,e=None):
        w,h= self.kwargs['width']//2+self.decalageX,self.kwargs['height']//2+self.decalageY
        if e == None:
            x,y = 0,0
            e = Nonee()
        else:
            x,y = e.x - w,e.y - h
        
        if e != None and 370 < e.x< 390 and 10<e.y<20:
            self.fermer_fenetre_interface_thermique()
        if e != None and 10<e.y<20 and 770<e.x<790:
            print('interface')
            self.fermer_fenetre_interface_hydrique()
        vec = self.inverse_z_zero(x,y)
        self.master.select_case = ((vec[0],vec[1]),None)
        self.master.coord = (vec[0],vec[1])
        self.master.m.reinit_couleur()
        
    def double_clic(self,e=None):
        if self.open_interface_thermique or self.open_interface_hydrique:
            return None
        w,h= self.kwargs['width']//2+self.decalageX,self.kwargs['height']//2+self.decalageY
        if e == None:
            x,y = 0,0
        else:
            x,y = e.x - w,e.y - h
        vec = self.inverse_z_zero(x,y)
        v = (int(vec[0]), int(vec[1]))
        print('Double clic à',v)
        try:
            mat = MATERIAU[(v[0],v[1],0)]
        except:
            INTERFACE.message_erreur("Il n'y a pas de matériau défini ici.")
            return True
        x,y,z = (v[0], v[1], 0)
        
        self.block_interface = True
        self.block_interface_tri = True
        self.open_interface_thermique = True
        self.open_interface_hydrique = True
        self.liste_int_th = []
        self.liste_int_th.append(self.create_rectangle(10,10,390,490,fill='#fcefce'))
        self.liste_int_th.append(self.create_rectangle(370,10,390,20, fill='red'))
        self.liste_int_th.append(self.create_rectangle(50,200, 350, 300, fill=MATERIAU_COULEUR(x,y,z), width=0))
        self.liste_int_th.append(self.create_line(30,30, 85, 200, arrow=LAST, fill = '#f5be34', width=int(10))) 
        self.liste_int_th.append(self.create_line(85,200, 100, 250, arrow=LAST, fill = '#f5be34', width=int(10*(1-ALBEDO(x,y,z))))) 
        self.liste_int_th.append(self.create_line(85,200, 100, 150, arrow=LAST, fill = '#f5be34', width=int(10*ALBEDO(x,y,z)))) 
        self.liste_int_th.append(self.create_line(105,200, 120, 150, arrow=LAST, fill = '#f09819', width=int(10)))
        self.liste_int_th.append(self.create_text(125,155,anchor="sw",fill='#f09819', text="Puissance rayonnée\n{0} W".format(PUISSANCE_RAYONNEMENT_THERMIQUE(x, y,z))))
        self.liste_int_th.append(self.create_text(50,50, fill = '#e4a830',text="Puissance solaire : {0} W/m² \n Puissance absorbée : {1} W \n Puissance réfléchie : {2} W".format(IRRADIANCE_OMBRAGE(x,y,z),PUISSANCE_ABSORBEE(x,y,z),PUISSANCE_REFLECHIE(x,y,z)), anchor = 'w'))
        self.liste_int_th.append(self.create_line(60,250,20,250, arrow=LAST,fill="#FF0000",width=10))
        self.liste_int_th.append(self.create_text(20, 310,fill="#FF0000", text="Puissance transmise aux mailles autour :\n-à {0} : {1} W\n-à {2} : {3} W\n-à {4} : {5} W\n-à {6} : {7} W".format((x+1,y,z),ECHANGE_PUISSANCE_MAILLE_(x,y,z,x+1,y,z),(x-1,y,z),ECHANGE_PUISSANCE_MAILLE_(x,y,z,x-1,y,z),(x,y+1,z),ECHANGE_PUISSANCE_MAILLE_(x,y,z,x,y+1,z),(x,y-1,z),ECHANGE_PUISSANCE_MAILLE_(x,y,z,x,y-1,z)), anchor="nw"))
        self.liste_int_th.append(self.create_line(330,250,330,400, arrow=LAST,fill="#875e47",width=10))
        self.liste_int_th.append(self.create_text(330,410, anchor="ne",fill="#875e47",text = "Puissance envoyée au sous-sol : \n{0} W".format(PUISSANCE_SOUSSOL(x,y,z))))
        self.liste_int_th.append(self.create_line(300,200,300,100, arrow=LAST,fill="#68c677",width=10))
        self.liste_int_th.append(self.create_line(330,200,330,180, arrow=LAST,fill="#b8bff3",width=10))
        self.liste_int_th.append(self.create_text(340,200, fill="#b8bff3", anchor = 'se',text = "Puissance de conducto-convection :\nConduction : {0} W\nConvection : {1} W".format(PUISSANCE_CONDUCTION_AIR(x,y,z),PUISSANCE_CONVECTION(x,y,z))))
        self.liste_int_th.append(self.create_text(340,100, fill="#68c677", anchor = 'se',text = "Puissance d'évapotranspiration : {0} W".format(PUISSANCE_EVAPOTRANSPIRATION(x,y,z))))
        self.liste_int_th.append(self.create_text(20,460,fill="#875e47",anchor = "w",text = "Puissance transoformée en T ({0},{1},{2})={3}W".format(x,y,z,SOMME_PUISSANCE(x, y,0))))
        self.liste_int_th.append(self.create_text(20,480,fill="#875e47",anchor = "w",text = "Bilan thermique de la maille ({0},{1},{2},t={3}), {4}".format(x,y,z,TEMPS_ABSOLU,MATERIAU[(x,y,z)])))
        self.liste_int_hy = []
        self.liste_int_hy.append(self.create_rectangle(410,10,790,390, fill='white'))
        self.liste_int_hy.append(self.create_rectangle(790,10,770,20,fill='red'))
    def fermer_fenetre_interface_thermique(self):
        if self.open_interface_thermique: 
            if not self.open_interface_hydrique and self.block_interface:
                self.block_interface = False
                self._after()
                self.block_interface_tri = False
            self.open_interface_thermique = False
            for i in self.liste_int_th:
                self.delete(self.master,i)
    def fermer_fenetre_interface_hydrique(self):
        if self.open_interface_hydrique: 
            if not self.open_interface_thermique and self.block_interface:
                self.block_interface = False
                self._after()
                self.block_interface_tri = False
            self.open_interface_hydrique = False
            for i in self.liste_int_hy:
                self.delete(self.master,i)
    def clic_press(self,e):
        w,h= self.kwargs['width']//2+self.decalageX,self.kwargs['height']//2+self.decalageY
        x,y = e.x - w,e.y - h
        if e != None and 370 < e.x< 390 and 10<e.y<20:
            self.fermer_fenetre_interface_thermique()
            return None
        
        if e != None and 10<e.y<20 and 770<e.x<790:
            self.fermer_fenetre_interface_hydrique()
            return None
        vec = self.inverse_z_zero(x,y)
        self.master.select_case = ((vec[0],vec[1]),None)
        self.master.coord = (vec[0],vec[1])
        self.master.m.reinit_couleur()
    def clic_relacher(self,e):
        w,h= self.kwargs['width']//2+self.decalageX,self.kwargs['height']//2+self.decalageY
        x,y = e.x - w,e.y - h
        vec = self.inverse_z_zero(x,y)
        self.master.select_case = (self.master.select_case[0],(vec[0],vec[1]))
        self.master.coord = (vec[0],vec[1])
        self.master.m.reinit_couleur()
    def zoom(self,e=None):
        if self.echelle < Canvas3D.MAXIMUM_ZOOM:
            self.echelle *= Canvas3D.PAS_ZOOM        
        self.reinit_vecteur()
    def dezoom(self,e=None):
        if self.echelle > Canvas3D.MINIMUM_ZOOM:
            self.echelle /= Canvas3D.PAS_ZOOM
        self.reinit_vecteur()
    def pivoter_droite(self,e=None):
        self.pivoter(-Canvas3D.PAS_ROTATION)
    def pivoter_gauche(self,e=None):
        self.pivoter(Canvas3D.PAS_ROTATION)
    def pivoter(self,angle):
        x0,x1 = self.vecteurx
        y0,y1 = self.vecteury
        ce = 1
        #self.vecteurx = (ce*x0*math.cos(angle)-ce*x1*math.sin(angle),ce*x1*math.cos(angle)+ce*x0*math.sin(angle))
        #self.vecteury = (ce*y0*math.cos(angle)-ce*y1*math.sin(angle),ce*y1*math.cos(angle)+ce*y0*math.sin(angle))
        
        self.avancement += angle
        self.reinit_vecteur()
    def reinit_vecteur(self):
        if self.mode_ == "3D":
            x0,x1 = self.vecteurx
            y0,y1 = self.vecteury
            z0,z1 = 0,-13
            alphax, alphay,alphaz = (x0**2+x1**2)**0.5,(y0**2+y1**2)**0.5,(z0**2+z1**2)**0.5
            
            coef_ellipse1 = 0.3*math.cos(2*self.avancement)+1
            coef_ellipse2 = 0.3*math.cos(2*self.avancement-self.difference_angle)+1
    
            self.difference_angle = (-Canvas3D.MIN_ANGLE-Canvas3D.MAX_ANGLE)/2 + (-Canvas3D.MIN_ANGLE+Canvas3D.MAX_ANGLE)/2*cos(4*self.avancement)
            self.vecteurx = (self.a*self.echelle*cos(2*self.avancement),self.b*self.echelle*sin(2*self.avancement))
            self.vecteury = (self.a*self.echelle*cos(2*self.avancement-self.difference_angle),self.b*sin(2*self.avancement-self.difference_angle)*self.echelle)
            self.vecteurz = (self.echelle*z0/alphaz,self.echelle*z1/alphaz)
        else:
            self.vecteurx = (cos(self.avancement),sin(self.avancement))
            self.vecteury = (-sin(self.avancement),cos(self.avancement))
            self.vecteurz = (0,-0.00000001)
    def get_vecteur_k(self):
        alpha = self.vecteurx[1]
        beta = self.vecteury[1]    
    
    def dessin(self):
        w,h= self.kwargs['width']//2+self.decalageX,self.kwargs['height']//2+self.decalageY
        for i in self.liste_dessin:
            if i[0][0] == 'ligne':
                x0,y0,z0,x1,y1,z1 = i[1],i[2],i[3],i[4],i[5],i[6]        
                u0,v0 = self.projectPoint3D(x0,y0,z0)
                u1,v1 = self.projectPoint3D(x1,y1,z1)
                l = i[-1]
                if l == None:
                    l = self.create_line(int(w+u0),int(h+v0),int(w+u1),int(h+v1))
                else:
                    self.coords(l,int(w+u0),int(h+v0),int(w+u1),int(h+v1))
                i[-1] = l
            if i[0][0] == 'quad':
                filln = i[13]
                x0,y0,z0,x1,y1,z1,x2,y2,z2,x3,y3,z3 = i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12]    
                u0,v0 = self.projectPoint3D(x0,y0,z0)
                u1,v1 = self.projectPoint3D(x1,y1,z1)
                u2,v2 = self.projectPoint3D(x2,y2,z2)
                u3,v3 = self.projectPoint3D(x3,y3,z3)
                l = i[-1]
                if l == None:
                    l = self.create_polygon(int(w+self.echelle*u0),int(h+self.echelle*v0),int(w+self.echelle*u1),int(h+self.echelle*v1),int(w+self.echelle*u2),int(h+self.echelle*v2),int(w+self.echelle*u3),int(h+self.echelle*v3), fill =filln)
                else:
                    comp = i[-2]
                    comp2=[int(w+self.echelle*u0),int(h+self.echelle*v0),int(w+self.echelle*u1),int(h+self.echelle*v1),int(w+self.echelle*u2),int(h+self.echelle*v2),int(w+self.echelle*u3),int(h+self.echelle*v3)]
                    if comp != comp2:
                        self.coords(l,*comp2)    
                        i[-2] = comp2
                    try:
                        self.itemconfig(l, fill=i[13])
                    except Exception as e:
                        INTERFACE.message_erreur('Erreur à {0}, {1}'.format(e,i))
                i[-1] = l
            self._liste_objets.append(l)
    def create_line3D(self,x0,y0,z0, x1,y1,z1):
        self.liste_dessin.append([['ligne',self.id],x0,y0,z0,x1,y1,z1,None,None])
        self.id += 1
        return self.id - 1
        self.create_line3D(x0,y0,z0,x0,y1,z0)
    def supprimer_id(self,id_):
        for i in self.liste_dessin:
            if i[0][1]==id_:
                self.liste_dessin.remove(i)
                break
        self.delete(self.master,id_)
    def create_polygon3D(self,x0,y0,z0, x1,y1,z1, x2,y2,z2,x3,y3,z3,fill='white', arbre = False, batiment = False):
        u0,v0 = self.projectPoint3D(x0,y0,z0)
        u1,v1 = self.projectPoint3D(x1,y1,z1)
        u2,v2 = self.projectPoint3D(x2,y2,z2)
        u3,v3 = self.projectPoint3D(x3,y3,z3)
        self.liste_dessin.append([['quad',self.id],x0,y0,z0, x1,y1,z1, x2,y2,z2,x3,y3,z3,fill,None,None])
        if arbre:
            Arbre.LISTE_ID.append(self.id)
        if batiment:
            
            Batiment.LISTE_ID.append(self.id)
        self.id += 1
    
        return self.id - 1
    def inverse_z_zero(self,u0,u1):
        self.reinit_vecteur()
        x = self.vecteurx
        y = self.vecteury
        u = (u0,u1)
        def produit_scalaire(a,b):
            return a[0]*b[0] + a[1]*b[1]
        def norme(vecteur):
            return produit_scalaire(vecteur,vecteur)**0.5
        xy = produit_scalaire(x,y)
        if xy == 0:
            (alpha,beta) = (produit_scalaire(u,x)/norme(x),produit_scalaire(u,y)/norme(y))
        else:
            beta = ((produit_scalaire(y,u)/produit_scalaire(y,x))-(produit_scalaire(x,u)/produit_scalaire(x,x)))/((produit_scalaire(y,y)/produit_scalaire(y,x))-(produit_scalaire(y,x)/produit_scalaire(x,x)))
            alpha = produit_scalaire(y,u)/produit_scalaire(y,x) - beta*produit_scalaire(y,y)/produit_scalaire(y,x)
        return (alpha/self.echelle,beta/self.echelle,0)
    def create_parallelepipede(self,x0,y0,z0,x1,y1,z1,fill=None, arbre = False, batiment = False):
        if fill == None:
            #a1=self.create_polygon3D(x0,y0,z0,x1,y0,z0,x1,y1,z0,x0,y1,z0,'red')
            a2=self.create_polygon3D(x0,y0,z0,x0,y0,z1,x0,y1,z1,x0,y1,z0,'pink')
            a3=self.create_polygon3D(x0,y0,z0,x1,y0,z0,x1,y0,z1,x0,y0,z1,'purple')
            a4=self.create_polygon3D(x1,y0,z0,x1,y0,z1,x1,y1,z1,x1,y1,z0,'blue')
            a5=self.create_polygon3D(x0,y1,z0,x1,y1,z0,x1,y1,z1,x0,y1,z1,'orange')
            a6=self.create_polygon3D(x0,y0,z1,x1,y0,z1,x1,y1,z1,x0,y1,z1,'yellow')
        else:
            #a1=self.create_polygon3D(x0,y0,z0,x1,y0,z0,x1,y1,z0,x0,y1,z0,fill, arbre, batiment)
            a2=self.create_polygon3D(x0,y0,z0,x0,y0,z1,x0,y1,z1,x0,y1,z0,assombrir_couleur_hex(fill,0.9), arbre, batiment)
            a3=self.create_polygon3D(x0,y0,z0,x1,y0,z0,x1,y0,z1,x0,y0,z1,assombrir_couleur_hex(fill,0.95), arbre, batiment)
            a4=self.create_polygon3D(x1,y0,z0,x1,y0,z1,x1,y1,z1,x1,y1,z0,assombrir_couleur_hex(fill,0.9), arbre, batiment)
            a5=self.create_polygon3D(x0,y1,z0,x1,y1,z0,x1,y1,z1,x0,y1,z1,assombrir_couleur_hex(fill,0.95), arbre, batiment)
            a6=self.create_polygon3D(x0,y0,z1,x1,y0,z1,x1,y1,z1,x0,y1,z1,fill, arbre, batiment)
        return [a2,a3,a4,a5,a6]
    def retirer_element(self,id_):
        for i in self.liste_dessin:
            if i[0][1] == id_:
                self.liste_dessin.remove(i)
    def recherche_id(self,id_):
        for i in self.liste_dessin:
            if i[0][1] == id_:
                return self.liste_dessin.index(i)
    
    def projectPoint3D(self,x,y,z):
        return (x*self.vecteurx[0]+y*self.vecteury[0]+z*self.vecteurz[0],x*self.vecteurx[1]+y*self.vecteury[1]+z*self.vecteurz[1])
    
    def dessin_vecteur(self):
        w,h= self.kwargs['width']//2+self.decalageX,self.kwargs['height']//2+self.decalageY
        if self.idx == None:
            x=self.create_line(w,h,w+self.vecteurx[0],h+self.vecteurx[1], fill = 'blue')
            self.idx = x 
        else:
            self.coords(self.idx,w,h,w+self.echelle*self.vecteurx[0],h+self.echelle*self.vecteurx[1])
        if self.idy == None:
            y=self.create_line(w,h,w+self.echelle*self.vecteury[0],h+self.echelle*self.vecteury[1], fill = 'green')
            self.idy = y
        else:
            self.coords(self.idy,w,h,w+self.echelle*self.vecteury[0],h+self.echelle*self.vecteury[1])
        if self.idz == None:
            z=self.create_line(w,h,w+self.echelle*self.vecteurz[0],h+self.echelle*self.vecteurz[1], fill = 'red')
            self.idz = z
        else:
            self.coords(self.idz,w,h,w+self.echelle*self.vecteurz[0],h+self.echelle*self.vecteurz[1])
        if self.id_vue == None:
            v = self.initialize_v()
            self.id_vue = self.create_line3D(0, 0, 0, v[0], v[1], v[2])
        else:
            l = self.liste_dessin[self.recherche_id(self.id_vue)]
            v = self.initialize_v()
            l[4],l[5],l[6] = 100*v[0],100*v[1],100*v[2]
        self.tag_raise(self.idx)
        self.tag_raise(self.idy)
        self.tag_raise(self.idz)
class Simulation:
    def __init__(self,fenetre):
        self.parametres = {}
        print(self.parametres)
        

class Maillage:
    def __init__(self,x,y,taille,hauteur = 0,fonction_couleur=cst_couleur, canvas = None):
        self.x = x
        self.y = y
        self.taille = taille
        self.hauteur = hauteur
        self.canvas = canvas
        self.couleur = cst_couleur
        self.albedo = None
        self.affiche(canvas)
    def set_couleur(self,vMax,vMin=0):
        i = self.canvas.recherche_id(self.id)
        if i==None:
            return None
        if self.canvas.liste_dessin[i][0][0] == 'quad':
            u,v = (self.x+self.taille//2,self.y+self.taille//2)
            ku,kv = -0.5,-0.5
            kw,ky = -0.75,-0.75
            if self.canvas.master.select_case[0] != None:
                ku,kv = (self.canvas.master.select_case[0])
                ku,kv = math.floor(ku),math.floor(kv)
                self.canvas.master.select_case = ((ku,kv), self.canvas.master.select_case[1])
            if self.canvas.master.select_case[1] != None:
                kw,ky = self.canvas.master.select_case[1]
                kw,ky = math.floor(kw), math.floor(ky)
                self.canvas.master.select_case = (self.canvas.master.select_case[0], (kw,ky))
            if (ku,kv) == (math.floor(u),math.floor(v)):
                self.canvas.liste_dessin[i][13] = 'black'
            elif (min(ku,kw) <= math.floor(u) <= max(ku,kw)) and (min(kv,ky)<=math.floor(v)<=max(kv,ky)):
                self.canvas.liste_dessin[i][13] = 'black'
            else:
                m = FONCTION_ACT(u,v,0)
                if type(m) == type(""):
                    self.canvas.liste_dessin[i][13] = ECHELLE_COULEUR(m)
                else:
                    self.canvas.liste_dessin[i][13] = ECHELLE_COULEUR(REDUCTION(FONCTION_ACT(u,v,0),vMax+0.00000001,vMin))
    def affiche(self,canvas):
        self.canvas = canvas
        self.id = canvas.create_polygon3D(self.x, self.y,self.hauteur, self.x+self.taille, self.y, self.hauteur,self.x+self.taille, self.y+self.taille, self.hauteur, self.x, self.y+self.taille, self.hauteur, self.couleur(self.x+self.taille/2,self.y+self.taille/2))
        
class Maillages:
    def __init__(self, x0,y0,taille,hauteur,N,M,fonction_couleur,canvas):
        self.liste_maillage = []
        x,y = x0,y0
        self.x0 = x0
        self.y0 = y0
        self.N = N
        self.M = M
        self.taille = taille
        self.hauteur = hauteur
        self.canvas = canvas
        self.repere_maillage = {}
        vMax = FONCTION_ACT(0,0)
        vMin = FONCTION_ACT(0,0)
        self.listeXY = [] #''' liste des abscisses x'''
        for i in range(M):
            x = x0
            for j in range(N):
                x += taille
                v = FONCTION_ACT(x,y)
                if vMax < v:
                    vMax = v
                if vMin > v:
                    vMin = v
                m = Maillage(x,y,self.taille,hauteur, fonction_couleur = fonction_couleur, canvas = canvas)
                self.repere_maillage[x,y] = m
                self.liste_maillage.append(m)
                self.listeXY.append((x,y))
            y += taille
        self.reinit_couleur()
    def set_albedo(self,x,y,albedo):
        try:
            self.repere_maillage[x,y].albedo = albedo
        except KeyError:
            pass
    def get_albedo(self,x,y,z=None):
        try:
            u = self.repere_maillage[x,y].albedo
        except KeyError:
            return None
        if u == None:
            return random.random()
        if (x,y,z) in MATERIAU.keys():
            u = MATERIAU[(x,y,z)]
        if type(u)==type(''):
            for i in BASE_DE_DONNEES:
                if i[0] == u:
                    return i[1]
        return u
    def set_couleur(self,clr):
        for i in self.liste_maillage:
            i.set_couleur(clr)
    def reinit_couleur(self):
        vMax = FONCTION_ACT(0,0)
        vMin = FONCTION_ACT(0,0)
        y = self.y0
        for i in range(self.M):
            x = self.x0
            for j in range(self.N):
                x += self.taille
                v = FONCTION_ACT(x,y)
                if vMax < v:
                    vMax = v
                if vMin > v:
                    vMin = v
            y += self.taille
        
        INTERFACE.VMAX = vMax
        INTERFACE.VMIN = vMin
        def fct(x,y):
            global ECHELLE_COULEUR,REDUCTION,FONCTION_ACT
            m = FONCTION_ACT(x,y,0)
            if type(m) == type("") or type(vMin)==type(''):
                return ECHELLE_COULEUR(m)
            return ECHELLE_COULEUR(REDUCTION(m,vMax,vMin-0.00000001))
        self.fct = fct
        self.max = vMax
        self.min = vMin
        for i in self.liste_maillage:
            i.set_couleur(vMax, vMin)
    def afficher(self,canvas):
        self.canvas = canvas
        pass
    
class Arbre():
    arbre = {}
    LISTE_ID = []
    TAUX_OMBRE = 0.2
    def __init__(self, x,y,z, KET, Tair, HR, h, R):
        self.x = x
        self.y = y
        self.z = z
        self.KET = KET
        self.Tair = Tair
        self.HR = HR
        self.h = h
        self.R = R
        Arbre.arbre[(x,y,z)]= self
    def __str__(self):
        return "KET : {0}, HR : {1}, Tair : {2}".format(self.KET, self.HR, self.Tair)

def assombrir_couleur_hex(couleur_hex, facteur=0.8):
    """
    Assombrit une couleur hexadécimale.
    :param couleur_hex: Chaine de caractères de la couleur (#RRGGBB)
    :param facteur: Facteur d'assombrissement (0 < facteur < 1)
    :return: Couleur assombrie en format hexadécimal (#RRGGBB)
    """
    # S'assurer que la couleur est au bon format
    if not couleur_hex.startswith("#") or len(couleur_hex) != 7:
        raise ValueError("Format de couleur invalide. Utilisez #RRGGBB.")

    # Extraire les composantes Rouge, Vert et Bleu
    r = int(couleur_hex[1:3], 16)
    g = int(couleur_hex[3:5], 16)
    b = int(couleur_hex[5:7], 16)

    # Appliquer le facteur d'assombrissement
    r_assombri = int(r * facteur)
    g_assombri = int(g * facteur)
    b_assombri = int(b * facteur)

    # S'assurer que les valeurs restent dans [0, 255]
    r_assombri = max(0, min(255, r_assombri))
    g_assombri = max(0, min(255, g_assombri))
    b_assombri = max(0, min(255, b_assombri))

    # Recréer la couleur en format hexadécimal
    couleur_assombrie = f"#{r_assombri:02X}{g_assombri:02X}{b_assombri:02X}"
    return couleur_assombrie

def couleur_complementaire(hex_color: str) -> str:
    """
    Calcule la couleur complémentaire d'une couleur donnée en format hexadécimal.
    
    Args:
        hex_color (str): Une chaîne représentant une couleur hexadécimale (ex: '#a2ef3g').
    
    Returns:
        str: La couleur complémentaire en format hexadécimal.
    """
    # Vérifier si le format est valide
    if not isinstance(hex_color, str) or not hex_color.startswith('#') or len(hex_color) != 7:
        raise ValueError("Entrée invalide. Format attendu : '#RRGGBB'")
    
    try:
        # Extraire les composants RGB
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
    except ValueError:
        raise ValueError("La couleur hexadécimale est invalide.")
    
    # Calculer la couleur complémentaire
    comp_r = 255 - r
    comp_g = 255 - g
    comp_b = 255 - b
    
    # Convertir en format hexadécimal
    return f'#{comp_r:02x}{comp_g:02x}{comp_b:02x}'

def couleur_luminosite_complementaire(hex_color: str) -> str:
    """
    Calcule la couleur complémentaire d'une couleur donnée en format hexadécimal.
    
    Args:
        hex_color (str): Une chaîne représentant une couleur hexadécimale (ex: '#a2ef3g').
    
    Returns:
        str: La couleur complémentaire en format hexadécimal.
    """
    # Vérifier si le format est valide
    if not isinstance(hex_color, str) or not hex_color.startswith('#') or len(hex_color) != 7:
        raise ValueError("Entrée invalide. Format attendu : '#RRGGBB'")
    
    try:
        # Extraire les composants RGB
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
    except ValueError:
        raise ValueError("La couleur hexadécimale est invalide.")
    
    # Calculer la couleur complémentaire
    comp_r = int(sum([255 - r, 255-g, 255-b])/3)
    comp_g = comp_r
    comp_b = comp_r
    
    if comp_r < 255/3:
        comp_r, comp_g, comp_b = 0,0,0
    else:
        comp_r, comp_g, comp_b = 200,200,200
    
    # Convertir en format hexadécimal
    f = f'#{comp_r:02x}{comp_g:02x}{comp_b:02x}'
    return f


class Batiment():
    bat = {}
    LISTE_ID = []
    liste_Batiment = []
    def __init__(self,x0,y0,z0,x1,y1,z1,couleur):
        self.point0 = (x0,y0,z0)
        self.point1 = (x1,y1,z1)
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1
        Batiment.liste_Batiment.append([x0,y0,z0,x1,y1,z1,couleur,abs(z1-z0)])

class Surface_d_eau():
    surface = {}
    def __init__(self):
        pass
    
class PanedWindowDefilant(PanedWindow):
    liste = {}
    n = {}
    def __init__(self, master, *args, **kwargs):
        self.liste_widget = []
        self.par_init = [master, args, kwargs]
        
        # Gestion des paramètres optionnels
        self.origine = kwargs.pop('origine', self)
        self.previous = kwargs.pop('previous', self)
        self.next_to = kwargs.pop('next_to', False)
        self.paned_gen = kwargs['paned_gen']
        try:
            kwargs['taille_paned']
        except:
            kwargs['taille_paned'] = 600
        self.taille_paned = kwargs['taille_paned']
        
            
        
        # Initialisation du PanedWindow
        kw = kwargs.copy()
        del kw['paned_gen']
        del kw['taille_paned']
        PanedWindow.__init__(self, master, *args, **kw)
        if self.origine == self:
            PanedWindowDefilant.liste[self.origine] = [self]
            PanedWindowDefilant.n[self.origine] = []
        else:
            PanedWindowDefilant.liste[self.origine].append(self)
        self.n = PanedWindowDefilant.n
    def defiler_previous(self):
        if self.previous != self:
            self.paned_gen.forget(self)
            self.paned_gen.add(self.previous)

    def defiler_next(self):
        if self.next_to:
            self.paned_gen.forget(self)
            self.paned_gen.add(self.next_to)
    
    def tout_cacher(self):
        pass
    def add(self, widget, **kw):
        # Calcul de la hauteur des widgets existants
        somme = sum([w.winfo_reqheight() for w in self.liste_widget]) +100
        if False:
            try:
                taille = self.par_init[0].master.winfo_reqheight()
            except:
                taille = self.par_init[0].winfo_reqheight() 
        taille = self.taille_paned
        if somme < taille:
            PanedWindow.add(self, widget, **kw)
            self.liste_widget.append(widget)
        else:
            if not self.next_to:
                # Création du nouveau PanedWindow si besoin
                bouton = Button(self.par_init[0],text = "Page suivante {0}".format(2+len(PanedWindowDefilant.n[self.origine])//2), command = self.defiler_next, bg='black',fg='white')
                PanedWindowDefilant.n[self.origine].append(bouton)
                self.bouton_ = bouton
                PanedWindow.add(self,bouton)
                self.liste_widget.append(bouton)
                self.next_to = PanedWindowDefilant(self.par_init[0], *self.par_init[1], **self.par_init[2], origine=self.origine, previous=self)
                bouton_avant = Button(self.par_init[0], bg='black',fg='white', text = 'Page précédente {0}'.format(len(PanedWindowDefilant.n[self.origine])//2+1), command = self.next_to.defiler_previous)
                PanedWindowDefilant.n[self.origine].append(bouton_avant)
                PanedWindow.add(self.next_to,bouton_avant)
                self.next_to.liste_widget.append(bouton_avant)
                n = len(PanedWindowDefilant.n[self.origine])//2
                for i in range(len(PanedWindowDefilant.n[self.origine])//2):
                    PanedWindowDefilant.n[self.origine][2*i]['text'] = "Page suivante {0}/{1}".format(i+2,n+1)
                    PanedWindowDefilant.n[self.origine][2*i+1]['text'] = "Page précédente {0}/{1}".format(i+1,n+1)
                    pass
            self.next_to.add(widget, **kw)

PanedWindow.tout_cacher = lambda self:0
try:
    Text.get_from_to
except:
    Text.get_from_to = Text.get 
    def get(self):
        return self.get_from_to("1.0","end-1c")
    Text.get = get
    Lab = Label
    class NewLabel(Lab):
        def __init__(self,*args,**kwargs):
            Lab.__init__(self, *args, **kwargs,font=(Interface.font_label,Interface.taille_font))
    Label = NewLabel
    
class Nonee():
    def __init__(self):
        self.x = 0
        self.y = 0

def INDICATRICE(a,x,b):
    if a < x < b:
        return 1 
    return 0

def solve_system(x0, y0, z0, x1, y1, z1):
    # Définir les équations
    def equations(vars):
        x, y, z = vars
        eq1 = x * x0 + y * y0 + z * z0
        eq2 = x * x1 + y * y1 + z * z1
        eq3 = x**2 + y**2 + z**2 - 1
        return [eq1, eq2, eq3]

    # Utiliser fsolve pour trouver les racines
    initial_guess = (1, 1, 1)  # Vous pouvez ajuster cette estimation initiale
    solution = fsolve(equations, initial_guess)

    # Vérifier si une solution valide a été trouvée et si z > 0
    if np.allclose(equations(solution), [0, 0, 0]) and solution[2] > 0:
        return solution
    else:
        return -solution


INTERFACE = 0

class InterfaceLancement(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Interface de lancement')
        paned = PanedWindow(self,orient=VERTICAL)
        paned.add(Label(self,text="Taille du maillage (en m/maille)"))
        
        self.entree_t = Entry(self)
        paned.add(self.entree_t) 
        
        paned.add(Label(self,text="Nombre de mailles selon x"))

        self.entree_M = Entry(self)
        paned.add(self.entree_M)
        
        paned.add(Label(self,text="Nombre de mailles selon y"))
        
        self.entree_N = Entry(self)
        paned.add(self.entree_N)
        bouton = Button(self,text="Lancer avec ces paramètres", command = self.lancer)
        paned.add(bouton)
        self.entree_adresse = Entry(self)
        self.entree_adresse.insert(0,"save.txt")
        paned.add(self.entree_adresse)
        paned.add(Button(self,text="Lancer avec le fichier ci-dessus.", command = self.lire_premiere_ligne))
        bouton = Button(self,text="Lancer avec les paramètres par défaut", command = self.lancer_defaut)
        paned.add(bouton)
        paned.add(Label(self,text = "Pour obtenir les paramètres idéaux\n entrez la surface x*y :"))
        self.entree_X = Entry(self)
        paned.add(self.entree_X)
        self.entree_Y = Entry(self)
        paned.add(self.entree_Y)
        self.entree_Nmailles = Entry(self)
        self.entree_Nmailles.insert(0,"1000")
        paned.add(self.entree_Nmailles)
        self.bouton_ideal = Button(self,text = "Valider", command = self.valider_ideal)
        paned.add(self.bouton_ideal)
        self.label_maille = Label(self, text = "Nombre de mailles : 0\n Recommandé <= 3000.\n S")
        paned.add(self.label_maille)
        paned.pack()
        self._after()
        self.mainloop()
    def valider_ideal(self):
        try:
            X = eval(self.entree_X.get())
            Y = eval(self.entree_Y.get())
            Nmailles = eval(self.entree_Nmailles.get())
            assert X > 0 
            assert Y > 0
        except Exception as e:
            Interface.message_erreur(self,"Format incorrect : {0}".format(e))
            return None
        
        N = int(sqrt(Y*Nmailles/X))
        M = int(Nmailles/N)
        t = sqrt(X*Y/(M*N))
        self.entree_M.delete(0,END)
        self.entree_M.insert(0,str(M))
        self.entree_N.delete(0,END)
        self.entree_N.insert(0,str(N))
        self.entree_t.delete(0,END)
        self.entree_t.insert(0,str(t))
        
    def _after(self):
        try:
            M = eval(self.entree_M.get())
            N = eval(self.entree_N.get())
            self.label_maille.config(text="Nombre de mailles : {0}\n (Recommandé <= 3000)\n".format(M*N))
        except:
            self.label_maille.config(text="Nombre de mailles : Indéfini\n Recommandé <= 3000.\n")
        try:
            t = eval(self.entree_t.get())
            self.label_maille.config(text="Nombre de mailles : >{0}\n (Recommandé <= 3000) \n Surface totale : {1}m*{2}m = {3}m²".format(M*N,round(t*M),round(t*N), round(t*M*t*N)))
        except:
            pass
        self.after(5, self._after)
    def lire_premiere_ligne(self):
        nom_fichier = self.entree_adresse.get()
        try:
            with open(nom_fichier, 'r') as fichier:
                premiere_ligne = fichier.readline().strip()
                premiere_ligne = eval(premiere_ligne)
                assert premiere_ligne[0] == 'format'
                M,N,t = premiere_ligne[1]
                self.lancer(M,N,t, nom_fichier)
                return premiere_ligne
        except FileNotFoundError:
            return f"Le fichier {nom_fichier} n'existe pas."
        except Exception as e:
            Interface.message_erreur(self,f"Une erreur s'est produite : {0}".format(e))
    def lancer_defaut(self):
        self.destroy()
        Interface()
    def lancer(self,M=None,N=None, t=None, adresse=None):
        print('Lancement du processus ',M,N,t)
        if M==None:
            t = eval(self.entree_t.get())
            N = eval(self.entree_N.get())
            M = eval(self.entree_M.get())
        if M*N >= 3000:
            Interface.message_erreur(self,"Attention, il y a beaucoup de mailles, il est possible que ça ne fonctionne pas.")
        self.destroy()
        if adresse != None:
            Interface(N,M,t,adresse)
        else:
            Interface(N,M,t)
InterfaceLancement()