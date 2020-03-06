# EEPROM - Arduino based EEPROM programmer

[![Build Status](https://travis-ci.org/lukeshiner/eeprom.svg?branch=master)](https://travis-ci.org/lukeshiner/eeprom)
[![Coverage Status](https://coveralls.io/repos/github/lukeshiner/eeprom/badge.svg?branch=master)](https://coveralls.io/github/lukeshiner/eeprom?branch=master)

This is a very simple and very slow EEPROM programmer using an Arduino Nano based on the [design from Ben Eater](https://youtu.be/K88pgWhEb1M) for his [8-bit computer project](https://eater.net/8bit). The original design supports the AT28C16 EEPROM used that project, however EEPROM currently only supports the [AT28C256](http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf) used in his [6502 Computer](https://eater.net/6502) project. It will be extended to support the [AT28C16](http://cva.stanford.edu/classes/cs99s/datasheets/at28c16.pdf) and could easily support other EEPROMs as well.

The Arduino is configured to accept commands over serial from a CLI application. The application is a python package located in the *eeprom* directory.

## Getting Started

To use the EEPROM programmer you will need to construct the hardware, flash the Arduino with the *eeprom_programmer* software and install the CLI.

## Hardware Requirements

- An **[Arduino Nano](https://store.arduino.cc/arduino-nano)**. Other Arduino models such as an Uno or Mega could be used, though this has not been tested and might require some modification the the pins used.
- **Mini USB cable** to program and communicate with the Arduino.
- **[74LS595](http://www.ti.com/lit/ds/scls041i/scls041i.pdf) 8-bit latching shift-in registers** (x2). A part very commonly used in Arduino projects when the Arduino does not provide enough digital pins. Allows three pins on the Arduino (2,3 and  4) to control 15 **address lines** and the **output enable**.
- **LEDs** (Optional). I used 24 LEDs to indicate the status of each **address line**, **data line** and the **output enable**, however this is not required. A current limiting resistor will be required for each LED.
- **[ZIF socket](https://en.wikipedia.org/wiki/Zero_insertion_force)** (Optional). I chose to use a **ZIF** (Zero Insertion Force) socket to reduce wear on the EEPROM and to make it easier to ensure it is located correctly.

## Building the programmer

For a full tutorial on building the programmer follow Ben Eater's [Build an Arduino EEPROM programmer](https://youtu.be/K88pgWhEb1M) video. You will have to add some extra connections for the additional address lines of the **AT28C256** and bear in mind the different pin locations compared with the **AT25C16**. Please refer to the [datasheet](http://cva.stanford.edu/classes/cs99s/datasheets/at28c16.pdf).

Basic instructions for wiring the programmer follow. A diagram to clarify this will be added in the future.

- Connect VCC (16) and S&#773;R&#773;C&#773;L&#773;R&#773; (10) pins of the shift registers to 5v.
- Connect the GND (8) and O&#773;E&#773; (13) pins of the shift registers to ground.
- Connect the SRCLK pin (12) of both shift registers to pin D3 of the Arduino.
- Connect the SRCLK (11) pin of both shift registers to pin D4 of the Arduino.
- Connect the SER pin (14) of the first shift register to pin D2 of the Arduino.
- Connect the QH` (9) pin of the first shift register to the SER (14) pin of the second.
- Connect the QA (15), QB (1), QC (2), QD (3), QE (4), QF (5), QG (6) and QH (7) pins of the first shift register to Address 0 through 7 on the EEPROM respectively.
- Connect the QA (15), QB (1), QC (2), QD (3), QE (4), QF (5), QG (6) pins of the first shift register to Address 8 through 14 on the EEPROM respectively.
- Connect QH (7) on the second shift register to the O&#773;E&#773; pin of the EEPROM.
- Connect D13 of the Arduino to the W&#773;E&#773; pin of the EEPROM.
- Connect D5 through D12 of the Arduino to I/O0 through I/07 of the EEPROM respectively.
- Connect VCC on the EEPROM to 5v.
- Connect GND and C&#773;E&#773; on the EEPROM to ground.

**NOTE:** Pin numbers for the EEPROM are not provided as they depend on the particular EEPROM model being used. Some EEPROMs may not use all the available address lines.

## Programming the programmer

Source code for the Arduino is located in the *eeprom_programmer* directory. This can be flashed to an Arduino using the [Arduino IDE](https://www.arduino.cc/en/main/software).

- Connect the Arduino Nano to your computer with the mini USB cable.
- Open the *eeprom_programmer.ino* file from the eeprom_programmer directory in the Arduino IDE.
- Select the appropriate board with *Tools* > *Board* > *Arduino Nano*.
- Select *ATmega328P (old bootloader)* from the *Tools* > *Processor* menu.
- Select *Arduino as ISP* from the *Tools* > *Programmer* menu.
- Select the port on which the Arduino is addressed from the *Tools* > *Port* menu. If you only have one Arduino connected to your computer it is likely that only one option will be available.
- Click the *Upload* button in the top right of the IDE.
- If you did not get any error messages after the upload the Arduino should be configured and ready to accept instructions over serial.

For Arduino models other than the Nano other configuration options will be required.

## Installing the CLI

**Note:** These instructions are for installing on Linux based operating systems. While the program should function on windows this has not been tested and the setup process may vary slightly.

The package can be installed using **pip**. It is strongly recommended that you do not install it using the system Python. You should use a virtualenv or pipx.

This package is build with poetry so it will require poetry to be installed and pip version 20.0.02 or higher to be used.

Clone or download this repo.

```bash
git clone https://github.com/lukeshiner/eeprom.git
cd EEPROM
```

With a virtualenv active:

```bash
pip install -e .
```

Or install with pipx:

```bash
pipx install -e .
```

## Using the programmer

The available commands are listed below.

**Note:** This is a work in progress. Most commands, including those for connecting to the Arduino using settings other than the defaults or for using different EEPROMs are not yet implemented.

### version

 The **version** command returns the current version of the *eeprom* package.

```bash
eeprom version
$ 0.1.0
```

### read-byte

The **read-byte** command reads the byte in a given address in hex of the EEPROM and prints it to **STDOUT**.

```bash
eeprom read-byte --address F563
$ EA
```

### write-byte

The **write-byte** command writes a given byte to a given address.

```bash
eeprom write-byte --address F563 --byte 2A
```

## write

The **write** command writes a binary file to the EEPROM.

```bash
eeprom write /home/user/binary.bin
```

## read

The **read** command reads the contents of the EEPROM and writes it to STDOUT in binary.

```bash
eeprom read > binary_file.bin
```

## verify

The **verify** command takes a binary file and compares it to the contents of the EEPROM. If the contents match the program will return a 0 exit code, otherwise it will print a list of differences to STDOUT and exit with 1.

```bash
eeprom verify binary_file.bin
$ 005A expected 2A found 3F
```

## update

The **update** command updates the contents of the EEPROM where it differs from the contents of a passed binary file. If they are similar this is much faster than writing the entire EEPROM, however it does add an extra read operation so if the contents differ greatly it can take longer.

```bash
eeprom update binary_file.bin
```
