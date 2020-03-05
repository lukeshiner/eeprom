import pytest

from eeprom import cli


@pytest.fixture
def read_byte_result(
    default_programmer, runner,
):
    default_programmer.arduino.serial_connection.readline.return_value = b"EA\n"
    return runner.invoke(cli, "read-byte 0B07")


@pytest.fixture
def invalid_address_result(default_programmer, runner):
    default_programmer.arduino.serial_connection.readline.return_value = b"EA\n"
    return runner.invoke(cli, "read-byte NOTANADDRESS")


def test_exit_code(read_byte_result):
    assert read_byte_result.exit_code == 0


def test_output(read_byte_result):
    assert read_byte_result.output == "00EA\n"


def test_invalid_address_error_message(invalid_address_result):
    assert invalid_address_result.output == "NOTANADDRESS is not a valid address.\n"


def test_invalid_address_error_exit_code(invalid_address_result):
    assert invalid_address_result.exit_code == 1


def test_serial_message_sent(default_programmer, read_byte_result, assert_message_sent):
    assert_message_sent(default_programmer, b"R0B07\n")
