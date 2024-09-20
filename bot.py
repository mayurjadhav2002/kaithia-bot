import os
import asyncio
from telethon import TelegramClient, events, functions, types
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_API_KEY')
api_id = os.getenv('TELEGRAM_APP_API_ID')
api_hash = os.getenv('TELEGRAM_APP_API_HASH')

session_dir = 'store'
clients = []


import re

async def check_command(event, client):
    sender = await event.get_sender()

    if event.message.from_id.user_id == sender.id and event.message.text.startswith("/group"):
        try:
            if event.message:
                kaithia_message = await event.message.reply(f"<b>@kaithia_bot</b> is creating the group...", parse_mode='HTML')

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

                created_group = await event.client(functions.messages.CreateChatRequest(
                    title=group_name,
                    users=participants,
                ))
                
                group_details = created_group.stringify()
                
                chat_id_match = re.search(r'peerchat\s*\(\s*chat_id\s*=\s*(\d+)\s*\)', group_details, re.IGNORECASE)
                
                if chat_id_match:
                    chat_id = int(chat_id_match.group(1))
                    
                    await event.client(functions.messages.EditChatAboutRequest(
                        peer=types.PeerChat(chat_id),
                        about="Created by @kaithia_bot"
                    ))

                    result = await client(functions.messages.ExportChatInviteRequest(peer=types.PeerChat(chat_id=chat_id), legacy_revoke_permanent=True))
                    invite_link = result.link
                    
                    
                    await kaithia_message.edit(
                            f"<b>@kaithia_bot</b> created group <b>{group_name}</b> successfully! \n\n Join the group using the link below: {invite_link}",
                            parse_mode='HTML'
                        )

                else:
                    await kaithia_message.edit(
                        f"<b>@Kaithia</b> created group <b>{group_name}</b> successfully!",
                        parse_mode='HTML'
                    )
        except Exception as e:
            print(f"Error creating group: {str(e)}")
            if event.message:
                await event.message.edit(f"Failed to create group: {str(e)}")



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
