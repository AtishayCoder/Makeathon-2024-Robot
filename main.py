import network
import machine as m
from time import sleep
from lcd import LCD, DEFAULT_PINS
import urequests as requests

# Microphone

ck = 1
ws = 2
da = 3
record_button = m.Pin(4, m.Pin.IN, m.Pin.PULL_UP)
button_enabled = True
i2s = m.I2S(0, sck=m.Pin(ck), ws=m.Pin(ws), sd=m.Pin(da), mode=m.I2S.RX, bits=16, format=m.I2S.MONO, rate=16000, ibuf=1024)
audio_buffer = bytearray(1024)
is_recording = False  # Start with recording stopped
audio_ready_to_send = False


def toggle_recording():
    global is_recording, audio_ready_to_send
    if is_recording:
        print("Stopping recording...")
        is_recording = False
        audio_ready_to_send = True
        lcd.write_auto_move("Recording stopped.")
    else:
        print("Starting recording...")
        is_recording = True
        audio_ready_to_send = False  # Reset the flag when starting a new recording
        lcd.write_auto_move("Recording...")


# LCD
lcd = LCD(pins=DEFAULT_PINS)
lcd.clear()
lcd.write("Connecting...")

# WiFi
SERVER_ENDPOINT = "https://glowworm-charmed-jointly.ngrok-free.app/"
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


def send():
    global is_recording, button_enabled
    lcd.write_auto_move("Please wait...")
    button_enabled = False
    is_recording = False
    print("Sending data. Making POST request.")
    reply = requests.get(f"{SERVER_ENDPOINT}post-recording", params={
        "audio": str(audio_buffer)
    })
    if str(reply).startswith("ask"):
        lcd.write_auto_move(str(reply.text).removeprefix("ask/"))
    elif str(reply).startswith("result"):
        lcd.write_auto_move(str(reply.text).removeprefix("result/"))
        sleep(5)
        tests = requests.get(f"{SERVER_ENDPOINT}get-tests")
        lcd.write_auto_move("Tests to be conducted.")
        sleep(5)


        # TODO: Write code to display tests.


        lcd.write("Cleaning up...")
        m.soft_reset()

# Mainloop

try:
    connect_to_wifi()
    lcd.clear()

    lcd.write_auto_move("Press the button to record.")

    sleep(3000)
    lcd.clear()
    
    lcd.write_auto_move("What is your gender?")

    while True:
        if button_enabled:
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
            lcd.write_auto_move("Listening...")
            num_bytes_read = i2s.readinto(audio_buffer)
            print("Captured", num_bytes_read, "bytes of audio data")
        elif audio_ready_to_send:
            send()
            audio_ready_to_send = False
            
except Exception as e:
    print(str(e))
