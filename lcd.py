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
        """Send 4 bits of data to LCD."""
        for i in range(4):
            self.data_pins[i].value((nibble >> i) & 0x01)
        self.pulse_enable()

    def send_byte(self, data, is_data=True):
        """Send 8 bits of data to LCD."""
        self.rs.value(is_data)
        self.send_nibble(data >> 4)  # Send higher nibble
        self.send_nibble(data & 0x0F)  # Send lower nibble

    def write_command(self, cmd):
        self.send_byte(cmd, is_data=False)

    def write_char(self, char):
        """Write one character"""
        self.send_byte(ord(char), is_data=True)

    def clear(self):
        """Clear the LCD screen."""
        self.write_command(0x01)
        sleep(0.002)

    def init_lcd(self):
        """Initialize LCD"""
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
        """Write some text to the LCD screen."""
        for char in message:
            self.write_char(char)
    
    def write_auto_move(self, message):
        """Write some text to the LCD screen. If text length exceeds 16 chars, automatically goes to next line."""
        self.clear()
        if len(str(message)) > 32:
            result = []
    
            while len(final_string) > max_length:
                # Find the last space within the first `max_length` characters
                last_space_index = final_string[:max_length].rfind(' ')
                
                if last_space_index != -1:
                    # Add the part up to the last space to the result list
                    result.append(final_string[:last_space_index])
                    # Remove the processed part from the string
                    final_string = final_string[last_space_index + 1:]
                else:
                    # If no space is found, split at the `max_length` character
                    result.append(final_string[:max_length])
                    final_string = final_string[max_length:]
    
            # Add the remaining part of the string (if any)
            if final_string:
                result.append(final_string)

            for i in result:
                self.clear()
                self.write_auto_move(i)
                sleep(5)

        elif len(str(message)) > 16:
            r1 = str(message)[:16].strip()
            r2 = str(message)[16:].strip()
            self.set_cursor(0, 0) # Go to first row, first position
            self.write(r1)
            self.set_cursor(1, 0) # Go to second row, first position
            self.write(r2)
        
        elif len(str(message)) < 16:
            self.write(message=message)
        
        elif len(str(message)) == "" or None:
            self.write("")

    def set_cursor(self, line, position):
        """Change position of cursor."""
        # Line 1 starts at 0x00, Line 2 starts at 0x40
        addr = position + (0x40 if line == 1 else 0x00)
        self.write_command(0x80 | addr)
        

# Default pin configuration
DEFAULT_PINS = {
    "RS": 6,
    "E": 7,
    "DB4": 8,
    "DB5": 9,
    "DB6": 10,
    "DB7": 11
}
