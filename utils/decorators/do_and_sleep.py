import functools
import logging
import random
import time


def do_and_sleep(func=None, *, level: int = 0):
    """
    A decorator to perform a sleep after executing a function
    :param func: Function to be decorated
    :param level: int
    """
    if func is None:
        return functools.partial(do_and_sleep, level=level)

    @functools.wraps(func)
    def wrapper_do_and_sleep(*args, **kwargs):
        value = func(*args, **kwargs)
        sort_delay = random.randint(1, 9)
        long_delay = random.randint(2, 4) * level
        delay = 0.1 * sort_delay + long_delay
        logging.info('Sleep in {} seconds'.format(delay))
        time.sleep(delay)
        return value
    return wrapper_do_and_sleep
