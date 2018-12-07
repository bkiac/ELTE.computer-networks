import socket
import sys
import struct


class Child:
    def __init__(self, server_addr='localhost', server_port=1207):
        self.setup_client(server_addr, server_port)

    def setup_client(self, server_addr, server_port):
        server_address = (server_addr, server_port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(server_address)

    def handle_connection(self):
        msg = raw_input('Name: ')
        if msg != '':
            msg = self.pack_name(msg)
            self.client.sendall(msg)
        self.handle_data_from_server()

    def pack_name(self, name):
        # packer = struct.Struct('s')
        # packed_data = packer.pack(name)
        # return packed_data
        return name

    def handle_data_from_server(self):
        data = self.client.recv(4096)
        if not data:
            sys.exit()
        else:
            print data

CHILD = Child()
CHILD.handle_connection()
