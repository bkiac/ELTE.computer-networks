import select
import socket
import sys
import random
import struct
import operator


class GuessingGameServer:
    def __init__(self, addr='localhost', port=8801, timeout=1):
        self.number = random.randint(1, 100)
        print 'n =', self.number
        self.has_game_ended = False

        self.server = self.setup_server(addr, port)
        # Sockets from which we expect to read
        self.inputs = [self.server]
        # Wait for at least one of the sockets to be ready for processing
        self.timeout = timeout

    def setup_server(self, addr, port):
        # Create a TCP/IP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the port
        server_address = (addr, port)
        server.bind(server_address)

        # Listen for incoming connections
        server.listen(5)
        return server

    def handle_connections(self):
        while len(self.inputs) > 1 or not self.has_game_ended:
            readable, writable, exceptional = select.select(
                self.inputs, [], self.inputs, self.timeout
            )

            if not (readable or writable or exceptional):
                #print >>sys.stderr, '  timed out, do some other work here'
                continue

            self.handle_inputs(readable)
            self.handle_exception(exceptional)

        print 'The game has ended.'

    def handle_exception(self, exceptional):
        for sock in exceptional:
            print >>sys.stderr, 'handling exceptional condition for', sock.getpeername()
            # Stop listening for input on the connection
            self.inputs.remove(sock)
            sock.close()

    def handle_inputs(self, readable):
        for sock in readable:
            if sock is self.server:
                self.handle_new_connection(sock)
            else:
                self.handle_data_from_client(sock)

    def handle_new_connection(self, sock):
        # A "readable" server socket is ready to accept a connection
        connection, client_address = sock.accept()
        connection.setblocking(0)  # or connection.settimeout(1.0)
        self.inputs.append(connection)

    def handle_data_from_client(self, sock):
        data = sock.recv(1024)
        data = data.strip()
        if data:
            message = self.check_guess(data)
            sock.sendall(message)
        else:
            # Interpret empty result as closed connection
            print >>sys.stderr, 'closing', sock.getpeername(), 'after reading no data'
            # Stop listening for input on the connection
            self.inputs.remove(sock)
            sock.close()

    def check_guess(self, packed_data):
        if self.has_game_ended:
            return 'end'

        ops = {'<': operator.lt, '>': operator.gt, '=': operator.eq}
        res = {True: 'yes', False: 'no'}

        unpacker = struct.Struct('cH')
        unpacked_data = unpacker.unpack(packed_data)

        op = unpacked_data[0]
        if op == '=':
            guess_result = ops[op](self.number, unpacked_data[1])
            if guess_result:
                self.has_game_ended = True
                return 'win'
            else:
                return 'no'
        else:
            guess_result = ops[op](self.number, unpacked_data[1])
            return res[guess_result]


GUESSING_GAME_SERVER = GuessingGameServer()
GUESSING_GAME_SERVER.handle_connections()
