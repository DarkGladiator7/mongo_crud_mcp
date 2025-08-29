from fastapi import APIRouter, HTTPException, Query
from .crud import create_user, get_users, get_user, update_user, delete_user
from .database import list_databases
from .models import User

router = APIRouter()

@router.get("/databases")
async def get_databases():
    return await list_databases()

@router.post("/users")
async def add_user(user: User, db_name: str = Query(..., description="Database name")):
    user_id = await create_user(user, db_name)
    return {"id": user_id}

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
async def edit_user(user_id: str, user: User, db_name: str = Query(..., description="Database name")):
    updated = await update_user(user_id, user, db_name)
    if not updated:
        raise HTTPException(404, "User not found")
    return updated

@router.delete("/users/{user_id}")
async def remove_user(user_id: str, db_name: str = Query(..., description="Database name")):
    success = await delete_user(user_id, db_name)
    if not success:
        raise HTTPException(404, "User not found")
    return {"deleted": True}
