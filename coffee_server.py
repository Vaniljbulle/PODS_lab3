import socketserver as SOCKETSERVER
import socket as SOCKET
import threading as THREADING
import time

import coffeemachine as COFFEEMACHINE
import fakeTCP

supplier_server_address = ("192.168.1.167", 4000)
coffee_server_address = ("192.168.1.167", 3000)
coffeeMachine = COFFEEMACHINE.CoffeeMachine(supplier_server_address, coffee_server_address)


class ThreadedUDPRequestHandler(SOCKETSERVER.BaseRequestHandler):
    def handle(self):
        payload = self.request[0].strip()
        socket = self.request[1]

        if payload == b"COFFEE":  # Coffee request
            if coffeeMachine.inventory() > len(coffeeMachine.coffee_queue):  # Check if there is enough coffee
                socket.sendto(b"ACCEPTED", self.client_address)  # Accept order
                coffeeMachine.coffee_queue.append(self.client_address)  # Add client to queue
            else:
                # socket.sendto(b"REJECTED - OUT OF COFFEE", self.client_address)  # Reject
                pass
        elif payload == b"COFFEE BEANS":  # Refill request
            coffeeMachine.supply_queue.append(self.client_address)  # Add supplier to queue
            coffeeMachine.pause()  # Pause coffee machine


class ThreadedUDPServer(SOCKETSERVER.ThreadingMixIn, SOCKETSERVER.UDPServer):
    pass


def startCoffeeMachine():
    while True:
        coffeeMachine.processSupply()

        coffeeMachine.processOrder()


def UDPServer():
    # Setup server
    # local_ip = SOCKET.gethostbyname(SOCKET.gethostname())
    server = ThreadedUDPServer(coffee_server_address, ThreadedUDPRequestHandler)

    try:
        print("Server started on {}".format(coffee_server_address))
        with server:
            # Threaded UDP Server to accept orders
            server_thread = THREADING.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            # server_thread.join()
            print("Server loop running in thread: {}".format(server_thread.name))

            # Coffee machine go brrrr
            startCoffeeMachine()

    except KeyboardInterrupt:
        print("Server shutting down")
        server_thread.join()
        server.shutdown()
        server.server_close()


def main():
    UDPServer()


if __name__ == '__main__':
    main()
