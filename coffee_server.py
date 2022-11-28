import socketserver as SOCKETSERVER
import socket as SOCKET
import threading as THREADING
import time

import coffeemachine as COFFEEMACHINE

coffeeMachine = COFFEEMACHINE.CoffeeMachine()
supplier_server_address = ("192.168.43.244", 4000)


class ThreadedUDPRequestHandler(SOCKETSERVER.BaseRequestHandler):
    def handle(self):
        payload = self.request[0].strip()
        socket = self.request[1]

        if payload == b"COFFEE":  # Coffee request
            if coffeeMachine.inventory() > len(coffeeMachine.coffeeQueue):  # Check if there is enough coffee
                socket.sendto(b"ACCEPTED", self.client_address)  # Accept order
                coffeeMachine.coffeeQueue.append(self.client_address)  # Add client to queue
            else:
                socket.sendto(b"REJECTED - OUT OF COFFEE", self.client_address)  # Reject order
        elif payload == b"COFFEE BEANS":  # Refill request
            coffeeMachine.supplyQueue.append(self.client_address)  # Add supplier to queue
            coffeeMachine.pause()  # Pause coffee machine


class ThreadedUDPServer(SOCKETSERVER.ThreadingMixIn, SOCKETSERVER.UDPServer):
    pass


def refillRequest(s_socket):
    if (coffeeMachine.inventory() == 0) and (coffeeMachine.supplyRequested is False):
        print(
            f"\nOut of coffee - requesting refill\nCoffee left: {coffeeMachine.inventory()}\nCustomers in queue: {len(coffeeMachine.coffeeQueue)}")

        s_socket.sendto(b"REFILL", supplier_server_address)

        payload = s_socket.recv(1024)
        if payload == b"ACCEPTED":  # Supplier accepted order
            coffeeMachine.supplyRequested = True


def sendAndReceive(s_socket, payload, address, asks, timeout, expected):
    s_socket.settimeout(timeout)
    for i in range(0, asks):
        try:
            s_socket.sendto(payload, address)
            payload = s_socket.recv(1024)
            if payload == expected:
                return True
        except SOCKET.timeout:
            print("Timeout - retrying")
            pass
    return False


def processOrders():
    while True:
        order_socket = SOCKET.socket(SOCKET.AF_INET, SOCKET.SOCK_DGRAM)
        order_socket.settimeout(15)

        refillRequest(order_socket)

        order = coffeeMachine.processOrder()
        if order:
            print("\nProcessing order from {}, ".format(order), end="")
            # Establish connection with client
            if sendAndReceive(order_socket, b"CONNECT", order, 5, 3, b"CONNECTED"):
                # Ask for payment once connected
                if sendAndReceive(order_socket, b"PAY", order, 5, 3, b"PAYMENT"):
                    # Confirm payment arrived, give receipt
                    if sendAndReceive(order_socket, b"RECEIPT", order, 5, 3, b"ARRIVED"):
                        # Confirm receipt arrived, give coffee
                        coffeeMachine.buy(1)
                        if sendAndReceive(order_socket, b"COFFEE", order, 5, 3, b"THANKS"):
                            print("Coffee delivered")
                    else:
                        print("Customer left without coffee")
                else:
                    print("Payment rejected")
            else:
                print("Connection rejected - order removed")
            coffeeMachine.coffeeQueue.pop(0)  # Remove client from queue
        elif len(coffeeMachine.supplyQueue) > 0:
            print("\nRefill order in process..")
            supplier = coffeeMachine.processSupply()
            coffeeMachine.fill()
            print("Coffee machine refilled - resuming")
            order_socket.sendto(b"REFILLED", supplier)
            coffeeMachine.supplyRequested = False
            coffeeMachine.resume()


def UDPServer():
    # Setup server
    # local_ip = SOCKET.gethostbyname(SOCKET.gethostname())
    server_address = ("192.168.43.244", 3000)
    server = ThreadedUDPServer(server_address, ThreadedUDPRequestHandler)

    try:
        print("Server started on {}".format(server_address))
        with server:
            # Threaded UDP Server to accept orders
            server_thread = THREADING.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            print("Server loop running in thread: {}".format(server_thread.name))

            # Process coffee orders
            processOrders()

    except KeyboardInterrupt:
        print("Server shutting down")
        # order_socket.close()
        server.shutdown()
        server.server_close()


def main():
    UDPServer()


if __name__ == '__main__':
    main()
