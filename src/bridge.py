'''
Handles communication between client and server over sockets.
'''

import socket


class Network:

    def __init__(self, Address, Port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = Address
        self.port = int(Port)
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def communicate(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
