import functools
import json

from utils.common import GLOBAL_CACHE
from utils.json_encoder import CustomJSONEncoder


def cached(
    func=None,
    *,
    memcached=None,
    expire=0,
    func_name=None,
):
    """
    A decorator to retrieve cached data from memcached
    :param func: Function to be decorated
    :param memcached: Memcached wrapper object
    :param expire: Expired time
    :param func_name: A customized name of the function
    """
    if func is None:
        return functools.partial(
            cached, memcached=memcached, expire=expire, func_name=func_name,
        )

    @functools.wraps(func)
    def wrapper_cache(*args, **kwargs):
        _name = func_name or func.__qualname__
        _args = json.dumps(
            args, sort_keys=True, cls=CustomJSONEncoder,
        ).replace(" ", "_") if args else ''
        _kwargs = json.dumps(
            kwargs, sort_keys=True, cls=CustomJSONEncoder,
        ).replace(" ", "_") if kwargs else ''
        key = f'{_name}{_args}{_kwargs}'
        cache = memcached or GLOBAL_CACHE
        value = cache.get(key=key)
        if value:
            return value
        value = func(*args, **kwargs)
        if value:
            cache.set(key=key, value=value, expire=expire)
        return value
    return wrapper_cache
