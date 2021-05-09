from typing import Dict, Iterator

from utils.dynamodb import Database
from utils.url_tracker import UrlTracker
from workflow.stage import Stage

from .scraper.scraper import CafeFLiveBoardScraper

TIME_FORMAT = '%-d/%-m/%Y %H:%M:%S'


class StockIdGettingStage(Stage):
    def __init__(
        self,
        scraper: CafeFLiveBoardScraper,
    ) -> None:
        super().__init__('StockIdGettingStage news')
        self.scraper = scraper
        self.page_tracker = UrlTracker(Database.load_database())

    def process(self, item: Dict) -> Iterator[Dict]:
        urls = [
            'https://liveboard.cafef.vn/?center=1',
            'https://liveboard.cafef.vn/?center=2',
            'https://liveboard.cafef.vn/?center=9',
        ]
        for url in urls:
            self.scraper.load_url(url)
            for item in self.scraper.get_stocks():
                yield {
                    'stock_id': item['id'],
                    'short_name': item['name'],
                }
