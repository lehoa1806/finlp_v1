from typing import Dict, Iterator

from workflow.stage import Stage

from .scraper.vndirect_scraper import VnDirectScraper

TIME_FORMAT = '%-d/%-m/%Y %H:%M:%S'


class WarrantGettingStage(Stage):
    def __init__(
        self,
        scraper: VnDirectScraper,
    ) -> None:
        super().__init__('VnDirect warrants')
        self.scraper = scraper

    def process(self, item: Dict) -> Iterator[Dict]:
        self.scraper.load_warrant_home()
        yield from self.scraper.get_warrant_info()
