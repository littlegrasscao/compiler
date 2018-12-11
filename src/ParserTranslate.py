class ParserTranslate():
	def __init__(self,token):
		self.token = token
		self.index = 0

	#parser token
	def parser(self):
		#print(self.token)
		#print(os.path.basename(pathname));
		parser = []
		parser += self.class_seq()

		#print(parser)
		return parser
		# #create output filename end with '.xml'
		# directory_name = os.path.splitext(pathname)[0]+'.xml'

		# out=open(directory_name,'w')
		# for line in parser:
		# 	out.write(''.join(line))
		# 	out.write('\n')
		# out.close()


	#parser the class
	#'class','className','{','classVarDec','subroutineDec','}'
	def class_seq(self):
		c_store = []
		#start
		c_store.append(['<class>'])	
		#class
		c_store += [self.token[self.index]]
		self.index += 1
		#className
		c_store += [self.token[self.index]]
		self.index += 1
		#{
		c_store += [self.token[self.index]]
		self.index += 1
		#classVarDec
		while self.token[self.index][1] in ['static','field']:
			c_store += self.classVarDec()
		#subroutineDec
		while self.token[self.index][1] in ['constructor','function','method']:
			c_store += self.subroutineDec()
		#}
		c_store += [self.token[self.index]]
		#end
		c_store.append(['</class>'])

		return c_store


	#parser the classVarDec
	#(static | field) type varName (',' varName) ;
	def classVarDec(self):
		cvd_store = []
		#<classVarDec>
		cvd_store += ['<classVarDec>']
		#varName
		while self.token[self.index][1] != ';':
			cvd_store += [self.token[self.index]]
			self.index+=1
		#;
		cvd_store += [self.token[self.index]]
		self.index += 1		
		#</classVarDec>
		cvd_store += ['</classVarDec>']
		return cvd_store


	#parser the subroutineDec
	#('constructor','function','method') (void|type) subroutineName '('parameterList')' subroutineBody
	def subroutineDec(self):
		sd_store = []
		#<subroutineDec>
		sd_store += ['<subroutineDec>']
		#('constructor','function','method')
		sd_store += [self.token[self.index]]
		self.index += 1	
		#(void|type)		
		sd_store += [self.token[self.index]]
		self.index += 1
		#subroutineName
		sd_store += [self.token[self.index]]
		self.index += 1
		#'('
		sd_store += [self.token[self.index]]
		self.index += 1
		#parameterList
		sd_store += ['<parameterList>']
		while self.token[self.index][1] != ')':
			sd_store += [self.token[self.index]]
			self.index += 1			
		sd_store += ['</parameterList>']
		#')'		
		sd_store += [self.token[self.index]]
		self.index += 1		
		#subroutineBody
		sd_store += self.subroutineBody();		
		#</subroutineDec>
		sd_store += ['</subroutineDec>']
		return sd_store

	#{ varDec statements }
	def subroutineBody(self):
		sub_store = []
		sub_store += ['<subroutineBody>']
		#{
		sub_store += [self.token[self.index]]
		self.index += 1	
		#varDec
		while self.token[self.index][1] == 'var':
			sub_store += self.varDec()
		#statements
		if self.token[self.index][1] != '}':
			sub_store += self.statements()
		#}		
		sub_store += [self.token[self.index]]
		self.index += 1			
		sub_store += ['</subroutineBody>']
		return sub_store

	#'var' type varName (, varName) ;
	def varDec(self):
		var_store = []
		var_store += ['<varDec>']
		#varName
		while self.token[self.index][1] != ';':
			var_store += [self.token[self.index]]
			self.index+=1
		#;
		var_store += [self.token[self.index]]
		self.index += 1						
		var_store += ['</varDec>']
		return var_store

	#statement #
	def statements(self):
		i=0;
		state_store = []
		state_store += ['<statements>']
		#check all the statements
		while self.token[self.index][1] != '}':
			#print("word:"+self.token[self.index][1])
			#print("\n%d\n"%i)
			if self.token[self.index][1] == 'let':
				state_store += self.letStatement()
			elif self.token[self.index][1] == 'if':
				state_store += self.ifStatement()
			elif self.token[self.index][1] == 'while':
				state_store += self.whileStatement()
			elif self.token[self.index][1] == 'do':
				state_store += self.doStatement()
			elif self.token[self.index][1] == 'return':
				state_store += self.returnStatement()
			i+=1;
		state_store += ['</statements>']
		return state_store

	#let varName [ expression ] = expression ;
	def letStatement(self):
		let_store = []
		let_store += ['<letStatement>']
		#let
		let_store += [self.token[self.index]]
		self.index += 1	
		#varName
		let_store += [self.token[self.index]]
		self.index += 1	
		#[ expression ]
		if self.token[self.index][1] == '[':
			#[
			let_store += [self.token[self.index]]
			self.index += 1
			let_store += self.expression();
			#]
			let_store += [self.token[self.index]]
			self.index += 1							
		#=
		let_store += [self.token[self.index]]
		self.index += 1	
		#expression
		let_store += self.expression();
		#check error
		if self.token[self.index][1] != ';':
			print("error in let!!")
			exit(0)
		#;
		let_store += [self.token[self.index]]
		self.index += 1					
		let_store += ['</letStatement>']
		return let_store

	#if ( expression ) { statements } (else { statements })?
	def ifStatement(self):
		if_store = []
		if_store += ['<ifStatement>']
		#if
		if_store += [self.token[self.index]]
		self.index += 1
		#(
		if_store += [self.token[self.index]]
		self.index += 1
		#expression
		if_store += self.expression();
		#)
		if_store += [self.token[self.index]]
		self.index += 1
		#{
		if_store += [self.token[self.index]]
		self.index += 1
		#statements
		if_store += self.statements();
		#}
		if_store += [self.token[self.index]]
		self.index += 1		
		#else { statements }
		if self.token[self.index][1] == 'else':
			#else
			if_store += [self.token[self.index]]
			self.index += 1
			#{
			if_store += [self.token[self.index]]
			self.index += 1
			#statements
			if_store += self.statements();
			#}
			if_store += [self.token[self.index]]
			self.index += 1
		if_store += ['</ifStatement>']
		return if_store
	
	#while ( expression ) { statements }
	def whileStatement(self):
		whlie_store = []
		whlie_store += ['<whileStatement>']
		#whlie
		whlie_store += [self.token[self.index]]
		self.index += 1
		#(
		whlie_store += [self.token[self.index]]
		self.index += 1
		#expression
		whlie_store += self.expression();
		#check error
		if self.token[self.index][1] != ')':
			print("error in while expression!!")
			exit(0)
		#)
		whlie_store += [self.token[self.index]]
		self.index += 1
		#{
		whlie_store += [self.token[self.index]]
		self.index += 1
		#statements
		whlie_store += self.statements();
		#check error
		if self.token[self.index][1] != '}':
			print("error in while statements!!")
			exit(0)
		#}
		whlie_store += [self.token[self.index]]
		self.index += 1
		whlie_store += ['</whileStatement>']
		return whlie_store

	#do subroutineCall ;
	def doStatement(self):
		do_store = []
		do_store += ['<doStatement>']
		#do
		do_store += [self.token[self.index]]
		self.index += 1
		#subroutinecall
		do_store += self.subroutinecall();
		#check error
		if self.token[self.index][1] != ';':
			print("error in do!!")
			exit(0)		
		#;
		do_store += [self.token[self.index]]
		self.index += 1 
		do_store += ['</doStatement>']
		return do_store

	#reutrn expression ;
	def returnStatement(self):
		return_store = []
		return_store += ['<returnStatement>']
		#return
		return_store += [self.token[self.index]]
		self.index += 1
		#expression?
		if self.token[self.index][1] != ';':			
			return_store += self.expression();
		#;
		return_store += [self.token[self.index]]
		self.index += 1			
		return_store += ['</returnStatement>']
		return return_store

	def expression(self):
		op = ['+','-','*','/','&amp;','|','&lt;','&gt;','=']
		ex_store = []
		ex_store += ['<expression>']
		ex_store += self.term();
		while self.token[self.index][1] in op:
			#add op
			ex_store += [self.token[self.index]]
			self.index += 1	
			#add term
			ex_store += self.term();
		ex_store += ['</expression>']
		return ex_store

	def term(self):
		term_store = []
		term_store += ['<term>']
		#print(self.token[self.index][0]+self.token[self.index][1])
		#varName [ expression ]
		if self.token[self.index][0] == '<identifier>' and self.token[self.index+1][1] == '[':
			term_store += [self.token[self.index]]
			self.index += 1
			term_store += [self.token[self.index]]
			self.index += 1
			term_store += self.expression();
			term_store += [self.token[self.index]]
			self.index += 1				
		#( expression )
		elif self.token[self.index][1] == '(':
			term_store += [self.token[self.index]]
			self.index += 1				
			term_store += self.expression();
			term_store += [self.token[self.index]]
			self.index += 1	
		#unaryOp term
		elif self.token[self.index][1] in ['-','~']:
			term_store += [self.token[self.index]]
			self.index += 1
			term_store += self.term();
		#subroutine call
		elif self.token[self.index][0] == '<identifier>' and (self.token[self.index+1][1] == '(' or self.token[self.index+1][1] == '.'):
			#print("subroutine call")
			term_store += self.subroutinecall();			
		#integer, string, keyword, var
		elif self.token[self.index][0] in ['<keyword>','<integerConstant>','<stringConstant>','<identifier>']:
			term_store += [self.token[self.index]]
			self.index += 1

		term_store += ['</term>']
		return term_store

	#subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
	def subroutinecall(self):
		subcall_store = []
		#print(self.token[self.index][1]+self.token[self.index+2][1])
		#<identifier>
		subcall_store += [self.token[self.index]]
		self.index += 1
		#subroutineName '(' expressionList ')'
		if self.token[self.index][1] == '(':
			#(
			subcall_store += [self.token[self.index]]
			self.index += 1
			#expressionList
			subcall_store += self.expressionList();
			#)
			subcall_store += [self.token[self.index]]
			self.index += 1				
		#( className | varName) '.' subroutineName '(' expressionList ')'
		elif self.token[self.index][1] == '.':
			#.
			subcall_store += [self.token[self.index]]
			self.index += 1
			#name
			subcall_store += [self.token[self.index]]
			self.index += 1
			#(
			subcall_store += [self.token[self.index]]
			self.index += 1
			#expressionList
			subcall_store += self.expressionList();
			#)
			subcall_store += [self.token[self.index]]
			self.index += 1			
		return subcall_store


	def expressionList(self):
		exlist_store = []
		exlist_store += ['<expressionList>']
		if self.token[self.index][1] != ')':
			exlist_store += self.expression();
			while self.token[self.index][1] == ',':
				#print(self.token[self.index+1][1])
				#,
				exlist_store += [self.token[self.index]]
				self.index += 1					
				exlist_store += self.expression();
		exlist_store += ['</expressionList>']
		return exlist_store