import pytest

from eeprom import cli


@pytest.fixture
def byte():
    return 0xEA


@pytest.fixture
def address():
    return 0x0B07


@pytest.fixture
def invalid_address():
    "INVALID_ADDRESS"


@pytest.fixture
def read_byte_serial_response(byte):
    return f"{byte:02X}\n".encode("utf8")


@pytest.fixture
def read_byte_serial_request(address):
    return f"R{address:04X}\n".encode("utf8")


@pytest.fixture
def read_byte_result(default_programmer, runner, read_byte_serial_response, address):
    default_programmer.arduino.serial_connection.readline.return_value = (
        read_byte_serial_response
    )
    return runner.invoke(cli, f"read-byte {address:04X}")


@pytest.fixture
def invalid_address_result(
    default_programmer, runner, read_byte_serial_response, invalid_address
):
    default_programmer.arduino.serial_connection.readline.return_value = (
        read_byte_serial_response
    )
    return runner.invoke(cli, f"read-byte {invalid_address}")


def test_exit_code(read_byte_result):
    assert read_byte_result.exit_code == 0


def test_output(read_byte_result, read_byte_serial_response, byte):
    assert read_byte_result.output == f"{byte:02X}\n"


def test_invalid_address_error_message(invalid_address_result, invalid_address):
    response = invalid_address_result.output
    assert response == f"{invalid_address} is not a valid address.\n"


def test_invalid_address_error_exit_code(invalid_address_result):
    assert invalid_address_result.exit_code == 1


def test_serial_message_sent(
    default_programmer, read_byte_result, assert_message_sent, read_byte_serial_request
):
    assert_message_sent(default_programmer, read_byte_serial_request)
