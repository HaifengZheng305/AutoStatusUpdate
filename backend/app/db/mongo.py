from pymongo.mongo_client import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os


load_dotenv()

MONGO_URI = os.getenv("mongo_uri")
DB_NAME = os.getenv("database")
CONTAINER_COLLECTION = os.getenv("container_collection")

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is missing!")

def get_db_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(MONGO_URI, server_api=ServerApi("1"))

def get_container_collection(client: AsyncIOMotorClient):
    db = client[DB_NAME]
    return db["CONTAINER_COLLECTION"]