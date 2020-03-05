from unittest.mock import Mock, call, patch

import pytest
from click.testing import CliRunner

from eeprom import Programmer


@pytest.fixture
def programmer(mock_serial_connection, mock_time):
    def _programmer(port=None, baud=None, eeprom_type=None, init_delay=None):
        kwargs = {
            "port": port,
            "baud": baud,
            "eeprom_type": eeprom_type,
            "init_delay": init_delay,
        }
        kwargs = {key: value for key, value in kwargs.items() if value is not None}
        return Programmer(**kwargs)

    return _programmer


@pytest.fixture
def default_programmer(programmer):
    return programmer()


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture()
def mock_serial_connection():
    mock_serial_connection = Mock()
    mock_serial = Mock(return_value=mock_serial_connection)
    with patch("eeprom.arduino.serial.Serial", mock_serial):
        yield mock_serial


@pytest.fixture
def mock_time():
    mock_time = Mock()
    with patch("eeprom.arduino.time", mock_time):
        yield mock_time


@pytest.fixture
def serial_ack():
    return b"ACK\n"


@pytest.fixture
def set_serial_response():
    def _set_serial_responses(programmer, response):
        if isinstance(response, list):
            programmer.arduino.serial_connection.readline.side_effect = response
        else:
            programmer.arduino.serial_connection.readline.return_value = response

    return _set_serial_responses


@pytest.fixture
def assert_message_sent():
    def _assert_message_sent(programmer, expected_message):
        programmer.arduino.serial_connection.write.assert_called_once_with(
            expected_message
        )

    return _assert_message_sent


@pytest.fixture
def assert_messages_sent():
    def _assert_messages_sent(programmer, expected_messages):
        calls = [call(message) for message in expected_messages]
        programmer.arduino.serial_connection.write.assert_has_calls(calls)

    return _assert_messages_sent
