import sys
import os
import filterfile

def vmtranslate(text,pathname):
	#store the translation result
	res=[]				
	#Arithmetic and logical commands
	add=['@SP','AM=M-1','D=M','A=A-1','M=M+D']
	sub=['@SP','AM=M-1','D=M','A=A-1','M=M-D']
	neg=['@SP','A=M-1','M=-M']
	eq=['@SP','AM=M-1','D=M','A=A-1','D=M-D','@TRUE','D;JEQ','@SP','A=M-1','M=0','@CONTINUE','0;JMP','(TRUE)','@SP','A=M-1','M=-1','(CONTINUE)']
	gt=['@SP','AM=M-1','D=M','A=A-1','D=M-D','@TRUE','D;JGT','@SP','A=M-1','M=0','@CONTINUE','0;JMP','(TRUE)','@SP','A=M-1','M=-1','(CONTINUE)']
	lt=['@SP','AM=M-1','D=M','A=A-1','D=M-D','@TRUE','D;JLT','@SP','A=M-1','M=0','@CONTINUE','0;JMP','(TRUE)','@SP','A=M-1','M=-1','(CONTINUE)']
	and1=['@SP','AM=M-1','D=M','A=A-1','M=M&D']
	or1=['@SP','AM=M-1','D=M','A=A-1','M=M|D']
	not1=['@SP','A=M-1','M=!M']
	Arithmetic={'add':add,'sub':sub,'neg':neg,'eq':eq,'gt':gt,'lt':lt,'and':and1,'or':or1,'not':not1}
	#define x to avoid same @TRUE and @CONTINUE.
	#@TRUE becomes @TRUE%x
	x=0

	#used in 'call f n'. to make each returAddress unique    
	count=1
	#push return-address
	returnAddress=['D=A','@SP','A=M','M=D','@SP','M=M+1']
	#push LCL
	LCL=['@LCL','D=M','@SP','A=M','M=D','@SP','M=M+1']
	#push ARG
	ARG=['@ARG','D=M','@SP','A=M','M=D','@SP','M=M+1']
	#push THIS
	THIS=['@THIS','D=M','@SP','A=M','M=D','@SP','M=M+1']
	#push THAT
	THAT=['@THAT','D=M','@SP','A=M','M=D','@SP','M=M+1']

	#record function name
	funcname = ''


	#initial Bootstrapping
	#SP=256
	res+=['@256','D=A','@SP','M=D']
	#call Sys.init
	res.append('@Sys.init.0')
	res+=returnAddress    							#push return-address
	res+=LCL; res+=ARG; res+=THIS; res+=THAT; 		#push
	res+=['@SP','D=M','@5','D=D-A','@ARG','M=D'] 	#ARG = SP-5
	res+=['@SP','D=M','@LCL','M=D']					#LCL = SP
	res+=['@Sys.init','0;JMP'] 						#goto f
	res.append('(Sys.init.0)') 						#(return-address)


	#go through input file
	for line in text:
		line=line.split()
		#print(line)

		#call f n
		if 'call' in line:
			count+=1;
			#push return-address
			res.append('@RET.%d'%count)
			res+=returnAddress
			#push LCL
			res+=LCL
			#push ARG
			res+=ARG
			#push THIS
			res+=THIS
			#push THAT
			res+=THAT
			#ARG = SP-n-5
			res+=['@SP','D=M']
			res.append('@%s'%line[-1])  #@n
			res+=['D=D-A','@5','D=D-A','@ARG','M=D']
			#LCL = SP
			res+=['@SP','D=M','@LCL','M=D']
			#goto f
			res.append('@%s'%line[1])
			res.append('0;JMP')
			#(return-address)
			res.append('(RET.%d)' %count)

		#function f k
		elif 'function' in line:
			#update current function name
			funcname = line[1]
			#(f), get address of f
			res.append('(%s)' %line[1])
			#push 0 for k times
			for i in range(int(line[-1])):
				res+=['@SP','A=M','M=0','@SP','M=M+1']

		elif 'return' in line:
			#FRAME=LCL
			res+=['@LCL','D=M','@FRAME','M=D']
			#RET=*(FRAME-5)
			res+=['@FRAME','D=M','@5','A=D-A','D=M','@RET','M=D']
			#*ARG=pop()
			res+=['@SP','A=M-1','D=M','@ARG','A=M','M=D']
			#SP=ARG+1
			res+=['@ARG','D=M+1','@SP','M=D']
			#THAT=*(FRAME-1)
			res+=['@FRAME','A=M-1','D=M','@THAT','M=D']
			#THIS=*(FRAME-2)
			res+=['@FRAME','D=M','@2','A=D-A','D=M','@THIS','M=D']
			#ARG=*(FRAME-3)
			res+=['@FRAME','D=M','@3','A=D-A','D=M','@ARG','M=D']
			#LCL=*(FRAME-4)
			res+=['@FRAME','D=M','@4','A=D-A','D=M','@LCL','M=D']
			#goto RET
			res+=['@RET','A=M','0;JMP']

		#label, if-goto, goto
		elif 'label' in line:
			res.append('(%s)' %line[1])
		elif 'if-goto' in line:
			res+=['@SP','AM=M-1','D=M']
			res.append('@%s' %line[1])
			res.append('D;JNE')
		elif 'goto' in line:
			res.append('@%s' %line[1])
			res.append('0;JMP')

		#if current line is Arithemitic
		elif line[0] in Arithmetic:
			#add each step into res
			for step in Arithmetic[line[0]]:
				#deal with jump @TRUE and @Continue,make sure each jump get different value
				if step=='@TRUE':
					res.append('@TRUE%d'%x)
				elif step=='@CONTINUE':
					res.append('@CONTINUE%d'%x)
				elif step=='(TRUE)':
					res.append('(TRUE%d)'%x)
				elif step=='(CONTINUE)':
					res.append('(CONTINUE%d)'%x)
					x+=1
				#rest step stays the same as defined
				else: 
					res.append(step)

		#if current line is memory commands
		else:
			#get i
			i=line[-1]

			#decide if pop or push one of static, pointer and tmp
			spt=False
			#get the address of static, pointer and tmp
			if 'static' in line:
				classname = funcname.split('.')[0]
				address='@%s.static.%d'%(classname,int(i))
				spt=True
			elif 'pointer' in line:
				address='@%d'%(3+int(i))
				spt=True
			elif 'temp' in line:
				address='@%d'%(5+int(i))
				spt=True 

			#push function for static, pointer and tmp
			PUSHspt=['D=M','@SP','A=M','M=D','@SP','M=M+1']
			#pop function for static, pointer and tmp
			POPspt=['@SP','AM=M-1','D=M','M=D']
			if 'push' in line and spt:
				res.append(address)
				res+=PUSHspt
				continue
			#add POP steps into the res. don't forget to add address also
			elif 'pop' in line and spt:
				res+=POPspt[:-1]
				res.append(address)
				res.append(POPspt[-1])
				continue

			#decide memory segments
			if 'argument' in line:
				res.append('@ARG')
			elif 'local' in line:
				res.append('@LCL')
			elif 'this' in line:
				res.append('@THIS')
			elif 'that' in line:
				res.append('@THAT')	

			#push or pop
			if 'push' in line:
				#push constant i
				if 'constant' in line:
					res.append("@%d" %int(i))  #@i
					res.append('D=A')
				#push segments i
				else:
					res.append('D=M')
					res.append("@%d" %int(i))  #@i
					res.append('A=D+A')
					res.append('D=M')
				res+=['@SP','A=M','M=D','@SP','M=M+1']
			#pop segments i
			elif 'pop' in line:
				res.append('D=M')
				res.append("@%d" %int(i))	#@i			
				res+=['D=D+A','@R13','M=D','@SP','AM=M-1','D=M','@R13','A=M','M=D']		

	#add infinite loop at the end
	res+=['(_1)','@_1','0;JMP']

	#create output filename end with '.asm'
	outname=os.path.basename(pathname)+'.asm'

	#create an ouput file an load text into the file
	completeName = os.path.join(pathname,outname)
	out=open(completeName,'w')
	for line in res:
		if line:
			out.write(line+'\n')
	out.close()


if __name__=="__main__":
	text=[]
	path=sys.argv[1]

	for filename in os.listdir(path):
		#report error if it is not a .asm file
		if filename[-3:]=='.vm':	
			#call the filterfile function to get rid of all the space and commnets
			filterpath = os.path.join(path,filename)
			text+=filterfile.main(filterpath,True)

	if not text:
		print("Error! Nothing valuable contained in .vm file!")
		exit(0);
	#print(text)

	#put filename into defined function
	vmtranslate(text,path)
	

