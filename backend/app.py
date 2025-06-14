from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db_connection
from models import (
    validate_user,
    register_user,
    add_security,
    get_security_contacts,
    get_criminal_by_face_id
)

from add_criminal import add_criminal
from telegram_alert import send_telegram_alert

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend')))
from detection import load_criminal_encodings

TELEGRAM_BOT_TOKEN = '8117158223:AAFUGkF1VuH7Pda2hq5mktihuu6iLw8dqgw'
TELEGRAM_CHAT_ID = '1539568940'

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({"message": "Vision Guard API is running"})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "fail", "message": "No JSON received"}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"status": "fail", "message": "Missing email or password"}), 400

        user = validate_user(email, password)
        if user:
            return jsonify({"status": "success", "user": user}), 200

        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({"status": "fail", "message": "No JSON received"}), 400

    result = register_user(data)
    return jsonify(result), 200 if result["status"] == "success" else 500

@app.route('/add_criminal', methods=['POST'])
def add_criminal_route():
    data = request.form.to_dict()
    photo = request.files.get('photo')1

    print(f"Received criminal data: {data}")
    print(f"Received file: {photo.filename if photo else 'No file'}")

    if not all([data.get('name'), data.get('age'), data.get('address'), data.get('crimes'), photo]):
        return jsonify({"status": "fail", "message": "All fields are required"})

    result = add_criminal(data, photo)
    print("Add criminal result:", result)
    return jsonify(result)


@app.route('/add_security', methods=['POST'])
def add_security_route():
    data = request.form.to_dict() if request.form else request.json
    if not data:
        return jsonify({"status": "fail", "message": "No data provided"}), 400

    result = add_security(data)
    return jsonify(result)

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    name = data.get("name")
    face_id = data.get("face_id")
    location = data.get("location", "Unknown")
    image_path = data.get("image_path")

    if not all([name, face_id, image_path]):
        return jsonify({"status": "fail", "message": "Missing alert fields"}), 400

    result = send_telegram_alert(
        name=name,
        bot_token=TELEGRAM_BOT_TOKEN,
        chat_id=TELEGRAM_CHAT_ID,
        face_id=face_id,
        location=location,
        image_path=image_path
    )
    return jsonify(result)

@app.route('/profile', methods=['GET'])
def get_profile():
    email = request.args.get("email")
    if not email:
        return jsonify({"status": "fail", "message": "Email is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, email FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()

        if row:
            user = {"name": row[0], "email": row[1]}
            return jsonify({"status": "success", "user": user})
        else:
            return jsonify({"status": "fail", "message": "User not found"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/add_camera', methods=['POST'])
def add_camera():
    data = request.form.to_dict()
    url = data.get("url")
    location = data.get("location")

    if not url or not location:
        return jsonify({"status": "fail", "message": "Missing camera URL or location"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cameras (url, location) VALUES (?, ?)", (url, location))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Camera added successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

