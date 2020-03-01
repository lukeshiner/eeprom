"""The Arduino class provides methods to commuinate with an Arduino over seiral."""
import time

import serial


class Arduino:
    """Handles communication with the Arduino over serial."""

    def __init__(self, port="/dev/ttyUSB0", baud=115200):
        """
        Create a connection with an arduino.

        Kwargs:
            port (str): The serial port on which the arduino is located.
                Default: "/dev/ttyUSB0"
            baud (int): The baud rate of the serial connection. Default: 115200.

        """
        self.port = port
        self.baud = baud
        self.serial_connection = None

    def open(self, init_delay=2):
        """
        Initialise a connection to the arduino.

        Kwargs:
            init_delay (int): The number of seconds to wait for the arduino to
                initialise. Default: 2
        """
        self.serial_connection = serial.Serial(self.port, self.baud)
        time.sleep(init_delay)  # Wait for arduino to initialize
        self.serial_connection.flush()
        self.serial_connection.reset_input_buffer()
        self.serial_connection.reset_output_buffer()

    def close(self):
        """Close the connection to the arduino."""
        self.serial_connection.close()

    def serial_recieve(self):
        """Return a serial message from the arduino."""
        message = self.serial_connection.readline()
        message = message.decode("utf8").strip()
        return message

    def serial_send(self, message):
        """
        Send a serial message to the arduino.

        Args:
            message (str): The message to send.

        """
        self.serial_connection.write(message.strip().encode("utf8") + b"\n")
