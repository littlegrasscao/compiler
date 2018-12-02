Note:
I use python 3.7 to write the file.
I take dest and comp permutatioin into consideration. DM=M+D is the same as MD=D+M.

Command input instruction:
Case 1.
If you are already in the directry of 'xxx/Assembler/src/', type 'python assembler.py xxx\max\Max.asm'  

For example: In my computer, 'assembler.py' is under directory 'C:\Assembler\src'.
'C:\Assembler\src>python assembler.py C:\Assembler\06\max\Max.asm' will create a 'Max.hack' in the same directory as 'Max.asm'.
'C:\Assembler\src>' is my working directory.
'C:\Assembler\06\max\Max.asm' is the directory of Max.asm file


Case 2.
If you are not in the directry of 'xxx/Assembler/src/', type 'python directory/assembler.py directory/Max.asm'

For example, In my computer, type 
C:\>python C:\Assembler\src\assembler.py C:\Assembler\06\max\Max.asm




Error conditions:
Violate any of following will get an error message!
1. The system only allows 1 input file at one time.
2. The system only handle '.asm' files.
3. Entering a invalid address.
4. If file can not be read.(error message shows by filterfile.py)
5. No effective content in '.asm' files, which means after filtering, there is no content left.
