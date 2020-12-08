import random
import time


def genRestricted(AC):
	global width, height
	restrictedFactor = 1
	for step in range((restrictedFactor*width*height)//300):
		i, j = random.randrange(0, height), random.randrange(0, width)
		AC[i][j] = "ZI"
		for step in range(random.randrange(5, 70)):
			change = 2*random.randrange(0,2)-1
			dir = random.randrange(0, 2)
			if dir == 0:
				j = (j+change)%width
			else:
				i = (i+change)%height
			AC[i][j] = "ZI"


def genUrban(AC):
	global width, height
	for i in range((5*height//10), (6*height//10)):
		for j in range((5*width//10), (6*width//10)):
			AC[i][j] = "U"
			


def genRoad(AC):
	global width, height
	chanceOfChange = 0.1
	roadPercent = 10
	dir = random.randrange(0,4)
	#i, j = random.randrange(0, height), random.randrange(0, width)
	i, j = height//2, width//2
	AC[i][j] = "R"
	for step in range((roadPercent*width*height)//100):
		if random.uniform(0,1) < chanceOfChange:
			change = 2*random.randrange(0,2)-1
			dir = (dir+change)%4
			chanceOfChange -= 1
		else:
			if chanceOfChange < 0.1:
				chanceOfChange += 0.05
		if dir == 0:
			j = (j+1)%width
		elif dir == 1:
			i = (i-1)%height
		elif dir == 2:
			j = (j-1)%width
		elif dir == 3:
			i = (i+1)%height
		AC[i][j] = "R"


def genAC(width, height):
	AC = [["NU" for i in range (width)] for j in range (height)]
	genRestricted(AC)
	genUrban(AC)
	genRoad(AC)
	return AC


def rule1(voisinage):
	return voisinage.count("U") >= 3


def rule2(voisinage):
	return voisinage.count("U") >= 2 and voisinage.count("R") >= 1


def evolve(AC):
	global width, height, rule
	L = AC
	for step in range(rule):
		L.insert(0, ["ZI" for i in range(len(L[0]))])
		L.append(["ZI" for i in range(len(L[0]))])
		for i in L:
			i.insert(0, "ZI")
			i.append("ZI")
	newAC = [[] for i in range(height)]
	size = 10
	for i in range(rule, height+rule):
		for j in range(rule, width+rule):
			if L[i][j] in ["ZI", "R", "U"]:
				newAC[i-rule].append(L[i][j])
			else:
				voisinage = [L[a][b] for a in range(i-rule, i+rule+1) for b in range(j-rule, j+rule+1) if not (a == i and b == j)]
				if (rule == 1 and rule1(voisinage)) or (rule == 2 and rule2(voisinage)):
					newAC[i-rule].append("U")
				else:
					newAC[i-rule].append(L[i][j])
	return newAC
		

colors = {'U': "#f26200", 'NU':"#ffda55", 'ZI': "#dc00e6", 'R': "#818181"}
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
height = 50
width = 100
AC = genAC(width, height)
prevAC = []
i = 0
while AC != prevAC:
	export_html(AC, "./view/export"+str(i))
	prevAC = [[a for a in b] for b in AC]
	AC = evolve(AC)
	i += 1

# affichage de la simulation :
import ui,os
from urllib.parse import urljoin
import webbrowser
for frame in range(i):
	file_path = "./view/export"+str(frame)+".html"
	file_path = urljoin('file://', os.path.abspath(file_path))
	file_path = ('%20').join(file_path.split(' '))
	webbrowser.open(file_path)
	time.sleep(1)
	

