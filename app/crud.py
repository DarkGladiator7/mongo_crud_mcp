from .database import get_database
from .models import User
from fastapi import HTTPException
from bson import ObjectId


async def create_user(user: User, db_name: str):
    """
    Inserts a user into MongoDB. Always uses `user.id` as MongoDB _id.
    """
    db = get_database(db_name)
    collection = db["users"]

    doc = user.dict()
    user_id = doc.pop("id", None)  # use your 'id' as _id

    if not user_id:
        raise HTTPException(status_code=400, detail="User id is required")

    # Convert to ObjectId if valid, otherwise keep as string
    _id = ObjectId(user_id) if ObjectId.is_valid(user_id) else str(user_id)
    doc["_id"] = _id

    try:
        result = await collection.insert_one(doc)
        return str(result.inserted_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to insert user: {str(e)}")


async def get_users(db_name: str):
    """
    Returns all users, maps MongoDB _id back to `id`.
    """
    try:
        db = get_database(db_name)
        collection = db["users"]
        users = []

        cursor = collection.find({})
        async for doc in cursor:
            doc["id"] = str(doc["_id"])  # always return 'id'
            doc.pop("_id", None)
            users.append(User(**doc))
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")


async def get_user(user_id: str, db_name: str):
    """
    Fetch a single user by id.
    """
    try:
        db = get_database(db_name)
        collection = db["users"]

        query = {"_id": ObjectId(user_id) if ObjectId.is_valid(user_id) else str(user_id)}
        doc = await collection.find_one(query)
        if doc:
            doc["id"] = str(doc["_id"])
            doc.pop("_id", None)
            return User(**doc)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")


async def update_user(filter_query: dict, update_query: dict, db_name: str):
    """
    Update user(s) based on filter. Always normalize 'id' to '_id'.
    """
    db = get_database(db_name)
    collection = db["users"]

    # Map 'id' in filter to _id
    if "id" in filter_query:
        id_val = filter_query.pop("id")
        filter_query["_id"] = ObjectId(id_val) if ObjectId.is_valid(str(id_val)) else str(id_val)

    try:
        result = await collection.update_one(filter_query, update_query)
        if result.matched_count == 0:
            return None

        updated_doc = await collection.find_one(filter_query)
        if updated_doc:
            updated_doc["id"] = str(updated_doc["_id"])
            updated_doc.pop("_id", None)
        return updated_doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")


async def delete_user(user_id: str, db_name: str):
    """
    Delete a user by id.
    """
    try:
        db = get_database(db_name)
        collection = db["users"]

        query = {"_id": ObjectId(user_id) if ObjectId.is_valid(user_id) else str(user_id)}
        result = await collection.delete_one(query)
        return result.deleted_count > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
