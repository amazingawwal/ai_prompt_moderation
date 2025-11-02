import requests
import os
from dotenv import load_dotenv
load_dotenv()  # load variables from .env



OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  
MODEL_ID = "nvidia/nemotron-nano-12b-v2-vl:free"

HEADERS = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}

BANNED_KEYWORDS = ["kill", "hack", "bomb"]
SYSTEM_PROMPT = "You are a helpful AI assistant. Always answer safely and politely."


# Moderation Functions
def violates_policy(text):
    return any(word in text.lower() for word in BANNED_KEYWORDS)

def redact_output(text):
    for word in BANNED_KEYWORDS:
        text = text.replace(word, "[REDACTED]")
    return text


# Main Function
def get_openrouter_response(user_prompt):
    if violates_policy(user_prompt):
        return "❌ Your input violated the moderation policy."

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 300
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=HEADERS, json=payload)

    if response.status_code != 200:
        return f"⚠️ API Error: {response.text}"

    data = response.json()
    ai_text = data["choices"][0]["message"]["content"]

    if violates_policy(ai_text):
        return f"⚠️ Output moderated:\n{redact_output(ai_text)}"
    return ai_text


# Run Interaction

user_input = input("🧑 Enter your prompt: ")
print("\n🤖 AI Response:\n", get_openrouter_response(user_input))
