import socket
import sys
import Queue


class PostOfficeServer:
    def __init__(self, ip='localhost', port=2448):
        self.server = self.setup_server(ip, port)
        self.address_table = {}
        self.queue_table = {}

    def setup_server(self, ip, port):
        server_address = (ip, port)
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(server_address)
        return server

    def send_packet(self, packet, socket_address):
        self.server.sendto(packet, socket_address)

    def receive_packet(self):
        return self.server.recvfrom(4096)

    def get_client_name_by_socket(self, client_address):
        for name, address in self.address_table.items():
            if address == client_address:
                return name

    def collect_messages(self, queue):
        messages = ''
        if queue.empty():
            messages = 'EMPTY'
            return messages
        while not queue.empty():
            messages = messages + queue.get() + '|'
        return messages[:-1]

    def handle_packets(self):
        while True:
            try:
                data, address = self.receive_packet()
                data = data.split('+')
                if data[0] == 'LOGIN':
                    self.address_table[data[1]] = address
                    self.queue_table[data[1]] = Queue.Queue()
                elif data[0] == 'QUERY':
                    client_name = self.get_client_name_by_socket(address)
                    queue = self.queue_table[client_name]
                    messages = self.collect_messages(queue)
                    self.send_packet(messages, address)
                elif data[0] in self.queue_table:
                    self.queue_table[data[0]].put(data[1])
            except KeyboardInterrupt:
                print 'Closing the post office...'
                sys.exit()


POST_OFFICE_SERVER = PostOfficeServer()
POST_OFFICE_SERVER.handle_packets()
