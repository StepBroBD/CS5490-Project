import socketserver
from typing import Self, Tuple
from project.common import recv_all, send_all
from rich import print


class RequestHandler(socketserver.BaseRequestHandler):
    def log(self: Self, message: str = "") -> None:
        print(f"[{self.client_address[0]}:{self.client_address[1]}] [{self.method} {self.path} {self.version}] {message}")

    def handle(self: Self) -> None:
        self.data = recv_all(self.request)
        self.method, self.path, self.version = parse_request(self.data)
        self.headers = parse_headers(self.data)

        self.log()
        self.request.sendall(form_response(
            self.method, self.path, self.version, False, "Hello World"
        ))


def parse_request(data: bytes) -> Tuple[str, str, str]:
    """
    Parse the request and return the method, path and version
    """
    lines = data.split(b"\r\n")
    method, path, version = lines[0].split(b" ")
    return method.decode(), path.decode(), version.decode()


def parse_headers(data: bytes) -> dict:
    headers = {}
    lines = data.split(b"\r\n")
    for line in lines[1:]:
        if line and b":" in line:
            key, value = line.split(b":", 1)
            headers[key.decode()] = value.decode()
    return headers


def form_response(method: str, path: str, version: str, blocked: bool, message: str) -> bytes:
    """
    Form a response from the request
    """
    if blocked:
        response = f"{version} 403 Forbidden\r\n"
        response += "Content-Type: text/html\r\n"
        response += "Content-Length: 0\r\n"
        response += "\r\n"
    else:
        response = f"{version} 200 OK\r\n"
        response += "Content-Type: text/html\r\n"
        response += f"Content-Length: {len(message)}\r\n"
        response += "\r\n"
        response += message
    return response.encode()
