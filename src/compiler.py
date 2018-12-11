# -*- coding: utf-8 -*-

import sys
import os
import tokenizer
from ParserTranslate import ParserTranslate


class CompilerTranslate():
	def __init__(self,analyze):
		self.parser = analyze
		self.classname = ''
		self.classVar = {'this':['pointer 0','object']}
		self.index = 0
		self.label_if = 0
		self.label_while = 0

	#output
	def Compiler(self,pathname):
		compiler = []

		#find classname
		while self.index < len(self.parser):
			if '<identifier>' in self.parser[self.index]:
				self.classname = self.parser[self.index][1]
				break;
			self.index += 1;

		#print(self.classname)

		#store all <classVarDec>
		static_count = 0
		field_count = 0
		static = False
		field = False
		while '<subroutineDec>' not in self.parser[self.index]:
			if '<classVarDec>' in self.parser[self.index]:
				#store everything inside <classVarDec>
				while '</classVarDec>' not in self.parser[self.index]:
					if 'field' in self.parser[self.index]:
						field = True
					elif 'static' in self.parser[self.index]:
						static = True
					#avoid className type variable
					if '<identifier>' in self.parser[self.index] and '<identifier>' in self.parser[self.index+1]:
						self.index += 1
					if '<identifier>' in self.parser[self.index]:
						cvar = self.parser[self.index][1] #variable
						#add and increase field
						if field == True:
							self.classVar[cvar] = ['this %d'%field_count,self.parser[self.index-1][1]] #[this i,type]
							field_count += 1
						#add and increase static	
						elif static == True:
							self.classVar[cvar] = ['static %d'%static_count,self.parser[self.index-1][1]] #[static i,type]
							static_count += 1
					self.index += 1
				static = False
				field = False
			self.index += 1

		# print(self.classVar)
		# exit(0)
		
		#find subroutineDec
		while self.index < len(self.parser):
			if '<subroutineDec>' in self.parser[self.index]:
				compiler += self.subroutineDec(field_count)
			self.index += 1

		#print(compiler)

		#create output filename end with '.vm'
		directory_name = os.path.splitext(pathname)[0]+'.vm'

		out=open(directory_name,'w')
		for line in compiler:
			out.write(line)
			out.write('\n')
		out.close()


	#subroutineDec
	def subroutineDec(self,field_count):
		sub_store = []
		ifmethod = False
		ifconstructor = False

		#find function name
		while self.index < len(self.parser):
			if 'method' in self.parser[self.index]:
				ifmethod = True
			elif 'constructor' in self.parser[self.index]:
				ifconstructor = True 
				self.index += 1;	
			elif '<identifier>' in self.parser[self.index]:
				if '<identifier>' in self.parser[self.index+1]:
					funcname = self.parser[self.index+1][1]
				else:	
					funcname = self.parser[self.index][1]
				break;
			self.index += 1;		

		#print(funcname)

		variable = {}
		if ifmethod:
			arg_count = 1
		else:
			arg_count = 0
		#get argument from <parameterList>
		while '<parameterList>' not in self.parser[self.index]:
			self.index += 1;
		while '</parameterList>' not in self.parser[self.index]: 
			#avoid className type variable
			if '<identifier>' in self.parser[self.index] and '<identifier>' in self.parser[self.index+1]:
				self.index += 1
			#add paramater into dic
			if '<identifier>' in self.parser[self.index]:
				parameter = self.parser[self.index][1] 
				if parameter not in variable:
					variable[parameter] = ['argument %d'%arg_count,self.parser[self.index-1][1]] #[argument i, type]
					arg_count += 1
			self.index += 1;			


		#find all local varibale 
		local_count = 0
		while '<statements>' not in self.parser[self.index]:
			#avoid className type variable
			if '<identifier>' in self.parser[self.index] and '<identifier>' in self.parser[self.index+1]:
				self.index += 1
			#add local variable to dic
			if '<identifier>' in self.parser[self.index]:
				parameter = self.parser[self.index][1] 
				if parameter not in variable:
					variable[parameter] = ['local %d'%local_count,self.parser[self.index-1][1]] #[local i, type]
					local_count += 1
			self.index += 1


		#function
		sub_store.append("function %s.%s %d"%(self.classname,funcname,local_count))

		if ifmethod:
			sub_store += ['push argument 0','pop pointer 0'] #setting 'this' 
		if ifconstructor:
			sub_store.append('push constant %d'%field_count)
			sub_store += ['call Memory.alloc 1','pop pointer 0']


		#go through <subroutineBody>
		while '</subroutineBody>' not in self.parser[self.index]:
			#do statement
			if '<doStatement>' in self.parser[self.index]:
				sub_store += self.doStatement(variable)
			#let statement
			if '<letStatement>' in self.parser[self.index]:
				sub_store += self.letStatement(variable)
			#if statement
			if '<ifStatement>' in self.parser[self.index]:
				sub_store += self.ifStatement(variable)
			#while statement
			if '<whileStatement>' in self.parser[self.index]:	
				sub_store += self.whileStatement(variable)
			#return statement
			if '<returnStatement>' in self.parser[self.index]:
				sub_store += self.returnStatement(variable)

			self.index += 1;
		
		return sub_store



	#expression
	def expression(self,variable):
		op = {'+':'add','-':'sub','*':'call Math.multiply 2','/':'call Math.divide 2','&amp;':'and','|':'or','&lt;':'lt','&gt;':'gt','=':'eq'}
		unaryOP = {'-':'neg','~':'not'}
		ex_store = []
		self.index += 1; #add one

		symbol =[]
		name = [] #store function name
		ifunaryOP = False
		#find the whole expression
		while '</expression>' not in self.parser[self.index]:
			#maybe another expression within expression
			if '<expression>' in self.parser[self.index]:
				ex_store += self.expression(variable)
			#true, false, null
			elif '<keyword>' in self.parser[self.index]:
				if self.parser[self.index][1] == 'true':
					ex_store += ['push constant 0','not']
				elif self.parser[self.index][1] == 'false':
					ex_store.append("push constant 0")
				elif self.parser[self.index][1] == 'null':
					ex_store.append("push constant 0")
				elif self.parser[self.index][1] in self.classVar: #this
					n = self.classVar[self.parser[self.index][1]][0]
					ex_store.append('push %s'%n)
			#add all names
			elif '<integerConstant>' in self.parser[self.index] or '<identifier>' in self.parser[self.index] or '<stringConstant>' in self.parser[self.index]:
				ifarray = False
				if '[' in self.parser[self.index+1]: #array
					ifarray = True
				if self.parser[self.index][1] in variable and '.' not in self.parser[self.index+1][1]: 		#local variable
					n = variable[self.parser[self.index][1]][0]
					ex_store.append('push %s'%n)
				elif self.parser[self.index][1] in self.classVar and '.' not in self.parser[self.index+1][1]: #class variable
					n = self.classVar[self.parser[self.index][1]][0]
					ex_store.append('push %s'%n)
				elif self.parser[self.index][1].isdigit(): #integer
					n = 'constant %s'%self.parser[self.index][1]
					ex_store.append('push %s'%n)
				elif self.parser[self.index][0] == '<stringConstant>': #string
					word = self.parser[self.index][1]
					ex_store.append('push constant %d'%len(word))
					ex_store.append('call String.new 1')
					for c in word:
						ex_store.append('push constant %d'%(ord(c)))
						ex_store.append('call String.appendChar 2')
				#if is calling a function
				elif self.parser[self.index][0] == '<identifier>': #function name
					name = self.parser[self.index][1]
					if self.parser[self.index+1][1] == '.': #Memory.peek
						name += '.'
						name += self.parser[self.index+2][1]
					#find # of arguments
					arg_count = 0
					#call it self to get function
					tmp_store = []
					while '</expressionList>' not in self.parser[self.index]:
						#count all expressions
						if '<expression>' in self.parser[self.index]:
							arg_count += 1
							#get the full expression
							tmp_store += self.expression(variable)
						self.index += 1

					#add all commands to do_store
					ex_store += tmp_store

					#if method
					if '.' not in name:    #self-called method
						ex_store.append("push pointer 0")
						name = self.classname+'.'+name
						arg_count += 1
					elif name[:name.index(".")] in self.classVar: #classname method
						ex_store.append("push %s"%self.classVar[name[:name.index(".")]][0])
						prefix = self.classVar[name[:name.index(".")]][1] #type
						name = prefix+name[name.index("."):] #change prefix of name
						arg_count += 1			
					#if start with local variable
					elif name[:name.index(".")] in variable: #varname method
						ex_store.append("push %s"%variable[name[:name.index(".")]][0]) #push local 0
						# print(variable)
						# exit(0)
						prefix = variable[name[:name.index(".")]][1] #type
						name = prefix+name[name.index("."):] #change prefix of name
						arg_count += 1

					ex_store.append("call %s %d"%(name,arg_count))
				#if is array
				if ifarray:
					while '<expression>' not in self.parser[self.index]:
						self.index += 1
					ex_store += self.expression(variable)
					ex_store += ["add",'pop pointer 1','push that 0']
			#add all operation 
			elif '<symbol>' in self.parser[self.index]:
				#unaryOP
				if '<term>' in self.parser[self.index-1]:
					ifunaryOP = True
				if ifunaryOP==True and self.parser[self.index][1] in unaryOP:
					symbol.append(unaryOP[self.parser[self.index][1]])
				#OP
				elif self.parser[self.index][1] in op:
					symbol.append(op[self.parser[self.index][1]])
				ifunaryOP = False
			self.index += 1;


		#add operation
		for i in symbol[::-1]:
			ex_store.append(i)

		return ex_store


	def doStatement(self,variable):
		do_store = []
		name = ""

		#get name
		while "<identifier>" not in self.parser[self.index]:
			self.index += 1
		while self.parser[self.index][1] != '(': #do bat.move();
			name += self.parser[self.index][1]
			self.index += 1

		#go through all content in do statement
		arg_count = 0

		tmp_store = []
		while '</expressionList>' not in self.parser[self.index]:
			#count all expressions
			if '<expression>' in self.parser[self.index]:
				arg_count += 1
				#get the full expression
				tmp_store += self.expression(variable)
			self.index += 1

		#if method
		if '.' not in name: #self-called method
			do_store.append("push pointer 0")
			name = self.classname+'.'+name
			arg_count += 1
		elif name[:name.index(".")] in self.classVar: #classname method
			do_store.append("push %s"%self.classVar[name[:name.index(".")]][0]) #push this 0
			prefix = self.classVar[name[:name.index(".")]][1] #type
			name = prefix+name[name.index("."):] #change prefix of name
			arg_count += 1			
		#if start with local variable
		elif name[:name.index(".")] in variable: #varname method
			do_store.append("push %s"%variable[name[:name.index(".")]][0]) #push local 0
			# print(variable)
			# exit(0)
			prefix = variable[name[:name.index(".")]][1] #type
			name = prefix+name[name.index("."):] #change prefix of name
			arg_count += 1
		#add rest and call function
		do_store += tmp_store
		do_store.append("call %s %d"%(name,arg_count))
		do_store.append("pop temp 0")
		return do_store


	def letStatement(self,variable):
		ifarray = False
		let_store = []
		
		#go through all content in let statement
		while '</letStatement>' not in self.parser[self.index]:
			#find value before =
			if "<identifier>" in self.parser[self.index]:
				#local name
				if self.parser[self.index][1] in variable:
					name = variable[self.parser[self.index][1]][0]
				#class name
				elif self.parser[self.index][1] in self.classVar:
					name = self.classVar[self.parser[self.index][1]][0]
				#array[expression]
				if '[' in self.parser[self.index+1]: #array
					ifarray = True
					self.index += 2
					let_store += self.expression(variable)
					let_store.append("push %s"%name)
					let_store.append('add')
			#count all expressions
			if '<expression>' in self.parser[self.index]:
				let_store += self.expression(variable)
			self.index += 1
		
		#let array = xxx
		if ifarray:
			let_store += ['pop temp 0','pop pointer 1','push temp 0','pop that 0']
		else:
			let_store.append("pop %s"%name)

		return let_store


	def ifStatement(self,variable):
		if_store = []

		#if (expression)
		while '<expression>' not in self.parser[self.index]:		
			self.index += 1	
		if_store += self.expression(variable)


		#if-goto IF_TRUE0
		if_store.append('if-goto IF_TRUE%d'%self.label_if)
		if_store.append("goto IF_FALSE%d"%self.label_if)
		if_store.append('label IF_TRUE%d'%self.label_if) #label IF_TRUE0

		tmp_label = self.label_if #temporary
		self.label_if += 1 #update label

		#if {statements}
		while '<statements>' not in self.parser[self.index]:
			self.index += 1	
		if_store += self.Statements(variable) #(statements)
		
		if_store.append('goto IF_END%d'%tmp_label)
		if_store.append('label IF_FALSE%d'%tmp_label) #label IF_FALSE0

		#check if there is else {}
		while '</ifStatement>' not in self.parser[self.index]:
			if '<statements>' in self.parser[self.index]:
				if_store += self.Statements(variable) #{statements}
			self.index += 1	
		if_store.append('label IF_END%d'%tmp_label) #label IF_END
		
		
		return if_store

	#{statements}
	def Statements(self,variable):
		state_store = []
		#go through <statements>
		while '</statements>' not in self.parser[self.index]:
			#do statement
			if '<doStatement>' in self.parser[self.index]:
				state_store += self.doStatement(variable)
			#let statement
			if '<letStatement>' in self.parser[self.index]:
				state_store += self.letStatement(variable)
			#if statement
			if '<ifStatement>' in self.parser[self.index]:
				state_store += self.ifStatement(variable)
			#while statement
			if '<whileStatement>' in self.parser[self.index]:	
				state_store += self.whileStatement(variable)
			#return statement
			if '<returnStatement>' in self.parser[self.index]:
				state_store += self.returnStatement(variable)
			self.index += 1;
		return state_store

	def whileStatement(self,variable):
		while_store = []

		#label WHILE_EXP0
		while_store.append("label WHILE_EXP%d"%self.label_while)

		#while (expression)
		while '<expression>' not in self.parser[self.index]:		
			self.index += 1	
		while_store += self.expression(variable)

		# not
		# if-goto WHILE_END0
		while_store.append("not")
		while_store.append("if-goto WHILE_END%d"%self.label_while)

		tmp_label = self.label_while
		self.label_while += 1
		#while {statements}
		while '<statements>' not in self.parser[self.index]:
			self.index += 1	
		while_store += self.Statements(variable) #(statements)

		while_store.append("goto WHILE_EXP%d"%tmp_label)
		while_store.append("label WHILE_END%d"%tmp_label)

		return while_store


	def returnStatement(self,variable):
		return_store = []
		#go through all content in return statement
		while '</returnStatement>' not in self.parser[self.index]:
			if '<expression>' in self.parser[self.index]:
				return_store += self.expression(variable)
			self.index += 1
		#return
		if not return_store:
			return_store.append('push constant 0')
		return_store.append('return')
		return return_store




if __name__=="__main__":
	path=sys.argv[1]

	for filename in os.listdir(path):
		#report error if it is not a .asm file
		if filename[-5:]=='.jack':
			#call the filterfile function to get rid of all the space and commnets
			filterpath = os.path.join(path,filename)
			text = tokenizer.filterfile(filterpath)

			#get tokens
			token = tokenizer.TokenTranslate(' '.join(text))

			#parser tokens
			parser = ParserTranslate(token)

			analyze = parser.parser()
			#print(analyze)

			#compile
			compiler = CompilerTranslate(analyze)
			compiler.Compiler(filterpath)