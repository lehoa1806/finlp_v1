import base64
import logging
from typing import Union

from .singleton import Singleton


class CipherHelper(metaclass=Singleton):
    def __init__(self, secret_key: str) -> None:
        """
        Util tool to encrypt, decrypt sensitive data
        :param secret_key: secret key
        """
        self.secret_key = secret_key

    def encrypt(self, text: str) -> str:
        """
        Encrypt the input text
        :param text: The text to be encrypted
        :return: str
        """
        encrypted = ''
        for index, text_char in enumerate(text):
            key_char = self.secret_key[index % len(self.secret_key)]
            encrypted += chr(ord(text_char) + ord(key_char) % 256)
        to_bytes = self.str_to_bytes(encrypted)
        base64_bytes = base64.urlsafe_b64encode(to_bytes)
        base64_text = self.bytes_to_str(base64_bytes.rstrip(b'='))
        return base64_text

    def decrypt(self, text: str) -> str:
        """
        Decrypt the encrypted text
        :param text: The text to be decrypted
        :return: str
        """
        base64_bytes = self.str_to_bytes(text) + b'==='
        decrypted = ''
        try:
            encrypted_bytes = base64.urlsafe_b64decode(base64_bytes)
            encrypted_text = self.bytes_to_str(encrypted_bytes)
            for index, text_char in enumerate(encrypted_text):
                key_char = self.secret_key[index % len(self.secret_key)]
                decrypted += chr((ord(text_char) - ord(key_char) + 256) % 256)
            return decrypted
        except UnicodeDecodeError as err:
            logging.error(f'Invalid input {text}. Failed to decrypt it')
            raise err

    @classmethod
    def str_to_bytes(cls, text: Union[bytes, str]) -> bytes:
        """
        Encode a string to utf-8
        :param text: string or bytes
        :return: bytes
        """
        if isinstance(text, str):
            return text.encode('utf8')
        try:
            text.decode('utf-8')
            return text
        except UnicodeDecodeError as err:
            logging.error(
                f'Invalid input {text}. Failed to encode it to utf-8')
            raise err

    @classmethod
    def bytes_to_str(cls, text: Union[bytes, str]) -> str:
        """
        Decode utf-8 bytes to string
        :param text: bytes or string
        :return: string
        """
        if isinstance(text, str):
            return text
        try:
            return text.decode('utf-8')
        except UnicodeDecodeError as err:
            logging.error(
                f'Invalid input {text}. Failed to decode it to string')
            raise err
