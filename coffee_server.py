import socketserver as SOCKETSERVER
import socket as SOCKET
import threading as THREADING
import coffeemachine as COFFEEMACHINE

debug = False
coffeeMachine = COFFEEMACHINE.CoffeeMachine()


class ThreadedUDPRequestHandler(SOCKETSERVER.BaseRequestHandler):
    def handle(self):
        payload = self.request[0].strip()
        socket = self.request[1]

        if payload == b"COFFEE":
            if coffeeMachine.inventory() > (len(coffeeMachine.coffeeQueue)):
                socket.sendto(b"ACCEPTED", self.client_address)
                coffeeMachine.coffeeQueue.append(self.client_address)
            else:
                socket.sendto(b"REJECTED - OUT OF COFFEE", self.client_address)


class ThreadedUDPServer(SOCKETSERVER.ThreadingMixIn, SOCKETSERVER.UDPServer):
    pass


def UDPServer():
    if debug:
        server_address = ("127.0.0.1", 3000)
    else:
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

            # Idle
            while True:
                pass
    except KeyboardInterrupt:
        print("Server shutting down")
        server.shutdown()
        server.server_close()


def main():
    UDPServer()


if __name__ == '__main__':
    main()
