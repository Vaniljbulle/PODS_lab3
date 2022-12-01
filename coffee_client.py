import socket
import threading
import time

import fakeTCP

coffee_machine_server_address = ("192.168.1.167", 3000)


def UDPClient():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Order coffee
    print("Ordering coffee.. ", end="", flush=True)
    if fakeTCP.sendAndReceive(sock, b"COFFEE", coffee_machine_server_address, 1, 2, b"ACCEPTED"):
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
        print(" Rejected - Out of coffee, supplier on the way!")


def order():
    for i in range(0, 13):
        print("\nCoffee #{}".format(i + 1))
        UDPClient()
        time.sleep(1)


def main():
    # Start multiple orders
    for i in range(0, 1):
        threading.Thread(target=order).start()


if __name__ == '__main__':
    main()
