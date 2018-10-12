import socket
import sys


class PostOfficeClient:
    def __init__(self, client_name, server_ip='localhost', server_port=2448):
        self.name = client_name
        self.server_address = (server_ip, server_port)
        self.client = self.setup_client()

        self.login_client()

    def setup_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return client

    def send_packet(self, packet):
        self.client.sendto(packet, self.server_address)

    def receive_packet(self):
        return self.client.recvfrom(4096)

    def login_client(self):
        packet = 'LOGIN+' + self.name
        self.send_packet(packet)

    def handle_inputs(self):
        while True:
            try:
                addressee = raw_input('Addressee: ').strip()
                if addressee == 'QUERY':
                    packet = 'QUERY+EMPTY'
                    self.send_packet(packet)
                    data, address = self.receive_packet()
                    print 'Your messages:', data
                else:
                    msg = raw_input('Message: ').strip()
                    packet = addressee + '+' + msg
                    self.send_packet(packet)
            except KeyboardInterrupt:
                print 'This client has been stopped.'
                sys.exit()


name = sys.argv[1].strip()
POST_OFFICE_CLIENT = PostOfficeClient(name)
POST_OFFICE_CLIENT.handle_inputs()
