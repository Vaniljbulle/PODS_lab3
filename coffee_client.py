import socket


def UDPClient():
    coffee_machine_server_address = ("192.168.1.167", 3000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    order = b"COFFEE"
    payment = b"PAYMENT"

    # Order coffee
    sock.sendto(order, coffee_machine_server_address)

    payload, address = sock.recvfrom(1024)
    if payload == b"ACCEPTED":
        print("Coffee machine accepted order - waiting for payment request")

        # Wait for payment request
        payload, address = sock.recvfrom(1024)
        if payload == b"PAY":  # Coffee machine requested payment
            print("Coffee machine requested payment - sending payment")
            # Send payment
            sock.sendto(payment, address)

        # Wait for payment confirmation
        payload, address = sock.recvfrom(1024)
        if payload == b"CONFIRMED":
            print("Coffee machine confirmed payment - waiting for coffee")

        # Wait for coffee
        payload, address = sock.recvfrom(1024)
        if payload == b"SERVED":
            print("Coffee machine served coffee - order finished")
        else:
            print("Coffee machine did not serve coffee - order failed")
    else:
        print("Coffee machine rejected order - OUT OF COFFEE")


def main():
    UDPClient()


if __name__ == '__main__':
    main()
