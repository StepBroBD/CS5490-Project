import click
import socket
import socketserver
from project.handler import RequestHandler
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
    print(f"Listening on {host}:{port}...")
    with socketserver.TCPServer((host, port), RequestHandler) as server:
        server.serve_forever()
