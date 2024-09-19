import time
import rtmidi
import rtmidi.midiconstants
from rtmidi.midiconstants import (CONTROL_CHANGE)
import numpy as np
import matplotlib.pyplot as plt
import sys

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
midiout.open_port(3)

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
BPM = 90
def modulation_shape(repeat=1):
    """ function which shows a modulation shape """
    t = np.arange(0, 80, 0.1)
    amplitude = np.sin(t)
    plt.plot(t[1:60], amplitude[1:60])
    plt.title("Modulation Shape")
    plt.xlabel("Time")
    plt.ylabel("Amplitude = sin(time)")
    plt.grid(True, which="both")
    plt.axhline(y=0, color="k")
    plt.show()
    send_mod(amplitude, repeat)

def duration_to_time_delay(duration, bpm):
    if duration == 'w':
        factor = 4
    elif duration == 'h':
        factor = 2
    elif duration == 'q':
        factor = 1
    elif duration == 'e':
        factor = 0.5
    elif duration == 's':
        factor = 0.25
    else:
        assert False;
    bps = bpm/60
    return factor * bps

# def duration_of_melody(melody, bpm):
#     t = 0
#     for _, duration in melody:
#         t += duration_to_time_delay(duration, bpm)
#     return t

def duration_of_melody(melody, bpm):
    return sum(duration_to_time_delay(duration, bpm) for _, duration in melody)

def main():
    melody = [(60, "e"), (67, "q"), (62, "q"), (67, "q")] * 8
    dur = duration_of_melody(melody, BPM)
    print(f"Duration of melody: {dur} seconds")
main()
#amp = modulation_shape(1)

