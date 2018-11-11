import select
import socket
import sys
import struct
from datetime import datetime
from datetime import timedelta


class CalculatorCacheProxy:
    def __init__(
            self,
            addr='localhost',
            port=8801,
            server_addr='localhost',
            server_port=8802,
            timeout=1,
            cache_lifetime=10
    ):
        self.client = self.setup_client()
        self.server = self.setup_server(addr, port)
        self.calc_server_address = (server_addr, server_port)
        self.inputs = [self.server]
        self.timeout = timeout
        self.cache = {}
        self.cache_lifetime = cache_lifetime

    def setup_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return client

    def setup_server(self, addr, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = (addr, port)
        server.bind(server_address)
        server.listen(5)
        return server

    def send_packet(self, packet):
        self.client.sendto(packet, self.calc_server_address)

    def receive_packet(self):
        return self.client.recvfrom(4096)

    def handle_connections(self):
        while self.inputs:
            self.clear_cache()
            readable, writable, exceptional = select.select(
                self.inputs, [], self.inputs, self.timeout
            )
            if not (readable or writable or exceptional):
                continue
            self.handle_inputs(readable)
            self.handle_exception(exceptional)

    def handle_exception(self, exceptional):
        for sock in exceptional:
            # print >>sys.stderr, 'Handling exceptional condition for', sock.getpeername()
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

    def handle_data_from_client(self, sock):
        data = sock.recv(1024)
        if data:
            result = self.calculate(data)
            sock.sendall(str(result))
        else:
            # print >>sys.stderr, 'Closing', sock.getpeername(), 'after reading no data'
            self.inputs.remove(sock)
            sock.close()

    def calculate(self, packed_data):
        unpacker = struct.Struct('f c f')
        unpacked_data = unpacker.unpack(packed_data)
        data_string = ' '.join(map(str, unpacked_data))
        print '>', data_string
        if data_string in self.cache:
            print 'Known calculation, getting result from cache...'
            return self.cache[data_string]['result']
        else:
            print 'New calculation, calculating...'
            self.send_packet(packed_data)
            result, address = self.receive_packet()
            cache_entry_lifetime = datetime.now() + timedelta(seconds=self.cache_lifetime)
            self.cache[data_string] = {
                'result': result,
                'lifetime': cache_entry_lifetime,
            }
            return result

    def clear_cache(self):
        now = datetime.now()
        self.cache = {k: v for k, v in self.cache.items() if v['lifetime'] > now}


CALCULATOR_CACHE_PROXY = CalculatorCacheProxy()
CALCULATOR_CACHE_PROXY.handle_connections()
