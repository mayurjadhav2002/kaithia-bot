import subprocess
import time
import os
from telebot import TeleBot, types
from db.connect import db 
from datetime import datetime
import bcrypt
import signal
import sys

bot = TeleBot(os.getenv("TELEGRAM_BOT_API_KEY"))

default_avatar = f"{os.getenv('BACKEND_URL')}/uploads/default.png"

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def authenticate(stored_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))

def find_user(query):
    return db['users'].find_one(query)

def save_user(user_data):
    user_data["createdAt"] = datetime.now()
    user_data["updatedAt"] = datetime.now()
    db['users'].insert_one(user_data)

@bot.message_handler(commands=['start'])
def start_handler(message):
    user = message.from_user
    full_name = f"{user.first_name} {user.last_name or ''}"
    welcome_message = (f"<b>Welcome to Kaithia Bot, {full_name}!</b>\n\n"
                       f"Kaithia Bot helps you manage groups and provides useful features to enhance your Telegram experience. "
                       f"Here are the commands you can use:\n\n"
                       f"Enjoy using Kaithia Bot!")

    if not find_user({"userId": user.id}):
        user_data = {
            "first_name": user.first_name or '',
            "last_name": user.last_name or '',
            "username": user.username or '',
            "userId": user.id,
            "password": None,
            "avatar": default_avatar,
            "password_reset": "",
            "password_reset_token": "",
            "date": "",
            "hasSession": False,
            "phone_code_hash": ""
        }
        save_user(user_data)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🤝 Join", callback_data="join"))
    markup.add(types.InlineKeyboardButton("❓ Help", callback_data="help"))
    
    bot.send_message(message.chat.id, welcome_message, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "join")
def join_handler(call):
    user_id = call.from_user.id
    join_url = f"https://kaithia.vercel.app?u={user_id}"
    full_name = f"{call.from_user.first_name or 'explorer'} {call.from_user.last_name or ''}"

    join_message = (f"✅ Great to see you onboard, {full_name}! You can easily connect with others and explore all the features of Kaithia Bot.\n\n"
                    f"Open Link to Sign Up: [Join Here]({join_url})")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🌐 Open Link", url=join_url))

    bot.send_message(call.message.chat.id, join_message, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "help")
@bot.message_handler(commands=['help'])
def help_handler(message):
    help_message = (f"🆘 Understanding Kaithia. Here are the instructions:\n\n"
                    f"👋 <b>/start</b> - Initialize or start Kaithia Bot.\n\n"
                    f"🤝 <b>/join</b> - Opens a sign-up window.\n\n"
                    f"👥 <b>/group [groupname]</b> - Create a group.\n\n"
                    f"❓ <b>/help</b> - Get information about the available commands.\n\n"
                    f"🔒 <b>/security</b> - Learn about data and security.\n\n"
                    f"Need further assistance? Reach out to <b>@mayur8908</b>")

    bot.send_message(message.chat.id, help_message, parse_mode="HTML")

@bot.message_handler(commands=['security'])
def security_handler(message):
    security_message = (f"<b>Security and Data Usage</b>\n\n"
                        f"At Kaithia Bot, we take your privacy and security seriously:\n\n"
                        f"<b>Phone Number, OTP, and 2FA:</b> Required but not stored.\n\n"
                        f"<b>Basic Information:</b> We store your username, first name, and last name.\n\n"
                        f"<b>Message Listening:</b> Kaithia Bot listens to your messages but does not store them.\n\n"
                        f"<b>Security and Infrastructure:</b> Our services are highly secured.")

    bot.send_message(message.chat.id, security_message, parse_mode="HTML")

@bot.message_handler(commands=['join'])
def join_command_handler(message):
    join_url = f"https://kaithia.vercel.app?u={message.from_user.id}"
    join_message = f"✅ You have chosen to join! Access the link here: [Join Here]({join_url})"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🌐 Open Link", url=join_url))

    bot.send_message(message.chat.id, join_message, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.lower() == 'hi')
def hi_handler(message):
    bot.send_message(message.chat.id, "👋 Hey there!")

def shutdown(signum, frame):
    bot.stop_polling()
    sys.exit(0)

def start_flask():
    return subprocess.Popen(['python', 'bot/api.py'])

def start_telegram_bot():
    return subprocess.Popen(['python', 'bot/bot.py'])

def main():
    
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    bot.polling()
    
   
if __name__ == '__main__':

    flask_app = start_flask()
    telegram_app = start_telegram_bot()

    while True:
        if flask_app.poll() is not None: 
            print('Flask app exited. Restarting...')
            flask_app = start_flask()
        
        if telegram_app.poll() is not None:
            print('Telegram bot exited. Restarting...')
            telegram_app = start_telegram_bot()
        
        time.sleep(1)
    main()