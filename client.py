#!/usr/bin/python3
from socket import *

SERVER_NAME = "localhost"
SERVER_PORT = 20000

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((SERVER_NAME, SERVER_PORT))

# Modtag login-prompt fra serveren
prompt = client_socket.recv(2048).decode()
print(prompt, end="")

# Send den oprindelige kode '1234'
code = input()
client_socket.send(code.encode())

# Modtag resultatet af verificeringen
authentication_response = client_socket.recv(2048).decode()
print(authentication_response)

# Luk hvis koden er forkert
if authentication_response == "Hash mismatch, disconnected.":
    client_socket.close()
    exit()

# Chat starter først efter korrekt authentication
while True:
    message = input("Message: ")

    if not message or message == "STOP":
        client_socket.send(message.encode())
        break

    client_socket.send(message.encode())

    modified_message = client_socket.recv(2048)
    print("From server:", modified_message.decode())

client_socket.close()