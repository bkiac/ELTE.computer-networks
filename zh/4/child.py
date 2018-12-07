import socket
import sys
import struct


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class Child:
    def __init__(self, server_addr='localhost', server_port=1207):
        self.setup_client(server_addr, server_port)
        self.setup_client_udp()

    def setup_client(self, server_addr, server_port):
        server_address = (server_addr, server_port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(server_address)

    def setup_client_udp(self):
        self.client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_packet(self, packet):
        self.client_udp.sendto(packet, self.server_address_udp)

    def receive_packet(self):
        return self.client_udp.recvfrom(4096)

    def handle_connection(self):
        name = raw_input('Name: ')
        if name != '':
            self.name = name
            self.client.sendall(name)
        self.handle_data_from_server()

    def handle_data_from_server(self):
        data = self.client.recv(4096)
        if not isInt(data):
            print data
        else:
            self.server_address_udp = ('localhost', int(data))
            self.send_packet(self.name)
            self.handle_data_from_server_udp()

    def handle_data_from_server_udp(self):
        data, address = self.receive_packet()
        print data


CHILD = Child()
CHILD.handle_connection()
