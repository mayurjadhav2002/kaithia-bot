from datetime import datetime
from db.connect import db
import bcrypt
import os

default_avatar = f"{os.getenv('BACKEND_URL')}/uploads/default.png"

class User:
    def __init__(self, first_name, user_id, last_name=None, username=None, phone_number=None, password=None,
                 avatar=default_avatar, password_reset="", password_reset_token="", date="", 
                 has_session=False, phone_code_hash=""):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.phone_number = phone_number
        self.user_id = user_id
        self.password = self.hash_password(password) if password else None
        self.avatar = avatar
        self.password_reset = password_reset
        self.password_reset_token = password_reset_token
        self.date = date
        self.has_session = has_session
        self.phone_code_hash = phone_code_hash
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def hash_password(self, password):
        """Hash the password."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def authenticate(self, password):
        """Authenticate user by comparing the stored and given password."""
        if self.password:
            return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        return False

    def save(self):
        user_data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "phone_number": self.phone_number,
            "userId": self.user_id,
            "password": self.password,
            "avatar": self.avatar,
            "password_reset": self.password_reset,
            "password_reset_token": self.password_reset_token,
            "date": self.date,
            "hasSession": self.has_session,
            "phone_code_hash": self.phone_code_hash,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }
        db['users'].insert_one(user_data)

    @staticmethod
    def find_one(query):
        """Find a single user by query."""
        return db['users'].find_one(query)

    def update_timestamp(self):
        """Update the timestamp when user data is modified."""
        self.updated_at = datetime.now()
