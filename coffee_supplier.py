import socket
from time import sleep

# Create a UDP server socket
Host = "192.168.1.167"
Port = 3000
bufferSize = 1024

request = b"REFILL"

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind the socket to the port
sock.bind((Host, Port))

print("supplier is listening on coffee machine")

while True:
    data, address = sock.recvfrom(bufferSize)
    print("received message: %s" % data)
    if data == request:
        sleep(1)  # wait for 1 second
        sock.sendto(b"REFILLED", address)
