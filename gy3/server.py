import socket
import sys

server = socket.socket() # default TCP
server_address = ('localhost', sys.argv[1])
server.bind(server_address)
server.listen(1) # only 1 client

client, client_address = server.accept()

data = client.recv(16)

print data

client.sendall('Hello client')