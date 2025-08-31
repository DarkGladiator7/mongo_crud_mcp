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

async def create_database(db_name: str):
    """
    Create a new MongoDB database by inserting a dummy document.
    Prevents duplicate creation if DB already exists.
    """
    try:
        existing_dbs = await client.list_database_names()
        if db_name in existing_dbs:
            return {"success": False, "message": f"Database '{db_name}' already exists"}

        db = client[db_name]
        await db["init_collection"].insert_one({"created": True})
        return {"success": True, "message": f"Database '{db_name}' created successfully"}
    except Exception as e:
        return {"success": False, "message": f"Error creating database: {str(e)}"}