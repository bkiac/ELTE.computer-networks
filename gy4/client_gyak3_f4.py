import socket
import struct

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
connection.connect(server_address)

values = (7.0, '-', 2.0)

packer = struct.Struct('f c f')
packed_data = packer.pack(*values)

print '%f %s %f' % values
connection.sendall(packed_data)

result = connection.recv(16)

print result

connection.close()