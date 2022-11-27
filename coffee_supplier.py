import socket
from time import sleep

supplier_server_address = ("192.168.1.167", 4000)
coffee_machine_server_address = ("192.168.1.167", 3000)


def supplyServer():
    supply_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    supply_socket.bind(supplier_server_address)

    while True:
        print("Waiting for refill request..")
        payload, address = supply_socket.recvfrom(1024)
        if payload == b"REFILL":
            supply_socket.sendto(b"ACCEPTED", address)  # Accept order

            print("Sending refill")
            for i in range(0, 10):
                print(".", end="", flush=True)
                sleep(0.5)
            print(" Coffee beans sent!")
            # Send refill
            supply_socket.sendto(b"COFFEE BEANS", coffee_machine_server_address)
            print("Waiting for refill confirmation")
            payload, address = supply_socket.recvfrom(1024)
            if payload == b"REFILLED":
                print("Refill confirmed")


def main():
    supplyServer()


if __name__ == '__main__':
    main()
