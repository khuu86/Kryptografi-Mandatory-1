#!/usr/bin/python3

from socket import *

SERVER_NAME = "localhost"
SERVER_PORT = 12000
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((SERVER_NAME, SERVER_PORT))
while True:
    message = input("Message: ")
    client_socket.send(message.encode())
    if message == "STOP":
        break
    response = client_socket.recv(1024).decode()
    print("From server:", response)
client_socket.close()


# Mads's kommentar