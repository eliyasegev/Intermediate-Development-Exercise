#!/usr/bin/env python3

import sys
import subprocess

# dict for CLI main menu commands
# options appear on screen whenever the user has to choose between them
Commands = {
    1: "Send command",
    2: "Refresh status",
    3: "Remove client",
    4: "Display Command Result"
    }

# dict for dll available function
# in case of adding functions this dictionary should be updated    
Functions = {
    1: "Hello",
    2: "Add",
    3: "Mul",
    4: "Fibonacci"
    }

# dict function: nacessary args for function
# in case of adding functions this dictionary should be updated   
argTypes = {
    "Hello": [],
    "Add": ["int", "int"],
    "Mul": ["int", "int"],
    "Fibonacci": ["int"]
    }

# CLI aim display server and client information 
# in addition to allow the client the execution of commands through the server to clients
class CLI():
    def __init__(self, clients):
        self.command = ""
        self.clients = clients
        self.args = []
# print table with server and clients current status
    def show_status(self):
        print('#' * 31)
        print("#{:^14}#{:^14}#".format("name","status"))
        print('-' * 31)
        print("#{:^14}#{:^14}#".format("server","alive"))
        print('-' * 31)
        for c in self.clients:
            client = "client " + str(c.client_num)
            if c.liveness == True:
                print("#{:^14}#{:^14}#".format(client ,"alive"))
            else:
                print("#{:^14}#{:^14}#".format(client ,"disconnected")) 
            print('-' * 31)       
        print('#' * 31)           
# get imput from server, following this logic:
# 1. Choose Operation (Send Command, Refresh Status, Remove/Kill Client, Display Command Result)
# 2. Choose Sub Menu (If needed, for example choosing command to send)
# 3. choose Single Client/Broadcast
# 4. Choose Client (If needed)
# 5. Receive Input Arguments (If needed). 
    def get_input(self):
        self.command = ""
        client = ""
        args=""
        res = self.choose_operation()
        if res == 1:
            func = self.choose_sub_menu() 
            args = self.receive_input_args(func)
        if res == 1 or res == 3:    
            client = self.choose_client()
        self.command += "arguments "
        self.command += args
        return client, self.command, Commands[res]  

    def choose_operation(self):
        operation = int(input("choose_operation: \n 1 for Send command \n 2 for Refresh status \n 3 for Remove client \n 4 for Display Command Result\n"))
        return operation

    def choose_sub_menu(self):
        command_id = int(input("choose function from library \n 1 for Hello \n 2 for Add \n 3 for Mul \n 4 for Fibonacci\n"))
        self.command+=Functions[command_id]
        self.command+=", "
        return Functions[command_id]

    def choose_client(self):
        client = input("choose client << type -1 for broadcast >>\n")
        return client

    def check_args(self, args, command):
        if command == "Add" or command == "Mul":
            for arg in args:
                if not (arg.isdigit() or (arg.startswith('-') and arg[1:].isdigit())):
                    return False
        elif command == "Fibonaci": 
                for arg in args:
                    if not arg.isdigit():
                        return False
        return True             
                                 

    def receive_input_args(self, command):
        if len(argTypes[command]) == 0:
            return ""
        args = input("insert " + str(len(argTypes[command])) + " args, types " + str(argTypes[command]) + "\nwith a space saparating beetween them, e.g for 3 args (1,2,3) insert: 1 2 3 \n")
        argsCheck = args.split()
        
        while len(argTypes[command]) != len(argsCheck) or not self.check_args(argsCheck, command):
            print("invalid args, wrong number of args or wrong types\n ")
            args = input("insert " + str(len(argTypes[command])) + " args, types " + str(argTypes[command]) + "\nwith a space saparating beetween them, e.g for 3 args (1,2,3) insert: 1 2 3 \n")
            argsCheck = args.split()
        return str(args)


