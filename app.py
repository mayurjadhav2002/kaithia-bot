from flask import Flask, request, jsonify
from src.Telegram import Telegram
import os
import requests
import asyncio
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()


api_id = os.getenv('TELEGRAM_APP_API_ID')
api_hash = os.getenv('TELEGRAM_APP_API_HASH')
node_backend = os.getenv('BACKEND_URL')
telegram_service = Telegram(api_id, api_hash)


app = Flask(__name__)
CORS(app)



async def update_backend_with_phone(userId, phone_number):
    try:
        response = requests.post(f"{node_backend}/api/update_phone", json={"userId": userId, "phone_number": phone_number})
        return response.json()
    except Exception as e:
        return {"success": False, "message": "Error updating backend"}




@app.route('/request_otp', methods=['POST'])
async def request_otp():
    phone_number = request.json.get('phone_number')
    userId = request.json.get('userId')
    if not phone_number:
        return jsonify({"error": "Phone number is required."}), 400

    try:
        result = await telegram_service.request_otp(phone_number)
        await update_backend_with_phone(userId, phone_number)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success": False, "message": "Internal Server Error", "error": str(e)}), 500



@app.route('/verify_otp', methods=['POST'])
async def verify_otp():
    phone_number = request.json.get('phone_number')
    otp = request.json.get('otp')
    phone_code_hash = request.json.get('phone_code_hash')
    password = request.json.get('password')

    if not phone_number or not otp or not phone_code_hash:
        return jsonify({"error": "Phone number, OTP, and phone_code_hash are required."}), 400

    try:
        result = await telegram_service.verify_otp(phone_number, otp, phone_code_hash, password)
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"Error verifying OTP: {str(e)}")
        return jsonify({"error": f"Error verifying OTP: {str(e)}", "success": False}), 500




@app.route("/", methods=['GET'])
def index():
    return jsonify({"success": True, "message": "Hello, World!"}), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
