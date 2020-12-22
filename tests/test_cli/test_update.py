import pytest

from eeprom import cli


@pytest.fixture
def altered_binary_file_contents(binary_file_contents):
    altered_binary_file_contents = list(binary_file_contents)
    altered_binary_file_contents[0x0050] = 0xFF
    return altered_binary_file_contents


@pytest.fixture
def matching_update_result(
    default_programmer,
    runner,
    read_serial_responses,
    binary_file_path,
    binary_file_contents,
):
    default_programmer.arduino.serial_connection.readline.side_effect = (
        read_serial_responses(binary_file_contents)
    )
    return runner.invoke(cli, f"update {binary_file_path}")


@pytest.fixture
def non_matching_update_result(
    default_programmer,
    runner,
    read_serial_responses,
    binary_file_path,
    altered_binary_file_contents,
    serial_ack,
):
    default_programmer.arduino.serial_connection.readline.side_effect = (
        read_serial_responses(altered_binary_file_contents) + [serial_ack]
    )
    return runner.invoke(cli, f"update {binary_file_path}")


def test_matching_exit_code(matching_update_result):
    assert matching_update_result.exit_code == 0


def test_non_matching_exit_code(non_matching_update_result):
    assert non_matching_update_result.exit_code == 0


def test_matching_serial_message_sent(
    default_programmer,
    matching_update_result,
    assert_messages_sent,
    read_serial_requests,
    binary_file_contents,
):
    assert_messages_sent(default_programmer, read_serial_requests(binary_file_contents))


def test_non_matching_serial_message_sent(
    default_programmer,
    non_matching_update_result,
    assert_messages_sent,
    read_serial_requests,
    binary_file_contents,
):
    block = "".join([f"{_:02X}" for _ in binary_file_contents[0x50 : 0x50 + 16]])
    write_messages = [f"S0050{block}\n".encode()]
    assert_messages_sent(
        default_programmer, read_serial_requests(binary_file_contents) + write_messages
    )
