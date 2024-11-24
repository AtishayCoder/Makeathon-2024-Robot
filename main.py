import network
import machine as m
from time import sleep
from lcd import LCD, PINS
import urequests as requests

# Microphone

ck = 1
ws = 2
da = 3
record_button = m.Pin(4, m.Pin.IN, m.Pin.PULL_UP)
i2s = m.I2S(0, sck=m.Pin(ck), ws=m.Pin(ws), sd=m.Pin(da), mode=m.I2S.RX, bits=16, format=m.I2S.MONO, rate=16000, ibuf=1024)
audio_buffer = bytearray(1024)
is_recording = False  # Start with recording stopped

# LCD
lcd = LCD(pins=PINS)
lcd.write("")

def toggle_recording():
    global is_recording
    if is_recording:
        print("Stopping recording...")
        is_recording = False
    else:
        print("Starting recording...")
        is_recording = True

# WiFi
SERVER_ENDPOINT = "glowworm-charmed-jointly.ngrok-free.app"
ssid = "kandarp_EXT"
password = "One@2@three"

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected to WLAN. IP address - {ip}")
    print("Attempting to visit server website...")
    requests.post()

# Mainloop

try:
    connect_to_wifi()
    while True:
        # Check for button press (when pin reads low)
        if record_button.value() == 0:
            # Debounce the button press
            sleep(0.2)
            if record_button.value() == 0:
                toggle_recording()
            
            # Wait for button release
            while record_button.value() == 0:
                pass
            sleep(0.2)  # Debounce for release
            
        # If recording, capture audio data
        if is_recording:
            num_bytes_read = i2s.readinto(audio_buffer)
            print("Captured", num_bytes_read, "bytes of audio data")
            
except Exception as e:
    print(str(e))
    
finally:
    i2s.deinit()  # Clean up I2S on exit
