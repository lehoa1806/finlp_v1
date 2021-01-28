from configparser import ConfigParser, ExtendedInterpolation
from typing import Dict, Optional

from scraper.common import BrowserType
from utils.common import GLOBAL_ENV
from utils.decorators.functools import cached_property


class ConfigFile:
    """
    [global]
    cipher_key: 123
    newsbot_token_code: 0987
    devbot_token_code: 1234
    [scraper]
    rakuten_creds_code: xyz
    i3investor_creds_code: abc
    """
    def __init__(self) -> None:
        self._parser = self._file_parser if GLOBAL_ENV.config_file else {}

    @cached_property
    def _file_parser(self) -> Dict:
        _parser = ConfigParser(interpolation=ExtendedInterpolation())
        _parser.read(GLOBAL_ENV.config_file)
        return dict(_parser)

    @cached_property
    def _global(self) -> Dict:
        try:
            return dict(self._parser['global'])
        except KeyError:
            return {}

    @cached_property
    def _default(self) -> Dict:
        try:
            return dict(self._parser['default'])
        except KeyError:
            return {}

    @cached_property
    def _scraper(self) -> Dict:
        try:
            return dict(self._parser['scraper'])
        except KeyError:
            return {}

    # =========================================================================
    # GLOBAL
    # =========================================================================
    @cached_property
    def cipher_key(self) -> str:
        return self._global.get('cipher_key')

    @cached_property
    def devbot_signing_secret_code(self) -> str:
        return self._global.get('devbot_signing_secret_code')

    @cached_property
    def devbot_token_code(self) -> str:
        return self._global.get('devbot_token_code')

    @cached_property
    def newsbot_token_code(self) -> str:
        return self._global.get('newsbot_token_code')

    @cached_property
    def postgresql_host(self) -> str:
        return self._global.get('postgresql_host')

    @cached_property
    def postgresql_port(self) -> int:
        return self._global.get('postgresql_port')

    @cached_property
    def postgresql_database(self) -> str:
        return self._global.get('postgresql_database')

    @cached_property
    def postgresql_creds_code(self) -> str:
        return self._global.get('postgresql_creds_code')

    # =========================================================================
    # DEFAULT
    # =========================================================================
    @cached_property
    def malaysia_channels(self) -> Dict:
        """
        Config data is a string like "channel_1:1;channel_2:2;channel_3:3;"
        :return: Dict
        """
        channels = self._default.get('malaysia_channels', '').split(';')
        return {
            int(channel.split(':')[1]): channel.split(':')[0]
            for channel in channels
        }

    @cached_property
    def vietnam_channels(self) -> Dict:
        """
        Config data is a string like "channel_1:1;channel_2:2;channel_3:3;"
        :return: Dict
        """
        channels = self._default.get('vietnam_channels', '').split(';')
        return {
            int(channel.split(':')[1]): channel.split(':')[0]
            for channel in channels
        }

    # =========================================================================
    # SCRAPER
    # =========================================================================
    @cached_property
    def browser_type(self) -> BrowserType:
        return BrowserType(self._scraper.get('browser_type', 'Chrome'))

    @cached_property
    def email_receiver(self) -> str:
        return self._scraper.get('email_receiver')

    @cached_property
    def email_sender(self) -> str:
        return self._scraper.get('email_sender')

    @cached_property
    def google_credentials_path(self) -> str:
        return self._scraper.get('google_credentials_path')

    @cached_property
    def google_token_path(self) -> str:
        return self._scraper.get('google_token_path')

    @cached_property
    def headless(self) -> Optional[bool]:
        headless = self._scraper.get('headless')
        if isinstance(headless, bool):
            return headless
        elif isinstance(headless, str):
            return headless in {'True', 'true'}
        return headless

    @cached_property
    def rakuten_creds_code(self) -> str:
        return self._scraper.get('rakuten_creds_code')

    @cached_property
    def i3investor_creds_code(self) -> str:
        return self._scraper.get('i3investor_creds_code')
