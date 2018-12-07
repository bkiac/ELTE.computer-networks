import socket
import sys
import random

class Elf:
    def __init__(self, ip='localhost', port=10002):
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
            data, address = self.receive_packet()
            gift = self.get_gift(data)
            self.send_packet(gift, address)

    def get_gift(self, data):
        # gifts = ['VIRGACS', 'SZALONCUKOR', 'LABDA']
        number = random.randint(0, 10)
        print number, 'for child', data
        if number < 4:
            return 'VIRGACS'
        elif 4 <= number < 7:
            return 'SZALONCUKOR'
        else:
            return 'LABDA'


port = sys.argv[1].strip()
ELF = Elf(port=int(port))
ELF.handle_packets()
