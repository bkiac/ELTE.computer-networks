import socket


def diff_manchester(bits):
    first = '01' if bits[0] == '1' else '10'
    clock = [first]
    for i in range(1, len(bits)):
        prev = clock[i-1]
        bit = bits[i]
        if bit == '1':
            if prev == '10':
                clock.append('01')
            else:
                clock.append('10')
        else:
            clock.append(prev)
    return clock

def manchester(bits):
    clock = ['10' if bit == '1' else '01' for bit in bits]
    return clock

def nrzl(bits):
    clock = [bit+bit for bit in bits]
    return clock

def rz(bits):
    clock = [bit+'0' for bit in bits]
    return clock


codings = {
    'DiffManchester': diff_manchester,
    'Manchester': manchester,
    'NRZ-L': nrzl,
    'RZ': rz,
}
server = socket.socket()
server_address = ('localhost', 9865)
server.bind(server_address)
server.listen(1)
while True:
    client, client_address = server.accept()
    coding, bits = client.recv(1024).split(',')
    clock = codings[coding](bits)
    clock_string = ','.join(clock)
    client.sendall(clock_string)
