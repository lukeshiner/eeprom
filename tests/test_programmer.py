import json
from pathlib import Path
from unittest.mock import call

import pytest

from eeprom.arduino import Arduino
from eeprom.eeprom_type import AT28C25


@pytest.fixture
def read_byte_valid_response():
    return 0xEA


@pytest.fixture
def set_serial_response():
    def _set_serial_responses(programmer, response):
        if isinstance(response, list):
            programmer.arduino.serial_connection.readline.side_effect = response
        else:
            programmer.arduino.serial_connection.readline.return_value = response

    return _set_serial_responses


@pytest.fixture
def programmer_with_valid_read_byte_response(default_programmer, set_serial_response):
    programmer = default_programmer
    set_serial_response(programmer, b"EA\n")
    return programmer


@pytest.fixture
def programmer_with_valid_read_block_response(default_programmer, set_serial_response):
    programmer = default_programmer
    set_serial_response(programmer, b"EA 2F A2 95 B3 55 6B 2A\n")
    return programmer


@pytest.fixture
def valid_eeprom_data():
    with open(Path(__file__).parent / "AT28C25_data.json", "r") as f:
        data = json.load(f)
    return data


@pytest.fixture
def programmer_with_valid_read_response(
    default_programmer, set_serial_response, valid_eeprom_data
):
    programmer = default_programmer
    data = []
    for i in range(0, len(valid_eeprom_data), 16):
        block = [f"{_:02X}" for _ in valid_eeprom_data[i : i + 16]]
        data.append(bytes(" ".join(block), "utf8") + b"\n")
    set_serial_response(programmer, data)
    return programmer


@pytest.fixture
def programmer_with_invalid_response(default_programmer, set_serial_response):
    programmer = default_programmer
    set_serial_response(programmer, b"ERROR\n")
    return programmer


@pytest.fixture
def programmer_with_serial_ack_response(
    default_programmer, set_serial_response, serial_ack
):
    programmer = default_programmer
    set_serial_response(programmer, serial_ack)
    return programmer


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


def test_default_arduino(default_programmer):
    assert isinstance(default_programmer.arduino, Arduino)


def test_default_port(default_programmer):
    assert default_programmer.arduino.port == "/dev/ttyUSB0"


def test_default_baud(default_programmer):
    assert default_programmer.arduino.baud == 115200


def test_default_eeprom_type(default_programmer):
    assert default_programmer.eeprom_type == "AT28C25"


def test_default_eeprom(default_programmer):
    assert isinstance(default_programmer.eeprom, AT28C25)


def test_disconnect(default_programmer):
    default_programmer.disconnect()
    default_programmer.arduino.serial_connection.close.assert_called_once()


def test_read_byte_sends_command(
    programmer_with_valid_read_byte_response, assert_message_sent
):
    programmer_with_valid_read_byte_response.read_byte(0x2A55)
    assert_message_sent(programmer_with_valid_read_byte_response, b"R2A55\n")


def test_read_byte_return_value(programmer_with_valid_read_byte_response):
    assert programmer_with_valid_read_byte_response.read_byte(0x00) == 0xEA


def test_read_byte_rejects_negative_address(programmer_with_valid_read_byte_response):
    with pytest.raises(ValueError):
        programmer_with_valid_read_byte_response.read_byte(-1)


def test_read_byte_rejects_address_beyond_eeprom_range(
    programmer_with_valid_read_byte_response,
):
    with pytest.raises(ValueError):
        programmer_with_valid_read_byte_response.read_byte(AT28C25.max_address + 1)


def test_read_byte_raises_for_invalid_response(programmer_with_invalid_response):
    with pytest.raises(ValueError):
        programmer_with_invalid_response.read_byte(0x2FAE)


def test_write_byte_sends_command(
    programmer_with_serial_ack_response, assert_message_sent
):
    programmer_with_serial_ack_response.write_byte(0x55EA, 0xEA)
    assert_message_sent(programmer_with_serial_ack_response, b"W55EAEA\n")


def test_write_byte_return_value(programmer_with_serial_ack_response):
    assert programmer_with_serial_ack_response.write_byte(0x55EA, 0xEA) is None


def test_write_byte_rejects_negative_address(default_programmer):
    with pytest.raises(ValueError):
        default_programmer.write_byte(-1, 0x56)


def test_write_byte_rejects_address_beyond_eeprom_range(
    programmer_with_serial_ack_response,
):
    with pytest.raises(ValueError):
        programmer_with_serial_ack_response.write_byte(AT28C25.max_address + 1, 0x56)


def test_write_byte_raises_for_data_below_zero(programmer_with_serial_ack_response):
    with pytest.raises(ValueError):
        programmer_with_serial_ack_response.write_byte(0x55EA, -1)


def test_write_byte_raises_for_data_over_one_byte(programmer_with_serial_ack_response):
    with pytest.raises(ValueError):
        programmer_with_serial_ack_response.write_byte(0x55EA, 0x100)


def test_write_byte_raises_for_invalid_response(programmer_with_invalid_response):
    with pytest.raises(ValueError):
        programmer_with_invalid_response.write_byte(0x2FAE, 0x56)


def test_read_block_sends_command(
    programmer_with_valid_read_block_response, assert_message_sent
):
    programmer_with_valid_read_block_response.read_block(0x2A55)
    assert_message_sent(programmer_with_valid_read_block_response, b"T2A55\n")


def test_read_block_return_value(programmer_with_valid_read_block_response):
    assert programmer_with_valid_read_block_response.read_block(0x00) == [
        0xEA,
        0x2F,
        0xA2,
        0x95,
        0xB3,
        0x55,
        0x6B,
        0x2A,
    ]


def test_read_block_rejects_negative_address(default_programmer):
    with pytest.raises(ValueError):
        default_programmer.read_block(-1)


def test_read_block_rejects_address_beyond_eeprom_range(default_programmer):
    with pytest.raises(ValueError):
        default_programmer.read_block(AT28C25.max_address + 1)


def test_read_block_raises_for_invalid_response(programmer_with_invalid_response):
    with pytest.raises(ValueError):
        programmer_with_invalid_response.read_block(0x2FAE)


def test_write_block_sends_command(
    programmer_with_serial_ack_response, assert_message_sent
):
    programmer_with_serial_ack_response.write_block(
        0x55EA, [0xEA, 0x2F, 0xA2, 0x95, 0xB3, 0x55, 0x6B, 0x2A]
    )
    assert_message_sent(programmer_with_serial_ack_response, b"S55EAEA2FA295B3556B2A\n")


def test_write_block_return_value(programmer_with_serial_ack_response):
    assert (
        programmer_with_serial_ack_response.write_block(
            0x55EA, [0xEA, 0x2F, 0xA2, 0x95, 0xB3, 0x55, 0x6B, 0x2A]
        )
        is None
    )


def test_write_block_rejects_negative_address(default_programmer):
    with pytest.raises(ValueError):
        default_programmer.write_block(-1, 0x56)


def test_write_block_rejects_address_beyond_eeprom_range(
    programmer_with_serial_ack_response,
):
    with pytest.raises(ValueError):
        programmer_with_serial_ack_response.write_block(
            AT28C25.max_address + 1, [0xEA, 0x2F, 0xA2, 0x95, 0xB3, 0x55, 0x6B, 0x2A]
        )


def test_write_block_raises_for_data_below_zero(programmer_with_serial_ack_response):
    with pytest.raises(ValueError):
        programmer_with_serial_ack_response.write_block(
            0x55EA, [0xEA, 0x2F, 0xA2, 0x95, 0xB3, -1, 0x6B, 0x2A]
        )


def test_write_block_raises_for_data_over_one_byte(programmer_with_serial_ack_response):
    with pytest.raises(ValueError):
        programmer_with_serial_ack_response.write_block(
            0x55EA, [0xEA, 0x2F, 0xA2, 0x95, 0xB3, 0x55, 0x100, 0x2A]
        )


def test_write_block_raises_for_invalid_response(programmer_with_invalid_response):
    with pytest.raises(ValueError):
        programmer_with_invalid_response.write_block(
            0x2FAE, [0xEA, 0x2F, 0xA2, 0x95, 0xB3, 0x55, 0x6B, 0x2A]
        )


def test_read_sends_commands(
    programmer_with_valid_read_block_response, assert_messages_sent
):
    programmer_with_valid_read_block_response.read()
    assert_messages_sent(
        programmer_with_valid_read_block_response,
        [
            bytes(f"T{i:04X}\n", "utf8")
            for i in range(
                0, programmer_with_valid_read_block_response.eeprom.max_address, 16
            )
        ],
    )


def test_read_return_value(programmer_with_valid_read_response, valid_eeprom_data):
    assert programmer_with_valid_read_response.read() == valid_eeprom_data


def test_read_raises_for_invalid_response(programmer_with_invalid_response):
    with pytest.raises(ValueError):
        programmer_with_invalid_response.read()


def test_write_sends_command(
    programmer_with_serial_ack_response, valid_eeprom_data, assert_messages_sent
):
    programmer_with_serial_ack_response.write(valid_eeprom_data)
    messages = []
    for i in range(0, len(valid_eeprom_data), 16):
        block = f"{i:04X}" + "".join(
            [f"{_:02X}" for _ in valid_eeprom_data[i : i + 16]]
        )
        messages.append(bytes(f"S{block}\n", "utf8"))
    assert_messages_sent(programmer_with_serial_ack_response, messages)


def test_write_return_value(programmer_with_serial_ack_response, valid_eeprom_data):
    return_value = programmer_with_serial_ack_response.write(valid_eeprom_data)
    assert return_value is None


def test_write_raises_for_data_below_zero(
    programmer_with_serial_ack_response, valid_eeprom_data
):
    valid_eeprom_data[65] = -1
    with pytest.raises(ValueError):
        programmer_with_serial_ack_response.write(valid_eeprom_data)


def test_write_raises_for_data_over_one_byte(
    programmer_with_serial_ack_response, valid_eeprom_data
):
    valid_eeprom_data[65] = 257
    with pytest.raises(ValueError):
        programmer_with_serial_ack_response.write(valid_eeprom_data)


def test_write_raises_for_invalid_response(
    programmer_with_invalid_response, valid_eeprom_data
):
    with pytest.raises(ValueError):
        programmer_with_invalid_response.write(valid_eeprom_data)
