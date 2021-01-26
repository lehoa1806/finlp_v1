import json
from typing import Any, Tuple

from pymemcache.client.base import PooledClient


class Cache:
    def __init__(
        self,
        memcached=None,
        prefix: str = '',
    ) -> None:
        self.memcached = memcached or PooledClient(
            ('localhost', 11211),
            connect_timeout=1,
            timeout=1,
            ignore_exc=True,
            serializer=self.serializer,
            deserializer=self.deserializer,
        )
        self.prefix = prefix

    @classmethod
    def serializer(cls, key, value) -> Tuple[bytes, int]:
        """
        Customized serializer to use memcached with multiple data types
        """
        if type(value) == str:
            return value.encode('utf-8'), 1
        return json.dumps(value).encode('utf-8'), 2

    @classmethod
    def deserializer(cls, key, value, flags) -> Any:
        """
        Customized deserializer to use memcached with multiple data types
        """
        if flags == 1:
            return value.decode('utf-8')
        if flags == 2:
            return json.loads(value.decode('utf-8'))
        raise ValueError(f'Unknown flags for value: {flags}')

    def get(self, key: str, default=None) -> str:
        """
        The memcached "get" command, but only for one key, as a convenience.
        :param key: item key
        :param default: Value that will be returned if the key was not found
        :return:
        """
        _key = self.prefix + key
        return self.memcached.get(key=_key, default=default)

    def set(self, key: str, value: Any, expire: int = 0) -> bool:
        """
        The memcached "set" command.
        :param key: cached key
        :param value: cached value
        :param expire: Number of seconds until the item is expired, zero for
                       no expiry
        :return: True if the command was successful
        """
        _key = self.prefix + key
        print(_key)
        import logging
        logging.info(_key)
        logging.info(value)
        logging.info(expire)
        return self.memcached.set(key, value, expire=expire)

    def delete(self, key: str) -> bool:
        """
        The memcached "set" command.
        :param key: cached key
        :return: True if the command was successful, False if the key doesn't
                 exist
        """
        _key = self.prefix + key
        return self.memcached.delete(key=_key)
