import os
import sys
from datetime import datetime
from werkzeug.utils import secure_filename

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from detection import load_criminal_encodings
from database import get_connection

CRIMINAL_IMAGES_FOLDER = os.path.join('static', 'criminal_images')

def add_criminal(data, photo_file):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if not os.path.exists(CRIMINAL_IMAGES_FOLDER):
            os.makedirs(CRIMINAL_IMAGES_FOLDER)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S') #e.g., 20250611123000
        original_filename = secure_filename(photo_file.filename)
        _, ext = os.path.splitext(original_filename)
        filename = f"{data['name'].replace(' ', '_')}_{timestamp}{ext}" #shivprasad_mali_20250611123000.jpg
        filepath = os.path.join(CRIMINAL_IMAGES_FOLDER, filename)

        photo_file.save(filepath)

        cursor.execute("""
            INSERT INTO criminals (name, age, address, crimes, image_path)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data['name'],
            int(data['age']),
            data['address'],
            data['crimes'],
            filepath
        ))
        conn.commit()

        load_criminal_encodings()

        return {"status": "success"}

    except Exception as e:
        return {"status": "fail", "message": str(e)}

    finally:
        conn.close()

#summary:

# Saves a criminal’s photo with a unique filename.
# Stores their details and image path in a database.
# Updates face encodings used for real-time recognition.
# Handles errors gracefully and ensures cleanup.
