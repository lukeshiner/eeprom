import pytest

from eeprom import cli


@pytest.fixture
def write_byte_result(default_programmer, runner, serial_ack, address, byte):
    default_programmer.arduino.serial_connection.readline.return_value = serial_ack
    return runner.invoke(cli, f"write-byte -a {address:04X} -b {byte:02X}")


@pytest.fixture
def invalid_address_result(
    default_programmer, runner, serial_ack, invalid_address, byte
):
    default_programmer.arduino.serial_connection.readline.return_value = serial_ack
    return runner.invoke(cli, f"write-byte -a {invalid_address} -b {byte:02X}")


@pytest.fixture
def invalid_byte_result(default_programmer, runner, serial_ack, address, invalid_byte):
    default_programmer.arduino.serial_connection.readline.return_value = serial_ack
    return runner.invoke(cli, f"write-byte -a {address} -b {invalid_byte}")


def test_exit_code(write_byte_result):
    assert write_byte_result.exit_code == 0


def test_output(write_byte_result, byte):
    assert write_byte_result.output == ""


def test_invalid_address_error_message(invalid_address_result, invalid_address):
    response = invalid_address_result.output
    assert f"{invalid_address} is not a valid hexidecimal integer." in response


def test_invalid_address_error_exit_code(invalid_address_result):
    assert invalid_address_result.exit_code == 2


def test_invalid_byte_error_message(invalid_byte_result, address, invalid_byte):
    response = invalid_byte_result.output
    assert f"{invalid_byte} is not a valid hexidecimal integer." in response


def test_invalid_byte_error_exit_code(invalid_byte_result):
    assert invalid_byte_result.exit_code == 2


def test_serial_message_sent(
    default_programmer,
    write_byte_result,
    assert_message_sent,
    write_byte_serial_request,
):
    assert_message_sent(default_programmer, write_byte_serial_request)
