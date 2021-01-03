
from selenium.webdriver.remote.webdriver import WebDriver

from common.setting import Setting


class Browser:
    def __init__(self, options=None, capabilities=None, **kwargs):
        headless = kwargs.get('headless', Setting().headless)
        options = options or self.get_options(headless)
        self.browser = self.get_browser(options=options,
                                        capabilities=capabilities)

    def get_options(self, headless):
        raise NotImplementedError

    def get_browser(self, options, capabilities) -> WebDriver:
        raise NotImplementedError
