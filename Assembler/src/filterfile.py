#import sys

def filterfile(filename,noncom):
	#open input file and filter each line
	text=[]
	#print a error statement if the address is invalid and exit
	try:
		f=open(filename,'r')
	except:
		print('Error! Please enter a valid address for filtering!')
		exit(0);

	#filter every line in the file
	for line in f:
		#skip the line if it is blank
		if not line:
			continue
		#t used to save valid elements in each line
		t=''
		#if request to delete comments
		if noncom:
			#save the element in each line that meets requirement
			for i in range(len(line)-1):
				if line[i]==line[i+1]=='/':
					break
				elif line[i]!=' ' and  line[i]!='\t':	
					t+=line[i]
		#if not resquest to delete comments
		else:
			#save the element in each line that meets requirement
			for i in line:
				if i!=' ' and  i!='\t' and i!='\n':
					t+=i
		#add t to text
		text.append(t)
	
	#deal with the last line if not ends with blank line or not contains commands
	last = line
	if last and '//' not in last and last[-1].isalpha():
		text[-1]+=last[-1]
	f.close()

	res=[]
	#only return valid text content
	for line in text:
		if line:
			res.append(line)
			
	return res

#filename and noncom are imported from outside
def main(filename,noncom):
	#put filename and nocom into defined function
	return filterfile(filename,noncom)
	

