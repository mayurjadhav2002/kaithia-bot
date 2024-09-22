## Overview

The project consists of two main components:

- **app.py**: A Flask application that provides endpoints for requesting and verifying OTPs. It creates user's telegram sessions.
- **bot.py**: A script that manages a Telegram group creation. It listens for commands from users and handles creation of group based on those commands.

## Session Creation - `app.py` 

### Endpoints

| Endpoint        | Method | Description                                                               | Request Body                                                                                                             | Response                                                                                          |
|-----------------|--------|---------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `/request_otp`  | POST   | Requests an OTP for a given phone number and updates the backend.       | ```json { "phone_number": "<user_phone_number>", "userId": "<user_id>" } ```                                          | 200 OK: Returns OTP request result.<br>400: Phone number is missing.<br>500: Internal Server Error. |
| `/verify_otp`   | POST   | Verifies the OTP provided by the user and creates a session file.       | ```json { "phone_number": "<user_phone_number>", "otp": "<otp_received>", "phone_code_hash": "<phone_code_hash>", "password": "<optional_password>" } ``` | 200 OK: Returns OTP verification result.<br>400: Required fields are missing.<br>500: Internal Server Error. |


**Session Management** - Upon successful verification of the OTP, a session file is created in the `store` folder. The bot script will monitor this folder, and after one minute of creating the session file, it will restart to create a client for that session.

## Bot Script - `bot.py`

- The bot listens for commands, specifically the `/group` command, which initiates the creation of a group chat.
- It handles incoming messages and executes actions based on user commands.


**Session Handling** The bot script uses a file system observer to watch for newly created session files in the `store` folder. When a new session file is detected, the bot waits for one minute and then attempts to load the client for that session.

## Run Locally

To run the Kaithia Bot locally, follow these steps:

**Step 1: Clone the Project**

```bash
git clone https://github.com/mayurjadhav2002/kaithia -b pybackend
```
**Step 2: Create Virtual Environment**
```bash
python3 -m venv venv

source venv/bin/activate 
```

**Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Step 4: Create `.env` File in root folder**
```env
TELEGRAM_BOT_API_KEY=<your-telegram-bot-api-key>
TELEGRAM_APP_API_ID=<your-telegram-app-api-id>
TELEGRAM_APP_API_HASH=<your-telegram-app-api-hash>
BACKEND_URL=http://<your-backend-url>

```

**Step 5: Run Project**

```bash
python3 run.py
```


