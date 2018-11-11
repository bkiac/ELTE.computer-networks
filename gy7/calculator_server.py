import socket
import sys
import struct
import operator


class CalculatorServer:
    def __init__(self, ip='localhost', port=8802):
        self.server = self.setup_server(ip, port)

    def setup_server(self, ip, port):
        server_address = (ip, port)
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(server_address)
        return server

    def send_packet(self, packet, socket_address):
        self.server.sendto(packet, socket_address)

    def receive_packet(self):
        return self.server.recvfrom(4096)

    def handle_packets(self):
        while True:
            packed_data, address = self.receive_packet()
            result = self.calculate(packed_data)
            self.send_packet(str(result), address)

    def calculate(self, packed_data):
        unpacker = struct.Struct('f c f')
        unpacked_data = unpacker.unpack(packed_data)
        data_string = ' '.join(map(str, unpacked_data))
        print '>', data_string
        print 'Calculating...'
        result = self.apply_operation(*unpacked_data)
        return result

    def apply_operation(self, a, op, b):
        ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.div}
        return ops[op](a, b)


CALCULATOR_SERVER = CalculatorServer()
CALCULATOR_SERVER.handle_packets()
