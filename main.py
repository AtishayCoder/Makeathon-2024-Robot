import network
import machine as m
from time import sleep

ck = 1
ws = 2
da = 3
record_button = m.Pin(4, m.Pin.IN, m.Pin.PULL_UP)

i2s = m.I2S(0, sck=m.Pin(ck), ws=m.Pin(ws), sd=m.Pin(da), mode=m.I2S.RX, bits=16, format=m.I2S.MONO, rate=16000, ibuf=1024)

audio_buffer = bytearray(1024)
is_recording = False  # Start with recording stopped

def toggle_recording():
    global is_recording
    if is_recording:
        print("Stopping recording...")
        is_recording = False
    else:
        print("Starting recording...")
        is_recording = True

try:
    while True:
        # Check for button press (when pin reads low)
        if button.value() == 0:
            # Debounce the button press
            time.sleep(0.2)
            if button.value() == 0:
                toggle_recording()
            
            # Wait for button release
            while button.value() == 0:
                pass
            time.sleep(0.2)  # Debounce for release
            
        # If recording, capture audio data
        if is_recording:
            num_bytes_read = i2s.readinto(audio_buffer)
            print("Captured", num_bytes_read, "bytes of audio data")
            # Send data

finally:
    i2s.deinit()  # Clean up I2S on exit
