import socket
import sys


class GuessingGameClient:
    def __init__(self, server_addr='localhost', server_port=10001):
        self.setup_client(server_addr, server_port)

    def setup_client(self, server_addr, server_port):
        server_address = (server_addr, server_port)

        # Create a TCP/IP socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.client.connect(server_address)

    def handle_data_from_server(self):
        data = self.client.recv(4096)
        if not data:
            print '\nDisconnected from server'
            sys.exit()
        else:
            print data

    def handle_connection(self):
        while True:
            msg = raw_input('Message: ')
            if msg != '':
                msg = msg.strip()
                self.client.send(msg)
            self.handle_data_from_server()


GUESSING_GAME_CLIENT = GuessingGameClient()
GUESSING_GAME_CLIENT.handle_connection()

