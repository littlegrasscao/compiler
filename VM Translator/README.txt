Name: Siyuan Cao

Note:
I use python 3.7 to write the file.
Only allow bootstrapping tests!!!!
I have modified 'filterfilel.py', which is used in Project0. It can be called by 'VMtranslator.py' through passing parameters to a main function instead of calling through command line. In this way, we can avoid import additional libary. 

Command input instruction:
Case 1.
If you are already in the directry of 'xxx/Siyuan_Cao_Project8/src/', type 'python VMtranslator.py directory/'  

For example: In my computer, 'VMtranslator.py' is under directory 'C:\Uchicago\introComputerSystem\HW\HW6\Cao_Siyuan_Project8\src'.

'C:\Uchicago\introComputerSystem\HW\HW6\Cao_Siyuan_Project8\src>python VMtranslator.py C:\Uchicago\introComputerSystem\HW\HW6\FunctionCalls\FibonacciElement' 
will create a 'FibonacciElement.asm' under the directory of 'C:\Uchicago\introComputerSystem\HW\HW6\FunctionCalls\FibonacciElement'.

'C:\Uchicago\introComputerSystem\HW\HW6\Cao_Siyuan_Project8\src' is my working directory.
'C:\Uchicago\introComputerSystem\HW\HW6\FunctionCalls\FibonacciElement' is the directory contain 'Main.vm' and 'Sys.vm' files


Case 2.
If you are not in the directry of 'xxx/Siyuan_Cao_Project8/src/', type 'python directory/VMtranslator.py directory/'

For example, In my computer, type 
C:\>python C:\Uchicago\introComputerSystem\HW\HW6\Cao_Siyuan_Project8\src\VMtranslator.py C:\Uchicago\introComputerSystem\HW\HW6\FunctionCalls\FibonacciElement



Error conditions:
Violate any of following will get an error message!
1. Error! Nothing valuable contained in .vm file!:
No sufficient contents in '.vm' files, which means after filtering, there is nothing left.
2. Error! Can not open directory/XXX.vm!:
'directory/XXX.vm'can't be open. This error happens in 'filterfile.py'.