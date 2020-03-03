import pytest

from eeprom import cli


@pytest.fixture
def read_byte_result(default_programmer, runner):
    default_programmer.arduino.serial_connection.readline.return_value = b"EA\n"
    return runner.invoke(cli, "read-byte")


def test_exit_code(read_byte_result):
    assert read_byte_result.exit_code == 0


def test_output(read_byte_result):
    assert read_byte_result.output == "00EA\n"
