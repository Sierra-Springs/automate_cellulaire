import random
import time


def newCaseAlea():
	val = random.uniform(0, 1)
	if val < 0.05:
		return "ZI"
	else:
		return "NU"


def genUrban(AC):
	global width, height
	for i in range((5*height//10), (6*height//10)):
		for j in range((5*width//10), (6*width//10)):
			AC[i][j] = "U"


def genRoad(AC):
	global width, height
	chanceOfChange = 0.10
	roadPercent = 15
	dir = 0
	#i, j = random.randrange(0, height), random.randrange(0, width)
	i, j = height//2, width//2
	AC[i][j] = "R"
	for step in range((roadPercent*width*height)//100):
		if random.uniform(0,1) < chanceOfChange:
			change = 2*random.randrange(0,2)-1
			dir = (dir+change)%4
			chanceOfChange -= 0.5
		else:
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
	AC = [[newCaseAlea() for i in range (width)] for j in range (height)]
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
	L.insert(0, ["ZI" for i in range(width)])
	L.append(["ZI" for i in range(width)])
	for i in L:
		i.insert(0, "ZI")
		i.append("ZI")
	newAC = [[] for i in range(height)]
	size = 10
	for i in range(1, height+1):
		for j in range(1, width+1):
			if L[i][j] in ["ZI", "R", "U"]:
				newAC[i-1].append(L[i][j])
			else:
				voisinage = [L[a][b] for a in range(i-1, i+2) for b in range(j-1, j+2) if not (a == i and b == j)]
				if (rule == 1 and rule1(voisinage)) or (rule == 2 and rule2(voisinage)):
					newAC[i-1].append("U")
				else:
					newAC[i-1].append(L[i][j])
	return newAC
		

colors = {'U': "#f26200", 'NU':"#ffda55", 'ZI': "#dc00e6", 'R': "#818181"}
def export_html(L, file):
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


rule = 2
height = 50#22
width = 100#42
AC = genAC(width, height)
prevAC = []
i = 0
while AC != prevAC:
	export_html(AC, "./view/export"+str(i))
	prevAC = [[a for a in b] for b in AC]
	AC = evolve(AC)
	i += 1

# ouverture html :
import ui,os
from urllib.parse import urljoin
import webbrowser
for frame in range(i):
	file_path = "./view/export"+str(frame)+".html"
	file_path = urljoin('file://', os.path.abspath(file_path))
	file_path = ('%20').join(file_path.split(' '))
	webbrowser.open(file_path)
	time.sleep(1)
	

