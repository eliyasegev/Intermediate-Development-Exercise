Intermediate Development Exercise solution
written by Eliya Segev

Summery:
Main goal - c&c - server that can Handle multiple clients.
This code allows the injection of a .dll file from server to the client 
and activate operations that are in the uploaded dynamic library(.dll)


In order to operate the project you will need:

1. Load the attached files: 
load server.py, cli.py, Lib.dll to a Folder name server
Load client.py to another folder
2. Run server.py from server dir
3. Run client.py from client dir

Note - For each client you want to run Open a new folder that will contain the file client.py



4. follow the CLI instruction - The instructions will be on the server terminal

The attached .dll currently supports the following functions:
Add(int a, int b)
Mul(int a, int b)
Fibonacci(int n) - calc the n'th Fibonacci number
Hello() - print message uploaded from the .dll file 

(All functions were written in c++)

At the end of the execution, the library will be unlinked and .dll file will be deleted (secure deletion).

plug-n-play capabilities:
In order to add functions to the library:
1. Create a new Lib.dll file with your new functions 
2. Replace the Lib.dll file located in server folder with the new .dll file
3. Update the function dictionary and the argTypes dictionary found in cli.py
4. Update the function check_args located in cli.py
5. Insert your new functions running command in the "run" function located in client.py


During the run, the server folder will have a file named log.txt that will record the run status and actions.
In addition, in the result file it will be possible to view the results of the commands sent to clients.
(You can view the results by insert 4 in the main menu)


Notes:
1. The current implementation supports the execution of operations from the same computer, but by changing the address it will be possible to perform this in other ways as well.

2. Currently the code only supports functions that accept int variables and return int/void

To expand this we will need to send pointers that represent the types of the return value and the arguments before calling a function from the loaded library.

3. The code currently works with 64-bit Python and 64-bit dll.


		