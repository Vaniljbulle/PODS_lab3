import socket
from time import sleep

supplier_server_address = ("192.168.43.244", 4000)
coffee_server_address = ("192.168.43.244", 3000)


def receiveAndSend(s_socket, payload, expected):
    data, address = s_socket.recvfrom(1024)
    if data == expected:
        s_socket.sendto(payload, address)
        return True
    return False


def supplyServer():
    supply_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    supply_socket.bind(supplier_server_address)

    try:
        while True:
            print("\nWaiting for refill request..")
            if receiveAndSend(supply_socket, b"ACCEPTED", b"REFILL"):

                print("Sending refill")
                for i in range(0, 10):
                    print(".", end="", flush=True)
                    sleep(0.5)
                print(" Coffee beans sent!")

                # Send refill
                supply_socket.sendto(b"COFFEE BEANS", coffee_server_address)
                print("Waiting for refill confirmation")
                payload, address = supply_socket.recvfrom(1024)
                if payload == b"REFILLED":
                    print("Refill confirmed")
    except KeyboardInterrupt:
        print("Exiting..")


def main():
    supplyServer()


if __name__ == '__main__':
    main()
