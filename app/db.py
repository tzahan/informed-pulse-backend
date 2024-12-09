from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.database_url)

db = client[settings.db_name]#[settings.collection_name]#client["user_db"]
