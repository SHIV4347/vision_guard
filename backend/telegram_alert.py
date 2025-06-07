import re
import requests
from database import get_db_connection
from models import get_criminal_by_face_id

def escape_markdown(text):
    escape_chars = r'([_*\[\]()~`>#+=|{}.!\\-])'
    return re.sub(escape_chars, r'\\\1', text)

def send_telegram_alert(name,bot_token, chat_id, face_id, location, image_path):
    try:

        criminal = get_criminal_by_face_id(face_id)
        if not criminal:
            print(f"⚠️ No criminal found with face_id: {face_id}")
            return {"status": "fail", "error": "Criminal not found in database"}

        caption = (
            f"🚨 *Criminal Detected\\!*\n"
            f"👤 *Name*: {escape_markdown(criminal['name'])}\n"
            f"🎂 *Age*: {escape_markdown(str(criminal['age']))}\n"
            f"🏠 *Address*: {escape_markdown(criminal['address'])}\n"
            f"⚖️ *Crimes*: {escape_markdown(criminal['crimes'])}\n"
            f"📍 *Location*: {escape_markdown(location)}"
        )

        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {
                'chat_id': chat_id,
                'caption': caption,
                'parse_mode': 'MarkdownV2'
            }
            url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
            response = requests.post(url, files=files, data=data)
            return response.json()

    except Exception as e:
        print(f"❌ Telegram alert failed: {e}")
        return {"status": "fail", "error": str(e)}
