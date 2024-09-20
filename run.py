import subprocess
import time

def start_flask():
    return subprocess.Popen(['python3', 'app.py'])

def start_telegram_bot():
    return subprocess.Popen(['python3', 'bot.py'])

def main():
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

if __name__ == '__main__':
    main()
