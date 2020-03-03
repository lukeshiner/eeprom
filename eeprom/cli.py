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
def read_byte():
    """Read a byte from the EEPROM."""
    programmer = Programmer()
    byte = programmer.read_byte(0)
    click.echo(f"{byte:04X}")


cli.add_command(version)
cli.add_command(read_byte)
