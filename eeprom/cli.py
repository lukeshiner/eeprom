"""
The eeprom package.

Tool for reading and writing EEPROMs over USB serial to an arduino based EEPROM programmer.
"""

import click

from .__version__ import __version__
from .programmer import Programmer


@click.group()
def cli():
    """Handle commands."""
    pass


@click.command()
def version():
    """Read a byte from the EEPROM."""
    click.echo(f"eeprom version: {__version__}")


@click.command()
@click.argument("address")
def read_byte(address):
    """Read a byte from the EEPROM."""
    try:
        address = int(address, 16)
    except ValueError:
        click.echo(f"{address} is not a valid address.", err=True)
        exit(1)
    programmer = Programmer()
    byte = programmer.read_byte(address)
    click.echo(f"{byte:02X}")


@click.command()
@click.argument("address")
@click.argument("byte")
def write_byte(address, byte):
    """Read a byte from the EEPROM."""
    try:
        address = int(address, 16)
    except ValueError:
        click.echo(f"{address} is not a valid address.", err=True)
        exit(1)
    try:
        byte = int(byte, 16)
    except ValueError:
        click.echo(f"{byte} is not a valid byte.", err=True)
        exit(1)
    programmer = Programmer()
    byte = programmer.write_byte(address, byte)


cli.add_command(version)
cli.add_command(read_byte)
cli.add_command(write_byte)
