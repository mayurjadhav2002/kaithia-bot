from gemini_handlers import BotOperation

import logging

gemini = BotOperation()

class Handlers:
    def __init__(self):
        self.bot_operation = BotOperation()

    
    async def generate_text(self, event, sender, client):
        try:
            kaithia_message = await event.edit(
                "<b>@kaithia_bot</b> is working...",
                parse_mode='HTML'
            )
            
            command_parts = event.message.text.split(" ", 1)
            message_to_generate = command_parts[1] if len(command_parts) > 1 else ""
            
            generated_result = self.bot_operation.Generative(message_to_generate)
            if generated_result:
                
                logging.info(f"Generated result: {generated_result}")
                match generated_result.lower():
                    case "this is a group operation.":
                        logging.info("Creating group...")
                        await self.createGroup(event, sender, client)
                        return
                    case _:
                        logging.info(f"Generated text: {generated_result}")
                        await kaithia_message.edit(generated_result, parse_mode='markdown')
                
            else:
                await kaithia_message.edit("Failed to generate text: No response from the model.", parse_mode='markdown')
                
        except Exception as e:
            logging.error(f"Error generating text: {str(e)}")
            await event.edit(f"Failed to generate text: {str(e)}")


    @staticmethod 
    async def createGroup(self, event, sender, client):
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