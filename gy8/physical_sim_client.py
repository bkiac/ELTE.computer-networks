import sys
import socket


client = socket.socket()
server_address = ('localhost', 9865)
client.connect(server_address)
input_coding = sys.argv[1]
input_bits = sys.argv[2][:16]
client.sendall(input_coding + ',' + input_bits)
clock = client.recv(1024)
print 'Coding:', input_coding
print 'Input:', input_bits
print '>', clock
client.close()
