"""TerminalGPT configuration file."""

import json
import platform
from os import path

APP_NAME = "terminalgpt"

BASE_PATH = f"~/.{APP_NAME}".replace("~", path.expanduser("~"))
DEFAULTS_PATH = f"{BASE_PATH}/defaults.json"
CONVERSATIONS_PATH = f"{BASE_PATH}/conversations"
SECRET_PATH = f"{BASE_PATH}/{APP_NAME}.encrypted"
KEY_PATH = f"{BASE_PATH}/{APP_NAME}.key"

ENCODING_MODEL = "cl100k_base"

# Update to use Gemini model identifiers and their token limits
MODELS = {
    "gemini-1.0-pro": 2048,          # Example token limit, adjust according to actual model specifications
    "gemini-1.0-pro-vision": 4096,   # For a multimodal model handling both text and images
    "gemini-1.5-pro-latest": 8192,   # Hypothetical latest model with larger token capacity
}

def machine_info():
    """Get the current machine info."""
    return platform.platform()

def get_default_config() -> dict:
    """Get the default configuration from the config file."""
    try:
        with open(DEFAULTS_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        # Default to a generic Gemini model if the file is not found
        return {"model": "gemini-1.0-pro", "style": "markdown", "models": MODELS}

INIT_SYSTEM_MESSAGE = {
    "role": "system",
    "content": f"""
- Your name is "TerminalGPT".
- You are a helpful personal assistant for programmers.
- You are running on {machine_info()} machine.
- Please note that your answers will be displayed on the terminal.
- So keep answers short as possible and use a suitable format for printing on a terminal.
""",
}

INIT_WELCOME_MESSAGE = {
    "role": "system",
    "content": """
- Please start the conversation with a random and short greeting message starts with 'Welcome to TerminalGPT'.
- Add a ton of self humor.
- Keep it short as possible, one line.
""",
}

INIT_WELCOME_BACK_MESSAGE = {
    "role": "system",
    "content": """
The conversation you remember was a while ago, now we are continuing it.
Please start the conversation with a random and short welcome back message.
- Start with 'Welcome back to TerminalGPT'.
- Add a ton of self humor.
- Keep it short as possible, one line.

After the welcome back message, please summarize the last conversation. (e.g. "Last time we talked about ...")
- End with something that invites the user to continue the conversation.
""",
}

TITLE_MESSAGE = """
Please give this conversation a short title.
I'm going to use this title as a file name for the conversation.
There are going to a lot of files like that under a folder "~/.terminalgpt/conversations"
- Hard limit of 5 words.
- Use underscores instead of spaces.
- Don't mention yourself in it. (e.g. "TerminalGPT conversation")
- Don't use any special characters.
- Don't use any numbers.
- Don't use any capital letters.
- Don't use any spaces.
- Don't use any punctuation.
- Don't use any symbols.
- Don't use any emojis.
- Don't use any accents.
- Don't use quotes.
- Don't use words like: "macos", "programmer_assistant", "conversation".
- Don't use any file extensions. (e.g. ".txt" or ".json")
"""
