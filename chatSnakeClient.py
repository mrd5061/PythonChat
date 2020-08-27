
#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    while True:
        try: 
            msg = client_socket.recv(BUFFERSZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError: 
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event = None):
    my_msg.set("{quit")
    send()

def create_Port(HOST, PORT):
    ADDR = (HOST, int(PORT))
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)
    return client_socket


"""Define the main tkinter window"""
top = tkinter.Tk()
top.title("Chat with Sneks")
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type Messages Here")
scrollbar = tkinter.Scrollbar(messages_frame)

""" Define the message window"""
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set) 
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

"""Define the entry field and the send button"""
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)

"""Set up the port protocols"""

HOST = input('Enter host: ')
PORT = input('Enter port: ')

BUFFERSZ = 1024
client_socket = create_Port(HOST,PORT)

"""Create a new thread and start the GUI loop"""
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.

