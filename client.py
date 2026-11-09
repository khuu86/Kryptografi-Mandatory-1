#!/usr/bin/python3
from socket import *

SERVER_NAME = "localhost"
SERVER_PORT = 20000
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((SERVER_NAME, SERVER_PORT))
while True:
    message = input("Message: ")
    client_socket.send(message.encode())
    if message == "STOP":
        break
    modified_message = client_socket.recv(2048)
    print("From server: ", modified_message.decode())
client_socket.close()