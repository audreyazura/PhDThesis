#!/usr/local/bin/xonsh

import re

rm Thesis.tex
echo 'Old Thesis.tex deleted'

packages = []
lastPack = 2

nullChain = ''
commentStr = re.compile(r'^%')
pictureStr = re.compile(r"Pictures/")
addrStr = re.compile(r"\.\./")
newlineStr = re.compile(r"\n")
usepackageStr = re.compile(r'\\usepackage(\[[\w=,]{1,50}\])?\{')
biblioStr = re.compile(r'\\biblio')
begindocStr = re.compile(r'\\begin{doc')
enddocStr = re.compile(r'\end{doc')
closebracStr = re.compile(r'\}')
docclassStr = re.compile(r'\\documentclass')
makeatStr = re.compile(r'\makeat')
newcomStr = re.compile(r'\\renewcommand')

for i in range(1,7):
	num = '0' + str(i)
	fold = re.search(num + '-[a-zA-z-]{1,10}', $(ls))
	if fold:
		folder = fold.group()
		pictureFold = folder + '/Pictures/'
		cfile = re.search(num + '-[a-zA-Z-]{4,8}.tex', $(ls @(folder)))
		if cfile:
			searchedFile = folder + '/' + cfile.group()
			with open(searchedFile, 'r') as inpFile:
				for line in inpFile:
					if not(commentStr.search(line)):
						treatedLine = pictureStr.sub(pictureFold, addrStr.sub(nullChain, newlineStr.sub(nullChain, line)))
						
						if i == 1 && not(biblioStr.search(treatedLine) || enddocStr.search(treatedLine)):
							echo @(treatedLine) >> Thesis.tex
							if usepackageStr.search(treatedLine):
								packages.append(usepackageStr.sub(nullChain, closebracStr.sub( nullChain, treatedLine)))
								lastPack+=1
								
						elif not(docclassStr.search(treatedLine) || makeatStr.search(treatedLine) || newcomStr.search(treatedLine) || begindocStr.search(treatedLine)):
							if usepackageStr.search(treatedLine):
								if not(any(s in line for s in packages)):
									packages.append(usepackageStr.sub(nullChain, closebracStr.sub(nullChain, treatedLine)))
									countLine = 1
									with open('Thesis.tex', 'r') as thesis:
										for copLine in thesis:
											copTreatedLine = newlineStr.sub(nullChain, copLine)
											if countLine == lastPack:
												adLine = copTreatedLine + '\n' + treatedLine
												echo @(adLine) >> copThesis.tex
											else:
												echo @(copTreatedLine) >> copThesis.tex
											countLine+=1
									lastPack+=1
									rm Thesis.tex
									mv copThesis.tex Thesis.tex
								
							elif i == 5:
								echo @(treatedLine) >> Thesis.tex
							
							elif not(biblioStr.search(treatedLine) || enddocStr.search(treatedLine)):
								echo @(treatedLine) >> Thesis.tex
					
			echo 'File ' @(cfile.group()) ' done'

echo 'Starting latex compilation'
pdflatex -synctex=1 -interaction=nonstopmode Thesis.tex
bibtex Thesis.aux
pdflatex -synctex=1 -interaction=nonstopmode Thesis.tex
pdflatex -synctex=1 -interaction=nonstopmode Thesis.tex
evince Thesis.pdf
