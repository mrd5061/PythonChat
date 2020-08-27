#!/usr/bin/env python3
"""Server program for a multithreaded (asynchronos) chat application"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_connection():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." %client_address)
        client.send(bytes("Hello! Please enter your name to get chatting!", "utf8"))
        addresses[client] = client_address
        Thread(target = handle_connection, args=(client,)).start()

def handle_connection(client):
    name = client.recv(BUFFERSZ).decode("utf8")
    welcome = 'Welcome %s! If you want to quit type {quit} to exit.' %name
    client.send(bytes(welcome,"utf8"))

    #Send message to all in the chat.
    msg = "%s has joined the chat!" %name
    send_message_all(bytes(msg,"utf8"))

    clients[client] = name #add the current clients to the list

    while True:
        msg = client.recv(BUFFERSZ)
        if msg != bytes("{quit}", "utf8"):
            send_message_all(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            send_message_all(bytes("%s has left the chat" %name , "utf8"))
            break

def send_message_all(msg, prefix=""): #prefix is used to identify users
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


clients = {}
addresses = {}

HOST = ''
PORT = 3300
BUFFERSZ = 1024
ADDR = (HOST,PORT)

SERVER = socket(AF_INET,SOCK_STREAM)
SERVER.bind((ADDR))

if __name__ == "__main__":
    SERVER.listen(5)
    print("waiting for connections...")
    
    ACCEPT_THREAD = Thread(target=accept_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
    exit()


