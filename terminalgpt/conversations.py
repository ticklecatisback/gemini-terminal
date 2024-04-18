import json
import logging
import os
import time
from colorama import Back, Style
from terminalgpt import config
from terminalgpt.printer import Printer
import google.generativeai as genai


class ConversationManager:
    """Manages conversations."""

    def __init__(self, **kwargs):
        logging.basicConfig(level=logging.INFO)
        self.__base_path = config.CONVERSATIONS_PATH
        self.__conversation_name = kwargs.get("conversation_name", "")
        self.__printer: Printer = kwargs["printer"]
        # Initialize Gemini client here instead of OpenAI client
        self.__client = genai.GenerativeModel(kwargs.get("model", config.get_default_config()["model"]))

    @property
    def conversation_name(self):
        return self.__conversation_name

    @conversation_name.setter
    def conversation_name(self, conversation_name: str):
        self.__conversation_name = conversation_name

    @property
    def client(self):
        return self.__client

    @client.setter
    def client(self, client):
        self.__client = client

    def get_system_answer(self, messages):
        """Returns the answer from Gemini API."""
        while True:
            try:
                # Modify to use the generate_content method of the Gemini API
                response = self.__client.generate_content(prompt=messages)
                return response.text  # Adjust according to the actual response structure
            except genai.RateLimitError:
                time.sleep(10)

    def create_conversation_name(self, messages: list):
        """Creates a context file name based on the title of the conversation."""
        files = self.get_conversations()
        message_suffix = f"- Keep it unique amongst the next file names list: {files}"
        title_message = {
            "role": "system",
            "content": config.TITLE_MESSAGE + message_suffix,
        }
        answer = self.get_system_answer(messages + [title_message])
        context_file_name = answer  # Adjust this line according to how response data is structured
        self.conversation_name = context_file_name or ""

    # Remaining methods (save_context, save_conversation, etc.) remain the same.

    def get_conversations(self):
        """Lists all saved conversations."""
        if not os.path.exists(self.__base_path):
            os.makedirs(self.__base_path)
        files = os.listdir(self.__base_path)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(self.__base_path, x)), reverse=True)
        return files

    def is_conversations_empty(self, files, message):
        if not files:
            logging.info(message)  # Use logging instead of print
            return True
        return False

