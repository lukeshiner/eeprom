import pytest

from eeprom import eeprom_type


@pytest.fixture
def eeprom():
    return eeprom_type.BaseEEPROM()


@pytest.fixture
def at28c25():
    return eeprom_type.AT28C25()


def test_eeprom_name(eeprom):
    assert eeprom.name == ""


def test_eeprom_min_address(eeprom):
    assert eeprom.min_address == 0


def test_eeprom_max_address(eeprom):
    assert eeprom.max_address == 0xFFFF


def test_eeprom_data_bits(eeprom):
    assert eeprom.data_bits == 8


def test_eeprom_max_byte(eeprom):
    assert eeprom.max_byte == 0xFF


def test_eeprom_is_valid_address(eeprom):
    for address in range(0, 0x10000):
        try:
            eeprom.is_valid_address(address)
        except ValueError as exception:
            raise pytest.fail(f"DID RAISE {exception}")
    with pytest.raises(ValueError):
        eeprom.is_valid_address(-1)
    with pytest.raises(ValueError):
        eeprom.is_valid_address(0x10000)


def test_eeprom_is_valid_data(eeprom):
    for address in range(0, 0x100):
        try:
            eeprom.is_valid_data(address)
        except ValueError as exception:
            raise pytest.fail(f"DID RAISE {exception}")
    with pytest.raises(ValueError):
        eeprom.is_valid_data(-1)
    with pytest.raises(ValueError):
        eeprom.is_valid_data(0x100)


def test_AT28C25_name(at28c25):
    assert at28c25.name == "AT28C25"


def test_AT28C25_max_address(at28c25):
    assert at28c25.max_address == 0x7FFF


def test_AT28C25_is_valid_address(at28c25):
    for address in range(0, 0x8000):
        try:
            at28c25.is_valid_address(address)
        except ValueError as exception:
            raise pytest.fail(f"DID RAISE {exception}")
    with pytest.raises(ValueError):
        at28c25.is_valid_address(-1)
    with pytest.raises(ValueError):
        at28c25.is_valid_address(0x8000)


def test_get_EEPROM():
    assert isinstance(eeprom_type.get_EEPROM("AT28C25"), eeprom_type.AT28C25)


def test_get_invalid_EEPROM():
    with pytest.raises(ValueError):
        eeprom_type.get_EEPROM("Test Name")
