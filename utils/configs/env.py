import os
from typing import Dict

from scraper.common import BrowserType
from utils.decorators.functools import cached_property


class Env:
    @classmethod
    def get_environment_variable(
        cls,
        env: str,
        default=None,
        require=False,
    ) -> str:
        val = os.getenv(env) or default
        if val is None and require:
            raise Exception(f'Environment variable [{env}] not available')
        return val

    @cached_property
    def config_file(self) -> str:
        return self.get_environment_variable('FINLP_CONFIG_FILE', '')

    @cached_property
    def rakuten_creds_code(self) -> str:
        return self.get_environment_variable('RAKUTEN_CREDS_CODE')

    @cached_property
    def i3investor_credentials(self) -> str:
        return self.get_environment_variable('I3INVESTOR_CREDS_CODE')

    # Slack
    @cached_property
    def devbot_token_code(self) -> str:
        return self.get_environment_variable('FINLP_DEVBOT_TOKEN_CODE')

    @cached_property
    def newsbot_token_code(self) -> str:
        return self.get_environment_variable('FINLP_NEWSBOT_TOKEN_CODE')

    # Scraper
    @cached_property
    def headless(self) -> bool:
        headless = self.get_environment_variable('SCRAPER_HEADLESS')
        return headless in {'True', 'true'}

    @cached_property
    def browser_type(self) -> BrowserType:
        """
        SCRAPER_BROWSER_TYPE: CHROME or FIREFOX
        """
        return BrowserType(
            self.get_environment_variable('SCRAPER_BROWSER_TYPE', 'Chrome'))

    # PostgreSQL
    @cached_property
    def postgresql_host(self) -> str:
        return self.get_environment_variable('POSTGRESQL_HOST')

    @cached_property
    def postgresql_port(self) -> str:
        return self.get_environment_variable('POSTGRESQL_PORT')

    @cached_property
    def postgresql_database(self) -> str:
        return self.get_environment_variable('POSTGRESQL_DATABASE')

    @cached_property
    def postgresql_creds_code(self) -> str:
        return self.get_environment_variable('POSTGRESQL_CREDS_CODE')

    ########
    @cached_property
    def google_credentials_path(self) -> str:
        return self.get_environment_variable('GOOGLE_CREDENTIALS_PATH')

    @cached_property
    def google_token_path(self) -> str:
        return self.get_environment_variable('GOOGLE_TOKEN_PATH')

    @cached_property
    def email_receiver(self) -> str:
        return self.get_environment_variable('GOOGLE_EMAIL_SENDER')

    @cached_property
    def email_sender(self) -> str:
        return self.get_environment_variable('GOOGLE_EMAIL_RECEIVER')

    @cached_property
    def malaysia_channels(self) -> Dict:
        """
        Config data is a string like "channel_1:1;channel_2:2;channel_3:3;"
        :return: Dict
        """
        channels = self.get_environment_variable(
            'MALAYSIA_CHANNELS', '').split(';')
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
        channels = self.get_environment_variable(
            'VIETNAM_CHANNELS', '').split(';')
        return {
            int(channel.split(':')[1]): channel.split(':')[0]
            for channel in channels
        }
