import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}


def call_llm(messages, temperature=0.3):
    """
    Calls Groq's LLaMA model via chat endpoint.
    :param messages: List of message dicts: [{"role": "user", "content": "..."}]
    :return: Assistant's reply string
    """
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": temperature,
    }

    response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"❌ LLM Error: {response.status_code} - {response.text}")


# Basic test (only if run directly)
if __name__ == "__main__":
    try:
        reply = call_llm([
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, world!"}
        ])
        print("LLM says:", reply)
    except Exception as e:
        print(str(e))
