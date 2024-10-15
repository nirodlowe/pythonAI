import cv2
import face_recognition
import mediapipe as mp

# Initialize Mediapipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Open a video capture (0 for webcam)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Convert the frame from BGR (OpenCV format) to RGB (face_recognition format)
    rgb_frame = frame[:, :, ::-1]

    # Detect faces in the frame using face_recognition
    face_locations = face_recognition.face_locations(rgb_frame)

    # For each detected face, draw a rectangle
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Process the frame using Mediapipe FaceMesh for facial landmarks
    results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Draw face landmarks if detected
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

    # Display the frame with rectangles and landmarks
    cv2.imshow('Face Recognition + Mediapipe', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
