import socket
import sys

client = socket.socket()

server_address = ('localhost', int(sys.argv[1]))
client.connect(server_address)

client.sendall('Hello server')

data = client.recv(16)

print data

client.close()