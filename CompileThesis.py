#!/usr/local/bin/xonsh

import re
#import antigravity

ignoreLorem = True
rm Thesis.tex
echo 'Old Thesis.tex deleted'

first = 1
maxCount = 5

packages = []
lastPack = 2

nullChain = ''
commentStr = re.compile(r'^%')
pictureStr = re.compile(r"Pictures/")
addrStr = re.compile(r"\.\./")
newlineStr = re.compile(r"\n")
usepackageStr = re.compile(r'\\usepackage(\[[\w=,]{1,50}\])?\{')
biblioStr = re.compile(r'[b,B]iblio')
printbibStr = re.compile(r'\\printbiblio')
bibresStr = re.compile(r'\\addbibres')
begindocStr = re.compile(r'\\begin{doc')
enddocStr = re.compile(r'\end{doc')
closebracStr = re.compile(r'\}')
docclassStr = re.compile(r'\\documentclass')
makeatStr = re.compile(r'\makeat')
newcomStr = re.compile(r'\\renewcommand')

if ignoreLorem:
	loremStr = re.compile(r'Lorem')
	curabiturStre = re.compile(r'Curabitur')

Thesis = open('Thesis.tex', 'w')
#for i in range(first,maxCount):
for i in [first, maxCount-1]:
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
					if not(commentStr.search(line) || (ignoreLorem && (loremStr.search(line) || curabiturStre.search(line)))):
						treatedLine = pictureStr.sub(pictureFold, addrStr.sub(nullChain, newlineStr.sub(nullChain, line)))
						
						if i == first && not(printbibStr.search(treatedLine) || enddocStr.search(treatedLine)):
							print(treatedLine, file=Thesis)
							if usepackageStr.search(treatedLine):
								package = usepackageStr.sub(nullChain, closebracStr.sub( nullChain, treatedLine))
								packages.append(package)
								print("Package added: " + package)
								lastPack+=1
								
						elif not(docclassStr.search(treatedLine) || makeatStr.search(treatedLine) || newcomStr.search(treatedLine) || begindocStr.search(treatedLine)):
							if usepackageStr.search(treatedLine):
								if not(any(s in line for s in packages)):
									package = usepackageStr.sub(nullChain, closebracStr.sub( nullChain, treatedLine))
									packages.append(package)
									print("Package added: " + package)
									lastPack+=1
									countLine = 1
									Thesis.close()
									with open('Thesis.tex', 'r') as refThesis:
										with open('copThesis.tex', 'w') as copiedThesis:
											for copLine in refThesis:
												copTreatedLine = newlineStr.sub(nullChain, copLine)
												if countLine == lastPack:
													adLine = copTreatedLine + '\n' + treatedLine
													print(adLine, file=copiedThesis)
												else:
													print(copTreatedLine, file=copiedThesis)
												countLine+=1
									rm Thesis.tex
									mv copThesis.tex Thesis.tex
									Thesis = open('Thesis.tex', 'a')
							
							elif i == maxCount-1 && not(bibresStr.search(treatedLine)):
								print(treatedLine, file=Thesis)
							
							elif not(biblioStr.search(treatedLine) || enddocStr.search(treatedLine)):
								print(treatedLine, file=Thesis)
				
			print('File ' + cfile.group() + ' done')

Thesis.close()
print('\nLaunch compilation manually writing:\n')
print('pdflatex -synctex=1 -interaction=nonstopmode Thesis.tex')
print('biber Thesis')
print('pdflatex -synctex=1 -interaction=nonstopmode Thesis.tex')
print('pdflatex -synctex=1 -interaction=nonstopmode Thesis.tex')
print('evince Thesis.pdf\n')
