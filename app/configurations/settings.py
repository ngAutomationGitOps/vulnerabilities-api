from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.getenv("ENV")
DATABASE_URL = os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
