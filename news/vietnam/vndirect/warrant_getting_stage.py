import logging
from time import sleep, time
from typing import Dict, Iterator

from workflow.stage import Stage

from .scraper.vndirect_scraper import VnDirectScraper

TIME_FORMAT = '%-d/%-m/%Y %H:%M:%S'


class WarrantGettingStage(Stage):
    def __init__(
        self,
        scraper: VnDirectScraper,
        cool_down: int = 60,
        break_period: int = 3600,
    ) -> None:
        super().__init__('VnDirect warrants')
        self.scraper = scraper
        self.cool_down = cool_down
        self.break_period = break_period

    def process(self, item: Dict) -> Iterator[Dict]:
        tm = time()
        self.scraper.load_warrant_home()
        while True:
            yield from self.scraper.get_warrant_info()
            # Stupid hack to push data to "bulk data processing" consumer
            yield from self.teardown(item)
            if time() - tm > self.break_period:
                logging.info('Break the loop to sleep and restart the scraper')
                break
            logging.info(f'Take a short sleep ({self.cool_down})')
            sleep(self.cool_down)
            yield from self.setup(item)
