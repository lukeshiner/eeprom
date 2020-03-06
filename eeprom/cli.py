"""
The eeprom package.

Tool for reading and writing EEPROMs over USB serial to an arduino based EEPROM programmer.
"""

import click

from .__version__ import __version__
from .programmer import Programmer


class HexInt(click.ParamType):
    """Parameter type for hexadecimail integers."""

    def convert(self, value, param, ctx):
        """Return the input as an integer or fail."""
        try:
            return int(value, 16)
        except ValueError:
            self.fail(f"{value} is not a valid hexidecimal integer.")


@click.group()
def cli():
    """Handle commands."""
    pass


@click.command()
def version():
    """Read a byte from the EEPROM."""
    click.echo(f"eeprom version: {__version__}")


@click.command()
@click.option(
    "--address", "-a", type=HexInt(), help="The address to read in hex. E.g 2F0A"
)
def read_byte(address):
    """Read a byte from the EEPROM."""
    programmer = Programmer()
    byte = programmer.read_byte(address)
    click.echo(f"{byte:02X}")


@click.command()
@click.option(
    "--address", "-a", type=HexInt(), help="The address to write to in hex. E.g 2F0A"
)
@click.option("--byte", "-b", type=HexInt(), help="The byte to write in hex. E.g E2")
def write_byte(address, byte):
    """Write a byte to the EEPROM."""
    programmer = Programmer()
    byte = programmer.write_byte(address, byte)


@click.command()
@click.argument("binary_file", type=click.File("rb"))
def write(binary_file):
    """Write a binary file to the EEPROM."""
    programmer = Programmer()
    programmer.write(binary_file.read())


cli.add_command(version)
cli.add_command(read_byte)
cli.add_command(write_byte)
cli.add_command(write)
