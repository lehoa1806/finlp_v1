from typing import Dict, Optional

from aws_apis.dynamodb.database import Database
from common.functools import cached_property
from scraper.common import BrowserType


class ConfigDB:
    def __init__(self) -> None:
        database = Database.load_database()
        self.config_table = database.load_configuration_table()

    @cached_property
    def scraper(self) -> Dict:
        config = self.config_table.get_item(
            partition_key='scraper',
            attributes_to_get=['configs', 'secret_keys']
        )
        return config

    @cached_property
    def default(self) -> Dict:
        default = self.config_table.get_item(
            partition_key='default',
            attributes_to_get=['malaysia_channels']
        )
        return default

    @cached_property
    def cipher_key(self) -> str:
        return self.scraper.get('secret_keys', {}).get('cipher_key')

    @cached_property
    def rakuten_creds_code(self) -> str:
        return self.scraper.get('secret_keys', {}).get('rakuten_creds_code')

    @cached_property
    def i3investor_creds_code(self) -> str:
        return self.scraper.get('secret_keys', {}).get('i3investor_creds_code')

    @cached_property
    def slack_token_code(self) -> str:
        return self.scraper.get('secret_keys', {}).get('slack_token_code')

    @cached_property
    def postgresql_creds_code(self) -> str:
        return self.scraper.get('secret_keys', {}).get('postgresql_creds_code')

    @cached_property
    def postgresql_host(self) -> str:
        return self.scraper.get('configs', {}).get('postgresql_host')

    @cached_property
    def postgresql_port(self) -> int:
        return self.scraper.get('configs', {}).get('postgresql_port')

    @cached_property
    def postgresql_database(self) -> str:
        return self.scraper.get('configs', {}).get('postgresql_database')

    @cached_property
    def headless(self) -> Optional[bool]:
        headless = self.scraper.get('configs', {}).get('headless')
        if isinstance(headless, bool):
            return headless
        elif isinstance(headless, str):
            return headless in {'True', 'true'}
        return headless

    @cached_property
    def browser_type(self) -> BrowserType:
        return BrowserType(
            self.scraper.get('configs', {}).get('browser_type', 'Chrome'))

    ########
    @cached_property
    def google_credentials_path(self) -> str:
        return self.scraper.get('configs', {}).get('google_credentials_path')

    @cached_property
    def google_token_path(self) -> str:
        return self.scraper.get('configs', {}).get('google_token_path')

    @cached_property
    def email_receiver(self) -> str:
        return self.scraper.get('configs', {}).get('email_receiver')

    @cached_property
    def email_sender(self) -> str:
        return self.scraper.get('configs', {}).get('email_sender')

    @cached_property
    def malaysia_channels(self) -> Dict:
        channels = self.default.get('malaysia_channels', {})
        return {int(v): k for k, v in channels.items()}
