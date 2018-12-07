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
        self.elfs = [10002, 10003]
        self.client_addresses = {}

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
        self.client_addresses[connection] = client_address
        print 'Accept new connection from', client_address

    def handle_data_from_client(self, sock):
        data = sock.recv(1024)
        data = data.strip()
        if data:
            elf = self.get_elf(sock)
            sock.sendall(str(elf))
            print 'Closing connection'
            self.inputs.remove(sock)
            sock.close()
        else:
            self.inputs.remove(sock)
            sock.close()

    def get_elf(self, sock):
        port = self.client_addresses[sock][1]
        print 'Calculating parity for', port
        parity = port % 2
        return self.elfs[parity]
        

SANTA = Santa()
SANTA.handle_connections()
