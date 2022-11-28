import socket


def sendAndReceive(s_socket, payload, address, asks, timeout, expected):
    s_socket.settimeout(timeout)
    for i in range(0, asks):
        try:
            s_socket.sendto(payload, address)
            payload = s_socket.recv(1024)
            if payload == expected:
                return True
        except socket.timeout:
            print("Timeout - retrying")
            pass
    return False


def receiveAndSend(s_socket, payload, timeout, expected):
    s_socket.settimeout(timeout)
    try:
        incoming, address = s_socket.recv(1024)
        if incoming == expected:
            s_socket.sendto(payload, address)
            return True
    except socket.timeout:
        print("Timeout - retrying")
        pass
    return False


def UDPClient():
    coffee_machine_server_address = ("192.168.43.244", 3000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Order coffee
    print("Ordering coffee . . ", end="", flush=True)
    if sendAndReceive(sock, b"COFFEE", coffee_machine_server_address, 5, 3, b"ACCEPTED"):
        print("Accepted. Waiting for connection . . ", end="", flush=True)

        # Wait for coffee machine to ask for connection
        if receiveAndSend(sock, b"CONNECTED", 300, b"CONNECT"):
            print("Connected. Waiting for payment . . ", end="", flush=True)

            # Wait for coffee machine to ask for payment
            if receiveAndSend(sock, b"PAYMENT", 10, b"PAY"):
                print("Payment accepted. Waiting for receipt . . ", end="", flush=True)

                # Wait for coffee machine to ask for receipt
                if receiveAndSend(sock, b"ARRIVED", 10, b"RECEIPT"):
                    print("Receipt accepted. Waiting for coffee . . ", end="", flush=True)

                    # Wait for coffee machine to ask for coffee
                    if receiveAndSend(sock, b"THANKS", 10, b"COFFEE"):
                        print("Coffee received. Enjoy!")
                    else:
                        print("Coffee machine did not respond")
                else:
                    print("Coffee machine did not respond")
            else:
                print("Coffee machine did not respond")
    else:
        print("Coffee machine rejected order - OUT OF COFFEE")


def main():
    for i in range(0, 10):
        print("Ordering coffee #{}".format(i + 1))
        UDPClient()


if __name__ == '__main__':
    main()
