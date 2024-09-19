import rtmidi
import time

midiout = rtmidi.MidiOut()
midiout.open_port(3)

def send_notes(pitch=60, repeat=2):
    for note in range(0, repeat):
        note_on = [0x90, pitch, 80]
        note_off = [0x80, pitch, 0]
        midiout.send_message(note_on)
        time.sleep(0.2)
        midiout.send_message(note_off)
with midiout:
    for i in range(4):
        send_notes(60)
        send_notes(63)
        send_notes(60)
        send_notes(63)