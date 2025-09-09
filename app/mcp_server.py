# app/mcp_server.py
import asyncio
from fastmcp import FastMCP
from .crud import create_user, get_users, get_user, update_user, delete_user
from .database import list_databases, create_database
from .models import User

# Create MCP server with description
mcp = FastMCP(
    "MongoDB MCP Agent",
    instructions="""
    You are a MongoDB MCP Agent. 
    You have tools to:
    - List all databases
    - Create a database
    - Create a user in a database
    - List users in a database
    - Get a user by ID
    - Update a user using a filter + update style
    - Delete a user by ID

    Always select the most appropriate tool based on the user’s natural language request.
    """
)

# 🗄️ Tool: List Databases
@mcp.tool()
async def list_dbs() -> list[str]:
    """List all available MongoDB databases."""
    return await list_databases()

# 🏗️ Tool: Create Database
@mcp.tool()
async def create_db(db_name: str) -> str:
    """Create a new MongoDB database."""
    success = await create_database(db_name)
    if not success:
        return f"❌ Failed to create database '{db_name}'"
    return f"✅ Database '{db_name}' created successfully"

# ➕ Tool: Create User
@mcp.tool()
async def add_user(db_name: str, name: str, email: str, age: int, id: str | None = None) -> str:
    """Create a new user in the given database."""
    user = User(id=id, name=name, email=email, age=age)
    user_id = await create_user(user, db_name)
    return f"✅ User created with ID {user_id}"

# 📋 Tool: List Users
@mcp.tool()
async def list_users_tool(db_name: str) -> list[dict]:
    """Get all users from a database."""
    users = await get_users(db_name)
    return [u.dict() for u in users]

# 🔍 Tool: Get User
@mcp.tool()
async def read_user_tool(db_name: str, user_id: str) -> dict | str:
    """Get a single user by ID."""
    user = await get_user(user_id, db_name)
    if not user:
        return "❌ User not found"
    return user.dict()

# ✏️ Tool: Update User
@mcp.tool()
async def modify_user(db_name: str, filter: dict, update: dict) -> str:
    """Update user(s) with a filter and update query."""
    updated = await update_user(filter, update, db_name)
    if not updated:
        return "❌ User not found or update failed"
    return f"✅ User updated: {updated.dict()}"

# 🗑️ Tool: Delete User
@mcp.tool()
async def remove_user_tool(db_name: str, user_id: str) -> str:
    """Delete a user by ID."""
    success = await delete_user(user_id, db_name)
    return "✅ User deleted" if success else "❌ User not found"

# Run MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
