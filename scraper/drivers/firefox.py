from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from .browser import Browser


class Firefox(Browser):
    def __init__(
        self,
        options: Options = None,
        capabilities=DesiredCapabilities.FIREFOX,
        **kwargs,
    ):
        capabilities = capabilities or DesiredCapabilities.FIREFOX
        super().__init__(options, capabilities, **kwargs)

    def get_options(self, headless: False) -> Options:
        options = Options()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--dns-prefetch-disable')
        options.add_argument('--window-size=1920,1080')
        return options

    def get_browser(self, options, capabilities) -> WebDriver:
        return WebDriver(firefox_options=options,
                         desired_capabilities=capabilities)
