from tkinter import * 
import random

width=600
height=width
taille_carte=10
unite=width/(taille_carte+2)
moitie_carre=(unite)/2
x0=unite
y0=height-unite
taux_suppr_bordures=0.7
couleurs=["red","blue","green","brown"]

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
		
	def creation_regions(self):
		#print(len(self.bordures))
		for bord in self.bordures:
			print(bord,self.nodes[bord[0]],self.nodes[bord[1]])
			if self.nodes[bord[0]]==2 or self.nodes[bord[1]]==2:
				print("on passe car node=2")
				continue
			if random.random()<taux_suppr_bordures:
				print("supprimé")
				#on récupère les coos du carré de région situé à côté de la bordure
				if bord[0][0]==bord[1][0]:
					#print("vertical")
					region_suppr=(bord[0][0]-0.5,(bord[0][1]+bord[1][1])/2)
					region_new=(bord[0][0]+0.5,(bord[0][1]+bord[1][1])/2)
				else:
					#print("horizontal")
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

				#voisins
				new_region.voisins_coos.remove(coos_libres)
				old_region.voisins_coos.remove(self.dico_regions_coos[new_region])
				anciennes_cos=self.dico_regions_coos[new_region][:]
				anciennes_voisins_cos=new_region.voisins_coos[:]
				for voisin in old_region.voisins_coos:
					if voisin not in new_region.voisins_coos:
						new_region.voisins_coos.append(voisin)
				#là new region a pour voisin les siens et ceux de old region
				#coos libres à remettre dans les dicos
				for i in coos_libres:
					self.dico_coos_regions[i]=new_region
				self.dico_regions_coos[new_region]+=coos_libres
				#màj des voisins de old_region et new_region
				for voisin in new_region.voisins_coos:
					if coos_libres in self.dico_coos_regions[voisin[0]].voisins_coos:
						self.dico_coos_regions[voisin[0]].voisins_coos.remove(coos_libres)
						self.dico_coos_regions[voisin[0]].voisins_coos.append(self.dico_regions_coos[new_region])
					elif anciennes_cos in self.dico_coos_regions[voisin[0]].voisins_coos:
						self.dico_coos_regions[voisin[0]].voisins_coos.remove(anciennes_cos)
						self.dico_coos_regions[voisin[0]].voisins_coos.append(self.dico_regions_coos[new_region])
					else:
						print(new_region.voisins_coos)
						print(voisin,self.dico_coos_regions[voisin[0]].voisins_coos)
						print(coos_libres,anciennes_cos)
						print("erreur")
					#self.dico_coos_regions[voisin[0]].voisins_coos.append(self.dico_regions_coos[new_region])
					


				#on retire une unité à chaque node concerné par la bordure disparue
				self.nodes[bord[0]]-=1
				self.nodes[bord[1]]-=1

				#on supprime la bordure
				self.bordures.remove(bord)
			else:
				print("pas supprimé")
		#print(len(self.bordures))
		#print(self.bordures)
	def coloriage(self):
		regions=[i for i in self.dico_regions_coos.keys()]
		used=[]
		for i in range(len(regions)):
			used.append([])
		i=0
		while i!=len(regions):
			couleurs_voisins=[]
			en_cours=regions[i]
			for voisin_coo in regions[i].voisins_coos:
				#print(regions[i].voisins_coos,voisin_coo)
				#print(self.dico_coos_regions[voisin_coo[0]])
				couleurs_voisins.append(self.dico_coos_regions[voisin_coo[0]].color)
			#on prend la première couleur dispo
			for couleur in couleurs:
				if couleur not in couleurs_voisins and couleur not in used[i]:
					regions[i].color=couleur
					break
			#si pas de couleurs choisie on revient en arrière
			if regions[i].color=="purple":
				regions[i-1].color="purple"
				i-=1
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
		self.voisins_coos=[]
		if x-1>0:
			self.bordures.append([(x-1/2,y-1/2),(x-1/2,y+1/2)])
			self.voisins_coos.append([(x-1,y)])
		if x+1<taille_carte:
			self.bordures.append([(x+1/2,y-1/2),(x+1/2,y+1/2)])
			self.voisins_coos.append([(x+1,y)])
		if y-1>0:
			self.bordures.append([(x-1/2,y-1/2),(x+1/2,y-1/2)])
			self.voisins_coos.append([(x,y-1)])
		if y+1<taille_carte:
			self.bordures.append([(x-1/2,y+1/2),(x+1/2,y+1/2)])
			self.voisins_coos.append([(x,y+1)])

		self.color="purple"


fenetre = Tk()

Canevas = Canvas(fenetre, width=width, height=height)
Canevas.pack()

Bouton1 = Button(fenetre, text = 'Quitter', command = fenetre.destroy)
Bouton1.pack()

carte=carte(taille_carte)
carte.creation_regions()
carte.affichage_init()
carte.affichage()
carte.coloriage()
carte.affichage()



fenetre.mainloop()