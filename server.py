from socket import *
import threading # brug threading for at flere klienter kan sende beskeder på samme tid
from argon2 import PasswordHasher

SECRET = "1234"
ph = PasswordHasher()
hash_secret = ph.hash(SECRET)

def check_hash(input_secret):
    ph.verify(hash_secret, input_secret)
    return

SERVER_PORT = 20000
def handle_client(connection, address):
    print(f"Client connected: {address}")

    try:
        authentication = connection.recv(1024).decode
    
    while True:
        message = connection.recv(2048)
        if not message:
            break
        message = message.decode().strip()
        if message == "STOP":
            break
        connection.send(message.encode())
    connection.close()
    print(f"Client disconnected: {address}")

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # lærer Alex's metode til genbrug af port
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

# password: 1234
# KDF-funktion: Argon2id