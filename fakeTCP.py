import socket


def sendAndReceive(s_socket, payload, address, asks, timeout, expected):
    s_socket.settimeout(timeout)
    for i in range(0, asks):
        try:
            s_socket.sendto(payload, address)
            payload = s_socket.recv(1024)
            if payload == expected:
                return True
        except socket.timeout:
            print("Timeout - retrying")
            pass
    return False


def receiveAndSend(s_socket, payload, timeout, expected):
    s_socket.settimeout(timeout)
    try:
        data, address = s_socket.recvfrom(1024)

        if data == expected:
            s_socket.sendto(payload, address)
            return True
    except socket.timeout:
        print("Timeout - retrying")
        pass
    return False
