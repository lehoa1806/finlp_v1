import json
from typing import Any

from utils.configs.env import Env
from utils.memcached import Cache

AWS_REGION = 'ap-southeast-1'
GLOBAL_CACHE = Cache()
GLOBAL_ENV = Env()


def parse_json(
    data: str = '',
    default: Any = None,
) -> Any:
    if not data or not isinstance(data, str):
        return default
    try:
        value = json.loads(data)
        return type(default)(value) if default is not None else value
    except (json.decoder.JSONDecodeError, TypeError):
        return default
