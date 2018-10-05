import socket
import struct
import sys

client = socket.socket()

server_address = ('localhost', 10000)
client.connect(server_address)

packer = struct.Struct('3s i i')
values = (sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
packed_data = packer.pack(*values)

client.sendall(packed_data)
