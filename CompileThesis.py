#!/usr/local/bin/xonsh

import re

rm Thesis.tex
echo 'Old Thesis.tex deleted'
packages = []
lastPack = 2
for i in range(1,7):
	num = '0' + str(i)
	fold = re.search(num + '-[a-zA-z-]{1,10}', $(ls))
	if fold:
		cfile = re.search(num + '-[a-zA-Z-]{4,8}.tex', $(ls @(fold.group())))
		if cfile:
			with open(fold.group() + '/' + cfile.group(), 'r') as inpFile:
				for line in inpFile:
					if not(re.search(r'^%', line)):
						treatedLine = re.sub(r"Pictures/", fold.group() + '/Pictures/', re.sub(r"\.\./", "", re.sub(r"\n", "", line)))
						if i == 1 && not(re.search(r'\\biblio', treatedLine) || re.search(r'\end{doc', treatedLine)):
							echo @(treatedLine) >> Thesis.tex
							if re.search(r'^\\usepackage', treatedLine):
								packages.append(re.sub(r'\\usepackage(\[[\w=,]{1,50}\])?\{', '', re.sub(r'\}', '', treatedLine)))
								lastPack+=1
						elif i == 5 && not(re.search(r'\\documentclass', treatedLine) || re.search(r'\\usepackage', treatedLine) || re.search(r'\makeat', treatedLine) || re.search(r'\\renewcommand', treatedLine) || re.search(r'\\begin{doc', treatedLine)):
							echo @(treatedLine) >> Thesis.tex
						elif not(re.search(r'\\documentclass', treatedLine) || re.search(r'\\usepackage', treatedLine) || re.search(r'\makeat', treatedLine) || re.search(r'\\renewcommand', treatedLine) || re.search(r'\\begin{doc', treatedLine) || re.search(r'\\biblio', treatedLine) || re.search(r'\end{doc', treatedLine)):
							echo @(treatedLine) >> Thesis.tex
					
						if i != 1 && re.search(r'^\\usepackage', treatedLine) && not(any(s in line for s in packages)):
							packages.append(re.sub(r'\\usepackage(\[[\w=,]{1,50}\])?\{', '', re.sub(r'\}', '', treatedLine)))
							countLine = 1
							with open('Thesis.tex', 'r') as thesis:
								for copLine in thesis:
									copTreatedLine = re.sub(r"\n", "", copLine)
									if countLine == lastPack:
										adLine = copTreatedLine + '\n' + treatedLine
										echo @(adLine) >> copThesis.tex
									else:
										echo @(copTreatedLine) >> copThesis.tex
									countLine+=1
							lastPack+=1
							rm Thesis.tex
							mv copThesis.tex Thesis.tex
					
			echo 'File ' @(cfile.group()) ' done'

echo 'Starting latex compilation'
pdflatex -synctex=1 -interaction=nonstopmode Thesis.tex
bibtex Thesis.aux
pdflatex -synctex=1 -interaction=nonstopmode Thesis.tex
pdflatex -synctex=1 -interaction=nonstopmode Thesis.tex
evince Thesis.pdf
