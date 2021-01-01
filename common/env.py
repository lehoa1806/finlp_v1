import json
import os
from typing import Dict

from common.config import Config
from tools.cipher import CipherHelper
from tools.functools import cached_property
from tools.singleton import Singleton


class Env(metaclass=Singleton):
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

    # Credentials
    def get_credentials(
        self,
        creds_code: str
    ) -> Dict:
        """
        SCRAPER_CREDENTIALS: '{username: password}'
        """
        encrypted = self.get_environment_variable(creds_code)
        creds_json = CipherHelper(Config().cipher_key).decrypt(encrypted)
        try:
            creds = json.loads(creds_json)
        except (json.decoder.JSONDecodeError, TypeError):
            creds = {}
        return creds if isinstance(creds, Dict) else {}

    @cached_property
    def rakuten_credentials(self):
        return self.get_credentials('RAKUTEN_CREDS_CODE')

    @cached_property
    def i3investor_credentials(self):
        return self.get_credentials('I3INVESTOR_CREDS_CODE')

    # Slack
    @cached_property
    def slack_token(self):
        return self.get_environment_variable('FINLP_SLACK_TOKEN')

    # Scraper
    @cached_property
    def browser_type(self):
        """
        SCRAPER_BROWSER_TYPE: CHROME or FIREFOX
        """
        return self.get_environment_variable('SCRAPER_BROWSER_TYPE')

    # PostgreSQL
    @cached_property
    def postgresql_host(self):
        return self.get_environment_variable('POSTGRESQL_HOST')

    @cached_property
    def postgresql_port(self):
        return self.get_environment_variable('POSTGRESQL_PORT')

    @cached_property
    def postgresql_database(self):
        return self.get_environment_variable('POSTGRESQL_DATABASE')

    @cached_property
    def postgresql_credentials(self):
        return self.get_credentials('POSTGRESQL_CREDS_CODE')
