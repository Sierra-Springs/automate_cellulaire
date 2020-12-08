import random
import time

def newCaseAlea():
	val = random.uniform(0, 1)
	if val < 0.30:
		return "U"
	if 0.30 <= val and val < 0.70:
		return "NU"
	if 0.70 <= val and val < 0.90 :
		return "ZI"
	if val >= 0.90:
		return "R"


def evolve(CA):
	height = len(CA)
	width = len(CA[0])
	L = CA
	L.insert(0, ["ZI" for i in range(width)])
	L.append(["ZI" for i in range(width)])
	for i in L:
		i.insert(0, "ZI")
		i.append("ZI")
	newCA = [[] for i in range(height)]
	size = 10
	for i in range(1, height+1):
		for j in range(1, width+1):
			if L[i][j] in ["ZI", "R", "U"]:
				newCA[i-1].append(L[i][j])
			else:
				voisinage = [L[a%height][b%width] for a in range(i-1, i+2) for b in range(j-1, j+2) if not (a == i and b == j)]
				if voisinage.count("U") >= 3:
					newCA[i-1].append("U")
				else:
					newCA[i-1].append(L[i][j])
	return newCA
		

colors = {'U': "#f26200", 'NU':"#ffda55", 'ZI': "#dc00e6", 'R': "#818181"}
def export_html(L, file):
	html = "<!doctype html>\n"+"<html>\n"+"	<head>\n"
	html += '		<meta charset="utf-8">\n'+"	</head>\n"
	html += "	<body>\n"+'		<table border="0">\n'
	for i in L:
		html += "			<tr>\n"
		for j in i:
			html += '				<td bgcolor="'+colors[j]+'">'+"<pre> "+str(j)+" </pre>"+"</td>\n"
		html += "			</tr>\n"
	html += "		</table>\n"+"	</body>\n"+"</html>"
	with open(file+".html", "w") as fichier:
		fichier.write(html)


height = 14
width = 30
AC = [[newCaseAlea() for i in range (width)] for j in range (height)]
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
	

