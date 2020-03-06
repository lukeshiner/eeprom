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


@click.command()
def read():
    """Read the contents of the EEPROM and print it a file."""
    programmer = Programmer()
    data = programmer.read()
    click.echo(bytes(data), nl=False)


@click.command()
@click.argument("binary_file", type=click.File("rb"))
def verify(binary_file):
    """
    Verify the contents of the EEPROM match a binary file.

    If the contents match the program will exit with 0.

    Otherwise a list of differences will be printed to STDOUT and the program will
    exit with 1.
    """
    programmer = Programmer()
    expected_data = list(binary_file.read())
    found_data = programmer.read()
    if expected_data != found_data:
        for address, expected in enumerate(expected_data):
            found = found_data[address]
            if found != expected:
                click.echo(f"{address:04X} expected {expected:02X} found {found:02X}")
        exit(1)


@click.command()
@click.argument("binary_file", type=click.File("rb"))
def update(binary_file):
    """
    Update the contents of the EEPROM with the contents of a binary file.

    This will read the EEPROM and overwrite any data that does not match the provided
    file. This is done in blocks of 16 addresses. When the existing contents are similar
    to the contents of the file this is much quicker than write command, however when
    they differ greatly the extra time taken to read the EEPROM should be taken into
    account.
    """
    programmer = Programmer()
    new_data = list(binary_file.read())
    existing_data = programmer.read()
    for address in range(0, len(new_data), 16):
        new_block = new_data[address : address + 16]
        existing_block = existing_data[address : address + 16]
        if new_block != existing_block:
            programmer.write_block(address, new_block)


cli.add_command(version)
cli.add_command(read_byte)
cli.add_command(write_byte)
cli.add_command(write)
cli.add_command(read)
cli.add_command(verify)
cli.add_command(update)
