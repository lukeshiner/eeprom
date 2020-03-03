"""
The eeprom package.

Read and write EEPROMs through serial.
"""
from .__version__ import __version__
from .cli import cli
from .programmer import Programmer

__all__ = ["__version__", "cli", "Programmer"]
