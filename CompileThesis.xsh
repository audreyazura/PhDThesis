#!/usr/local/bin/xonsh
import re
rm Thesis.tex
echo 'Old Thesis.tex deleted'
for i in range(1,7):
	num = '0' + str(i)
	fold = re.search(num + '-[a-zA-z-]{1,10}', $(ls))
	if fold:
		file = re.search(num + '-[a-zA-Z-]{4,8}.tex', $(ls @(fold.group())))
		if file:
			adress = fold.group() + '/' + file.group()
			with open(adress) as inpFile:
				for line in inpFile:
					shortline = re.sub(r"\n", "", line)
					lineGoodUpAdr = re.sub(r"\.\./", "", shortline)
					lineGoodAdr = re.sub(r"Pictures/", fold.group() + '/Pictures/', lineGoodUpAdr)
					if i == 1 && not(re.search(r'\\biblio', line) || re.search(r'\end{doc', line)):
						echo @(lineGoodAdr) >> Thesis.tex
					elif i == 5 && not(re.search(r'\\documentclass', line) || re.search(r'\\usepackage', line) || re.search(r'\makeat', line) || re.search(r'\\renewcommand', line) || re.search(r'\\begin{doc', line)):
						echo @(lineGoodAdr) >> Thesis.tex
					elif not(re.search(r'\\documentclass', line) || re.search(r'\\usepackage', line) || re.search(r'\makeat', line) || re.search(r'\\renewcommand', line) || re.search(r'\\begin{doc', line) || re.search(r'\\biblio', line) || re.search(r'\end{doc', line)):
						echo @(lineGoodAdr) >> Thesis.tex
					
			echo 'File ' @(file.group()) ' done'
