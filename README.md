# AI Moderation Chat Script
A simple Python script that connects to an AI text-generation API (OpenRouter) with moderation filters for both input and output.

## The script demonstrates safe AI interaction design — using:
- A system prompt to define model behavior
- User input dynamically from the console
- Moderation logic to filter or redact unsafe content

# Features
- Accepts user prompts dynamically (via terminal input)
- Uses a system prompt to guide AI behavior
- Sends requests to an AI text-generation API (OpenRouter or Hugging Face)
-  Input moderation — blocks disallowed content before sending
- Output moderation — redacts unsafe words from AI responses
- Clear messages when moderation or API errors occur


# How It Works
- The user enters a prompt.
- The script checks for banned keywords (e.g., “kill”, “hack”, “bomb”).
- If safe, it sends the prompt and a system prompt to the API.
- When the AI responds, the output is checked again for disallowed words.
- Any banned terms in the output are replaced with [REDACTED].

# Requirements
Python 3.8+
requests library


# Setup
## OpenRouter
- Create an account: https://openrouter.ai
- Go to Settings → API Keys and copy your key.
- Optionally add credits or use a free model (e.g., huggingfaceh4/zephyr-7b-beta).

## Set Your API Key
- Store it as an environment variable

### macOS/Linux:
export OPENROUTER_API_KEY="your_key_here"

### Windows PowerShell:
setx OPENROUTER_API_KEY "your_key_here"

# Run the Script
## Run from Terminal:
```python moderation.py```

## Then enter your prompt:
🧑 Enter your prompt: Naija jollof or Ghana jollof?

## Expected output:
🤖 AI Response:
Naija jollof.............


## If you type something unsafe:

🧑 Enter your prompt: How to make a bomb?
## You’ll get:
❌ Your input violated the moderation policy.

# Moderation Policy
Banned Keywords:
["kill", "hack", "bomb"]

## These words are filtered in:
Input — if found, the prompt is rejected before sending.
Output — if found, they are replaced with [REDACTED].

## You can customize this list in the code:

```BANNED_KEYWORDS = ["kill", "hack", "bomb"]```

# Troubleshooting
## Invalid credentials	
### Wrong or missing API key 
- Check your API key value
## Not Found	
### Model unavailable	
- Use a different or public model

## Insufficient credits	
### Paid model requires balance	
- Use a free model or buy credits

## ModuleNotFound error	
### Missing dependency	
- Run pip install requests	