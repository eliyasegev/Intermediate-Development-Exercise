#!/usr/bin/env python3

import socket
import threading
import sys
import os
import time
from cli import CLI

# send 4096 bytes each time step
BUFFER_SIZE = 4096 
# define host and port
HOST = "localhost"
PORT = 5000
clients = []
number_of_clients = 0 


# client class to handle the data received from the user 
# in case pipe betwenn server and client were broken
# or keppAlive message not sent for 20 seconds - 
# client not availabe, print info to log.txt and update log.txt
class Client(threading.Thread):
    def __init__(self, socket, address, client_num, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.client_num = client_num
        self.signal = signal
        self.keepAlive = int(time.time())
        self.liveness = True


    def __str__(self):
        return str(self.id) + " " + str(self.address)

# hanlde received  data from client
# 1. if massege is "alive" update keep alive timer
#    in case server did not receive "alive" message for 20 seconds - client is not available
# 2. take care of any othoe givan data , print input to log or result file according to input content


    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(BUFFER_SIZE)
                time.sleep(1)
                if (str(data.decode("utf-8"))) == "alive":
                        self.keepAlive = int(time.time())
                elif "[Result]" in str(data.decode("utf-8")):
                        log_file = open("result.txt", "a")       
                        log_file.write("from client " + str(self.client_num) + ": " + str(data.decode("utf-8") +"\n"))
                        log_file.close()
                elif str(data.decode("utf-8")): 
                        log_file = open("log.txt", "a")       
                        log_file.write("[Message...] from client " + str(self.client_num) + ": " + str(data.decode("utf-8") +"\n"))
                        log_file.close()
                if (time.time() - self.keepAlive) > 20:
                        log_file = open("log.txt", "a")
                        log_file.write("Client " + str(self.address) + " has disconnected\n")
                        log_file.close()
                        self.signal = False
                        self.liveness = False
                        break   
            except:
                log_file = open("log.txt", "a")
                log_file.write("Client " + str(self.address) + " has disconnected\n")
                log_file.close()
                self.signal = False
                self.liveness = False
                break





# Wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global number_of_clients
        clients.append(Client(sock, address, number_of_clients, True))
        clients[len(clients) - 1].start()
        number_of_clients += 1
        

# send chosen client the .dll file
def sendLib(client_num):
    try:
        file_size = str(os.path.getsize('Lib.dll'))
        clients[int(client_num)].socket.sendall(str.encode(file_size))
        f = open("Lib.dll", 'rb')    
        command = f.read(int(file_size))
        clients[int(client_num)].socket.sendall(command)
    except:
        print("There was a problem sending the .dll file")
        sys.exit(0)      


# send chosen client the message, message contain name of function and values of arguments
# in case number pf client is '-1' --> send broadcast command to all clients 
# return true when number of client is legal
# return false otherwise
def sendClient(clients, myMessage, clientNum):
    try:
        ret = True
        if clientNum >= 0 and clientNum<len(clients) and clients[clientNum].liveness:
            sendLib(clientNum)
            clients[clientNum].socket.sendall(str.encode(myMessage))
        elif clientNum == -1:
            for client in clients:
                if client.liveness:
                    sendLib(client.client_num)
                    client.socket.sendall(str.encode(myMessage))     
        else:
            ret = False
        return ret
    except:
        print("There was a problem sending the data to the client")
        sys.exit(0)           

# remove client - close client socket and reupdate client liveness in clients list
# in case number pf client is '-1' --> send broadcast command to all clients 
# return true when number of client is legal
# return false otherwise
def removeClient(clients, clientNum):
     ret = True
     if clientNum >= 0 and  clientNum<len(clients) and clients[clientNum].liveness:
        clients[clientNum].socket.shutdown(socket.SHUT_RDWR)
        clients[clientNum].socket.close()
        clients[clientNum].liveness = False
     elif clientNum == -1:
        for client in clients:
            if client.liveness:
                client.socket.shutdown(socket.SHUT_RDWR)
                client.socket.close()
                client.liveness = False
     else:
        ret = False
     return ret 


# open log and result files, create new socket to wait for client connection
def initServer():
    log_file = open("log.txt", "w")
    log_file.close()
    result_file = open("result.txt", "w")
    result_file.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    return sock

# main functions will create a new thread  to wait for connections
# call CLI and follow the operator input
# loop make sure number of client is ok
def main():
    sock = initServer()
    newConnectionsThread = threading.Thread(target=newConnections, args=(sock,))
    newConnectionsThread.start()
    my_cli=CLI(clients)
    lock = threading.Lock()
    while True:
        with lock:
            my_cli.show_status()
        with lock:
            client_num, command, res = my_cli.get_input()
            if res == "Send command":
                while not sendClient(clients, command, int(client_num)):
                       client_num = input("client not available, please insert client number again:\n")                 
            elif res == "Refresh status":
                continue
            elif res == "Remove client":
                    while not removeClient(clients, int(client_num)):
                        client_num = input("client not available, please insert client number again:\n")                
            elif res == "Display Command Result":
                f = open("result.txt", "r")
                print(f.read())
                        
    #status()
  #  while True:

main()
