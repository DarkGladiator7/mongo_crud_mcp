from .database import get_database
from .models import User
from bson import ObjectId
from fastapi import HTTPException


async def create_user(user: User, db_name: str):
    db = get_database(db_name)
    collection = db["users"]

    doc = user.dict()
    user_id = doc.pop("id", None)

    try:
        if user_id:  # user gave custom id
            _id = ObjectId(user_id) if ObjectId.is_valid(user_id) else str(user_id)
            doc["_id"] = _id
            result = await collection.insert_one(doc)
            return str(result.inserted_id)
        else:  # mongo generates id
            result = await collection.insert_one(doc)
            return str(result.inserted_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to insert user: {str(e)}")


async def get_users(db_name: str):
    try:
        db = get_database(db_name)
        collection = db["users"]
        users = []
        cursor = collection.find({})
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            users.append(User(**doc))
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")


async def get_user(user_id: str, db_name: str):
    try:
        db = get_database(db_name)
        collection = db["users"]
        query = {"_id": ObjectId(user_id)} if ObjectId.is_valid(user_id) else {"_id": str(user_id)}
        doc = await collection.find_one(query)
        if doc:
            doc["id"] = str(doc["_id"])
            return User(**doc)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")


async def update_user(filter_query: dict, update_query: dict, db_name: str):
    db = get_database(db_name)
    collection = db["users"]

    # Normalize _id if present
    if "_id" in filter_query:
        id_val = filter_query["_id"]
        if ObjectId.is_valid(str(id_val)):
            filter_query["_id"] = ObjectId(str(id_val))
        else:
            filter_query["_id"] = str(id_val)

    try:
        result = await collection.update_one(filter_query, update_query)

        if result.matched_count == 0:
            return None

        updated_doc = await collection.find_one(filter_query)
        if updated_doc:
            updated_doc["id"] = str(updated_doc["_id"])
        return updated_doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")


async def delete_user(user_id: str, db_name: str):
    try:
        db = get_database(db_name)
        collection = db["users"]
        query = {"_id": ObjectId(user_id)} if ObjectId.is_valid(user_id) else {"_id": str(user_id)}
        result = await collection.delete_one(query)
        return result.deleted_count > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
