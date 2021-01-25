from typing import Dict, Optional

from aws_apis.dynamodb.database import Database
from common.functools import cached_property
from scraper.common import BrowserType


class ConfigDB:
    def __init__(self) -> None:
        database = Database.load_database()
        self.config_table = database.load_configuration_table()
        self.scraper = self.config_table.get_item(
            partition_key='scraper',
            attributes_to_get=['configs', 'secret_keys']
        )
        self.default = self.config_table.get_item(partition_key='default')
        self._dynamic: Dict = {}

    @property
    def dynamic(self) -> Dict:
        if not self._dynamic:
            self._dynamic = self.get_dynamic()
        return self._dynamic

    def get_dynamic(self) -> Dict:
        self._dynamic = self.config_table.get_item(partition_key='dynamic')
        return self._dynamic

    # UTILS
    @property
    def repo_updated(self) -> bool:
        return self.dynamic.get('configs', {}).get(
            'git', {}).get('repo_updated', False)

    def reset_repo_updated(self) -> None:
        if self.repo_updated:
            self._dynamic['configs']['git']['repo_updated'] = False
            self.config_table.put_item(self._dynamic)

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

    @cached_property
    def vietnam_channels(self) -> Dict:
        channels = self.default.get('vietnam_channels', {})
        return {int(v): k for k, v in channels.items()}
