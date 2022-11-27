import socket


def UDPClient():
    server_address = ("127.0.0.1", 3000)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    data = "Hello World"

    sock.sendto(bytes(data + "\n", "utf-8"), server_address)
    received = str(sock.recv(1024), "utf-8")
    print("Sent: {}".format(data))
    print("Received: {}".format(received))


def main():
    UDPClient()


if __name__ == '__main__':
    main()
