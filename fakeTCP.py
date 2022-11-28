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
        data = s_socket.recv(1024)
        if data[0] == expected:
            s_socket.sendto(payload, data[1])
            return True
    except socket.timeout:
        print("Timeout - retrying")
        pass
    return False
