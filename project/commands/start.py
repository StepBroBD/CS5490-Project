import click
import socket
import socketserver
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
def client(host: str, port: int) -> None:
    """
    Start the client.
    """
    # test client
    # send a hello world message to the server
    # and close the connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        send_all(s, b"Hello World")
        data = recv_all(s)
        print(f"Received {data} from {host}:{port}")
