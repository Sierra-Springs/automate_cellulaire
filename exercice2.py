import random
import time

def newCaseAlea():
	val = random.randrange(0, 3)
	if val == 0:
		return "A"
	if val == 1:
		return "A"
	if val == 2:
		return "V"

def evolve(L):
	newCA = [[] for i in range(10)]
	size = len(newCA)
	for i in range(size):
		for j in range(size):
			if L[i][j] in ["V", "C"]:
				newCA[i].append(L[i][j])
			elif L[i][j] == "F":
				newCA[i].append("C")
			else:
				voisinage = [
											L[(i-1)%size][(j-1)%size],
											L[(i-1)%size][j],
											L[(i-1)%size][(j+1)%size],
											L[i][(j-1)%size],
											L[i][(j+1)%size],
											L[(i+1)%size][(j-1)%size],
											L[(i+1)%size][j],
											L[(i+1)%size][(j+1)%size]
										]
				if "F" in voisinage:
					newCA[i].append("F")
				else:
					newCA[i].append(L[i][j])
	return newCA
		

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


AC = [[newCaseAlea() for i in range (10)] for j in range (10)]
AC[random.randrange(0, 10)][random.randrange(0, 10)] = "F"
print(AC)

for i in range(10):
	export_html(AC, "./view/export"+str(i))
	AC = evolve(AC)

# ouverture html :
import ui,os
from urllib.parse import urljoin
import webbrowser
for i in range(10):
	file_path = "./view/export"+str(i)+".html"
	file_path = urljoin('file://', os.path.abspath(file_path))
	#print(file_path)
	webbrowser.open(file_path)
	time.sleep(1)
