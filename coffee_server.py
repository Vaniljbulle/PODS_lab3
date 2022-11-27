import socketserver as SOCKETSERVER
import socket as SOCKET
import threading as THREADING
import coffeemachine as COFFEEMACHINE

coffeeMachine = COFFEEMACHINE.CoffeeMachine()


class ThreadedUDPRequestHandler(SOCKETSERVER.BaseRequestHandler):
    def handle(self):
        payload = self.request[0].strip()
        socket = self.request[1]

        if payload == b"COFFEE":
            if coffeeMachine.inventory() > (len(coffeeMachine.coffeeQueue) - 1):
                socket.sendto(b"ACCEPTED", self.client_address)
                coffeeMachine.coffeeQueue.append(self.client_address)
            else:
                socket.sendto(b"REJECTED - OUT OF COFFEE", self.client_address)
                print(f"\nOut of coffee - {coffeeMachine.inventory()}")


class ThreadedUDPServer(SOCKETSERVER.ThreadingMixIn, SOCKETSERVER.UDPServer):
    pass


def UDPServer():
    local_ip = SOCKET.gethostbyname(SOCKET.gethostname())
    server_address = (local_ip, 3000)

    server = ThreadedUDPServer(server_address, ThreadedUDPRequestHandler)

    try:
        print("Server started on {}".format(server_address))
        with server:
            server_thread = THREADING.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            print("Server loop running in thread: {}".format(server_thread.name))

            # Process coffee orders
            order_socket = SOCKET.socket(SOCKET.AF_INET, SOCKET.SOCK_DGRAM)
            order_socket.settimeout(15)
            while True:
                order = coffeeMachine.processOrder()
                if order:
                    print("\nProcessing order from {}".format(order))

                    # Request payment from client
                    order_socket.sendto(b"PAY", order)
                    try:
                        payload = order_socket.recv(1024)
                        if payload == b"PAYMENT":
                            print("Payment received from {}".format(order))
                            order_socket.sendto(b"CONFIRMED", order)
                            coffeeMachine.buy(1)
                            print("Coffee served to {} - order complete".format(order))
                            order_socket.sendto(b"SERVED", order)
                    except SOCKET.timeout:
                        print("Client did not respond - order nullified")

    except KeyboardInterrupt:
        print("Server shutting down")
        order_socket.close()
        server.shutdown()
        server.server_close()


def main():
    UDPServer()


if __name__ == '__main__':
    main()
