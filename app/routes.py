from fastapi import APIRouter, HTTPException, Query
from .crud import create_user, get_users, get_user, update_user, delete_user
from .database import list_databases, create_database
from .models import User, DBRequest

router = APIRouter()


@router.get("/databases")
async def get_databases():
    try:
        return await list_databases()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing databases: {str(e)}")


@router.post("/databases")
async def add_database(request: DBRequest):
    try:
        created = await create_database(request.db_name)
        if not created:
            raise HTTPException(400, f"Database '{request.db_name}' could not be created")
        return {"message": f"Database '{request.db_name}' created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating database: {str(e)}")


@router.post("/users")
async def add_user(user: User, db_name: str = Query(..., description="Database name")):
    return {"id": await create_user(user, db_name)}


@router.get("/users")
async def list_users(db_name: str = Query(..., description="Database name")):
    return await get_users(db_name)


@router.get("/users/{user_id}")
async def read_user(user_id: str, db_name: str = Query(..., description="Database name")):
    user = await get_user(user_id, db_name)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.put("/users/{user_id}")
async def edit_user(
    user_id: str,
    payload: dict,
    db_name: str = Query(..., description="Database name")
):
    """
    Update user dynamically using filter + update style.
    Example:
    {
        "filter": {"_id": "123"},
        "update": {"$set": {"name": "new_name"}}
    }
    """

    filter_query = payload.get("filter", {})
    update_query = payload.get("update")

    if not update_query:
        raise HTTPException(400, "Missing 'update' field in request body")

    # fallback to path param if filter has no _id
    if "_id" not in filter_query:
        filter_query["_id"] = user_id

    updated = await update_user(filter_query, update_query, db_name)
    if not updated:
        raise HTTPException(404, f"User with filter {filter_query} not found")

    return {"message": "User updated successfully", "user": updated}



@router.delete("/users/{user_id}")
async def remove_user(user_id: str, db_name: str = Query(..., description="Database name")):
    success = await delete_user(user_id, db_name)
    if not success:
        raise HTTPException(404, "User not found")
    return {"deleted": True}
