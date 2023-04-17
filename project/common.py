
import socket


def send_all(sock: socket.socket, data: bytes) -> None:
    """
    Send all data to the socket.
    """
    sock.sendall(data)


def recv_all(sock: socket.socket) -> bytes:
    """
    Receive all data from the socket.
    """
    data = b""
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    return data
