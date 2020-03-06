import pytest

from eeprom import cli


@pytest.fixture
def read_result(default_programmer, runner, read_serial_responses, valid_eeprom_data):
    default_programmer.arduino.serial_connection.readline.side_effect = read_serial_responses(
        valid_eeprom_data
    )
    return runner.invoke(cli, "read")


def test_exit_code(read_result):
    assert read_result.exit_code == 0


def test_output(read_result, read_serial_responses, valid_eeprom_data):
    assert read_result.stdout_bytes == bytes(valid_eeprom_data)


def test_serial_message_sent(
    default_programmer,
    read_result,
    assert_messages_sent,
    read_serial_requests,
    valid_eeprom_data,
):
    assert_messages_sent(default_programmer, read_serial_requests(valid_eeprom_data))
