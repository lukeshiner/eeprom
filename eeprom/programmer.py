"""The Programmer class manages communication with the EEPROM programmer."""

from . import programmer_commands as commands
from .arduino import Arduino
from .eeprom_type import get_EEPROM


class Programmer:
    """Manages communication with the EEPROM programmer."""

    def __init__(
        self, port="/dev/ttyUSB0", baud=115200, eeprom_type="AT28C25", init_delay=2
    ):
        """
        Create a connection to the EEPROM programer.

        Kwargs:
            port (str): The serial port on which the arduino is located.
                Default: "/dev/ttyUSB0"
            baud (int): The baud rate of the serial connection. Default: 115200.
            eeprom_type (str): The name of the type of EEPROM in use. Default: "AT28C25".
            init_delay (int): The time in seconds to wait for the Arduino to initialise.

        """
        self.eeprom_type = eeprom_type
        self.eeprom = get_EEPROM(self.eeprom_type)
        self.arduino = Arduino(port=port, baud=baud)
        self.arduino.open(init_delay=init_delay)

    def disconnect(self):
        """Close the connection to the arduino."""
        self.arduino.close()

    def read_byte(self, address):
        """
        Return the byte stored in a particular address of the EEPROM.

        Kwargs:
            address (int): The address number to read from.
        """
        self.eeprom.is_valid_address(address)
        return commands.ReadByte.send(self, address)

    def write_byte(self, address, byte):
        """
        Write a byte to an address in the EEPROM.

        Kwargs:
            address (int): The address to write to.
            byte (int): The byte to write.

        Raises:
            ValueError if address or byte is out of range for the EEPROM.

        """
        self.eeprom.is_valid_address(address)
        self.eeprom.is_valid_data(byte)
        return commands.WriteByte.send(self, address, byte)

    def read_block(self, address):
        """
        Return a block of 16 consecutive bytes from the EEPROM.

        Kwargs:
            address (int): The address of the first byte in the block.

        Returns:
            int

        Raises:
            ValueError if address is out of range for the EEPROM.

        """
        self.eeprom.is_valid_address(address)
        self.eeprom.is_valid_address(address + 15)
        return commands.ReadBlock.send(self, address)

    def write_block(self, address, data):
        """
        Write a block of 16 consecutive bytes to the EEPROM.

        Kwargs:
            address (int): The address of the first byte in the block.
            data (list[int]): A list of 16 bytes to write.

        Raises:
            ValueError if address or data is out of range for the EEPROM.

        """
        self.eeprom.is_valid_address(address)
        self.eeprom.is_valid_address(address + 15)
        for byte in data:
            self.eeprom.is_valid_data(byte)
        return commands.WriteBlock.send(self, address, data)

    def read(self, start_address=None, end_address=None):
        """
        Return a block of data from the EEPROM.

        Kwargs:
            start_address (int): The start address of the block. Defaults to the
                lowest address on the EEPROM.
            end_address (int): The end address of the block. Defaults to the
                highest address on the EEPROM.

        Returns:
            list(int)

        Raises:
            ValueError if address is out of range for the EEPROM.
        """
        start = start_address or self.eeprom.min_address
        end = end_address or self.eeprom.max_address
        data = []
        for address in range(start, end - 1, 16):
            data += self.read_block(address)
        return data

    def write(self, data, start_address=None):
        """
        Write a block of data to the EEPROM.

        Args:
            data (list(int)): A list of bytes to write to the EEPROM.

        Kwargs:
            start_address (int): The first address to write to. Defaults to the lowest
                address on the EEPROM.

        Returns:
            list(int)

        Raises:
            ValueError if address or data is out of range for the EEPROM.

        """
        start = start_address or 0
        address = start or self.eeprom.min_address
        self.eeprom.is_valid_address(start + len(data) - 1)
        for i in range(0, len(data), 16):
            block = data[i : i + 16]
            self.write_block(address, block)
            address += 16
