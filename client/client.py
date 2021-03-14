#!/usr/bin/env python3

import socket
import threading
import sys
import os
import re
import time
import ctypes
from ctypes import wintypes


BUFFER_SIZE = 4096 # send 4096 bytes each time step
# define host and port
host = "localhost"
port = 5000
counter = 0


class Command(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.func = ""
        self.args = []


# run each command in a new thread
def run(sock, func, args):
        #print(args)
        #print(func)
        new_com = Command()
        time.sleep(1)
        absPath = os.path.dirname(__file__) + "\\myDLL.dll"
        MyLib = ctypes.cdll.LoadLibrary(absPath)
        if func == "Add":
            x = int(args[0])
            y = int(args[1])
            res = MyLib.Add(x,y)
        elif func == "Mul":
            x = int(args[0])
            y = int(args[1])
            res = MyLib.Mul(x,y)
        elif func == "Fibonacci":
            x = int(args[0])
            res = MyLib.Fibonacci(x)
        elif func == "Hello":
            MyLib.Hello()
            res = "Upload succeeded"



        handle = MyLib._handle
        #print(handle)
        del MyLib
        ctypes.windll.kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]
        ctypes.windll.kernel32.FreeLibrary(handle)
        os.remove("myDLL.dll")

        result = "[Result] for command " + func + " with args "+ str(args) +"is " + str(res)
        sock.sendall(str.encode(result))


def sendError(sock):
    try:
        update = "[ERROR] command execution failed"
        sock.sendall(str.encode(update)) 
    except:
        print("[ERROR] connection aborted by the server") 
        sys.exit(0)   


# Create new thread - this thread will take care of sending keep alive messages once in a while
def keepAliveCheck():
    threading.Timer(10.0, keepAliveCheck).start()
    try:
        message = "alive"
        sock.sendall(str.encode(message))
       # print("alive")
    except:
        sys.exit(0)


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    keepAliveCheck()
except:
    print("Could not make a connection to the server")
    input("Press enter to quit")
    sys.exit(0)




# recieve data from server
# 1. recieve the size of the .dll file
# 2. recieve the .dll file and save it as myDLL.dll
# 3. send server updates on each step of the command receipt and execution
# str.encode is used to turn the string message into bytes so it can be sent across the network

while True:
    # recieve function library
    try: 
        size = sock.recv(8)
        file_size = int(size)
        data = sock.recv(file_size)
        f = open("myDLL.dll", 'wb')
        f.write(data)
        f.close()
        update = "[Recieved] library from server"
        sock.sendall(str.encode(update))
    except:
        sendError(sock)
    # receive function name and arguments, parse input
    try:
        data1 = sock.recv(BUFFER_SIZE)
        command_details = str(data1.decode("utf-8"))
        lock = threading.Lock()
        func = command_details.split(', arguments')[0]
        args = command_details.split(', arguments')[1]
        args = args.split()
        update = "[Initilized] command: " +func+ " with args: " +str(args)
        sock.sendall(str.encode(update))       
    except:
        sendError(sock)
    try:
        time.sleep(1)
        update = "[Running] command: " +func+ " with args: " +str(args)
        sock.sendall(str.encode(update))
        receiveThread = threading.Thread(target=run, args=(sock,func,args))
        receiveThread.start()    
    except:
        sendError(sock)

        time.sleep(1) 
        finish = "[Finished] Finish, Library removed!!"
        sock.sendall(str.encode(finish))  

  

