from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URL)

async def list_databases():
    """Return list of available databases in MongoDB."""
    return await client.list_database_names()

def get_database(db_name: str):
    """Return a MongoDB database handle."""
    return client[db_name]