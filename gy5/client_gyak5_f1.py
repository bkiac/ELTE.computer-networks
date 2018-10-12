import socket

connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)

connection.sendto('Hello szerver', server_address)

data, address = connection.recvfrom(4096)

print "Incoming message from", address
print "Message:", data

connection.close()
