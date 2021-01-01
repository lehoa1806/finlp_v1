import os

from tools.functools import cached_property


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
    def config_file(self):
        return self.get_environment_variable('CONFIG_FILE', '')

    @cached_property
    def rakuten_creds_code(self):
        return self.get_environment_variable('RAKUTEN_CREDS_CODE')

    @cached_property
    def i3investor_credentials(self):
        return self.get_environment_variable('I3INVESTOR_CREDS_CODE')

    # Slack
    @cached_property
    def slack_token_code(self):
        return self.get_environment_variable('FINLP_SLACK_TOKEN_CODE')

    # Scraper
    @cached_property
    def headless(self):
        return self.get_environment_variable('SCRAPER_HEADLESS')

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
    def postgresql_creds_code(self):
        return self.get_environment_variable('POSTGRESQL_CREDS_CODE')
