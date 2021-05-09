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
        headless = kwargs.get('headless') or Setting().headless
        timeout = kwargs.get('timeout') or Setting().scraper_timeout
        super().__init__(browser=browser, headless=headless, timeout=timeout)
