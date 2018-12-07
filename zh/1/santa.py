import select
import socket
import sys
import random
import struct
import operator


class Santa:
    def __init__(self, addr='localhost', port=1207, timeout=1):
        self.server = self.setup_server(addr, port)
        self.inputs = [self.server]
        self.timeout = timeout
        self.gifts = {
            'Arthur': 'horse',
            'Jack': 'book',
        }

    def setup_server(self, addr, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = (addr, port)
        server.bind(server_address)
        server.listen(5)
        return server

    def handle_connections(self):
        while self.inputs:
            readable, writable, exceptional = select.select(
                self.inputs, [], self.inputs, self.timeout,
            )
            if not (readable or writable or exceptional):
                continue
            self.handle_inputs(readable)
            self.handle_exception(exceptional)

    def handle_exception(self, exceptional):
        for sock in exceptional:
            self.inputs.remove(sock)
            sock.close()

    def handle_inputs(self, readable):
        for sock in readable:
            if sock is self.server:
                self.handle_new_connection(sock)
            else:
                self.handle_data_from_client(sock)

    def handle_new_connection(self, sock):
        connection, client_address = sock.accept()
        connection.setblocking(0)
        self.inputs.append(connection)
        print 'Accept new connection from', client_address

    def handle_data_from_client(self, sock):
        data = sock.recv(1024)
        data = data.strip()
        if data:
            gift = self.get_gift(data)
            sock.sendall(gift)
            print 'Closing connection'
            self.inputs.remove(sock)
            sock.close()
        else:
            self.inputs.remove(sock)
            sock.close()

    def get_gift(self, packed_data):
        # unpacker = struct.Struct('s')
        # unpacked_data = unpacker.unpack(packed_data)
        if packed_data in self.gifts:
            gift = self.gifts[packed_data]
            del self.gifts[packed_data]
            return gift
        else:
            return 'No gift for you!'

SANTA = Santa()
SANTA.handle_connections()
