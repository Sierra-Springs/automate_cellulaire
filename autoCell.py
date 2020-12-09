# Automate Cellulaire supplémentaire.
# fait evoluer un système sur une dimension en fonction d'une règle de voisinnage
# le fichier de sortie correspond à l'evolution temporelle du systeme, ligne par ligne


# initialisation ([0, 0, ..., 1, 0, 0, ...])
table = [[0 for i in range(41)]]
table[0][20] = 1

# règle d'evolution en fonction des voisins
# ex: gauche==0, current==0, droite==1 -> "001" : 0 -> current =1
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
	'''fait evoluer le dernier état dans la liste L en fonction de la règle définie et l'ajoute à L'''
	L.append([])
	size = len(L[-2])
	for i in range(len(L[-2])):
		L[-1].append(rule[str(L[-2][i])+str(L[-2][(i-1)%size])+str(L[-2][(i+1)%size])])
		#print(str((i-1)%size)+)
		

colors = {0: "#328dc7", 1:"#c5a531", "C": "#25c7e0", "D": "#ffda55"}  # codes couleurs
def export_html(L):
	'''exporte une representation graphique du systeme en html'''
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
	with open("autoCell.html", "w") as fichier:
		fichier.write(html)

# génération de 20 étapes
for i in range(100):
	evolve(table)  # evolution du sytème
export_html(table)  # export de la représentation graphique au format html

# ouverture et affichage du fichier html :
# (nom du fichier : autoCell.html)
import ui,os
from urllib.parse import urljoin
import webbrowser
file_path = "autoCell.html"
file_path = urljoin("file://", os.path.abspath(file_path))
file_path = ('%20').join(file_path.split(' '))
print(file_path)
webbrowser.open(file_path)
