from flask import Blueprint, request, jsonify, Flask
from src.Telegram import Telegram
import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

api_id = os.getenv('TELEGRAM_APP_API_ID')
api_hash = os.getenv('TELEGRAM_APP_API_HASH')
bot_key= os.getenv('TELEGRAM_BOT_API_KEY')
telegram_service = Telegram( api_id, api_hash)



app = Flask(__name__)
CORS(app)

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)



@app.route('/request_otp', methods=['POST'])
def request_otp():
    phone_number = request.json.get('phone_number')
    if not phone_number:
        return jsonify({"error": "Phone number is required."}), 400

    try:
        result = run_async(telegram_service.request_otp(phone_number))
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success": False, "message": "Internal Server Error", "error": str(e)}), 500

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    phone_number = request.json.get('phone_number')
    otp = request.json.get('otp')
    phone_code_hash = request.json.get('phone_code_hash')
    password = request.json.get('password')

    if not phone_number or not otp or not phone_code_hash:
        return jsonify({"error": "Phone number, OTP, and phone_code_hash are required."}), 400

    try:
        result = run_async(telegram_service.verify_otp(phone_number, otp, phone_code_hash, password))
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Error verifying OTP: {str(e)}", "success": False}), 500




@app.route("/", methods=['GET'])
def index():
    return jsonify({"success": True, "message": "Hello, World!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
