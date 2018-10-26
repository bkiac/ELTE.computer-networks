import socket
import struct
import sys


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.settimeout(3)

ttl = struct.pack('b', 1) # time to live / "hop count"
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

multicast_group_address = ('224.3.29.71', 10000)
try:
    sock.sendto('Hello clients', multicast_group_address)

    while True:
        try:
            data, client_address = sock.recvfrom(4096)
        except socket.timeout:
            print 'Timed out...'
        else:
            print 'Incoming message from', client_address
            print 'Message: ', data
finally:
    print >>sys.stderr, 'Closing socket...'
    sock.close()
