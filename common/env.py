import json
import os
from typing import Dict

from tools.cipher import CipherHelper
from common.config import Config


def get_environment_variable(env, default=None, require=False):
    val = os.getenv(env) or default
    if val is None and require:
        raise Exception('Environment variable [{}] not available.'.format(env))
    return val


# Credentials
def get_credentials(creds_code: str):
    """
    SCRAPER_CREDENTIALS: '{username: password}'
    """
    encrypted = get_environment_variable(creds_code)
    creds_json = CipherHelper(Config().cipher_key).decrypt(encrypted)
    try:
        creds = json.loads(creds_json)
    except (json.decoder.JSONDecodeError, TypeError):
        creds = {}
    return creds if isinstance(creds, Dict) else {}


def get_rakuten_credentials():
    return get_credentials('RAKUTEN_CREDS_CODE')


def get_i3investor_credentials():
    return get_credentials('I3INVESTOR_CREDS_CODE')


# Slack
def get_slack_token():
    return get_environment_variable('FINLP_SLACK_TOKEN')


# Scraper
def get_browser_type():
    """
    SCRAPER_BROWSER_TYPE: CHROME or FIREFOX
    """
    return get_environment_variable('SCRAPER_BROWSER_TYPE')


# PostgreSQL
def get_postgresql_host():
    return get_environment_variable('POSTGRESQL_HOST')


def get_postgresql_port():
    return get_environment_variable('POSTGRESQL_PORT')


def get_postgresql_database():
    return get_environment_variable('POSTGRESQL_DATABASE')


def get_postgresql_credentials():
    return get_credentials('POSTGRESQL_CREDS_CODE')
