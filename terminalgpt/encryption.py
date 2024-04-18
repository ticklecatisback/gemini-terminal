import os
import sys
from cryptography.fernet import Fernet
from colorama import Fore, Style
from terminalgpt import config
import logging

class EncryptionManager:
    """Manages encryption and decryption of secrets."""

    def __init__(self):
        self.key_file_path = config.KEY_PATH  # Correct configuration of key path
        self.key = self.load_or_create_key(self.key_file_path)
        self.cipher = Fernet(self.key)  # Ensure cipher is properly initialized

    def load_or_create_key(self, key_path):
        """Load an encryption key from a file, or create it if it does not exist."""
        if os.path.exists(key_path):
            with open(key_path, 'rb') as key_file:
                return key_file.read()
        else:
            new_key = Fernet.generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(new_key)
            return new_key

    def encrypt(self, data):
        """Encrypts a string or bytes using the initialized cipher."""
        # Check if the data is already in bytes, if not, encode it
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self.cipher.encrypt(data)

    def decrypt(self, token: bytes) -> str:
        """Decrypts data using Fernet encryption and returns a string."""
        try:
            decrypted_data = self.cipher.decrypt(token)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            logging.error(f"Error decrypting API key: {str(e)}")
            return None

    def generate_and_store_key(self):
        """Generates and stores the encryption key."""
        key = Fernet.generate_key()
        try:
            os.makedirs(os.path.dirname(self.key_file_path), exist_ok=True)
            with open(self.key_file_path, "wb") as key_file:
                key_file.write(key)
        except OSError as e:
            logging.error(f"Failed to store key at {self.key_file_path}: {e}")
            sys.exit(1)
        return key

    def check_api_key_presence(self):
        """Checks if the Gemini API key is properly set up."""
        if not os.path.exists(config.SECRET_PATH) and "GEMINI_API_KEY" not in os.environ:
            message = f"Gemini API key is missing! Please install the API key first with '{config.APP_NAME} install' command."
            logging.error(message)
            sys.exit(1)

    def load_encrypted_api_key(self):
        """Loads the encrypted API key from a secure file."""
        try:
            with open(self.key_file_path, "rb") as file:
                encrypted_api_key = file.read()
            return encrypted_api_key
        except FileNotFoundError:
            logging.error(f"Encrypted API key file not found at {self.key_file_path}.")
            return None
        except Exception as e:
            logging.error(f"Failed to load the encrypted API key: {e}")
            return None

    def get_api_key(self):
        encrypted_api_key = self.load_encrypted_api_key()
        if encrypted_api_key is None:
            logging.error("API Key could not be loaded. Exiting.")
            sys.exit(1)
        try:
            return self.decrypt(encrypted_api_key)
        except Exception as e:
            logging.error(f"Error decrypting API key: {e}")
            sys.exit(1)
