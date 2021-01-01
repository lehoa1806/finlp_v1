import functools
import logging
import random
import time
from contextlib import contextmanager
from enum import Enum
from functools import partial, wraps

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class BrowserType(Enum):
    CHROME = 'Chrome'
    FIREFOX = 'Firefox'


def is_stale(element: WebElement) -> bool:
    """
    Check if the element is stale
    :param element: WebElement
    :return: bool
    """
    try:
        _ = element.size
        return False
    except StaleElementReferenceException:
        return True


@contextmanager
def wait_for_page_load(browser: WebDriver):
    """
    A context to wait for the new page after switching from a html page
    :param browser: WebDriver
    """
    old_html = browser.find_element_by_tag_name('html')
    wait_time = 60
    while is_stale(old_html) or wait_time > 0:
        time.sleep(1)
        wait_time -= 1
    yield


def do_and_sleep(func=None, *, long: bool = False):
    """
    A decorator to perform a sleep after executing a function
    :param func: Function to be decorated
    :param long: bool
    """
    if func is None:
        return partial(do_and_sleep, long=long)

    @functools.wraps(func)
    def wrapper_do_and_sleep(*args, **kwargs):
        value = func(*args, **kwargs)
        sort_delay = random.randint(1, 9)
        long_delay = random.randint(2, 4) * int(long)
        delay = 0.1 * sort_delay + long_delay
        logging.info('Sleep in {} seconds'.format(delay))
        time.sleep(delay)
        return value
    return wrapper_do_and_sleep


def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    """
    A decorator to print logs
    :param func: Function to be decorated
    :param level: Log level
    :param name: Logger name
    :param message: message
    """
    if func is None:
        return partial(logged, level=level, name=name, message=message)
    logger = logging.getLogger(name)

    @wraps(func)
    def wrapper_logged(*args, **kwargs):
        if level == logging.DEBUG and not message:
            logger.log(level, f'Leave: {func.__name__}')
        else:
            logger.log(level, message)
        value = func(*args, **kwargs)
        if level == logging.DEBUG and not message:
            logger.log(level, f'Leave: {func.__name__}')
        return value
    return wrapper_logged