import pytest

from eeprom.programmer_commands import ProgrammerCommand


def test_base_programmer_command_raises_not_implemented():
    programmer_command = ProgrammerCommand()
    with pytest.raises(NotImplementedError):
        programmer_command.format_arguments(None)
