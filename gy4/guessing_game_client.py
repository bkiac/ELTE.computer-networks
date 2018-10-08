import socket
import sys
import struct


class GuessingGameClient:
    def __init__(self, server_addr='localhost', server_port=8801):
        self.setup_client(server_addr, server_port)

    def setup_client(self, server_addr, server_port):
        server_address = (server_addr, server_port)

        # Create a TCP/IP socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.client.connect(server_address)

    def handle_connection(self):
        while True:
            # '> n' OR '< n' OR '= n'
            msg = raw_input('Guess: ')
            if msg != '':
                msg = self.pack_guess(msg)
                self.client.sendall(msg)
            self.handle_data_from_server()

    def pack_guess(self, guess):
        packer = struct.Struct('cH')

        unpacked_data = guess.split(' ')
        packed_data = packer.pack(unpacked_data[0], int(unpacked_data[1]))

        return packed_data


    def handle_data_from_server(self):
        data = self.client.recv(4096)
        if not data:
            print 'The game has already ended.'
            sys.exit()
        elif data == 'win' or data == 'end':
            print data
            sys.exit()
        else:
            print data


GUESSING_GAME_CLIENT = GuessingGameClient()
GUESSING_GAME_CLIENT.handle_connection()
