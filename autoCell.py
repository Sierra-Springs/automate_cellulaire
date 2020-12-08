table = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
rule = {
				"000" : 0,
				"001" : 1,
				"010" : 1,
				"011" : 0,
				"100" : 1,
				"101" : 0,
				"110" : 0,
				"111" : 1
				}

def evolve(L):
	L.append([])
	size = len(L[-2])
	for i in range(len(L[-2])):
		L[-1].append(rule[str(L[-2][i])+str(L[-2][(i-1)%size])+str(L[-2][(i+1)%size])])
		#print(str((i-1)%size)+)
		

colors = {0: "#328dc7", 1:"#c5a531", "C": "#25c7e0", "D": "#ffda55"}
def export_html(L):
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
	with open("export.html", "w") as fichier:
		fichier.write(html)

for i in range(20):
	evolve(table)		
export_html(table)

# ouverture html :
import ui,os
from urllib.parse import urljoin
import webbrowser
file_path = "export.html"
file_path = urljoin("file://", os.path.abspath(file_path))
file_path = ('%20').join(file_path.split(' '))
print(file_path)
webbrowser.open(file_path)
