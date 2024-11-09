from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_db():
    mongo_uri = os.getenv("MONGODB_URI", "your_mongodb_uri")
    client = MongoClient(mongo_uri)
    db = client['Kaithia']
    return db

db = connect_to_db()
