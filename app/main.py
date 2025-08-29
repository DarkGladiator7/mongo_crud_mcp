from fastapi import FastAPI
from .routes import router

app = FastAPI(title="MCP Mongo CRUD API")

app.include_router(router)

# Run with: uvicorn app.main:app --reload