import click
from project.commands.start import start
from project.commands.plot import plot


@click.group()
@click.version_option()
def cli() -> None:
    """
    CS 5490 Spring 2023 @ The University of Utah.

    by:

    Gates Lamb <u1033920@utah.edu>

    Sam Smith <u0629883@utah.edu>

    Yifei Sun <u1298569@utah.edu>
    """


cli.add_command(start)
cli.add_command(plot)
