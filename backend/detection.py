import face_recognition
import os
import cv2
import requests


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
DETECTED_DIR = os.path.join(BASE_DIR, '..', 'static', 'detected')
os.makedirs(DETECTED_DIR, exist_ok=True) 

CRIMINAL_IMAGES_PATH = "static/criminal_images"
ALERT_IMAGE_SAVE_PATH = "static/detected"

TELEGRAM_ALERT_URL = "http://127.0.0.1:5000/alert"  

known_encodings = []
known_names = []

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.database import get_db_connection

def get_criminal_name_by_filename(filename):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM Criminals WHERE image_path = ?", filename)
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]  
    return filename.split('.')[0] 


def load_criminal_encodings():
    known_encodings.clear()
    known_names.clear()
    print("🔍 Loading known criminal images...")

    for filename in os.listdir(CRIMINAL_IMAGES_PATH):
        if filename.lower().endswith((".jpg", ".png")):
            path = os.path.join(CRIMINAL_IMAGES_PATH, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                name = get_criminal_name_by_filename(filename)
                known_encodings.append(encodings[0])
                known_names.append(name)
                print(f"[✓] Loaded: {filename} as {name}")
            else:
                print(f"[x] No face found in: {filename}")


def send_criminal_alert(name, face_id, frame):
    try:
        os.makedirs(ALERT_IMAGE_SAVE_PATH, exist_ok=True)
        image_filename = f"{name}.jpg"
        image_path = os.path.join(DETECTED_DIR, image_filename)

        success = cv2.imwrite(image_path, frame)
        if success:
            print(f"✅ Frame saved: {image_path}")
        else:
            print(f"❌ Failed to save frame: {image_path}")

        relative_image_path = f"static/detected/{image_filename}"
        
        # Send alert to backend
        response = requests.post(TELEGRAM_ALERT_URL, json={
            "name": name,
            "face_id": face_id,
            "location": "Web Camera",
            "image_path": relative_image_path
        })

        try:
            print("📨 Alert sent to Telegram:", response.json())
        except Exception:
            print("❌ Failed to parse response as JSON:", response.text)

    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

def detect_criminal(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
     
    print(f"👁️ Detected {len(face_encodings)} face(s) in current frame.")

    matches = []
    for face_encoding, location in zip(face_encodings, face_locations):
        results = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
        print("   ➜ Match results:", results)

        if True in results:
            match_index = results.index(True)
            name = known_names[match_index]
            face_id = name.lower().replace(" ", "_") 
            matches.append(name)

            send_criminal_alert(name, face_id, frame)

    return matches
