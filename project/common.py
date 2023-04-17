import socket


def send_all(sock: socket.socket, data: bytes) -> None:
    """
    Send all data to the socket.
    """
    sock.sendall(data)


def recv_all(sock: socket.socket, buffer_size: int = 2048) -> bytes:
    """
    Receive all data from the socket.
    """
    data = b""
    while True:
        chunk = sock.recv(buffer_size)
        data += chunk
        if len(chunk) < buffer_size:
            break

    return data
