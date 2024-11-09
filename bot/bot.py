import os
import asyncio
import logging
from telethon import TelegramClient, events, functions, types
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re
import subprocess

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot_token = os.getenv('TELEGRAM_BOT_API_KEY')
api_id = os.getenv('TELEGRAM_APP_API_ID')
api_hash = os.getenv('TELEGRAM_APP_API_HASH')

session_dir = 'store'
clients = []


async def check_command(event, client):
    sender = await event.get_sender()
    me = await client.get_me()

    if sender.id != me.id:
        return

    if event.message.text.startswith("/group") and event.message.to_id.user_id != sender.id:
        try:
            
            kaithia_message = await event.message.edit(
                f"<b>@kaithia_bot</b> is creating the <code>/group</code>...",
                parse_mode='HTML')

            command_parts = event.message.text.split(" ", 1)

            group_command = command_parts[1] if len(command_parts) > 1 else ""
            add_kaithia = "@kaithia" in group_command
            group_command = group_command.replace("@kaithia", "").strip()

            recipient_id = event.message.to_id.user_id
            recipient = await event.client.get_entity(recipient_id)
            recipient_first_name = getattr(recipient, 'first_name', None)

            group_name = group_command if group_command else f"{sender.first_name} <> {recipient_first_name}"
            participants = [sender, recipient]

            if add_kaithia:
                participants.append("@kaithia_bot")

            created_group = await event.client(
                functions.messages.CreateChatRequest(title=group_name,
                                                     users=participants))
            group_details = created_group.stringify()
            
            chat_id_match = re.search(r'peerchat\s*\(\s*chat_id\s*=\s*(\d+)\s*\)', group_details, re.IGNORECASE)
            
            if chat_id_match:
                chat_id = int(chat_id_match.group(1))
                await event.client(functions.messages.EditChatAboutRequest(
                        peer=types.PeerChat(chat_id),
                        about="Created by @kaithia_bot"
                        ))
                
                result = await client(functions.messages.ExportChatInviteRequest(
                        peer=types.PeerChat(chat_id=chat_id),
                        legacy_revoke_permanent=True
                        )) 
                invite_link = result.link
                
                await kaithia_message.edit(f"<b>@kaithia_bot</b> created group <b>{group_name}</b> successfully! \n\n Join the group using the link below: {invite_link}", parse_mode='HTML')
           
            else:
                await kaithia_message.edit(
                    f"<b>@Kaithia</b> created group <b>{group_name}</b> successfully!",
                    parse_mode='HTML')
        except Exception as e:
            logging.error(f"Error creating group: {str(e)}")
            if event.message:
                await event.message.edit(f"Failed to create group: {str(e)}")


# it handles new session file created by Flask app
async def handle_new_session(session_file):
    logging.info(f"New session file detected: {session_file}. Waiting for 1 minute...")
    
    await asyncio.sleep(60)
    await load_client_for_session(session_file)


typing_timers = {}  # Store timers per user to handle debouncing

DEBOUNCE_TIME = 2 
# It checks for new session file and loads the client
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
