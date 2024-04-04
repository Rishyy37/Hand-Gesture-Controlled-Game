import cv2
import numpy as np
import mediapipe as mp
from pynput.keyboard import Controller, Key
import time
import socket


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

def detect_movement(prev,current,keyboard):
    dx = current[0][0] - prev[0][0]
    dy =  current[0][1] - prev[0][1]

    # print(f"dx:{dx} , dy:{dy}")
    direction_byte = None
    if abs(dx) > 0.009:
        if dx > 0:
            print('right')
            # keyboard.press(Key.right)
            direction_byte = b'\x01'
        else:
            print('left')
            # keyboard.press(Key.left)
            direction_byte = b'\x00'

    elif abs(dy) > 0.009:
        if dy < 0:
            print('up')
            # keyboard.press(Key.up)
            direction_byte = b'\x02'
        else:
            print('down')
            # keyboard.press(Key.down)
            direction_byte = b'\x03'
    
    # if direction_byte is None:
    #     direction_byte = b'\x04'
    # elif abs(dx) > 0.009 and abs(dy) > 0.009:
    #     if dx > 0 and dy > 0:
    #         print( 'up and right')
    #     elif dx < 0 and  dy > 0:
    #         print("up and left")
    #     elif dx< 0 and dy <0:
    #         print( "down and left")
    #     else:
    #         print("down and right")
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
                wrist =  hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                current_landmark = [(wrist.x,wrist.y)]
                # print(
                #     f'Index finger tip coordinates: (',
                #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x }, '
                #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y})'
                # )
                # print(
                #     f'THUMB_TIP coordinates: (',
                #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x}, '
                #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y})'
                # )
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                dis_index_thumb = np.sqrt((index_tip.x-thumb.x)**2 + (index_tip.y-thumb.y)**2 + (index_tip.z-thumb.z)**2)
                # print(dis_index_thumb)
                # print(f"z index:{index_tip.z}")
                
                # Calculate Euclidean distance between wrist and middle finger tip
                distance = np.sqrt((wrist.x - middle_finger_tip.x) ** 2 + (wrist.y - middle_finger_tip.y) ** 2)
                # distance_middle_thumb  = np.sqrt((thumb.x - middle_finger_tip.x) ** 2 + (thumb.y - middle_finger_tip.y) ** 2)
                # print(distance)
                jump.append(distance)
                if len(jump) > 2:
                    if jump[-1] <= 0.13:
                        direction_byte = b'\x05'
                        print("jump")
                        client_socket.sendto(direction_byte, server_address)
                        response, server_address = client_socket.recvfrom(1024)
                        print("Received response:", response)

                # print(distance_middle_thumb)
                threshold_middle_wrist = 0.21 
                threshold_thumb_index = 0.095

                # # If the distance is below a certain threshold, consider it as a fist
                # if dis_index_thumb < threshold_thumb_index:  
                #     keyboard.press(Key.space)
                #     # keyboard.press(Key.up)
                # else:
                #     # keyboard.press(Key.up)
                #     keyboard.release(Key.space)
                if prev_landamark:
                    direction_byte = detect_movement(prev=prev_landamark,current=current_landmark,keyboard=keyboard)
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
            # print("FPS:", fps)
            cv2.putText(image, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0, 0), 2)
            frames = 0
            start = time.time()
        
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
        

cap.release()
cv2.destroyAllWindows()
client_socket.close()
