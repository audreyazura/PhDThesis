#!/usr/local/bin/xonsh

import re
#import antigravity

####################### PARAMETERS #######################

first = 1
maxCount = 5
ignoreLorem = True

########################## CODE ##########################

rm Thesis.tex
echo 'Old Thesis.tex deleted'

packages = []
lastPack = 2

nullChain = ''
commentStr = re.compile(r'^%')
pictureStr = re.compile(r"Pictures/")
addrStr = re.compile(r"\.\./")
newlineStr = re.compile(r"\n")
usepackageStr = re.compile(r'\\usepackage(\[[\w=,\{\}]{1,50}\])?\{')
biblioStr = re.compile(r'[b,B]iblio')
printbibStr = re.compile(r'\\printbiblio')
bibresStr = re.compile(r'\\addbibres')
begindocStr = re.compile(r'\\begin{doc')
enddocStr = re.compile(r'\end{doc')
closebracStr = re.compile(r'\}')
docclassStr = re.compile(r'\\documentclass')
makeatStr = re.compile(r'\makeat')
newcomStr = re.compile(r'\\renewcommand')
floatsetStr = re.compile(r'\\floatsetup')

if ignoreLorem:
	loremStr = re.compile(r'Lorem')
	curabiturStre = re.compile(r'Curabitur')
	lipsumStr = re.compile(r'ipsum')

Thesis = open('Thesis.tex', 'w')
for i in range(first,maxCount+1):
#for i in [first, maxCount-1]:
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
					if not(commentStr.search(line) || (ignoreLorem && (loremStr.search(line) || curabiturStre.search(line) || lipsumStr.search(line)))):
						treatedLine = pictureStr.sub(pictureFold, addrStr.sub(nullChain, newlineStr.sub(nullChain, line)))
						
						#first file: we print all the package and add it to the package library
						if i == first && not(printbibStr.search(treatedLine) || enddocStr.search(treatedLine)):
							print(treatedLine, file=Thesis)
							if usepackageStr.search(treatedLine):
								package = usepackageStr.sub(nullChain, closebracStr.sub( nullChain, treatedLine))
								packages.append(package)
#								print("Package added: " + package)
								lastPack+=1
								
						#for all other file, we ignore the header, but will have to test if a new package is introduced
						elif not(docclassStr.search(treatedLine) || makeatStr.search(treatedLine) || newcomStr.search(treatedLine) || begindocStr.search(treatedLine) || floatsetStr.search(treatedLine)):
							
							#if we find a new package, we have to add it to the header and to the list of used package
							if usepackageStr.search(treatedLine):
								if not(any(s in line for s in packages)):
									package = usepackageStr.sub(nullChain, closebracStr.sub( nullChain, treatedLine))
									packages.append(package)
#									print("Package added: " + package)
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
							
							#for the last file, we print all the line with the exception above, and have to not ignore the printbiblio and end{document}
							elif i == maxCount-1 && not(bibresStr.search(treatedLine)):
								print(treatedLine, file=Thesis)
							
							#for all the other line in any file, we just ignore the printbiblio and end{document}, and print otherwise
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
