"""EEPROM types."""


class BaseEEPROM:
    """Base class for EEPROMs."""

    name = ""
    min_address = 0x0000
    max_address = 0xFFFF
    data_bits = 8
    max_byte = 0xFF

    @classmethod
    def is_valid_address(cls, address):
        """Raise ValueError if address is not valid for this EEPROM."""
        if address < cls.min_address or address > cls.max_address:
            raise ValueError(
                (
                    f"Address {address:04X} out of range {cls.min_address:04X} - "
                    f"{cls.max_address:04X}"
                )
            )

    @classmethod
    def is_valid_data(cls, data):
        """Raise ValueError if data is not a valid byte."""
        if data < 0 or data > cls.max_byte:
            raise ValueError(f"Data {data:02X} out of range 0x00 - {cls.max_byte:02X}")


class AT28C25(BaseEEPROM):
    """EEPROM type for the Atmel AT28C25."""

    name = "AT28C25"
    max_address = 0x7FFF


def get_EEPROM(name):
    """Return the EEPROM type matching name or raise ValueError."""
    for eeprom in BaseEEPROM.__subclasses__():
        if eeprom.name == name:
            return eeprom()
    raise ValueError(f"No known EEPROM named {name}.")
