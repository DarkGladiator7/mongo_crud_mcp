from .database import get_database
from .models import User
from bson import ObjectId

async def create_user(user: User, db_name: str):
    db = get_database(db_name)
    collection = db["users"]

    doc = user.dict()
    user_id = doc.pop("id", None)  # remove id from dict if present

    if user_id:  # user provided id
        try:
            # Use provided ID (convert to ObjectId if it looks like one)
            _id = ObjectId(user_id) if ObjectId.is_valid(user_id) else user_id
            doc["_id"] = _id
            result = await collection.insert_one(doc)
            return str(result.inserted_id)
        except Exception as e:
            raise Exception(f"Failed to insert with custom id: {e}")
    else:  # no id -> let Mongo generate one
        result = await collection.insert_one(doc)
        return str(result.inserted_id)

async def get_users(db_name: str):
    db = get_database(db_name)
    collection = db["users"]
    users = []
    cursor = collection.find({})
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        users.append(User(**doc))
    return users

async def get_user(user_id: str, db_name: str):
    db = get_database(db_name)
    collection = db["users"]
    doc = await collection.find_one({"_id": ObjectId(user_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        return User(**doc)
    return None

async def update_user(user_id: str, user: User, db_name: str):
    db = get_database(db_name)
    collection = db["users"]
    await collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict(exclude={"id"})})
    return await get_user(user_id, db_name)

async def delete_user(user_id: str, db_name: str):
    db = get_database(db_name)
    collection = db["users"]

    query = {"_id": ObjectId(user_id)} if ObjectId.is_valid(user_id) else {"_id": user_id}
    result = await collection.delete_one(query)

    return result.deleted_count > 0
