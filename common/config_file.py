from configparser import ConfigParser, ExtendedInterpolation
from typing import Dict, Optional

from common.common import GLOBAL_ENV
from common.functools import cached_property
from scraper.common import BrowserType


class ConfigFile:
    """
    [scraper]
    cipher_key: 123
    rakuten_creds_code: xyz
    i3investor_creds_code: abc
    slack_token_code: 0987
    """
    def __init__(self) -> None:
        self.parser = ConfigParser(interpolation=ExtendedInterpolation())
        self.parser.read(GLOBAL_ENV.config_file)

    @cached_property
    def scraper(self) -> Dict:
        try:
            return dict(self.parser['scraper'])
        except KeyError:
            return {}

    @cached_property
    def default(self) -> Dict:
        try:
            return dict(self.parser['default'])
        except KeyError:
            return {}

    @cached_property
    def cipher_key(self) -> str:
        return self.scraper.get('cipher_key')

    @cached_property
    def rakuten_creds_code(self) -> str:
        return self.scraper.get('rakuten_creds_code')

    @cached_property
    def i3investor_creds_code(self) -> str:
        return self.scraper.get('i3investor_creds_code')

    @cached_property
    def slack_token_code(self) -> str:
        return self.scraper.get('slack_token_code')

    @cached_property
    def postgresql_creds_code(self) -> str:
        return self.scraper.get('postgresql_creds_code')

    @cached_property
    def postgresql_host(self) -> str:
        return self.scraper.get('postgresql_host')

    @cached_property
    def postgresql_port(self) -> int:
        return self.scraper.get('postgresql_port')

    @cached_property
    def postgresql_database(self) -> str:
        return self.scraper.get('postgresql_database')

    @cached_property
    def headless(self) -> Optional[bool]:
        headless = self.scraper.get('headless')
        if isinstance(headless, bool):
            return headless
        elif isinstance(headless, str):
            return headless in {'True', 'true'}
        return headless

    @cached_property
    def browser_type(self) -> BrowserType:
        return BrowserType(self.scraper.get('browser_type', 'Chrome'))

    ########
    @cached_property
    def google_credentials_path(self) -> str:
        return self.scraper.get('google_credentials_path')

    @cached_property
    def google_token_path(self) -> str:
        return self.scraper.get('google_token_path')

    @cached_property
    def email_receiver(self) -> str:
        return self.scraper.get('email_receiver')

    @cached_property
    def email_sender(self) -> str:
        return self.scraper.get('email_sender')

    @cached_property
    def malaysia_channels(self) -> Dict:
        """
        Config data is a string like "channel_1:1;channel_2:2;channel_3:3;"
        :return: Dict
        """
        channels = self.default.get('malaysia_channels', '').split(';')
        return {
            int(channel.split(':')[1]): channel.split(':')[0]
            for channel in channels
        }
