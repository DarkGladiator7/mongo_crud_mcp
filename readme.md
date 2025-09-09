🚀 MCP Mongo Multi-DB CRUD + LLM Agent

This project is a MongoDB CRUD system with multi-database support, powered by FastMCP.

It allows you to:

Connect to multiple MongoDB databases

Perform CRUD operations on users via tools

Create databases dynamically

Interact with the system using CLI commands, with the LLM agent selecting the appropriate tool based on natural language input



🚀 Run Instructions

Install requirements

pip install -r requirements.txt

Set environment variables in .env

MONGO_URL=mongodb://localhost:27017
OPENAI_API_KEY=your_api_key

Start MCP server

python -m app.mcp_server

Run MCP client (CLI agent)

python app/client.py