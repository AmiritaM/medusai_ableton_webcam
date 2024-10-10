import sounddevice as sd
import numpy as np

SAMPLE_RATE = 44100
BLOCK_SIZE = 1024
THRESHOLD_DB = -35
DEVICE_INDEX = 1

def audio_callback(indata, frames, time, status):
    if status:
        print(f"Stream status: {status}")

    amplitude = np.sqrt(np.mean(indata ** 2))
    db_level = 20 * np.log10(amplitude + 1e-6)

    if db_level > THRESHOLD_DB:
        print("Sound detected! dB Level:", db_level)
    else:
        print("No sound detected. dB Level:", db_level)

with sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE, device=DEVICE_INDEX):
    print("Listening for sound... Press Ctrl+C to stop.")
    sd.sleep(100000)
