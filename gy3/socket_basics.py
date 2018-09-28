import socket

print "machine's hostname: " + socket.gethostname()

hostnames = ["homer", "www.python.org", "inf.elte.hu"]
addresses = ["157.181.161.79", "185.43.207.92"]

for hostname in hostnames:
    print "> " + hostname
    try:
        print socket.gethostbyname(hostname)
        print socket.gethostbyname_ex(hostname)
    except:
        print "Name or service not known"

for address in addresses:
    print "> " + address
    print socket.gethostbyaddr(address)

print "> getaddrinfo python.org"
for response in socket.getaddrinfo("www.python.org", "http"):
    family, socktype, proto, canonname, sockaddr = response
    print family, socktype, proto, canonname, sockaddr

print "> getaddrinfo inf.elte.hu"
for response in socket.getaddrinfo(
    "inf.elte.hu", 
    "http",
    socket.AF_INET,
    socket.SOCK_STREAM,
    socket.IPPROTO_TCP,
    socket.AI_CANONNAME,
):
    family, socktype, proto, canonname, sockaddr = response
    print family, socktype, proto, canonname, sockaddr

