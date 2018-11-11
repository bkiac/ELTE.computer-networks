import socket
import sys
import struct


class CalculatorClient:
    def __init__(self, server_addr='localhost', server_port=8801):
        self.setup_client(server_addr, server_port)

    def setup_client(self, server_addr, server_port):
        server_address = (server_addr, server_port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(server_address)

    def handle_connection(self):
        while True:
            msg = raw_input('Calculate: ')
            if msg != '':
                packed_data = self.pack_operation(msg)
                self.client.sendall(packed_data)
            self.handle_data_from_server()

    def pack_operation(self, operation):
        unpacked_data = operation.split(' ')
        unpacked_data[0] = float(unpacked_data[0])
        unpacked_data[2] = float(unpacked_data[2])
        packer = struct.Struct('f c f')
        packed_data = packer.pack(*unpacked_data)
        return packed_data

    def handle_data_from_server(self):
        data = self.client.recv(4096)
        if not data:
            print 'The server has stopped.'
            sys.exit()
        else:
            print '>', float(data)


CALCULATOR_CLIENT = CalculatorClient()
CALCULATOR_CLIENT.handle_connection()
