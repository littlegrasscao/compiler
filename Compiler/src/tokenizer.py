# -*- coding: utf-8 -*-

#translate text into tokens
def TokenTranslate(text):
	keyword = ['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
	symbol = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
	tokendic = {'keyword':['<keyword>','</keyword>'],'symbol':['<symbol>','</symbol>'],'integerConstant':['<integerConstant>','</integerConstant>'],'stringConstant':['<stringConstant>','</stringConstant>'],'identifier':['<identifier>','</identifier>']}

	#print(text)

	separate = []
	i = 0  #index
	countstr = 0 #count the number of "
	for j in range(len(text)):
		#decide if current visited j is in a string
		if text[j] == '"':
			countstr += 1
			#add string into separate
			if countstr%2 == 0:
				separate.append(text[i:j+1])
				i = j+1

		#separate every word by a space or a symbol
		if countstr%2 == 0 and (text[j] == ' ' or text[j] in symbol):
			separate.append(text[i:j])
			i = j+1
			#append symbols 
			if text[j] in symbol:
				separate.append(text[j])

	#print(separate)


	token = [] #store parser output

	#make each word into a token
	for word in separate:
		if word in keyword:
			token.append(tokendic['keyword'][0])
			token.append(word)
			token.append(tokendic['keyword'][1])
			token.append('\n')
		elif word in symbol:
			token.append(tokendic['symbol'][0])
			if word == '<':
				token.append('&lt;')
			elif word == '>':
				token.append('&gt;')
			elif word == '&':
				token.append('&amp;')
			else:
				token.append(word)
			token.append(tokendic['symbol'][1])
			token.append('\n')	
		elif word and word[0]=='"' and word[-1]=='"':
			token.append(tokendic['stringConstant'][0])
			token.append(word[1:-1])
			token.append(tokendic['stringConstant'][1])
			token.append('\n')				
		elif word.isdigit():
			token.append(tokendic['integerConstant'][0])
			token.append(word)
			token.append(tokendic['integerConstant'][1])
			token.append('\n')
		elif word:
			token.append(tokendic['identifier'][0])
			token.append(word)
			token.append(tokendic['identifier'][1])
			token.append('\n')			

	#print(token)

	#return token in separate lines
	output = []
	tmp = []
	for i in token:
		if i == '\n':
			output.append(tmp)
			tmp=[]
		else:
			tmp.append(i)

	return output



#function used to filter file
def filterfile(filename):
	#open input file and filter each line
	text=[]
	#print a error statement if the address is invalid and exit
	try:
		f=open(filename,'r')
	except:
		print('Error! Can not open %s!'%filename)
		exit(0);

	#used to chekc if current line is in comment
	com = False
	#filter every line in the file
	for line in f:
		#skip the line if it is blank
		if not line:
			continue
		#t used to save valid elements in each line
		t=''

		#check comment start
		if '/*' in line:
			com = True
		#check comment end
		if '*/' in line and com==True:
			com = False			
		#take in words when not comments
		elif com == False:
			#delete comments
			#save the element in each line that meets requirement
			for i in range(len(line)-1):
				if line[i]==line[i+1]=='/':
					break
				else:
					t+=line[i]
		if t.lstrip().rstrip():
			#add t to text
			text.append(t.lstrip().rstrip())

	f.close()

	return text

	
 