import socketserver
from typing import Tuple
import time
import math
from project.common import recv_all, send_all
from rich import print


# dictionary of requests
requests = {}
size_counts = {}
times = {}
start = time.time()

blacklist = []

window_size = 2
block_frequency = 0.2


class RequestHandler(socketserver.BaseRequestHandler):
    def log(self, message: str = "") -> None:
        print(f"[{self.client_address[0]}:{self.client_address[1]}] [{self.method} {self.path} {self.version}] {message}")

    def handle(self) -> None:
        self.data = recv_all(self.request)
        self.method, self.path, self.version = parse_request(self.data)
        self.headers = parse_headers(self.data)
        self.payload = parse_payload(self.data)

        self.log(f"Headers: {self.headers}, Payload: {self.payload}")

        # length of headers in bytes for analysis
        headers_length = len(self.headers['user-agent']) + len(
            self.headers['sec-ch-ua']) + len(self.headers['accept'])
        # add request to dictionary
        requests[self.client_address[0] + ":" +
                 str(self.client_address[1])] = headers_length

        # print(math.trunc(time.time() - start) % 3)

        # check blacklist
        if headers_length in blacklist:
            self.request.sendall(form_response(
                self.method, self.path, self.version, True, "Go Away"
            ))
        else:
            # add header lengths to dictionary
            if headers_length in size_counts.keys():
                size_counts[headers_length] = size_counts[headers_length] + 1
                if math.trunc(time.time() - start) % 3 == 0:
                    for c in size_counts.keys():
                        if size_counts[c] > 3:
                            blacklist.append(c)
                    size_counts.clear()
            else:
                # haven't seen before send ok response
                size_counts[headers_length] = 1
                times[headers_length] = time.time()
            self.request.sendall(form_response(
                self.method, self.path, self.version, False, "Hello World"
            ))

            # if size_counts[headers_length] % window_size == 0:
            #     if time.time() - times[headers_length] < block_frequency:
            #         print("blocked")
            #         # block
            #         self.request.sendall(form_response(
            #             self.method, self.path, self.version, True, "Go Away"
            #         ))
            #     else:
            #         print("allowed")
            #         # allow
            #         times[headers_length] = time.time()
            #         self.request.sendall(form_response(
            #             self.method, self.path, self.version, False, "Hello World"
            #         ))
            # else:
            #     self.request.sendall(form_response(
            #         self.method, self.path, self.version, False, "Hello World"
            #     ))
        # if len(requests.keys()) >= 1000:
            # reset and write to file
        # self.request.sendall(form_response(
        #     self.method, self.path, self.version, True, "Hello World"


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
            headers[
                key.decode().lower().strip()
            ] = value.decode().lower().strip()
    return headers


def parse_payload(data: bytes) -> bytes:
    return data.split(b"\r\n\r\n")[-1]


def form_response(method: str, path: str, version: str, blocked: bool, message: str) -> bytes:
    """
    Form a response from the request
    """
    if blocked:
        response = f"{version} 403 Forbidden\r\n"

    else:
        response = f"{version} 200 OK\r\n"

    response += "Content-Type: text/html\r\n"
    response += f"Content-Length: {len(message)}\r\n"
    response += "\r\n"
    response += message

    return response.encode()
