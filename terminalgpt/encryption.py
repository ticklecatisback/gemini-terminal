"""Encryption module for terminalgpt."""

import os
import sys
from cryptography.fernet import Fernet
from colorama import Fore, Style
from terminalgpt import config

class EncryptionManager:
    """Manages encryption and decryption of secrets."""

    def __init__(self):
        self.__key_path = config.KEY_PATH


    def generate_and_store_key(self):
        """Generates and stores the encryption key."""
        key = Fernet.generate_key()
        try:
            os.makedirs(os.path.dirname(self.__key_path), exist_ok=True)
            with open(self.__key_path, "wb") as key_file:
                key_file.write(key)
        except OSError as e:
            print(Style.BRIGHT + Fore.RED + f"Failed to store key at {self.__key_path}: {e}" + Style.RESET_ALL)
            sys.exit(1)
        return key

    def load_key(self):
        """Loads the encryption key from a file."""
        try:
            with open(self.__key_path, "rb") as file:
                return file.read()
        except FileNotFoundError:
            print(Style.BRIGHT + Fore.RED + f"Encryption key file not found at {self.__key_path}." + Style.RESET_ALL)
            sys.exit(1)

    def encrypt(self, data: str, key: bytes) -> bytes:
        """Encrypts a string using Fernet encryption."""
        cipher = Fernet(key)
        return cipher.encrypt(data.encode('utf-8'))

    def decrypt(self, data: bytes, key: bytes) -> str:
        """Decrypts data using Fernet encryption and returns a string."""
        cipher = Fernet(key)
        return cipher.decrypt(data).decode('utf-8')

    def check_api_key_presence(self):
        """Checks if the Gemini API key is properly set up."""
        if not os.path.exists(config.SECRET_PATH) and "GEMINI_API_KEY" not in os.environ:
            message = f"Gemini API key is missing! Please install the API key first with '{config.APP_NAME} install' command."
            print(Style.BRIGHT + Fore.RED + message + Style.RESET_ALL)
            sys.exit(1)

    def get_api_key(self) -> str:
        """Retrieves the API key, preferring environment variable if set."""
        if "GEMINI_API_KEY" in os.environ:
            return os.environ["GEMINI_API_KEY"]
        encryption_key = self.load_key()
        api_key_encrypted = os.path.join(config.SECRET_PATH, 'api_key.enc')
        return self.decrypt(api_key_encrypted, encryption_key)

