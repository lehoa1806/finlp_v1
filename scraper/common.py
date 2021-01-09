import time
from contextlib import contextmanager
from enum import Enum

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
def wait_for_change(element: WebElement):
    """
    A context to wait for the element to be changed
    :param element: WebDriver
    """
    yield
    wait_time = 60
    while not is_stale(element) and wait_time > 0:
        time.sleep(1)
        wait_time -= 1


@contextmanager
def wait_for_page_load(browser: WebDriver):
    """
    A context to wait for the new page after switching from a html page
    :param browser: WebDriver
    """
    old_html = browser.find_element_by_tag_name('html')
    yield
    wait_time = 60
    while not is_stale(old_html) and wait_time > 0:
        time.sleep(1)
        wait_time -= 1
