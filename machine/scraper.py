from selenium.webdriver.remote.webdriver import WebDriver

from scraper.scraper import Scraper as WebScraper
from utils.configs.setting import Setting


class Scraper(WebScraper):
    """Web Browser scraper"""

    def __init__(
        self,
        browser: WebDriver = None,
        **kwargs,
    ) -> None:
        timeout = kwargs.get('timeout') or Setting().scraper_timeout
        headless = kwargs.get('headless')
        if headless is None:
            headless = Setting().headless
        super().__init__(browser=browser, headless=headless, timeout=timeout)
