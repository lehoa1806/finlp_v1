from typing import Any, Dict, Optional

from aws_apis.dynamodb.database import Database
from scraper.common import BrowserType
from utils.common import GLOBAL_CACHE
from utils.decorators.function_cache import cached
from utils.decorators.functools import cached_property

CONFIG_TABLE = Database.load_database().load_configuration_table()


@cached(memcached=GLOBAL_CACHE, expire=900, func_name='ConfigDB.get_config')
def get_config(
    partition_key: str,
    sort_key: Any = None,
):
    return CONFIG_TABLE.get_item(
        partition_key=partition_key,
        sort_key=sort_key,
    )


class ConfigDB:
    def __init__(self) -> None:
        self.scraper = CONFIG_TABLE.get_item(
            partition_key='scraper',
            attributes_to_get=['configs', 'secret_keys']
        )
        self.default = CONFIG_TABLE.get_item(partition_key='default')

    @property
    def dynamic(self) -> Dict:
        return get_config(partition_key='dynamic')

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

    # UTILS
    @classmethod
    def reset_dynamic(cls) -> bool:
        # Dirty trick to reset cached dynamic value
        return GLOBAL_CACHE.delete(
            key='ConfigDB.get_config{"partition_key":_"dynamic"}')

    @property
    def repo_updated(self) -> bool:
        return self.dynamic.get('configs', {}).get(
            'git', {}).get('repo_updated', False)

    def reset_repo_updated(self) -> None:
        if self.repo_updated:
            self.dynamic['configs']['git']['repo_updated'] = False
            CONFIG_TABLE.put_item(self.dynamic)
            self.reset_dynamic()
