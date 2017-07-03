#!/usr/local/bin/xonsh

import re
#import antigravity

packages = []
lastPack = 2

nullChain = ''
keepingLine = re.compile(r'^[\t {]*\\')
newlineStr = re.compile(r"\n")
beginnewStr = re.compile(r'^\n')

#inpChap = input("Chapter to empty: ")
inpChap = '5'
num = '0' + inpChap

fold = re.search(num + '-[a-zA-z-]{1,10}', str(!(dir)))
if fold:
	folder = fold.group()
	pictureFold = folder + '/Pictures/'
	cfile = re.search(num + '-[a-zA-Z-]{4,8}.tex', str(!(dir @(folder))))
	if cfile:
		searchedFile = folder + '/' + cfile.group()
		
		outString = folder + '/' + 'NoTxt_' + cfile.group()
		!(del @(outString + '.tex'))
		print('Old ' + cfile.group() + '.tex deleted')
		chapter = open(outString, 'w')
		with open(searchedFile, 'r') as inpFile:
			for line in inpFile:
				if keepingLine.search(line):
					treatedLine = newlineStr.sub(nullChain, line)
					print(treatedLine, file=chapter)

chapter.close()
print('\nLaunch compilation manually writing:\n')
print('pdflatex -synctex=1 -interaction=nonstopmode ' + outString)
print('biber Thesis')
print('pdflatex -synctex=1 -interaction=nonstopmode ' + outString)
print('pdflatex -synctex=1 -interaction=nonstopmode ' + outString + '\n')
