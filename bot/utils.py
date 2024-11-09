from telebot import types

def send_welcome_message(message, full_name):
    welcome_message = (f"<b>Welcome to Kaithia Bot, {full_name}!</b>\n\n"
                       f"Kaithia Bot helps you manage groups and provides useful features.")
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🤝 Join", callback_data="join"))
    markup.add(types.InlineKeyboardButton("❓ Help", callback_data="help"))
    
    bot.send_message(message.chat.id, welcome_message, parse_mode="HTML", reply_markup=markup)
