import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Setup MediaPipe and PyAutoGUI
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
drawing_utils = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Sensitivity settings
cursor_sensitivity = 1.2  # Adjust to control cursor speed/movement sensitivity
click_sensitivity = 40  # Adjust for click sensitivity (increased for better accuracy)
smoothness_factor = 0.85  # Higher means smoother movement

# Initialize positions for smoothing
prev_index_x, prev_index_y = 0, 0
index_x, index_y = 0, 0

# Toggle cursor visibility
cursor_visible = True

# Debounce setup for clicks
last_click_time = 0
click_debounce_interval = 0.3  # Minimum time between clicks (in seconds)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)  # Mirror the frame
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    # Draw landmarks and process hand gestures
    if hands:
        hand = hands[0]  # Process only one hand for simplicity
        drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

        landmarks = hand.landmark

        # Track index finger for cursor position (id == 8)
        index_finger = landmarks[8]
        x = int(index_finger.x * frame_width)
        y = int(index_finger.y * frame_height)

        # Apply smooth movement by interpolating between previous and current positions
        index_x = smoothness_factor * prev_index_x + (1 - smoothness_factor) * (screen_width / frame_width * x)
        index_y = smoothness_factor * prev_index_y + (1 - smoothness_factor) * (screen_height / frame_height * y)

        prev_index_x, prev_index_y = index_x, index_y  # Update previous positions

        if cursor_visible:
            cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)

        # Move cursor smoothly
        pyautogui.moveTo(index_x * cursor_sensitivity, index_y * cursor_sensitivity)

        # Track thumb for clicking (id == 4)
        thumb = landmarks[4]
        thumb_x = screen_width / frame_width * int(thumb.x * frame_width)
        thumb_y = screen_height / frame_height * int(thumb.y * frame_height)

        if abs(index_y - thumb_y) < click_sensitivity:
            current_time = time.time()
            if current_time - last_click_time > click_debounce_interval:
                pyautogui.click()
                last_click_time = current_time

    # Toggle cursor visibility with 'v' key
    if cv2.waitKey(1) & 0xFF == ord('v'):
        cursor_visible = not cursor_visible

    # Exit command with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('Virtual Mouse', frame)

cap.release()
cv2.destroyAllWindows()
