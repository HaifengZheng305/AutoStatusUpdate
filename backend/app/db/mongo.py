from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

print("Connecting to MongoDB...")

MONGO_URI = os.getenv("mongo_uri")
DB_NAME = os.getenv("database")
ContainerCollection = os.getenv("container_collection")

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is missing!")

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise e

db = client[DB_NAME]

def get_container_collection():
    return db["ContainerCollection"]