from telethon import TelegramClient
import os

class Telegram:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash

    def get_client(self, phone_number):
        session_path = f'store/{phone_number}_session'
        return TelegramClient(session_path, self.api_id, self.api_hash)

    async def request_otp(self, phone_number):
        client = self.get_client(phone_number)
        await client.connect()

        try:
            if not await client.is_user_authorized():
                result = await client.send_code_request(phone_number)
                return {"success": True, "phone_code_hash": result.phone_code_hash}
            else:
                return {"success": False, "message": "Phone number already authorized."}
        finally:
            await client.disconnect()

    async def verify_otp(self, phone_number, otp, phone_code_hash, password=None):
        client = self.get_client(phone_number)
        await client.connect()

        try:
            await client.sign_in(phone_number, otp, phone_code_hash=phone_code_hash)
            return {"success": True, "message": "Successfully signed in."}
        except Exception as e:
            if "password is required" in str(e):
                if not password:
                    return {"success": False, "error": "Password is required for two-step verification."}
                await client.sign_in(phone_number, password=password)
                return {"success": True, "message": "Successfully signed in with password."}
            return {"success": False, "error": "Unexpected error occurred., {}".format(str(e))}
        finally:
            await client.disconnect()

    async def get_phone_number(self, username):
        client = TelegramClient('anon', self.api_id, self.api_hash)
        await client.connect()

        try:
            user = await client.get_entity(username)
            return {"success": True, "phone_number": user.phone}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            await client.disconnect()
