import pytest

from eeprom import cli


@pytest.fixture
def read_serial_requests(binary_file_contents):
    messages = []
    for i in range(0, len(binary_file_contents), 16):
        message = f"T{i:04X}\n"
        messages.append(message.encode("utf8"))
    return messages


@pytest.fixture
def read_serial_responses():
    def _read_serial_responses(data):
        messages = []
        for i in range(0, len(data), 16):
            block = " ".join([f"{byte:02X}" for byte in data[i : i + 16]])
            message = f"{block}\n"
            messages.append(message.encode("utf8"))
        return messages

    return _read_serial_responses


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
def altered_binary_file_contents(binary_file_contents):
    altered_binary_file_contents = list(binary_file_contents)
    altered_binary_file_contents[0x0050] = 0xFF
    return altered_binary_file_contents


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
):
    assert_messages_sent(default_programmer, read_serial_requests)