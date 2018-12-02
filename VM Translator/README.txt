Note:
I use python 3.7 to write the file.
Only allow bootstrapping tests!!!!

Command input instruction:
Case 1.
If you are already in the directry of 'xxx/VM Translator/src/', type 'python VMtranslator.py directory/'  

For example: In my computer, 'VMtranslator.py' is under directory 'C:\VM Translator\src\'.

'C:\VM Translator\src\>python VMtranslator.py C:\VM Translator\FunctionCalls\FibonacciElement' 
will create a 'FibonacciElement.asm' under the directory of 'C:\VM Translator\FunctionCalls\FibonacciElement'.

'C:\VM Translator\src\' is my working directory.
'C:\VM Translator\FunctionCalls\FibonacciElement' is the directory contain 'Main.vm' and 'Sys.vm' files


Case 2.
If you are not in the directry of 'xxx/VM Translator/src/', type 'python directory/VMtranslator.py directory/'

For example, In my computer, type 
C:\>python C:\VM Translator\src\VMtranslator.py C:\VM Translator\FunctionCalls\FibonacciElement



Error conditions:
Violate any of following will get an error message!
1. Error! Nothing valuable contained in .vm file!:
No sufficient contents in '.vm' files, which means after filtering, there is nothing left.
2. Error! Can not open directory/XXX.vm!:
'directory/XXX.vm'can't be open. This error happens in 'filterfile.py'.
