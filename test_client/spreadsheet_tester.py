"""""/
@Author: Sergio Remigio, Travis Schnider
@Date: 04/28/2021
"""

from socket import *
from random import randint
import time
import multiprocessing
import os
import unittest
import json

server_ip = '136.36.159.0'
server_port = 1100
connection_to_server = socket(AF_INET, SOCK_STREAM)


def send_to_server(message):
    """
    Sends a message to the serever as a string
    :param message: Message to send(string)
    """
    message_in_bytes = bytes(message, "utf-8")
    print("Trying to send this to server:", message)
    connection_to_server.sendall(message_in_bytes)
    print("Finished sending:", message )


def receive_from_server():
    """
    return received data from server as string
    decoded with utf-8
    :return: response data(string)
    """
    print("Expecting to receive from server:")
    data = connection_to_server.recv(1024)
    print(data)
    response = data.decode("utf-8")
    print("Received:", response)
    return response


def connect_to_server():
    try:
        global connection_to_server
        # Attempt to connect to host
        connection_to_server = socket(AF_INET, SOCK_STREAM)
        # Connect to spreadsheet_server
        connection_to_server.connect((server_ip, server_port))
        print("Connection Success")
    # Reconnect
    except ConnectionRefusedError:
        print("Reconnecting in 5 seconds.")
        time.sleep(5)
    except:
        print("Connection aborted")


def close_server():
    connection_to_server.close()


def check_received_spreadsheet_files(response):
    """
    :param response: response from server
    :return: True if response are spreadsheet files, False if not
    """
    return '\n\n' in response


def do_hand_shake():
    """
    Helper method to do handshake protocol.
    Used to reduce duplicate lines.
    """
    send_to_server("Dude\n")
    receive_from_server()
    send_to_server("MegaDude\n")
    receive_from_server()


"""--------------------------------Begin Test Cases----------------------------------------------------------"""


class Handshake(unittest.TestCase):
    def test_fullHandshake_NoServerErrors(self):
        connect_to_server()
        send_to_server("Dude\n")
        response = receive_from_server()
        self.assertTrue(check_received_spreadsheet_files(response))
        send_to_server("MegaDude\n")
        response = receive_from_server()
        self.assertTrue(isinstance(int(response), int))
        close_server()

    def test_sendNameThenCloseSocket_serverClosesGracefully(self):
        connect_to_server()
        send_to_server("MegaDude\n")
        response = receive_from_server()
        self.assertTrue(check_received_spreadsheet_files(response))
        close_server()



class CellUpdate(unittest.TestCase):
    connect_to_server()
    do_hand_shake()
    request = '{"requestType":"editCell","cellName":"K16","contents":"18"}'
    send_to_server(request)
    response = receive_from_server()
    print("-------------------------------------------------------")
    close_server()


class SelectCell(unittest.TestCase):
    def test_cellSelected_continueWithoutCrash(self):
        connect_to_server()
        do_hand_shake()
        request = '{"requestType": "selectCell", "cellName": "K16"}'
        send_to_server(request)
        send_to_server(request)
        close_server()

    def test__cellSelectedInvalidCell_continueWithoutCrash(self):
        connect_to_server()
        do_hand_shake()
        request = '{"requestType": "selectCell", "cellName": "!@#%%!@#$!@#$$$$$$"}'
        send_to_server(request)
        request = '{"requestType": "selectCell", "cellName": "K16"}'
        send_to_server(request)
        close_server()


class RequestType(unittest.TestCase):
    def test_cellSelected_continueWithoutCrash(self):
        connect_to_server()
        do_hand_shake()
        request = '{"requestType": "selectCell", "102983)(*^)(*": "K16"}'
        send_to_server(request)
        request = '{"requestType": "selectCell", "cellName": "K16"}'
        send_to_server(request)
        close_server()


class Undo(unittest.TestCase):
    def test_sendUndo_continueWithoutCrash(self):
        connect_to_server()
        do_hand_shake()
        request = '{"requestType": "undo"}'
        send_to_server(request)
        request = '{"requestType": "selectCell", "cellName": "K16"}'
        send_to_server(request)
        close_server()


"""--------------------------------End Test Cases----------------------------------------------------------"""

if __name__ == "__main__":
    unittest.main()
