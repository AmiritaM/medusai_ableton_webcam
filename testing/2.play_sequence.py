import rtmidi
import time

midiout = rtmidi.MidiOut()
ports = midiout.get_ports()
print(ports)
midiout.open_port(3)

tempo = 0.4

# with midiout:
#     for bar in range(4):
#         for note in range(0, 4):
#             note_on = [0x90, 60, 50]
#             note_off = [0x80, 60, 0]
#             midiout.send_message(note_on)
#             time.sleep(tempo)
#             midiout.send_message(note_off)
#         for note in range(4):
#             note_on = [0x90, 62, 50]
#             note_off = [0x80, 62, 0]
#             midiout.send_message(note_on)
#             time.sleep(tempo)
#             midiout.send_message(note_off)
#         for note in range(4):
#             note_on = [0x90, 60, 50]
#             note_off = [0x80, 60, 0]
#             midiout.send_message(note_on)
#             time.sleep(tempo)
#             midiout.send_message(note_off)