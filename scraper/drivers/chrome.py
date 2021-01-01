from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from .browser import Browser


class Chrome(Browser):
    def __init__(
        self,
        options: Options = None,
        capabilities=DesiredCapabilities.CHROME,
        **kwargs,
    ):
        capabilities = capabilities or DesiredCapabilities.CHROME
        super().__init__(options, capabilities, **kwargs)

    def get_options(self, headless: False) -> Options:
        options = Options()
        if headless:
            options.add_argument('-headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--dns-prefetch-disable')
        options.add_argument('--window-size=1920,1080')
        return options

    def get_browser(self, options, capabilities) -> WebDriver:
        return WebDriver(chrome_options=options,
                         desired_capabilities=capabilities)