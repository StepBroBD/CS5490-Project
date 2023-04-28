import click
import socket
import socketserver
import random
import json
from project.handler import RequestHandler
from project.common import send_all, recv_all
from rich import print


@click.group()
def start() -> None:
    """
    Start either the server or the client.
    """
    pass


@start.command()
@click.option(
    "--host",
    "-h",
    required=True,
    type=str,
)
@click.option(
    "--port",
    "-p",
    required=True,
    type=int,
)
def server(host: str, port: int) -> None:
    """
    Start the server.
    """
    print(f"[{host}:{port}] Starting server...")
    with socketserver.TCPServer((host, port), RequestHandler) as server:
        server.serve_forever()


@start.command()
@click.option(
    "--host",
    "-h",
    required=True,
    type=str,
)
@click.option(
    "--port",
    "-p",
    required=True,
    type=int,
)
@click.option(
    "--count",
    "-n",
    required=True,
    type=int,
)
def attack(host: str, port: int, count: int) -> None:
    """
    Start the attack.
    """
    http_methods = ["GET", "POST"]  # ["PUT", "DELETE", "PATCH", "HEAD"]
    http_versions = ["HTTP/1.0", "HTTP/1.1", "HTTP/2.0"]
    http_endpoints = ["/", "/search", "/login", "/register"]
    http_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "TE": "trailers",
        "sec-ch-ua": '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
    }

    for i in range(count):
        # randomly select a method, version, and endpoint
        method = random.choice(http_methods)
        version = random.choice(http_versions)
        endpoint = random.choice(http_endpoints)

        # for all headers, randomly select, keep or not, mutate or not
        headers = {}
        for header in http_headers.keys():
            if random.random() > 0.5:
                headers[header] = http_headers[header]
            else:
                headers[header] = "".join(
                    [chr(random.randint(32, 126))
                     for _ in range(random.randint(1, 10))]
                )

        # if the method is POST, add a body, generate a random json payload
        if method == "POST":
            headers["Content-Type"] = "application/json"
            body = json.dumps(
                {
                    "".join(
                        [chr(random.randint(32, 126))
                         for _ in range(random.randint(1, 10))]
                    ): "".join(
                        [chr(random.randint(32, 126))
                         for _ in range(random.randint(1, 10))]
                    )
                    for _ in range(random.randint(1, 10))
                }
            )
            headers["Content-Length"] = len(body)

        # form the request inline
        request = f"{method} {endpoint} {version}\r\n"
        for header in headers.keys():
            request += f"{header}: {headers[header]}\r\n"
        request += "\r\n"
        if method == "POST":
            request += body

        # send the request
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            send_all(sock, request.encode())
            response = recv_all(sock).decode().split("\r\n")
            print(
                f"{sock.getsockname()[0]}:{sock.getsockname()[1]} -> {host}:{port} [{i+1}/{count}] {method} {endpoint} {version} Responded: {response}"
            )
