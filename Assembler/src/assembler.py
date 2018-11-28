import sys
import filterfile

def translate(text,filename):
	#store the translation result
	res=[]				
	#system reconized table
	sysdic={'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4, 'SCREEN':16384, 'KBD':24576,'R0':0,'R1':1, 'R2':2,'R3':3,'R4':4,'R5':5,'R6':6,'R7':7,'R8':8,'R9':9,'R10':10,'R11':11,'R12':12,'R13':13,'R14':14,'R15':15}
	#store user variable index from 16
	uservar=16
	userdic={}
	#store @value:machine_code in a form of key:value. @LOOP is an example  
	atdic={}			
	#I store key as a tuple, so that reverse order of key doesn't matter
	destdic={'M':['0','0','1'],'D':['0','1','0'],('D','M'):['0','1','1'],('A'):['1','0','0'],('A','M'):['1','0','1'],('A','D'):['1','1','0'],('A','D','M'):['1','1','1']} 
	#store jump value
	jumpdic={'JGT':['0','0','1'],'JEQ':['0','1','0'],'JGE':['0','1','1'],'JLT':['1','0','0'],'JNE':['1','0','1'],'JLE':['1','1','0'],'JMP':['1','1','1']}
	#store comp
	a1=['M','!M','-M','M+1','M-1','D+M','M+D','D-M','M-D','D&M','M&D','D|M','M|D']
	compdic={'0':['1','0','1','0','1','0'],'1':['1','1','1','1','1','1'],'-1':['1','1','1','0','1','0'],'D':['0','0','1','1','0','0'],'A':['1','1','0','0','0','0'],'M':['1','1','0','0','0','0'],'!A':['1','1','0','0','0','1'],'!M':['1','1','0','0','0','1'],'-D':['0','0','1','1','1','1'],'-A':['1','1','0','0','1','1'],'-M':['1','1','0','0','1','1'],'D+1':['0','1','1','1','1','1'],'A+1':['1','1','0','1','1','1'],'M+1':['1','1','0','1','1','1'],'D-1':['0','0','1','1','1','0'],'A-1':['1','1','0','0','1','0'],'M-1':['1','1','0','0','1','0'],'D+A':['0','0','0','0','1','0'],'D+M':['0','0','0','0','1','0'],'A+D':['0','0','0','0','1','0'],'M+D':['0','0','0','0','1','0'],'D-A':['0','1','0','0','1','1'],'D-M':['0','1','0','0','1','1'],'A-D':['0','0','0','1','1','1'],'M-D':['0','0','0','1','1','1'],'D&A':['0','0','0','0','0','0'],'A&D':['0','0','0','0','0','0'],'D&M':['0','0','0','0','0','0'],'M&D':['0','0','0','0','0','0'],'D|A':['0','1','0','1','0','1'],'D|M':['0','1','0','1','0','1'],'A|D':['0','1','0','1','0','1'],'M|D':['0','1','0','1','0','1']}

	
	"""
	bin(x) is used to translate integer to bianry language
	for example, 2 -> 0b10. We ignore '0b' and only take '10' for binary
	binary.rjust(16,'0') is fill 0 on the left to 16 bits
	"""
	#go through every line and delete jump instruction like (LOOP) and store address
	row=0
	while row<len(text):
		if text[row][0]=='(':
			#translate current row value to binary value
			binary=bin(row)[2:]
			atvalue=text[row][1:-1]
			#store binary value in dic. For example, '{@LOOP:'0000000000001010'}'
			#binary.rjust(16,'0') fills in 16 bits with 0
			atdic[atvalue]=binary.rjust(16,'0')
			#delete (LOOP) line
			text.remove(text[row])
			row=0
			continue
		row+=1

	#go through all the lines of newtext again
	for line in text:
		#if line starts with @
		if line[0]=='@':
			#if current line is a jump instruction, like @LOOP
			if line[1:] in atdic:
				res.append(atdic[line[1:]])
			#if @integer
			elif line[1:].isdigit():
				#translate current @value to binary value
				binary=bin(int(line[1:]))[2:]				
				res.append(binary.rjust(16,'0'))
			#if @ a system build in variable like @SCREEN
			elif line[1:] in sysdic:
				binary=bin(sysdic[line[1:]])[2:]
				res.append(binary.rjust(16,'0'))
			#if @ any other variable
			else:
				if line[1:] not in userdic:
					userdic[line[1:]]=bin(uservar)[2:].rjust(16,'0')
					uservar+=1
				res.append(userdic[line[1:]])
		else:
			#tmporary store every line of machine code
			tmp=['1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0']
			#see if there is equal and semicolon sign
			equal=semi=False
			#check if = in line
			if '=' in line:
				equal=True
				#equal index
				ei=line.index('=')
				#find dest
				if len(line[:ei])==1:
					dest=line[:ei]
				else:
					dest=tuple(sorted(line[:ei]))
				#replace d1 d2 d3 base on dest type
				tmp[10:13]=destdic[dest]
			#check if ; in line
			if ';' in line:
				semi=True
				#semicolon index
				si=line.index(';')
				#find jump
				jump=line[si+1:]
				#replace j1 j2 j3 base on jump type
				tmp[13:16]=jumpdic[jump]				
			
			#find comp
			if equal and semi:
				comp=line[ei+1:si]
			elif equal:
				comp=line[ei+1:]
			elif semi:
				comp=line[:si]
			#determine a
			if comp in a1:
				tmp[3]='1'
			if comp in compdic:
				tmp[4:10]=compdic[comp]			
			res.append(''.join(tmp))


	#create output filename by replace '.asm' to '.hack'
	outname=filename[:-4]+'.hack'

	#create an ouput file an load text into the file
	out=open(outname,'w')
	for line in res:
		if line:
			out.write(line+'\n')
	out.close()


if __name__=="__main__":
	if len(sys.argv)!=2:
		print("Error! You can only work on one file at the same time!")
		exit(0);		

	#load filename from command line
	try:
		filename=sys.argv[1]
	except:
		print("Error! Enter a valid file address!")
		exit(0);
	
	#report error if it is not a .asm file
	if filename[-4:]!='.asm':
		print("Error! System can only handle .asm file!")
		exit(0);

	#call the filterfile function to get rid of all the space and commnets
	text=filterfile.main(filename,True)
	if not text:
		print("Error! Nothing valuable contained in .asm file!")
		exit(0);
	#put filename into defined function
	translate(text,filename)
	

