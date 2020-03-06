import pytest

from eeprom import cli


@pytest.fixture
def write_serial_requests(binary_file_contents):
    messages = []
    for i in range(0, len(binary_file_contents), 16):
        block = "".join([f"{byte:02X}" for byte in binary_file_contents[i : i + 16]])
        message = f"S{i:04X}{block}\n"
        messages.append(message.encode("utf8"))
    return messages


@pytest.fixture
def write_result(default_programmer, runner, serial_ack, binary_file_path):
    default_programmer.arduino.serial_connection.readline.return_value = serial_ack
    return runner.invoke(cli, f"write {binary_file_path}")


@pytest.fixture
def invalid_file_path():
    return "non_existant_file"


@pytest.fixture
def invalid_file_result(default_programmer, runner, serial_ack, invalid_file_path):
    default_programmer.arduino.serial_connection.readline.return_value = serial_ack
    return runner.invoke(cli, f"write {invalid_file_path}")


def test_exit_code(write_result):
    assert write_result.exit_code == 0


def test_output(write_result):
    assert write_result.output == ""


def test_invalid_file_error_message(invalid_file_result, invalid_file_path):
    response = invalid_file_result.output
    assert 'Invalid value for "BINARY_FILE"' in response


def test_invalid_address_error_exit_code(invalid_file_result):
    assert invalid_file_result.exit_code == 2


def test_serial_message_sent(
    default_programmer, write_result, assert_messages_sent, write_serial_requests,
):
    assert_messages_sent(default_programmer, write_serial_requests)
