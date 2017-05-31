#!/usr/local/bin/xonsh

import re
#import antigravity

first = 1
maxCount = 5

!(del Thesis.tex)
print('Old Thesis.tex deleted')

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
enddocStr = re.compile(r'\\end{doc')
closebracStr = re.compile(r'\}')
docclassStr = re.compile(r'\\documentclass')
makeatStr = re.compile(r'\\makeat')
newcomStr = re.compile(r'\\renewcommand')
quoteStr = re.compile(r'\"')

with open('Thesis.tex', 'w') as Thesis:
        for i in range(first,maxCount):
        	num = '0' + str(i)
        	fold = re.search(num + '-[a-zA-z-]{1,10}', str(!(dir)))
        	if fold:
        		folder = fold.group()
        		pictureFold = folder + '/Pictures/'
        		cfile = re.search(num + '-[a-zA-Z-]{4,8}.tex', str(!(dir @(folder))))
        		if cfile:
        			searchedFile = folder + '/' + cfile.group()
        			with open(searchedFile, 'r') as inpFile:
                                        for line in inpFile:
        					if not(commentStr.search(line)):
        						treatedLine = pictureStr.sub(pictureFold, addrStr.sub(nullChain, newlineStr.sub(nullChain, line)))
                        				
                        				if i == first && not(printbibStr.search(treatedLine) || enddocStr.search(treatedLine)):
                        					print(treatedLine, file=Thesis)
                        					if usepackageStr.search(treatedLine):
                        						package = usepackageStr.sub(nullChain, closebracStr.sub( nullChain, treatedLine))
                        						packages.append(package)
                        						print('Package added: ' + package)
                        						lastPack+=1
                        						
                        				elif not(docclassStr.search(treatedLine) || makeatStr.search(treatedLine) || newcomStr.search(treatedLine) || begindocStr.search(treatedLine)):
                        					if usepackageStr.search(treatedLine):
                        						if not(any(s in line for s in packages)):
                        							package = usepackageStr.sub(nullChain, closebracStr.sub( nullChain, treatedLine))
                        							packages.append(package)
                        							print("Package added: " + package)
                        							lastPack+=1
                        							countLine = 1
                        							with open('Thesis.tex', 'r') as originThesis:
                                                                                        with open('copThesis.tex', 'w') as copiedThesis:
                                                                                                for copLine in originThesis:
                                                                                                        print(copLine)
                                                                                                	copTreatedLine = newlineStr.sub(nullChain, copLine)
                                                                                                	if countLine == lastPack:
                                                                                                		adLine = copTreatedLine + '\n' + treatedLine
                                                                                                		print(adLine, file=copiedThesis) 
                                                                                                	if countLine != lastPack:
                                                                                                		print(copTreatedLine, file=copiedThesis)
                                                                                                	countLine+=1
                        							#originThesis.close()
                        							#Thesis.close()
                        							#$(del Thesis.tex)
                        							#rename copThesis.tex Thesis.tex
                        							#Thesis = open('Thesis.tex', 'a')
                        						
                        					elif i == maxCount-1 && not(bibresStr.search(treatedLine)):
                        						print(treatedLine, file=Thesis)
                        					
                        					elif not(biblioStr.search(treatedLine) || enddocStr.search(treatedLine)):
                        						print(treatedLine, file=Thesis)
                        			
                        	print('File ' + cfile.group() + ' done')

print('\nLaunch compilation manually writing:\n')
print('pdflatex -synctex=1 -interaction=nonstopmode Thesis.tex')
print('pdflatex -synctex=1 -interaction=nonstopmode Thesis.tex')
print('biber Thesis')
print('pdflatex -synctex=1 -interaction=nonstopmode Thesis.tex\n')
