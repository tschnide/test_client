from socket import *
import json
import sys


if __name__ == "__main__":
    json = b'{"id": 2, "name": "abc"}'

    serverPort = 1100
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen()
    print('The server is ready to receive')
    while True:
        connectionSocket, addr = serverSocket.accept()
        # Receive data
        sentence = connectionSocket.recv(1024).decode()
        # Send Json
        connectionSocket.send(json)
