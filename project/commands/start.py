import click
import socketserver
from project.handler import RequestHandler
from project.common import send_all, recv_all
from project.attack import Attack
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
@click.option(
    "--save",
    "-s",
    required=False,
    type=bool,
    is_flag=True,
    default=False,
)
def attack(host: str, port: int, count: int, save: bool) -> None:
    """
    Start the attack (minimal 1000 requests, if count is less than 1000, set to 1000).

    Blocking strategy:
    1. Check user-agent, sec-ch-ua, and accept headers (these three headers are required to be considered as a valid request)
    2. Check the sum of sizes above three headers, save the size as headers to dictionary and the value is the number of times the size appears
    3. 
    """
    if count < 1000:
        count = 1000

    attack = Attack(host, port, count)
    attack.run()

    if save:
        attack.save_results()
