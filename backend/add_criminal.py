import os
import sys
from datetime import datetime
from werkzeug.utils import secure_filename

# Add backend folder to path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import required logic
from detection import load_criminal_encodings
from models import add_criminal as insert_criminal_into_db  # handles DB insert

# Image folder
CRIMINAL_IMAGES_FOLDER = os.path.join('static', 'criminal_images')

def add_criminal(data, photo_file):
    try:
        print("[DEBUG] add_criminal called")

        # Validate photo presence
        if not photo_file:
            print("[ERROR] photo_file is None")
            return {"status": "fail", "message": "No file uploaded"}

        print(f"[DEBUG] Received file: {photo_file.filename}")
        if photo_file.filename == '':
            print("[ERROR] Empty filename")
            return {"status": "fail", "message": "Empty filename"}

        # Validate file extension
        _, ext = os.path.splitext(photo_file.filename)
        if ext.lower() not in ['.jpg', '.jpeg', '.png']:
            print("[ERROR] Invalid file type:", ext)
            return {"status": "fail", "message": "Unsupported file type"}

        # Create image folder if it doesn't exist
        if not os.path.exists(CRIMINAL_IMAGES_FOLDER):
            os.makedirs(CRIMINAL_IMAGES_FOLDER)
            print(f"[DEBUG] Created folder: {CRIMINAL_IMAGES_FOLDER}")
        else:
            print(f"[DEBUG] Folder already exists: {CRIMINAL_IMAGES_FOLDER}")

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = secure_filename(f"{data['name'].replace(' ', '_')}_{timestamp}{ext}")
        filepath = os.path.join(CRIMINAL_IMAGES_FOLDER, filename)

        print(f"[DEBUG] Saving to filepath: {filepath}")
        photo_file.save(filepath)

        if not os.path.exists(filepath):
            print("[ERROR] File not saved!")
            return {"status": "fail", "message": "File save failed"}

        print("[DEBUG] File saved successfully.")

        # Save to database
        result = insert_criminal_into_db(
            data['name'],
            int(data['age']),
            data['address'],
            data['crimes'],
            filepath
        )

        # Reload encodings after adding new face
        load_criminal_encodings()

        return result

    except Exception as e:
        print("[EXCEPTION]", str(e))
        return {"status": "fail", "message": str(e)}
