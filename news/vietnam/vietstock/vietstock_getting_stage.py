import logging
from typing import Dict, Iterator

from aws_apis.dynamodb.database import Database
from news.utils.common import VN_TIMEZONE, get_time
from utils.url_tracker import UrlTracker
from workflow.stage import Stage

from .scraper.vietstock_scraper import VietStockScraper

TIME_FORMAT = '%d/%m/%Y %H:%M:%S'


class VietStockGettingStage(Stage):
    def __init__(
        self,
        scraper: VietStockScraper,
    ) -> None:
        super().__init__('VietStockGettingStage news')
        self.scraper = scraper
        self.page_tracker = UrlTracker(Database.load_database())

    def process(self, item: Dict) -> Iterator[Dict]:
        self.scraper.load_vietstock_home()
        for article in self.scraper.get_articles():
            with self.page_tracker.track(article['url']) as url:
                if url is None:
                    logging.warning('Many known articles. Stopped ...')
                    return
                elif url == '':
                    logging.warning(
                        f'Known article: {article["url"]}. Ignored ...')
                    continue
            self.scraper.short_sleep()  # Avoid stressing DynamoDB
            time = get_time(
                article.get('datetime'), TIME_FORMAT, VN_TIMEZONE)
            if time < item['start_time']:
                logging.warning('Old articles. Stopped ...')
                return
            elif time < item['end_time']:
                yield {
                    'datetime': time,
                    'title': article['title'],
                    'category': article['category'],
                    'content': '',
                    'url': article['url'],
                }
