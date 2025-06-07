
import os
import sys

backend_path = os.path.abspath(os.path.dirname(__file__))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from database import get_db_connection, execute_query
from detection import load_criminal_encodings

CRIMINAL_IMAGES_PATH = os.path.abspath(os.path.join(backend_path, '..', 'static/criminal_images'))
os.makedirs(CRIMINAL_IMAGES_PATH, exist_ok=True)

def register_user(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        """, (data['name'], data['email'], data['password']))
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def validate_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE email=? AND password=?", (email, password))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "name": row[1], "email": row[2]}
    return None

def add_criminal(name, age, address, crimes, image_path):
    conn = get_db_connection()
    cursor = conn.cursor()

    face_id = name.lower().replace(" ", "_")

    try:
        cursor.execute(
            "INSERT INTO Criminals (name, age, address, crimes, image_path, face_id) VALUES (?, ?, ?, ?, ?, ?)",
            (name, age, address, crimes, image_path, face_id)
        )
        conn.commit()
        return {"status": "success", "face_id": face_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

def add_security(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
              INSERT INTO security_personnel (name, email, chat_id)
              VALUES (?, ?, ?)
        """, (data['name'], data['email'], data['chat_id']))

        conn.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}
  
def get_security_contacts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM security_personnel")
    return [row[0] for row in cursor.fetchall()]


def get_criminal_by_face_id(face_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, age, address, crimes FROM criminals WHERE face_id = ?", (face_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "name": row.name,
            "age": row.age,
            "address": row.address,
            "crimes": row.crimes
        }
    return None
