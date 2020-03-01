import pytest
from click.testing import CliRunner

from eeprom import __version__, cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def version_result(runner):
    return runner.invoke(cli, "version")


def test_exit_code(version_result):
    assert version_result.exit_code == 0


def test_output(version_result):
    assert version_result.output == f"eeprom version: {__version__}\n"
