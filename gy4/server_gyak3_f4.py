import socket
import struct
import operator

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
sock.bind(server_address)

sock.listen(1)

connection, client_address = sock.accept()

data = connection.recv(16)
print 'Packed data:', data

unpacker = struct.Struct('f c f')
unpacked_data = unpacker.unpack(data)
print 'Unpacked data:', unpacked_data

def applyOp(in1, op, in2):
  ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.div}
  return ops[op](in1, in2)

result = applyOp(*unpacked_data)

print 'Result:', result

connection.sendall(str(result))