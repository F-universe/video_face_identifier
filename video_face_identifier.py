import face_recognition
import cv2
import dlib
import numpy as np
import pyautogui
import threading
import time
import os

# Configurations
known_image = face_recognition.load_image_file("C:/Users/fabio/OneDrive/Desktop/recorder/person_target.jpg")

known_encoding = face_recognition.face_encodings(known_image)[0]
predictor = dlib.shape_predictor("C:/Users/fabio/OneDrive/Desktop/recorder/shape_predictor_68_face_landmarks (1).dat")
output_directory = "C:/Users/fabio/OneDrive/Desktop/recorder/detected_person"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

is_recording = False

# Function to save frames with detected face
def save_detected_person(original_frame, count):
    filename = f"{output_directory}/person_{count}.jpg"
    cv2.imwrite(filename, original_frame)
    print(f"Frame saved: {filename}")

# Function to detect faces during screen recording
def detect_and_save_faces(frame, count):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    found_match = False

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces([known_encoding], face_encoding)

        if matches[0]:
            found_match = True
            print(f"Matching face found in frame {count}!")
            
            # Save the original frame without rectangles or red points
            save_detected_person(frame, count)

    if not found_match:
        print(f"No matching face found in frame {count}")

# Function to record the screen and detect faces
def record_screen_and_detect_person():
    global is_recording
    is_recording = True
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("screen_recording.avi", fourcc, 20.0, (screen_size.width, screen_size.height))

    count = 0
    while is_recording:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)

        # Detect and save the face if it matches
        detect_and_save_faces(frame, count)
        count += 1
        time.sleep(0.01)  # Reduced to 10 milliseconds for more frequent capturing

    out.release()
    print("Recording completed.")

# Function to start recording
def start_recording():
    global recording_thread
    recording_thread = threading.Thread(target=record_screen_and_detect_person)
    recording_thread.start()

# Function to stop recording
def stop_recording():
    global is_recording
    is_recording = False
    recording_thread.join()

# Start the recording (call this function when you want to start)
start_recording()

# To stop the recording (call this function when you want to stop)
# stop_recording()
