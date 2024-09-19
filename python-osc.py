import cv2
import time
import mediapipe as mp
import numpy as np
from pythonosc import udp_client

# OSC setup
ip = "10.91.166.7"
port = 8000
osc_client = udp_client.SimpleUDPClient(ip, port)

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

TEMPO = 0.2

def convert_range(value, in_min, in_max, out_min, out_max):
    l_span = in_max - in_min
    r_span = out_max - out_min
    scaled_value = (value - in_min) / l_span
    return np.round(out_min + (scaled_value * r_span))

def send_osc_notes(pitch=60, repeat=1):
    for i in range(repeat):
        osc_client.send_message("/note", pitch)
        time.sleep(TEMPO)

def send_osc_mod(cc=1, value=0):
    osc_client.send_message("/mod", [cc, value])
    print(f"OSC CC {cc} with value {value}")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = hands.process(imgRGB)
    if result.multi_hand_landmarks:
        h, w, c = img.shape
        for hand_landmarks in result.multi_hand_landmarks:
            pink_x = hand_landmarks.landmark[mpHands.HandLandmark.PINKY_TIP].x
            pink_y = hand_landmarks.landmark[mpHands.HandLandmark.PINKY_TIP].y
            if pink_x * w < 540:
                print("Left, OSC CC DATA")
                v1 = convert_range(pink_y, 1.0, 0.0, 0, 127)
                send_osc_mod(1, v1)
            elif pink_x * w > 540:
                print("Right, OSC Notes")
                v2 = convert_range(pink_y, 1.0, -1.0, 60, 92)
                send_osc_notes(v2, 1)
            mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)

    fps = 1
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 200, 5), 3)
    cv2.imshow("Ami", img)
    cv2.waitKey(fps)
