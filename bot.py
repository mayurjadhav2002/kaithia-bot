import os
import asyncio
from telethon import TelegramClient, events, functions
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_API_KEY')
api_id = os.getenv('TELEGRAM_APP_API_ID')
api_hash = os.getenv('TELEGRAM_APP_API_HASH')

session_dir = 'store'
clients = []


async def check_command(event, client):
    sender = await event.get_sender()

    if event.message.from_id.user_id == sender.id and event.message.text.startswith("/group"):
        try:
            if event.message:
                await event.message.edit("Kaithia is creating the group...")

                recipient_id = event.message.to_id.user_id
                recipient = await event.client.get_entity(recipient_id)
                recipient_first_name = getattr(recipient, 'first_name', None)

                command_parts = event.message.text.split(" ", 1)
                group_name = command_parts[1] if len(command_parts) > 1 else f"{sender.first_name} & {recipient_first_name}"

                participants = [sender, recipient, "@kaithia_bot"]

                created_group = await event.client(functions.messages.CreateChatRequest(
                    title=group_name,
                    users=participants
                ))

                await event.message.edit(f"Kaithia Created Group '{group_name}' successfully!")

        except Exception as e:
            print(f"Error creating group: {str(e)}")
            if event.message:
                await event.message.edit(f"Failed to create group: {str(e)}")
    else:
        print(f"Command not triggered: {event.message.text} from {sender.id}")


async def load_clients():
    session_files = [f for f in os.listdir(session_dir) if f.endswith('_session.session')]
    for session_file in session_files:
        session_path = os.path.join(session_dir, session_file)
        print(f"Attempting to load session from: {session_path}") 
        
        client = TelegramClient(session_path, api_id, api_hash)
        
        try:
            await client.connect()  

            if not await client.is_user_authorized():
                print(f"Session for {session_file} is not authorized, login required.")
                await client.disconnect()
                continue
            else:
                print(f"Session for {session_file} authorized and connected!")

            @client.on(events.NewMessage)
            async def handle_message(event):
                await check_command(event, client)

            await client.start() 
            print(f"{session_file} connected successfully!")  
            clients.append(client)

        except Exception as e:
            print(f"Failed to connect {session_file}: {str(e)}")
            await client.disconnect() 



async def main():
    await load_clients()
    await asyncio.gather(*[client.run_until_disconnected() for client in clients])

if __name__ == "__main__":
    asyncio.run(main())
