from scraper.common import BrowserType
from tools.singleton import Singleton


class Config(metaclass=Singleton):

    @property
    def headless(self) -> bool:
        return True

    @property
    def browser_type(self) -> BrowserType:
        return BrowserType.CHROME

    @property
    def cipher_key(self) -> str:
        return ''
