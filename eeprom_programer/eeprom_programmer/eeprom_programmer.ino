#define ADD_DATA 2
#define ADD_CLK 3
#define ADD_LATCH 4

#define EEPROM_D0 5
#define EEPROM_D7 12
#define WRITE_ENABLE 13

const char WRITE_CODE = 'W';
const char READ_CODE = 'R';
const char READ_16_CODE = 'T';
const char WRITE_16_CODE = 'S';

int writeEnableDelay = 1;
int betweenWriteDelay = 12;

String message;

void setup()
{
  pinMode(ADD_DATA, OUTPUT);
  pinMode(ADD_CLK, OUTPUT);
  pinMode(ADD_LATCH, OUTPUT);
  digitalWrite(WRITE_ENABLE, HIGH);
  pinMode(WRITE_ENABLE, OUTPUT);
  Serial.begin(115200);
}

void loop()
{
  recieve();
}

//EEPROM Functions
void outputAddress()
{
  digitalWrite(ADD_LATCH, LOW);
  digitalWrite(ADD_LATCH, HIGH);
  digitalWrite(ADD_LATCH, LOW);
}

void setAddress(int address, bool outputEnable)
{
  shiftOut(ADD_DATA, ADD_CLK, MSBFIRST, (address >> 8) | (outputEnable ? 0x00 : 0x80));
  shiftOut(ADD_DATA, ADD_CLK, MSBFIRST, address);
  outputAddress();
}

byte readEEPROM(int address)
{
  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin++)
  {
    pinMode(pin, INPUT);
  }
  setAddress(address, /*outputEnable*/ true);
  byte data = 0;
  for (int pin = EEPROM_D7; pin >= EEPROM_D0; pin--)
  {
    data = (data << 1) + digitalRead(pin);
  }
  return data;
}

void writeEEPROM(int address, byte data)
{
  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin++)
  {
    pinMode(pin, OUTPUT);
  }
  setAddress(address, /*outputEnable*/ false);
  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin++)
  {
    digitalWrite(pin, data & 1);
    data = data >> 1;
  }
  digitalWrite(WRITE_ENABLE, LOW);
  delayMicroseconds(writeEnableDelay);
  digitalWrite(WRITE_ENABLE, HIGH);
  delay(betweenWriteDelay);
}

void writeEnableEEPROM()
{
  int oldWriteEnableDelay = writeEnableDelay;
  int oldBetweenWriteDelay = betweenWriteDelay;
  writeEnableDelay = 0;
  betweenWriteDelay = 0;
  writeEEPROM(0x5555, 0xAA);
  writeEEPROM(0x2AAA, 0x55);
  writeEEPROM(0x5555, 0x80);
  writeEEPROM(0x5555, 0xAA);
  writeEEPROM(0x2AAA, 0x55);
  writeEEPROM(0x5555, 0x20);
  writeEnableDelay = oldWriteEnableDelay;
  betweenWriteDelay = oldBetweenWriteDelay;
}

// Serial Functions
void recieve()
{
  while (!Serial.available())
  {
  }

  while (Serial.available())
  {
    char c = Serial.read();
    message += c;
    delay(30);
    if (c == '\n')
    {
      break;
    }
  }
  parseMessage(message);
  message = "";
}

void parseMessage(String message)
{
  char instructionCode = message.charAt(0);
  if (instructionCode == WRITE_CODE)
  {
    handleWriteByte(message);
  }
  else if (instructionCode == READ_CODE)
  {
    handleReadByte(message);
  }
  else if (instructionCode == READ_16_CODE)
  {
    handleRead16(message);
  }
  else if (instructionCode == WRITE_16_CODE)
  {
    handleWrite16(message);
  }
  else
  {
    recieveError(instructionCode);
  }
}

void recieveError(char instructionCode)
{
  Serial.println(instructionCode);
}

void writeSuccess()
{
  Serial.println("ACK");
}

void handleReadByte(String message)
{
  long address = parseHexInString(message, 1, 5);
  Serial.println(readEEPROM(address), HEX);
}

void handleWriteByte(String message)
{
  long address = parseHexInString(message, 1, 5);
  long data = parseHexInString(message, 5, 7);
  writeEEPROM(address, data);
  writeSuccess();
}

void handleRead16(String Message)
{
  char buf[47];
  byte data[16];
  long address = parseHexInString(message, 1, 5);
  for (int i = 0; i < 16; i++)
  {
    data[i] = readEEPROM(address + i);
  }
  sprintf(
      buf,
      "%02X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X ",
      data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
      data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15]);
  Serial.println(buf);
}

void handleWrite16(String message)
{
  byte data;
  long address = parseHexInString(message, 1, 5);
  for (int i = 0; i < 16; i++)
  {
    data = parseHexInString(message, 5 + i * 2, 7 + i * 2);
    writeEEPROM(address + i, data);
  }
  writeSuccess();
}

long parseHexInString(String message, int from, int to)
{
  char buf[5];
  message.substring(from, to).toCharArray(buf, 5);
  return strtol(buf, NULL, 16);
}

void printContents()
{
  for (long base = 0; base < 32768; base += 16)
  {
    byte data[16];
    Serial.print(base, HEX);
    Serial.print("\t");
    for (int offset = 0; offset <= 15; offset++)
    {
      if (offset == 8)
      {
        Serial.print("\t");
      }
      else
      {
        Serial.print(" ");
      }
      Serial.print(readEEPROM(base + offset), HEX);
    }
    Serial.print("\n");
  }
  Serial.println();
}
