import requests
import json
from agent.llm_setup import call_llm

API_URL = "http://localhost:8000"


def api_url(endpoint: str, **params):
    params_str = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{API_URL}{endpoint}?{params_str}"


def process_user_input(user_input: str):
    system_prompt = """
    You are an AI agent that converts natural language instructions 
    into structured MongoDB CRUD actions. 

    Output ONLY valid JSON with the format:
    {
        "action": "create_user | list_users | update_user | delete_user | create_db",
        "db_name": "string",
        "params": { ... }
    }
    """

    reply = call_llm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ])

    print("\n🤖 LLM Parsed Instruction:\n", reply)

    try:
        instruction = json.loads(reply)
    except json.JSONDecodeError:
        print("❌ Could not parse LLM response.")
        return

    action = instruction.get("action")
    db_name = instruction.get("db_name")
    params = instruction.get("params", {})

    if "id" in params and params["id"] is not None:
        params["id"] = str(params["id"])

    try:
        if action == "create_db":
            res = requests.post(api_url("/databases"), json={"db_name": db_name})
            if res.status_code == 200:
                print("DB Created:", res.json())
            else:
                print("❌ Failed to create DB:", res.json())

        elif action == "create_user":
            res = requests.post(api_url("/users", db_name=db_name), json=params)
            if res.status_code == 200:
                print("User Created:", res.json())
            else:
                print("❌ Failed to create user:", res.json())

        elif action == "list_users":
            res = requests.get(api_url("/users", db_name=db_name))
            if res.status_code == 200:
                print("Users:", res.json())
            else:
                print("❌ Failed to list users:", res.json())

        elif action == "update_user":
            filter_query = params.get("filter")
            update_query = params.get("update")

            if not filter_query or not update_query:
                print("❌ Missing filter or update for update_user")
                return

            res = requests.put(api_url("/users/update", db_name=db_name), json=params)
            if res.status_code == 200:
                print("User Updated:", res.json())
            else:
                print("❌ Failed to update user:", res.json())

        elif action == "delete_user":
            user_id = params.get("id")
            if not user_id:
                print("❌ Missing user ID for delete")
                return
            res = requests.delete(api_url(f"/users/{user_id}", db_name=db_name))
            if res.status_code == 200:
                print("User Deleted:", res.json())
            else:
                print("❌ Failed to delete user:", res.json())

        else:
            print("❌ Unknown action.")

    except Exception as e:
        print("❌ API error:", str(e))


if __name__ == "__main__":
    print("🚀 LLM MongoDB CLI Agent (type 'exit' to quit)\n")
    while True:
        user_input = input(">> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        process_user_input(user_input)
