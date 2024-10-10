import sounddevice as sd

# List all available audio input devices
print(sd.query_devices())
