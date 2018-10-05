import socket
import struct

server = socket.socket()
server_address = ('localhost', 10000)
server.bind(server_address)
server.listen(1)

client, client_address = server.accept()

unpacker = struct.Struct('3s i i')

packed_data = client.recv(32)
unpacked_data = unpacker.unpack(packed_data)
print unpacked_data

operation = unpacked_data[0]
num1 = unpacked_data[1]
num2 = unpacked_data[2]

if operation == 'add':
    print num1 + num2
elif operation == 'sub':
    print num1 - num2
elif operation == 'mul':
    print num1 * num2
elif operation == 'div':
    print float(num1) / num2
