Name: Siyuan Cao

Note:
I use python 3.7 to write the file.
***Every .jack file *must* end with an empty line!!! Otherwise, python can't read in the last line.
/src contains three python files. tokenizer.py used to translate jack language to tokens. parser.py used to parser tokens. compiler.py takes output from parser and compile a final .vm file.

Command input instruction:
Case 1.
If you are already in the directry of 'xxx/Cao_Siyuan_Project11/src/', type 'python compiler.py directory/'  

For example: In my computer, compiler.py' is under directory 'C:\Uchicago\introComputerSystem\HW\HW9\Cao_Siyuan_Project11\src'.

'C:\Uchicago\introComputerSystem\HW\HW9\Cao_Siyuan_Project11\src>python compiler.py C:\Uchicago\introComputerSystem\HW\HW9\11\ComplexArrays' 
will create a 'Main.vm' under the directory of 'C:\Uchicago\introComputerSystem\HW\HW9\11\ComplexArrays'.

'C:\Uchicago\introComputerSystem\HW\HW9\Cao_Siyuan_Project11\src>' is my working directory.
'C:\Uchicago\introComputerSystem\HW\HW9\11\ComplexArrays' is the directory contain 'Main.jack'


Case 2.
If you are not in the directry of 'xxx/Cao_Siyuan_Project11/src/', type 'python directory/compiler.py directory/'

For example, In my computer, type 
C:\>python C:\Uchicago\introComputerSystem\HW\HW9\Cao_Siyuan_Project11\src\compiler.py C:\Uchicago\introComputerSystem\HW\HW9\11\ComplexArrays
