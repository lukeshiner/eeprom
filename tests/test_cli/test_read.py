import pytest

from eeprom import cli


@pytest.fixture
def read_serial_requests(valid_eeprom_data):
    messages = []
    for i in range(0, len(valid_eeprom_data), 16):
        message = f"T{i:04X}\n"
        messages.append(message.encode("utf8"))
    return messages


@pytest.fixture
def read_serial_responses(valid_eeprom_data):
    messages = []
    for i in range(0, len(valid_eeprom_data), 16):
        block = " ".join([f"{byte:02X}" for byte in valid_eeprom_data[i : i + 16]])
        message = f"{block}\n"
        messages.append(message.encode("utf8"))
    return messages


@pytest.fixture
def read_result(default_programmer, runner, read_serial_responses):
    default_programmer.arduino.serial_connection.readline.side_effect = (
        read_serial_responses
    )
    return runner.invoke(cli, "read")


def test_exit_code(read_result):
    assert read_result.exit_code == 0


def test_output(read_result, read_serial_responses, valid_eeprom_data):
    assert read_result.stdout_bytes == bytes(valid_eeprom_data)


def test_serial_message_sent(
    default_programmer, read_result, assert_messages_sent, read_serial_requests,
):
    assert_messages_sent(default_programmer, read_serial_requests)
