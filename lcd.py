from machine import Pin
from time import sleep

class LCD:
    def __init__(self, pins):
        self.rs = Pin(pins["RS"], Pin.OUT)
        self.e = Pin(pins["E"], Pin.OUT)
        self.data_pins = [
            Pin(pins["DB4"], Pin.OUT),
            Pin(pins["DB5"], Pin.OUT),
            Pin(pins["DB6"], Pin.OUT),
            Pin(pins["DB7"], Pin.OUT),
        ]
        self.init_lcd()
        self.clear()  # Clear the LCD to ensure it's blank at start

    def pulse_enable(self):
        self.e.value(1)
        sleep(0.0005)
        self.e.value(0)
        sleep(0.0005)

    def send_nibble(self, nibble):
        for i in range(4):
            self.data_pins[i].value((nibble >> i) & 0x01)
        self.pulse_enable()

    def send_byte(self, data, is_data=True):
        self.rs.value(is_data)
        self.send_nibble(data >> 4)  # Send higher nibble
        self.send_nibble(data & 0x0F)  # Send lower nibble

    def write_command(self, cmd):
        self.send_byte(cmd, is_data=False)

    def write_char(self, char):
        self.send_byte(ord(char), is_data=True)

    def clear(self):
        self.write_command(0x01)
        sleep(0.002)

    def init_lcd(self):
        sleep(0.02)  # Wait for power-up
        self.send_nibble(0x03)
        sleep(0.005)
        self.send_nibble(0x03)
        sleep(0.005)
        self.send_nibble(0x03)
        self.send_nibble(0x02)  # Set to 4-bit mode

        # Function set: 4-bit mode, 2 lines, 5x8 dots
        self.write_command(0x28)

        # Display control: Display on, cursor off, blink off
        self.write_command(0x0C)

        # Entry mode set: Increment cursor, no shift
        self.write_command(0x06)

    def write(self, message):
        for char in message:
            self.write_char(char)

    def set_cursor(self, line, position):
        # Line 1 starts at 0x00, Line 2 starts at 0x40
        addr = position + (0x40 if line == 1 else 0x00)
        self.write_command(0x80 | addr)
        

# Pin configuration
PINS = {
    "RS": 6,
    "E": 7,
    "DB4": 8,
    "DB5": 9,
    "DB6": 10,
    "DB7": 11
}
