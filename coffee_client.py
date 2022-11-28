import socket
import time

import fakeTCP


def UDPClient():
    coffee_machine_server_address = ("192.168.1.167", 3000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Order coffee
    print("Ordering coffee.. ", end="", flush=True)
    if fakeTCP.sendAndReceive(sock, b"COFFEE", coffee_machine_server_address, 5, 3, b"ACCEPTED"):
        print("Accepted.\nWaiting for my turn.. ", end="", flush=True)

        # Wait for coffee machine to ask for connection
        if fakeTCP.receiveAndSend(sock, b"CONNECTED", 300, b"CONNECT"):
            print("My turn!\nWaiting for payment.. ", end="", flush=True)

            # Wait for coffee machine to ask for payment
            if fakeTCP.receiveAndSend(sock, b"PAYMENT", 10, b"PAY"):
                print("Payment accepted.\nWaiting for receipt.. ", end="", flush=True)

                # Wait for coffee machine to ask for receipt
                if fakeTCP.receiveAndSend(sock, b"ARRIVED", 10, b"RECEIPT"):
                    print("Receipt arrived.\nWaiting for coffee.. ", end="", flush=True)

                    # Wait for coffee machine to ask for coffee
                    if fakeTCP.receiveAndSend(sock, b"THANKS", 10, b"COFFEE"):
                        print("Coffee received. Enjoy!")
                    else:
                        print("Coffee machine did not respond - no coffee for you!")
                else:
                    print("Coffee machine did not respond")
            else:
                print("Coffee machine did not respond")
    else:
        print("Coffee machine rejected order")


def main():
    for i in range(0, 10):
        print("\nCoffee #{}".format(i + 1))
        UDPClient()
        time.sleep(1)


if __name__ == '__main__':
    main()
