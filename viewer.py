import os, sys
from urllib.parse import urljoin
import webbrowser
import time

i = 0
while 1:
	file_path = os.path.dirname(sys.argv[0])+"/view/export"+str(i)+".html"
	#print(file_path)
	file_path = urljoin('file://', os.path.abspath(file_path))
	file_path = ('%20').join(file_path.split(' '))
	webbrowser.open(file_path)
	if i%5 == 0:
		b = input("ss")
	time.sleep(3)
	i += 1
