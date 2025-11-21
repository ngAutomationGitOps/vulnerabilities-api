from pymongo import MongoClient
from dotenv import load_dotenv
import os


def get_db():
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME")

    client = MongoClient(mongo_uri)
    return client[db_name]
