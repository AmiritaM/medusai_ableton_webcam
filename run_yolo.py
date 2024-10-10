import math
import random

from ultralytics import YOLO
import cv2
from pythonosc import udp_client
import rtmidi
import numpy as np

KP_NOSE = 0
KP_EYE_RIGHT = 1
KP_EYE_LEFT = 2
KP_EAR_RIGHT = 3
KP_EAR_LEFT = 4
KP_SHOULDER_RIGHT = 5
KP_SHOULDER_LEFT = 6
KP_ELBOW_RIGHT = 7
KP_ELBOW_LEFT = 8
KP_WRIST_RIGHT = 9
KP_WRIST_LEFT = 10
KP_WAIST_RIGHT = 11
KP_WAIST_LEFT = 12
KP_KNEE_RIGHT = 13
KP_KNEE_LEFT = 14
KP_ANKLE_RIGHT = 15
KP_ANKLE_LEFT = 16

client = udp_client.SimpleUDPClient('127.0.0.1', 7099)
# midiout = rtmidi.MidiOut()
# midiout.open_virtual_port("Medusai")

midiout = rtmidi.MidiOut()
ports = midiout.get_ports()
midiout.open_port(2)


cap = cv2.VideoCapture(1)
model = YOLO("yolov8n-pose.pt")

import cv2


# def list_webcams():
#     index = 0
#     available_cameras = []
#
#     # Try up to 10 indices (or more, depending on your system)
#     while index < 10:
#         cap = cv2.VideoCapture(index)
#         if cap.isOpened():
#             print(f"Camera found at index {index}")
#             available_cameras.append(index)
#             cap.release()
#         index += 1
#
#     if not available_cameras:
#         print("No cameras found.")
#     else:
#         print("Available camera indices:", available_cameras)
#
#
# list_webcams()


class MessageSender:
    def __init__(self):
        self.keypoints_history = []
        self.veloc_history = []

    def compute_derivatives(self, keypoints):
        veloc = []
        acc = []
        for i, k in enumerate(keypoints):
            if len(self.keypoints_history) > 0:
                x = k[0] - self.keypoints_history[-1][i][0]
                y = k[1] - self.keypoints_history[-1][i][1]
                veloc.append([x, y])
            else:
                veloc.append([0, 0])

        for i, k in enumerate(veloc):
            if len(self.veloc_history) > 0:
                x = k[0] - self.veloc_history[-1][i][0]
                y = k[1] - self.veloc_history[-1][i][1]
                acc.append([x, y])
            else:
                acc.append([0, 0])

        self.keypoints_history.append(keypoints)
        self.veloc_history.append(veloc)



        if len(self.keypoints_history) > 5:
            self.keypoints_history = self.keypoints_history[1:]
        if len(self.veloc_history) > 5:
            self.veloc_history = self.veloc_history[1:]
        return veloc, acc
# velocity - tempo
# sigmoid function/tan
    def moving_average(self):
        kps = np.array(self.keypoints_history)
        velocs = np.array(self.veloc_history)
        return kps.mean(axis=0), velocs.mean(axis=0)

    def send_midi(self, keypoints, human_id):
        veloc, acc = self.compute_derivatives(keypoints)
        keypoints, veloc = self.moving_average()

        cutoff = math.log(keypoints[KP_WRIST_RIGHT][1] + 1) * 127
        res = abs(keypoints[KP_WRIST_LEFT][1]) * 127


        head_tilt = (keypoints[KP_EYE_LEFT][1] - keypoints[KP_EYE_RIGHT][1]) * 64 + 64
        hand_dist = abs(keypoints[KP_WRIST_RIGHT][0] - keypoints[KP_WRIST_LEFT][0]) * 32 + 64
        print(veloc[KP_WRIST_LEFT][1])
        midiout.send_message([0xB0 + human_id, 74, cutoff])
        midiout.send_message([0xB0 + human_id, 71, res])
        midiout.send_message([0xB0 + human_id, 80, head_tilt]) # oscillator pitch
        midiout.send_message([0xB0 + human_id, 82, hand_dist]) # frequency modulation

sender = MessageSender()

print('LEARN MODE')

for cc in [71, 74, 80, 81, 82]:
    while True:
        _, img = cap.read()
        cv2.imshow('test', img)
        k = cv2.waitKey(1) & 0xFF
        midiout.send_message([0xB0, cc, random.randint(0, 127)])
        print(cc)
        if k == ord('a'):
            break
while True:
    _, img = cap.read()
    results = model(img, stream=True)

    for r in results:
        humans = r.boxes.xyxy
        keypoints = r.keypoints.xy.tolist()
        keypoints_n = r.keypoints.xyn.tolist()
        for hi, human in enumerate(humans):
            x1, y1, x2, y2 = human.tolist()
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 5)
            print(len(keypoints[hi]))
            for ki, k in enumerate(keypoints[hi]):
                point = (int(k[0]), int(k[1]))
                cv2.circle(img, point, 8, (100, 100, 255), 5)
                cv2.putText(img, "k_" + str(hi) + "_" + str(ki), point, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100, 255, 80), 2, 2)

                sender.send_midi(keypoints_n[hi], ki)

        # img = r.plot()
    cv2.imshow('window', img)
    cv2.waitKey(1)


    #
