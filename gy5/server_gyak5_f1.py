import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
sock.bind(server_address)

data, address = sock.recvfrom(4096)

print "Incoming message from", address
print "Message:", data

sock.sendto('Hello kliens', address)

