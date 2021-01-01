
from selenium.webdriver.remote.webdriver import WebDriver

from common.config import Config


class Browser:
    def __init__(self, options=None, capabilities=None, **kwargs):
        headless = kwargs.get('headless') or Config().headless
        options = options or self.get_options(headless)
        self.browser = self.get_browser(options=options,
                                        capabilities=capabilities)

    def __del__(self):
        if self.browser:
            self.browser.close()
            self.browser = None

    def __enter__(self):
        return self.browser

    def __exit__(self, exc_type, exc_value, traceback):
        if self.browser:
            self.browser.quit()
            self.browser = None

    def get_options(self, headless):
        raise NotImplementedError

    def get_browser(self, options, capabilities) -> WebDriver:
        raise NotImplementedError
