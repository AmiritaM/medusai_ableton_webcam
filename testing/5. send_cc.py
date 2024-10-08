import time
import rtmidi
import rtmidi.midiconstants
from rtmidi.midiconstants import (CONTROL_CHANGE)
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import sys

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
midiout.open_port(2)

CHANNEL = 0
CC_NUM = 75
SPEED = 0.02

def convert_range(value, in_min, in_max, out_min, out_max):
    l_span = in_max - in_min
    r_span = out_max - out_min
    scaled_value = (value - in_min) / l_span
    scaled_value = out_min + (scaled_value * r_span)
    return np.round(scaled_value)

def send_mod(amplitude, repeat):
    """ function that sends cc data to midi driver"""
    scaled = []
    for amp in amplitude:
        val = (convert_range(amp, -1, 1.0, 0, 127))
        scaled.append(val)
    for _ in range(repeat):
        for value in scaled:
            mod = ([CONTROL_CHANGE | CHANNEL, CC_NUM, value])
            midiout.send_message(mod)
            time.sleep(SPEED)

def modulation_shape(shape: str, period: float, max_duration: float):
    """ function which shows a modulation shape """
    x = np.arange(0, max_duration, 0.01)

    if shape == 'sine':
        y = np.sin(2 * np.pi / period * x)
    elif shape == 'saw':
        y = signal.sawtooth(2 * np.pi / period * x)
    elif shape == 'square':
        y = signal.square(2 * np.pi / period * x)
    else:
        print("That wave is not supported")
        sys.exit()
    plt.plot(x, y)
    plt.ylabel(f"Amplitude = {shape} (time)")
    plt.xlabel('Time')
    plt.title('Modulation Shape')
    plt.axhline(y=0, color ='blue')
    plt.show()
# amp = modulation_shape(1)

modulation_shape("square", 1.0, 16.0)
