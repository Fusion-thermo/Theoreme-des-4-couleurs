from tkinter import * 
import random
from PIL import ImageGrab
from datetime import datetime

width=850
height=width
taille_carte=10
unite=width/(taille_carte)
moitie_carre=(unite)/2
x0=0
y0=height
taux_suppr_bordures=0.5
couleurs=["red","blue","green","purple"]

class carte:
	def __init__(self,taille):
		self.taille=taille
		self.dico_regions_coos={}
		self.dico_coos_regions={}
		for i in range(taille):
			for j in range(taille):
				regi=region((1/2+i,1/2+j))
				self.dico_regions_coos[regi] = [(1/2+i,1/2+j)]
				self.dico_coos_regions[(1/2+i,1/2+j)] = regi
		#print([i for i in self.dico_coos_regions.keys()])
		self.bordures=[]
		for i in range(taille):
			for j in range(1,taille):
				self.bordures.append([(i,j),(i+1,j)])
				self.bordures.append([(j,i),(j,i+1)])
		self.nodes={}
		for i in range(taille+1):
			for j in range(taille+1):
				self.nodes[(i,j)]=4

	def affichage_init(self):
		Canevas.create_rectangle(x0,y0,x0+self.taille*unite,y0-self.taille*unite,outline="red")
	def affichage(self):
		for region in self.dico_regions_coos.keys():
			for coo in self.dico_regions_coos[region]:
				Canevas.create_rectangle(x0+coo[0]*unite - moitie_carre,y0-coo[1]*unite - moitie_carre,x0+coo[0]*unite + moitie_carre,y0-coo[1]*unite + moitie_carre,fill=region.color,outline="")
		for bord in self.bordures:
			for i in range(len(bord)-1):
				Canevas.create_line(x0+bord[i][0]*unite,y0-bord[i][1]*unite,x0+bord[i+1][0]*unite,y0-bord[i+1][1]*unite)
		
	def agrandissement_regions(self):
		#print(len(self.bordures))
		for bord in self.bordures:
			#print(bord,self.nodes[bord[0]],self.nodes[bord[1]])
			if self.nodes[bord[0]]==2 or self.nodes[bord[1]]==2:
				#print("on passe car node=2")
				continue
			if random.random()<taux_suppr_bordures:
				#print("supprimé")
				#on récupère les coos du carré de région situé à côté de la bordure
				if bord[0][0]==bord[1][0]:
					#bordure verticale
					region_suppr=(bord[0][0]-0.5,(bord[0][1]+bord[1][1])/2)
					region_new=(bord[0][0]+0.5,(bord[0][1]+bord[1][1])/2)
				else:
					#bordure horizontale
					region_suppr=((bord[0][0]+bord[1][0])/2,bord[0][1]-0.5)
					region_new=((bord[0][0]+bord[1][0])/2,bord[0][1]+0.5)
				#on retire une des deux régions
				for old_region in self.dico_regions_coos.keys():
					if region_suppr in self.dico_regions_coos[old_region]:
						coos_libres=self.dico_regions_coos[old_region]
						del self.dico_regions_coos[old_region]
						break
				#on attribue les coos libres, les bordures et les voisins de l'ancienne région à l'autre région
				new_region = self.dico_coos_regions[region_new]
				#bordures
				new_region.bordures.remove(bord)
				old_region.bordures.remove(bord)
				new_region.bordures+=old_region.bordures
				#coos libres à remettre dans les dicos
				for i in coos_libres:
					self.dico_coos_regions[i]=new_region
				self.dico_regions_coos[new_region]+=coos_libres
					


				#on retire une unité à chaque node concerné par la bordure disparue
				self.nodes[bord[0]]-=1
				self.nodes[bord[1]]-=1

				#on supprime la bordure
				self.bordures.remove(bord)
				#! self.bordures n'est pas màj
			else:
				#print("pas supprimé")
				pass
		#print(len(self.bordures))
		#print(self.bordures)
	def coloriage(self):
		regions=[i for i in self.dico_regions_coos.keys()]
		used=[]
		for i in range(len(regions)):
			used.append([])
		i=0
		max=0
		compteur=0
		compteur_max=0
		while i!=len(regions):
			compteur+=1
			compteur_max+=1
			if i>max:
				max=i
				compteur_max=0
			if compteur_max>10:
				#print("plafond",max,compteur_max,used)
				pass
			#print(i)
			couleurs_voisins=[]
			
			for bord in regions[i].bordures:
				if bord[0][0]==bord[1][0]:
					#bordure verticale
					if self.dico_coos_regions[(bord[0][0]-0.5,(bord[0][1]+bord[1][1])/2)]==regions[i]:
						#le voisin est à droite de la bordure
						voisin=self.dico_coos_regions[(bord[0][0]+0.5,(bord[0][1]+bord[1][1])/2)]
					else:
						#le voisin est à gauche de la bordure
						voisin=self.dico_coos_regions[(bord[0][0]-0.5,(bord[0][1]+bord[1][1])/2)]
				else:
					#bordure horizontale
					if self.dico_coos_regions[((bord[0][0]+bord[1][0])/2,bord[0][1]-0.5)]==regions[i]:
						#le voisin est au dessus de la bordure
						voisin=self.dico_coos_regions[((bord[0][0]+bord[1][0])/2,bord[0][1]+0.5)]
					else:
						#le voisin est en dessous de la bordure
						voisin=self.dico_coos_regions[((bord[0][0]+bord[1][0])/2,bord[0][1]-0.5)]
				couleurs_voisins.append(voisin.color)
			#on prend la première couleur dispo
			for couleur in couleurs:
				if couleur not in couleurs_voisins and couleur not in used[i]:
					regions[i].color=couleur
					break
			#si pas de couleurs choisie on revient en arrière
			if regions[i].color=="brown":
				regions[i-1].color="brown"
				used[i].clear()
				i-=1
				#print("MOINS")
				if i<0:
					print("erreur i<0")
					break
			else:
				used[i].append(couleur)
				i+=1

class region:
	#les coos sont les centres des carrés composant l'aire de la région
	#exemple : [(0.5,0.5),(1.5,0.5)] est la région rectangulaire entre (0,0) et (2,1)
	def __init__(self,coordonnees):
		self.coos=[coordonnees]
		x=self.coos[0][0]
		y=self.coos[0][1]
		self.bordures=[]
		if x-1>0:
			self.bordures.append([(x-1/2,y-1/2),(x-1/2,y+1/2)])
		if x+1<taille_carte:
			self.bordures.append([(x+1/2,y-1/2),(x+1/2,y+1/2)])
		if y-1>0:
			self.bordures.append([(x-1/2,y-1/2),(x+1/2,y-1/2)])
		if y+1<taille_carte:
			self.bordures.append([(x-1/2,y+1/2),(x+1/2,y+1/2)])

		self.color="brown"

def save():
	img= ImageGrab.grab((500, 0, 2235, 1710)).save(str(datetime.now()).replace(":","-")[:-7]+" taille "+str(taille_carte)+".png")


fenetre = Tk()
fenetre.attributes('-fullscreen', True)
fenetre.bind('<Escape>',lambda e: fenetre.destroy())

Canevas = Canvas(fenetre, width=width, height=height)
Canevas.pack()

Bouton1 = Button(fenetre, text = 'Quitter', command = fenetre.destroy)
Bouton1.pack()

BoutonSave = Button(fenetre,  text = 'Save',  command = save)
BoutonSave.pack()

carte=carte(taille_carte)
carte.agrandissement_regions()
carte.affichage_init()
carte.affichage()
carte.coloriage()
carte.affichage()




fenetre.mainloop()