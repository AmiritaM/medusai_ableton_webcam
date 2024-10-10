import sounddevice as sd
import numpy as np
from pythonosc import udp_client

SAMPLE_RATE = 44100
BLOCK_SIZE = 1024
THRESHOLD_DB = -35
DEVICE_INDEX = 1

# Set up the UDP client to send messages to the lab computer
ip = "192.168.1.100"  # Replace with the IP address of the lab computer
port = 8000  # The port you want to send data to
client = udp_client.SimpleUDPClient(ip, port)

def audio_callback(indata, frames, time, status):
    if status:
        print(f"Stream status: {status}")

    amplitude = np.sqrt(np.mean(indata ** 2))
    db_level = 20 * np.log10(amplitude + 1e-6)

    if db_level > THRESHOLD_DB:
        print("Sound detected! dB Level:", db_level)
        client.send_message("/pluck", "Pluck detected!")  # Send OSC message to the lab computer
    else:
        print("No sound detected. dB Level:", db_level)

with sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE, device=DEVICE_INDEX):
    print("Listening for sound... Press Ctrl+C to stop.")
    sd.sleep(100000)
