"""Serial commands for the EEPROM progammer."""


class ProgrammerCommand:
    """Base class for programmer commands."""

    CODE = ""
    SUCCESS_MESSAGE = "ACK"
    name = ""

    @classmethod
    def send(cls, programmer, *args):
        """Send a command to the programmer and handle the response."""
        message = cls.CODE + cls.format_arguments(*args)
        programmer.arduino.serial_send(message)
        response = programmer.arduino.serial_recieve()
        return cls.process_response(response)

    @classmethod
    def format_arguments(self, *args):
        """Return the command arguments as a string."""
        raise NotImplementedError()

    @classmethod
    def process_response(cls, response):
        """Handle the serial response."""
        if response != cls.SUCCESS_MESSAGE:
            raise ValueError(f"{cls.name} got unexpected response: {response}")

    @classmethod
    def format_address(cls, address):
        """Return an address number as a formatted string."""
        return f"{address:04X}"

    @classmethod
    def format_byte(cls, byte):
        """Return a byte as a formatted string."""
        return f"{byte:02X}"

    @classmethod
    def format_data(cls, data):
        """Return a list containing bytes of data as a formatted string."""
        return "".join([cls.format_byte(_) for _ in data])


class ReadByte(ProgrammerCommand):
    """
    Return the byte stored in a particular address of the EEPROM.

    Args:
        address (int): The address number to read from.
    """

    CODE = "R"
    name = "read_byte"

    @classmethod
    def format_arguments(cls, address):
        """Return the command arguments as a string."""
        return cls.format_address(address)

    @classmethod
    def process_response(cls, response):
        """Handle the serial response."""
        try:
            return int(response, 16)
        except ValueError:
            raise ValueError(f"{cls.name} got unexpected response: {response}")


class WriteByte(ProgrammerCommand):
    """
    Write a byte to an address in the EEPROM.

    Args:
        address (int): The address to write to.
        data (int): The byte to write.

    """

    CODE = "W"
    name = "write_byte"

    @classmethod
    def format_arguments(cls, address, data):
        """Return the command arguments as a string."""
        return "".join([cls.format_address(address), cls.format_byte(data)])


class ReadBlock(ProgrammerCommand):
    """
    Return a block of 16 consecutive bytes from the EEPROM.

    Args:
        address (int): The address of the first byte in the block.
    """

    CODE = "T"
    name = "read_block"

    @classmethod
    def format_arguments(cls, address):
        """Return the command arguments as a string."""
        return cls.format_address(address)

    @classmethod
    def process_response(cls, response):
        """Handle the serial response."""
        try:
            return [int(digit, 16) for digit in response.strip().split(" ")]
        except ValueError:
            raise ValueError(f"{cls.name} got unexpected response: {response}")


class WriteBlock(ProgrammerCommand):
    """
    Write a block of 16 consecutive bytes to the EEPROM.

    Args:
        address (int): The address of the first byte in the block.
        data (list[int]): A list of 16 bytes to write.
    """

    CODE = "S"
    name = "write_block"

    @classmethod
    def format_arguments(cls, address, data):
        """Return the command arguments as a string."""
        return "".join([cls.format_address(address), cls.format_data(data)])
