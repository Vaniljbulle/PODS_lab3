import socketserver as SOCKETSERVER
import socket as SOCKET
import threading as THREADING

debug = False


class ThreadedUDPRequestHandler(SOCKETSERVER.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address)


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
