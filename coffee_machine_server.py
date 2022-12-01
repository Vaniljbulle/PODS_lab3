import socketserver
import threading

import coffeemachine

supplier_server_address = ("192.168.1.167", 4000)
coffee_server_address = ("192.168.1.167", 3000)
coffeeMachine = coffeemachine.CoffeeMachine(supplier_server_address, coffee_server_address)


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        payload = self.request[0].strip()
        socket = self.request[1]

        if payload == b"COFFEE":  # Coffee request
            if coffeeMachine.put_in_order(self.client_address):  # Put in order
                socket.sendto(b"ACCEPTED", self.client_address)  # Order accepted
            else:
                socket.sendto(b"REJECTED", self.client_address)  # Order rejected
        elif payload == b"COFFEE BEANS":  # Refill request
            coffeeMachine.supply_queue.put(self.client_address)  # Add supplier to queue


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


def UDPServer():
    server = ThreadedUDPServer(coffee_server_address, ThreadedUDPRequestHandler)

    try:
        print("Server started on {}".format(coffee_server_address))
        with server:
            # Threaded UDP Server to accept orders
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            # server_thread.join()
            print("Server loop running in thread: {}".format(server_thread.name))

            # Coffee machine go brrrr
            while True:
                coffeeMachine.process_supply()
                coffeeMachine.process_order()

    except KeyboardInterrupt:
        print("Server shutting down")
        #server_thread.join()
        server.shutdown()
        server.server_close()


def main():
    UDPServer()


if __name__ == '__main__':
    main()
