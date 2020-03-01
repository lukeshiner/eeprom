from unittest.mock import Mock, patch

import pytest

from eeprom.arduino import Arduino


@pytest.fixture
def arduino():
    return Arduino()


@patch("eeprom.arduino.serial")
@patch("eeprom.arduino.time")
def open_arduino(mock_time, mock_serial):
    arduino = Arduino()
    mock_serial_connection = Mock()
    mock_serial.Serial.return_value = mock_serial_connection
    arduino.open()
    return arduino, mock_time, mock_serial, mock_serial_connection


def test_arduino_port(arduino):
    assert arduino.port == "/dev/ttyUSB0"


def test_arduino_baud(arduino):
    assert arduino.baud == 115200


def test_arduino_serial_connection(arduino):
    assert arduino.serial_connection is None


def test_arduino_open_delays():
    arduino, mock_time, mock_serial, mock_serial_connection = open_arduino()
    mock_time.sleep.assert_called_once_with(2)


def test_arduino_open_creates_connection():
    arduino, mock_time, mock_serial, mock_serial_connection = open_arduino()
    mock_serial.Serial.assert_called_with(arduino.port, arduino.baud)


def test_arduino_open_flushes():
    arduino, mock_time, mock_serial, mock_serial_connection = open_arduino()
    mock_serial_connection.flush.assert_called_once()


def test_arduino_open_resets_input():
    arduino, mock_time, mock_serial, mock_serial_connection = open_arduino()
    mock_serial_connection.reset_input_buffer.assert_called_once()


def test_arduino_open_resets_output():
    arduino, mock_time, mock_serial, mock_serial_connection = open_arduino()
    mock_serial_connection.reset_output_buffer.assert_called_once()


def test_arduino_close():
    arduino, mock_time, mock_serial, mock_serial_connection = open_arduino()
    arduino.close()
    mock_serial_connection.close.assert_called_once()


def test_serial_recieve():
    arduino, mock_time, mock_serial, mock_serial_connection = open_arduino()
    mock_serial_connection.readline.return_value = b"Hello, World\n"
    response = arduino.serial_recieve()
    mock_serial_connection.readline.assert_called_once()
    assert response == "Hello, World"


def test_serial_send():
    arduino, mock_time, mock_serial, mock_serial_connection = open_arduino()
    arduino.serial_send("Hello, World")
    mock_serial_connection.write.assert_called_once_with(b"Hello, World\n")
