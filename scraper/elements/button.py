from selenium.webdriver.remote.webelement import WebElement

from scraper.common import wait_for_change
from utils.decorators.do_and_sleep import do_and_sleep


class Button:
    def __init__(self, element: WebElement) -> None:
        self.html = element

    @do_and_sleep(level=1)
    def click(self) -> None:
        self.html.click()

    def click_and_wait(self) -> None:
        with wait_for_change(self.html):
            self.html.click()
