from bot.utils import send_welcome_message
from db.connect import db
from telebot import types
from datetime import datetime

def start_handler(message):
    user = message.from_user
    full_name = f"{user.first_name} {user.last_name or ''}"
    
    send_welcome_message(message, full_name)

    if not db['users'].find_one({"userId": user.id}):
        user_data = {
            "first_name": user.first_name or '',
            "last_name": user.last_name or '',
            "username": user.username or '',
            "userId": user.id,
            "password": None,
            "avatar": "default_avatar_url",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now()
        }
        db['users'].insert_one(user_data)

def help_handler(message):
    help_message = "Help message goes here..."
    bot.send_message(message.chat.id, help_message, parse_mode="HTML")
