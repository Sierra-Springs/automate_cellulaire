import random
import time


def newCaseAlea():
	val = random.randrange(0, 2)
	if val == 0:
		return "A"
	if val == 1:
		return "V"


def evolve(AC):
	height = len(AC)
	width = len(AC[0])
	L = AC
	L.insert(0, ["V" for i in range(width)])
	L.append(["V" for i in range(width)])
	for i in L:
		i.insert(0, "V")
		i.append("V")
	newAC = [[] for i in range(height)]
	for i in range(1, height+1):
		for j in range(1, width+1):
			if L[i][j] in ["V", "C"]:
				newAC[i-1].append(L[i][j])
			elif L[i][j] == "F":
				newAC[i-1].append("C")
			else:
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
					newAC[i-1].append("F")
				else:
					newAC[i-1].append(L[i][j])
	return newAC
		

colors = {'A': "#32c73f", 'V':"#000000", 'F': "#f9d13e", 'C': "#a4a4a4"}
def export_html(L, file):
	html = "<!doctype html>\n"+"<html>\n"+"	<head>\n"
	html += '		<meta charset="utf-8">\n'+"	</head>\n"
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

height = 14
width = 35
AC = [[newCaseAlea() for i in range (width)] for j in range (height)]
AC[random.randrange(0, height)][random.randrange(0, width)] = "F"
print(AC)


nFrame = 0

while "F" in [AC[i][j] for i in range(len(AC)) for j in range(len(AC[i]))]:
	export_html(AC, "./view/export"+str(nFrame))
	AC = evolve(AC)
	nFrame += 1
export_html(AC, "./view/export"+str(nFrame))
print(nFrame)

# ouverture html :
import ui,os
from urllib.parse import urljoin
import webbrowser
for i in range(nFrame+1):
	file_path = "./view/export"+str(i)+".html"
	file_path = urljoin('file://', os.path.abspath(file_path))
	file_path = ('%20').join(file_path.split(' '))
	webbrowser.open(file_path)
	time.sleep(0.5)
