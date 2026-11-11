from socket import *
import threading # brug threading for at flere klienter kan sende beskeder på samme tid
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

password_hasher = PasswordHasher()

# Genereret midlertidig hash: python3 -c "from argon2 import PasswordHasher; print(PasswordHasher().hash('1234'))" 
STORED_HASH = "$argon2id$v=19$m=65536,t=3,p=4$o6kmtal9+D+3bjdGgDxS3Q$J0MdpJSo7DAiLRrOSudQCijIOsQGhVaqdNmWDSNLCAo"

def verify_code(code):
    try:
        return password_hasher.verify(STORED_HASH, code)
    except VerifyMismatchError:
        return False

SERVER_PORT = 20000
def handle_client(connection, address):
    print(f"Client connected: {address}")

    # Login skal ske før chatten starter
    connection.send(b"Enter code: ")

    code = connection.recv(2048).decode().strip()

    if verify_code(code):
        connection.send(b"Hash match, you are connected.")
        print(f"Authentication successful: {address}")
    else:
        connection.send(b"Hash mismatch, disconnected.")
        connection.close()
        print(f"Authentication failed: {address}")
        return

    # Chat-loopet starter først efter korrekt login
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