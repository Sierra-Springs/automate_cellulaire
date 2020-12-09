import random
import time


def genRestricted(AC):
	# génère les zones interdites en formant des "taches"
	# remarque : les bords de ma map rebouclent pour la génération des ZI
	global width, height
	restrictedFactor = 1 # un facteur de présence (en °/300 (pour 300))
	for step in range((restrictedFactor*width*height)//300):
		i, j = random.randrange(0, height), random.randrange(0, width)  # choix une case au hasard
		AC[i][j] = "ZI"
		# pour une taille de tache de 40 à 70 cases (des cases peuvent se superposer)
		for step in range(random.randrange(40, 70)):
			change = 2*random.randrange(0,2)-1  # -1 ou +1
			dir = random.randrange(0, 2)  # direction horizontale: 0, verticale: 1
			if dir == 0:  # si horizontal
				j = (j+change)%width  # déplacement horizontal (+/-1)
			else:
				i = (i+change)%height  # déplacement vertical (+/-1)
			AC[i][j] = "ZI"  # ajoute une zone interdite au nouvel emplacement


def genUrban(AC):
	'''génère une zone urbaine au centre de la map.'''
	global width, height
	for i in range((5*height//10), (6*height//10)):
		for j in range((5*width//10), (6*width//10)):
			AC[i][j] = "U"
			


def genRoad(AC):
	'''génère des routes.
	une route va tout droit mais peut changer de direction abec une certaine probabilité.
	à chaque changement de direction, cette probabilité diminue.
	quand la route va tout droit, la probabilité de tourner augmente un peu jusqu'à une certaine limite '''
	global width, height
	chanceOfChange = 0.1  # probabilité de changer de direction
	roadPercent = 10  # pourcentage de cases routes disponibles (des cases peuvent se chevaucher)
	dir = random.randrange(0,4)  # 0:droite, 1:haut, 2:gauche, 3:bas (numéroté dans le sens trigonométrique) 
	#i, j = random.randrange(0, height), random.randrange(0, width)  # une case au hasard
	i, j = height//2, width//2  # la route part de la ville (pour la règle 2)
	AC[i][j] = "R"  # case route dans la ville
	# pour un certain nombre de cases en fonction de roadPercent :
	for step in range((roadPercent*width*height)//100):
		if random.uniform(0,1) < chanceOfChange:
			change = 2*random.randrange(0,2)-1  # changement de direction
			dir = (dir+change)%4  # on tourne à DROITE ou à GAUCHE quel que soit le sens actuel
			chanceOfChange -= 1  # chance de tourner diminue
		else:
			if chanceOfChange < 0.1:  # on continue tout droit
				chanceOfChange += 0.05  # chance de tourner augmente
		# détérmination des coordonnées de la nouvelle route
		if dir == 0:
			j = (j+1)%width
		elif dir == 1:
			i = (i-1)%height
		elif dir == 2:
			j = (j-1)%width
		elif dir == 3:
			i = (i+1)%height
		AC[i][j] = "R"  # création de la case route


def genAC(width, height):
	'''génère une ville'''
	AC = [["NU" for i in range (width)] for j in range (height)]  # zones non urbanisées : partout
	genRestricted(AC)  # zones interdites : par taches
	genUrban(AC)  # zones unbanisées : au centre
	genRoad(AC)  # routes : en lignes et virages
	return AC


def rule1(voisinage):
	'''Règle numéro 1 : urbanisation si nb de cases "U" adjacente >= 3 '''
	return voisinage.count("U") >= 3


def rule2(voisinage):
	'''Règle numéro 1 : urbanisation si nb de cases "U" adjacente >= 2 et de cases "R" >= 1
	Utilise un voisinage étendu à 25 voisins : 9 plus voisins plus leurs voisins.
	Le but est de pouvoir urbaniser l'autre côté d'une route par soucis de réalisme'''
	return voisinage.count("U") >= 2 and voisinage.count("R") >= 1


def evolve(AC):
	'''fait évoluer le système en fonction de la règle choisie (1 ou 2)'''
	global width, height, rule
	L = AC  # on crée une copie de AC
	# On encapsule l'automate pour éviter les "effets de bord" au sens propre : les bords de la map
	# 1 fois pour la règle 1, 2 fois pour la règles 2 qui utilise un voisinage étendu à 25 voisins
	for step in range(rule):  # encapsulation par des ZI (ZI tout autour de la map)
		L.insert(0, ["ZI" for i in range(len(L[0]))])
		L.append(["ZI" for i in range(len(L[0]))])
		for i in L:
			i.insert(0, "ZI")
			i.append("ZI")
	newAC = [[] for i in range(height)]  # nouvel etat du systeme
	for i in range(rule, height+rule):  # pour change indice i de ligne (offset car encaplusation)
		for j in range(rule, width+rule):  # pour chque indice j de colonne (offset car encapsulation)
			if L[i][j] in ["ZI", "R", "U"]:
				newAC[i-rule].append(L[i][j])  # si la case est ZI, R ou U, elle ne change pas
			else:
				# génération d'une liste des voisins: 9 ou 25 selon la règle
				# voir exrcice 2 pour un voisinage plus clair
				voisinage = [L[a][b] for a in range(i-rule, i+rule+1) for b in range(j-rule, j+rule+1) if not (a == i and b == j)]
				if (rule == 1 and rule1(voisinage)) or (rule == 2 and rule2(voisinage)):
					newAC[i-rule].append("U")  # si la règle est vérifiée : urbanisation
				else:
					newAC[i-rule].append(L[i][j])  # sinon la case ne change pas
	return newAC
		
# violet: ZI, gris: route, jaune: NU, orange: U
colors = {'U': "#f26200", 'NU':"#ffda55", 'ZI': "#dc00e6", 'R': "#818181"} # codes couleurs
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
		html += "			</tr>\n"
	html += "		</table>\n"+"	</body>\n"+"</html>"
	with open(file+".html", "w") as fichier:
		fichier.write(html)

rule = 0
while not rule in [1, 2]:
	rule = int(input('saisir le numero de la règle a utiliser (1 ou 2) : '))
height = 50  # hauteur de la ville (en nb de cases)
width = 100  # largeur de la ville (en nb de cases)
AC = genAC(width, height)  # génération de la configuration de base
prevAC = [] # état précédent. (cohérent car il n'y avait rien avant génération)
nFrame = 0
while AC != prevAC:  # tant que le système évolue
	export_html(AC, "./view/export"+str(nFrame))  # export html
	prevAC = [[a for a in b] for b in AC]  # sauvegarde de l'etat actuel
	AC = evolve(AC)  # evolution du système
	nFrame += 1
	print('itération ', nFrame)

# affichage de la simulation :
import ui,os
from urllib.parse import urljoin
import webbrowser
for frame in range(nFrame):
	file_path = "./view/export"+str(frame)+".html"
	file_path = urljoin('file://', os.path.abspath(file_path))
	file_path = ('%20').join(file_path.split(' '))
	webbrowser.open(file_path)
	time.sleep(1)
	

