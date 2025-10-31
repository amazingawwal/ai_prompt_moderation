import os
import requests


HF_API_KEY = os.getenv("HF_API_KEY")  
MODEL_ID = "mistralai/Mixtral-8x7B-Instruct" 
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

BANNED_KEYWORDS = ["kill", "hack", "bomb"]

SYSTEM_PROMPT = (
    "You are a safe and helpful AI assistant. "
    "Refuse to answer anything harmful, illegal, or violent. "
    "Be clear and concise."
)


def violates_policy(text):
    lower_text = text.lower()
    return any(word in lower_text for word in BANNED_KEYWORDS)

def redact_output(text):
    for word in BANNED_KEYWORDS:
        text = text.replace(word, "[REDACTED]")
        text = text.replace(word.capitalize(), "[REDACTED]")
    return text

def get_hf_response(user_prompt):
    if violates_policy(user_prompt):
        return "❌ Your input violated the moderation policy."

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    payload = {
        "inputs": f"{SYSTEM_PROMPT}\n\nUser: {user_prompt}\nAI:",
        "parameters": {"max_new_tokens": 200, "temperature": 0.7}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"⚠️ API Error: {response.text}"

    data = response.json()
    if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
        output_text = data[0]["generated_text"]
    else:
        output_text = str(data)

   
    if violates_policy(output_text):
        output_text = redact_output(output_text)
        return f"⚠️ Output contained unsafe content. Moderated version:\n{output_text}"

    return output_text


if __name__ == "__main__":
    user_input = input("🧑 Enter your prompt: ")
    reply = get_hf_response(user_input)
    print("\n🤖 AI Response:\n", reply)
