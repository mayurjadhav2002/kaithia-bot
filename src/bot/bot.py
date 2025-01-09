import os
import asyncio
import logging
from telethon import TelegramClient, events, functions, types
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re
import subprocess
from handlers import Handlers
load_dotenv()

logging.basicConfig(level=logging.INFO)

bot_token = os.getenv('TELEGRAM_BOT_API_KEY')
api_id = os.getenv('TELEGRAM_APP_API_ID')
api_hash = os.getenv('TELEGRAM_APP_API_HASH')

session_dir = 'store'
clients = []

Handler = Handlers()
async def check_command(event, client):
    sender = await event.get_sender()
    me = await client.get_me()

    if sender.id != me.id:
        return
    
    if event.message.text.contains("kaithia") and event.message.to_id.user_id != sender.id:
        await Handler.generate_text(event, sender, client)
    
 
        



async def handle_new_session(session_file):
    logging.info(f"New session file detected: {session_file}. Waiting for 1 minute...")
    
    await asyncio.sleep(60)
    await load_client_for_session(session_file)


typing_timers = {}  

DEBOUNCE_TIME = 2 


async def process_message_after_delay(user_id, message, client):
    """Process the message after a debounce delay."""
    await asyncio.sleep(DEBOUNCE_TIME)  

    modified_message = f"Modified: {message}"

    logging.info(f"Sending modified message to {user_id}: {modified_message}")

    await client.send_message(user_id, modified_message)
    
    
async def load_client_for_session(session_file):
    global clients
    
    session_path = os.path.join(session_dir, session_file)
    logging.info(f"Attempting to load session from: {session_path}")

    client = TelegramClient(session_path, api_id, api_hash)
    try:
        await client.connect()
        
        if not await client.is_user_authorized():
            logging.warning(f"Session for {session_file} is not authorized, login required.")
            await client.disconnect()
            os.remove(session_path)  
            logging.info(f"Deleted unauthorized session file: {session_path}")
            return

        logging.info(f"Session for {session_file} authorized and connected!")

        @client.on(events.NewMessage)
        async def handle_message(event):
            user_id = event.sender_id
            message = event.raw_text
            
            logging.info(f"Received message from {user_id}: {message}")

            if user_id in typing_timers:
                typing_timers[user_id].cancel()

            typing_timers[user_id] = asyncio.create_task(process_message_after_delay(user_id, message, client))

            await check_command(event, client)

        await client.start()
        
        logging.info(f"{session_file} connected successfully!")
        clients.append(client)
        
        
    except Exception as e:
        logging.error(f"Failed to connect {session_file}: {str(e)}")
        await client.disconnect()



# creating new client for each session file in /store folder
async def load_clients():
    session_files = [f for f in os.listdir(session_dir) if f.endswith('_session.session')]
    
    for session_file in session_files:
        await load_client_for_session(session_file)




class SessionFileEventHandler(FileSystemEventHandler):

    def __init__(self, loop):
        self.loop = loop

    def on_created(self, event):
        # file change event tracking
        if event.is_directory or not event.src_path.endswith('_session.session'):
            return
        session_file = os.path.basename(event.src_path)
        asyncio.run_coroutine_threadsafe(handle_new_session(session_file), self.loop)


def start_observer(loop):
    event_handler = SessionFileEventHandler(loop)
    
    observer = Observer()
    observer.schedule(event_handler, path=session_dir, recursive=False)
    observer.start()
    return observer


async def main():
    loop = asyncio.get_event_loop()
    observer = start_observer(loop)
    await load_clients()
    try:
        while True:
            await asyncio.sleep(1)
    finally:
        observer.stop()
        observer.join()




if __name__ == "__main__":
    
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            logging.error(
                f"Error occurred: {str(e)}. Restarting the script...")
            subprocess.run(["python3", "bot.py"])
