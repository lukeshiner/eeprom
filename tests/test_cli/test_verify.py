import pytest

from eeprom import cli


@pytest.fixture
def matching_verify_result(
    default_programmer,
    runner,
    read_serial_responses,
    binary_file_path,
    binary_file_contents,
):
    default_programmer.arduino.serial_connection.readline.side_effect = read_serial_responses(
        binary_file_contents
    )
    return runner.invoke(cli, f"verify {binary_file_path}")


@pytest.fixture
def non_matching_verify_result(
    default_programmer,
    runner,
    read_serial_responses,
    binary_file_path,
    binary_file_contents,
    altered_binary_file_contents,
):
    default_programmer.arduino.serial_connection.readline.side_effect = read_serial_responses(
        altered_binary_file_contents
    )
    return runner.invoke(cli, f"verify {binary_file_path}")


def test_matching_exit_code(matching_verify_result):
    assert matching_verify_result.exit_code == 0


def test_matching_output(matching_verify_result, read_serial_responses):
    assert matching_verify_result.output == ""


def test_non_matching_exit_code(non_matching_verify_result):
    assert non_matching_verify_result.exit_code == 1


def test_non_matching_output(non_matching_verify_result, binary_file_contents):
    assert (
        non_matching_verify_result.output
        == f"0050 expected {binary_file_contents[0x50]:02X} found FF\n"
    )


def test_serial_message_sent(
    default_programmer,
    matching_verify_result,
    assert_messages_sent,
    read_serial_requests,
    binary_file_contents,
):
    assert_messages_sent(default_programmer, read_serial_requests(binary_file_contents))
