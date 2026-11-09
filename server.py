#!/usr/bin/python3

from socket import *
import threading

SERVER_PORT = 12000
def handle_client(connection, address):
    print(f"Client connected: {address}")
    while True:
        message = connection.recv(1024)
        if not message:
            break
        message = message.decode().strip()
        if message == "STOP":
            break
        connection.send(message.encode())
    connection.close()
    print(f"Client disconnected: {address}")

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", SERVER_PORT))
server_socket.listen()

print(f"Server listening on port {SERVER_PORT}")
while True:
    connection, address = server_socket.accept()
    thread = threading.Thread(
        target=handle_client,
        args=(connection, address)
    )
    thread.start()