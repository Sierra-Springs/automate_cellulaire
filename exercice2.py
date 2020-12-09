import random
import time


def genEmpty(AC):
	'''génère des cases vides par tâches (clairières, rocher, etc)'''
	global width, height
	restrictedFactor = 3  # facteur de présence
	for step in range((restrictedFactor*width*height)//300):
		i, j = random.randrange(0, height), random.randrange(0, width)  # choix d'une case au hasard
		AC[i][j] = "V"  # la case choisie est un arbre
		for step in range(random.randrange(50, 70)):  # tâches de 50-70 arbres (des cases peuvent se superposer)
			change = 2*random.randrange(0,2)-1  # -1 ou 1
			dir = random.randrange(0, 2)  # direction horizontale: 0, verticale: 1
			if dir == 0:  # si horizontal
				j = (j+change)%width  # déplacement horizontal (+/-1)
			else:
				i = (i+change)%height  # déplacement vertical (+/-1)
			AC[i][j] = "V"  # ajoute un arbre au nouvek emplacement


def evolve(AC):
	'''fait évoluer le système'''
	global height, width
	L = AC  # copie du systeme
	# On encapsule l'automate pour éviter les "effets de bord" au sens propre : les bords de la map
	L.insert(0, ["V" for i in range(width)])
	L.append(["V" for i in range(width)])
	for i in L:
		i.insert(0, "V")
		i.append("V")
	newAC = [[] for i in range(height)]  # nouvel etat
	for i in range(1, height+1):  # pour change indice i de ligne (offset car encaplusation)
		for j in range(1, width+1):  # pour chque indice j de colonne (offset car encapsulation)
			if L[i][j] in ["V", "C"]:
				newAC[i-1].append(L[i][j])  # les arbres et cendres ne changent 
			elif L[i][j] == "F":
				newAC[i-1].append("C")  # si la case est en feu, elle devient cendre
			else:
				# voir exercice 1 pour une methode de contruction plus efficace
				voisinage = [
											L[(i-1)][(j-1)],
											L[(i-1)][j],
											L[(i-1)][(j+1)],
											L[i][(j-1)],
											L[i][(j+1)],
											L[(i+1)][(j-1)],
											L[(i+1)][j],
											L[(i+1)][(j+1)]
										]
				if "F" in voisinage:
					newAC[i-1].append("F")  # si un arbre voisin est en feu, l'arbre prends feu
				else:
					newAC[i-1].append(L[i][j])  # sinon l'arbre de change pas'
	return newAC
		

# vert: arbre, blanc/gris: vide, jaune: feu, gris: cendres
colors = {'A': "#32c73f", 'V':"#e6e6e6", 'F': "#f9d13e", 'C': "#a4a4a4"}  # code couleur
def export_html(L, file):
	'''exporte la simulation pour affichage'''
	html = "<!doctype html>\n"+"<html>\n"+"	<head>\n"
	html += '		<meta charset="utf-8">\n'
	html += "<style>*{zoom: 75%;}</style>"
	html += "	</head>\n"
	html += "	<body>\n"+'		<table border="0">\n'
	for i in L:
		html += "			<tr>\n"
		for j in i:
			html += '				<td bgcolor="'+colors[j]+'">'+"<pre> "+str(j)+" </pre>"+"</td>\n"
			#html += "				<td><pre>  </pre></td>\n"
		html += "			</tr>\n"
	html += "		</table>\n"+"	</body>\n"+"</html>"
	with open(file+".html", "w") as fichier:
		fichier.write(html)

height = 40  # hauteur de la ville (en nb de cases)
width = 100  # largeur de la ville (en nb de cases)
AC = [["A" for i in range (width)] for j in range (height)]  # etat inital 1 (arbres partout)
genEmpty(AC)  # ajout des cases vides
AC[random.randrange(0, height)][random.randrange(0, width)] = "F"  # un départ de feu aléatoire


# simulation
nFrame = 0
while "F" in [AC[i][j] for i in range(len(AC)) for j in range(len(AC[i]))]:  # tant qu'il y a du feu
	export_html(AC, "./view/export"+str(nFrame))  # export html
	AC = evolve(AC)  # evolution du système
	nFrame += 1
	print('itération ', nFrame)
export_html(AC, "./view/export"+str(nFrame))  # dernier export html

# affichage de la simulation:
import ui,os
from urllib.parse import urljoin
import webbrowser
for i in range(nFrame+1):
	file_path = "./view/export"+str(i)+".html"
	file_path = urljoin('file://', os.path.abspath(file_path))
	file_path = ('%20').join(file_path.split(' '))
	webbrowser.open(file_path)
	time.sleep(1)
