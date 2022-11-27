import socketserver as SOCKETSERVER
import socket as SOCKET
import threading as THREADING
import coffeemachine as COFFEEMACHINE

coffeeMachine = COFFEEMACHINE.CoffeeMachine()
supplier_server_address = ("192.168.1.167", 4000)


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
        print(f"\nOut of coffee - requesting refill\nCoffee left: {coffeeMachine.inventory()}\nCustomers in queue: {len(coffeeMachine.coffeeQueue)}")

        s_socket.sendto(b"REFILL", supplier_server_address)

        payload = s_socket.recv(1024)
        if payload == b"ACCEPTED":  # Supplier accepted order
            coffeeMachine.supplyRequested = True


def processOrders(order_socket):
    order_socket.settimeout(15)
    while True:
        refillRequest(order_socket)
        order = coffeeMachine.processOrder()
        if order:
            print("\nProcessing order from {}, ".format(order), end="")

            # Request payment from client
            order_socket.sendto(b"PAY", order)
            try:
                payload = order_socket.recv(1024)
                if payload == b"PAYMENT":  # Client sent payment
                    print("Payment received, ".format(order))
                    order_socket.sendto(b"CONFIRMED", order)  # Confirm payment to client
                    coffeeMachine.buy(1)  # Pour coffee
                    coffeeMachine.orderPop()  # Remove order from queue
                    order_socket.sendto(b"SERVED", order)  # Serve coffee
            except SOCKET.timeout:
                # Client didn't pay in time
                print(" Payment unsuccessful - order nullified")
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
    local_ip = SOCKET.gethostbyname(SOCKET.gethostname())
    server_address = (local_ip, 3000)
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
            order_socket = SOCKET.socket(SOCKET.AF_INET, SOCKET.SOCK_DGRAM)
            processOrders(order_socket)

    except KeyboardInterrupt:
        print("Server shutting down")
        order_socket.close()
        server.shutdown()
        server.server_close()


def main():
    UDPServer()


if __name__ == '__main__':
    main()
