import cv2
import face_recognition
import numpy as np
import csv
from datetime import datetime
import os
import sys

# ✅ Get the base directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Helper function to get face encoding
def get_face_encoding(image_path):
    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            return encodings[0]
        else:
            print(f"⚠️ No face found in {image_path}")
            return None
    except Exception as e:
        print(f"❌ Error loading {image_path}: {e}")
        return None

# ✅ Match your actual image filenames here
faces = {
    "Anas": os.path.join(BASE_DIR, "faces", "anas.jpg"),
    "Ronaldo": os.path.join(BASE_DIR, "faces", "Ronaldo.jpg"),
    "SRK": os.path.join(BASE_DIR, "faces", "srk.jpg"),
    "Virat Kohli": os.path.join(BASE_DIR, "faces", "virat kohli.jpg")
}

known_face_encodings = []
known_face_names = []

# ✅ Load all encodings
for name, path in faces.items():
    encoding = get_face_encoding(path)
    if encoding is not None:
        known_face_encodings.append(encoding)
        known_face_names.append(name)

if len(known_face_encodings) == 0:
    print("❌ No valid face encodings found. Exiting.")
    sys.exit(1)

students = known_face_names.copy()

# ✅ Access webcam
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("❌ Error: Cannot access webcam.")
    sys.exit(1)

# ✅ Prepare attendance file
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)
lnwriter.writerow(["SR.NO", "Name", "Time"])

serial_number = 1

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Failed to grab frame from webcam.")
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.9)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            print("Detected:", name)

            top, right, bottom, left = location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.9, (255, 255, 255), 2)

            if name in students:
                print("Attendance for", name, "recorded.")
                students.remove(name)
                current_time = datetime.now().strftime("%H:%M:%S")
                lnwriter.writerow([serial_number, name, current_time])
                serial_number += 1

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ✅ Clean up
video_capture.release()
cv2.destroyAllWindows()
f.close()
