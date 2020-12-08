import random
import time

def newCaseAlea():
	val = random.randrange(0, 4)
	if val == 0:
		return "U"
	if val == 1:
		return "NU"
	if val == 2:
		return "ZI"
	if val == 3:
		return "R"

	
rulesForU = [
							["U", "U", "U", "U"],
							["NU", "U", "U", "U"],
							["RU", "U", "U", "U"],
							["U", "U", "U", "ZI"]
						]

def evolve(L):
	newCA = [[] for i in range(10)]
	size = 10
	for i in range(size):
		for j in range(size):
			if L[i][j] in ["ZI", "R", "U"]:
				newCA[i].append(L[i][j])
			else:
				voisinage = [
											L[(i-1)%size][j],
											L[i][(j-1)%size],
											L[i][(j+1)%size],
											L[(i+1)%size][j]
										]
				if sorted(voisinage) in rulesForU:
					newCA[i].append("U")
				else:
					newCA[i].append(L[i][j])
	return newCA
		

colors = {'U': "#328dc7", 'NU':"#c5a531", 'ZI': "#25c7e0", 'R': "#ffda55"}
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
	file_path = ('%20').join(file_path.split(' '))
	print(file_path)
	webbrowser.open(file_path)
	time.sleep(1)
	

