"""""/
@Author: Sergio Remigio
@Date: 03/03/2021
@Email: sergioremigio16@gmail.com
"""

from socket import *
from random import randint
import time
import multiprocessing
import os
import unittest

server_ip = '172.17.0.7'
server_port = 1100

class SelectCell(unittest.TestCase):
    def expectedbehavior_result:
        pass


if __name__ == "__main__":
    # Create TCP socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    # Connect to spreadsheet_server
    first_contact = 'userName\nNewSpreadsheet\n'
    client_socket.sendall(first_contact.encode())
    final_contact = False
    # We get back every file name
    while True:
        data = client_socket.recv(1024)
        receivedMessage = data.decode()
        if receivedMessage.find("\n\n"):
            print(data)
            break

    # Positive tests
    # Negative tests

