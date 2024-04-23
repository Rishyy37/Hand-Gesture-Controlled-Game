import cv2
import numpy as np
import mediapipe as mp
from pynput.keyboard import Controller, Key
import time
import socket
import ctypes

# Function to get the screen resolution
def get_screen_resolution():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Create a socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_socket.connect(('localhost', 8000))  # Connect to the server
server_address = ('localhost', 8000)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

keyboard = Controller()  # Initialize the keyboard controller
start = time.time()
frames = 0

prev_landamark = None
jump = []

# Get screen resolution
screen_width, screen_height = get_screen_resolution()
print(screen_width, screen_height)

def detect_movement(prev, current, keyboard):
    dx = current[0][0] - prev[0][0]
    dy = current[0][1] - prev[0][1]

    direction_byte = None
    if abs(dx) > 0.009:
        if dx > 0:
            print('right')
            direction_byte = b'\x01'
        else:
            print('left')
            direction_byte = b'\x00'

    elif abs(dy) > 0.009:
        if dy < 0:
            print('up')
            direction_byte = b'\x02'
        else:
            print('down')
            direction_byte = b'\x03'

    return direction_byte

with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        results = hands.process(image)
        image_height, image_width, _ = image.shape

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                current_landmark = [(wrist.x, wrist.y)]
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                dis_index_thumb = np.sqrt(
                    (index_tip.x - thumb.x)**2 + (index_tip.y - thumb.y)**2 + (index_tip.z - thumb.z)**2)
                
                distance = np.sqrt((wrist.x - middle_finger_tip.x)
                                   ** 2 + (wrist.y - middle_finger_tip.y) ** 2)
                jump.append(distance)
                if len(jump) > 2:
                    if jump[-1] <= 0.13:
                        direction_byte = b'\x05'
                        print("jump")
                        client_socket.sendto(direction_byte, server_address)
                        response, server_address = client_socket.recvfrom(1024)
                        print("Received response:", response)

                threshold_middle_wrist = 0.21
                threshold_thumb_index = 0.095

                if prev_landamark:
                    direction_byte = detect_movement(
                        prev=prev_landamark, current=current_landmark, keyboard=keyboard)
                    if direction_byte:
                        client_socket.sendto(direction_byte, server_address)
                        response, server_address = client_socket.recvfrom(1024)
                        print("Received response:", response)
                prev_landamark = current_landmark

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        frames += 1
        elapsed_time = time.time() - start
        if elapsed_time:  # Update FPS every second
            fps = frames / elapsed_time
            cv2.putText(image, f"FPS: {int(fps)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            frames = 0
            start = time.time()

        # Get the size of the window
        window_width, window_height = 400, 300

        # Calculate the position to place the window (top-right corner)
        x_position = screen_width - window_width
        y_position = 0

        # Move the window to the calculated position
        cv2.namedWindow("MediaPipe Hands", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("MediaPipe Hands", window_width, window_height)
        cv2.moveWindow("MediaPipe Hands", x_position, y_position)

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
client_socket.close()
