import json
from typing import Any, Dict, Tuple

from scraper.common import BrowserType
from utils.common import AWS_REGION, GLOBAL_ENV
from utils.configs.config_db import ConfigDB
from utils.configs.config_file import ConfigFile
from utils.decorators.functools import cached_property
from utils.tools.cipher import CipherHelper
from utils.tools.singleton import Singleton


class Setting(metaclass=Singleton):
    def __init__(self):
        self.aws_region = AWS_REGION
        self.env = GLOBAL_ENV
        self.config_file = ConfigFile()
        self.config_db = ConfigDB()
        self.cipher_helper = CipherHelper(self.cipher_key)

    def get_attribute(self, name: str) -> Any:
        for config in [self.config_db, self.config_file, self.env]:
            attr = getattr(config, name)
            if attr is not None:
                return attr
        return None

    def decrypt_json(self, encrypted: str, default=None) -> Any:
        try:
            decrypted = self.cipher_helper.decrypt(encrypted)
            if isinstance(default, str):
                return decrypted
            loaded = json.loads(decrypted)
            return type(default)(loaded) if default is not None else loaded
        except (json.decoder.JSONDecodeError, TypeError):
            return default

    def parse_credentials(self, encrypted: str) -> Tuple:
        """
        SCRAPER_CREDENTIALS: '(username, password)'
        """
        return self.decrypt_json(encrypted, tuple())

    # =========================================================================
    # GLOBAL
    # =========================================================================
    @cached_property
    def cipher_key(self) -> str:
        return self.config_db.cipher_key or self.config_file.cipher_key

    @cached_property
    def postgresql_credentials(self) -> Tuple:
        encrypted = self.get_attribute('postgresql_creds_code')
        return self.parse_credentials(encrypted)

    @cached_property
    def devbot_signing_secret(self) -> str:
        encrypted = self.get_attribute('devbot_signing_secret_code')
        return self.decrypt_json(encrypted, '')

    @cached_property
    def devbot_token(self) -> str:
        encrypted = self.get_attribute('devbot_token_code')
        return self.decrypt_json(encrypted, '')

    @cached_property
    def newsbot_token(self) -> str:
        encrypted = self.get_attribute('newsbot_token_code')
        return self.decrypt_json(encrypted, '')

    @cached_property
    def postgresql_host(self) -> str:
        return self.get_attribute('postgresql_host')

    @cached_property
    def postgresql_port(self) -> int:
        return int(self.get_attribute('postgresql_port'))

    @cached_property
    def postgresql_database(self) -> str:
        return self.get_attribute('postgresql_database')

    # =========================================================================
    # DYNAMIC
    # =========================================================================
    @property
    def repo_updated(self) -> bool:
        return self.config_db.repo_updated

    def reset_repo_updated(self) -> None:
        self.config_db.reset_repo_updated()

    # =========================================================================
    # DEFAULT
    # =========================================================================
    @cached_property
    def malaysia_channels(self) -> Dict:
        return self.get_attribute('malaysia_channels')

    @cached_property
    def vietnam_channels(self) -> Dict:
        return self.get_attribute('vietnam_channels')

    # =========================================================================
    # SCRAPER
    # =========================================================================
    @cached_property
    def browser_type(self) -> BrowserType:
        browser_type = self.get_attribute('browser_type')
        return BrowserType.CHROME if browser_type is None else browser_type

    @cached_property
    def headless(self) -> bool:
        headless = self.get_attribute('headless')
        return True if headless is None else headless

    @cached_property
    def scraper_timeout(self) -> int:
        return int(self.get_attribute('scraper_timeout'))

    @cached_property
    def email_receiver(self) -> str:
        return self.get_attribute('email_receiver')

    @cached_property
    def email_sender(self) -> str:
        return self.get_attribute('email_sender')

    @cached_property
    def google_credentials_path(self) -> str:
        return self.get_attribute('google_credentials_path')

    @cached_property
    def google_token_path(self) -> str:
        return self.get_attribute('google_token_path')

    @cached_property
    def i3investor_credentials(self) -> Tuple:
        encrypted = self.get_attribute('i3investor_creds_code')
        return self.parse_credentials(encrypted)

    @cached_property
    def rakuten_credentials(self) -> Tuple:
        encrypted = self.get_attribute('rakuten_creds_code')
        return self.parse_credentials(encrypted)
