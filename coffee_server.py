import socketserver as SOCKETSERVER
import socket as SOCKET

debug = True


class CoffeeMachine:
    def __init__(self):
        self.coffee = 0
        self.gold = 0

    def __str__(self):
        return "The coffee machine has:\n" \
               "{} coffee\n" \
               "{} gold\n".format(self.coffee, self.gold)

    def fill(self, coffee):
        self.coffee += coffee

    def buy(self, coffee, gold):
        self.coffee -= coffee
        self.gold += gold


class UDPHandler(SOCKETSERVER.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address)


def UDPServer():
    if debug:
        server_address = ("127.0.0.1", 3000)
    else:
        local_ip = SOCKET.gethostbyname(SOCKET.gethostname())
        server_address = (local_ip, 3000)
    server = SOCKETSERVER.UDPServer(server_address, UDPHandler)

    try:
        server.serve_forever()
        print("Server started on {}".format(server_address))
    except KeyboardInterrupt:
        print("Server shutting down")
        server.shutdown()
        server.server_close()


def main():
    UDPServer()


if __name__ == '__main__':
    main()
