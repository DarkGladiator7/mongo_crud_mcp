# client_agent.py

import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

# --- Load environment variables ---
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# --- Setup LLM ---
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

async def main():
    # ---- MCP client setup ----
    client = MultiServerMCPClient(
        {
            "database": {
                "command": "python",
                "args": ["-m", "app.mcp_server"],  # Path to your MCP server script
                "transport": "stdio",     # could also be "http" if you run MCP server with HTTP transport
            }
        }
    )

    # Get tool schema from MCP server
    tools = await client.get_tools()

    # ---- Create ReAct-style agent ----
    agent = create_react_agent(
        model=model,
        tools=tools
    )

    print("🚀 LLM + MCP Agent ready! Type 'exit' to quit.\n")

    while True:
        query = input("Your query: ")
        if query.lower() in ["exit", "quit"]:
            break
        try:
            result = await agent.ainvoke({"messages": [("user", query)]})
            print("\n🤖 Agent response:\n", result["messages"][-1].content)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
