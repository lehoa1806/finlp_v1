import logging
from typing import Dict, Iterator

from aws_apis.dynamodb.database import Database
from common.url_tracker import UrlTracker
from news.utils.common import VN_TIMEZONE, Subscription, get_time
from workflow.stage import Stage

from .scraper.fireant_scraper import FireAntScraper

TIME_FORMAT = '%-d/%-m/%Y %H:%M:%S'


class FireAntGettingStage(Stage):
    def __init__(
        self,
        scraper: FireAntScraper,
    ) -> None:
        super().__init__('FireAnt news')
        self.scraper = scraper
        self.page_tracker = UrlTracker(Database.load_database())

    def process(self, item: Dict) -> Iterator[Dict]:
        self.scraper.load_fireant_home()
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
            time = get_time(article.get('datetime'), TIME_FORMAT, VN_TIMEZONE)
            if time < item['start_time']:
                logging.warning('Old articles. Stopped ...')
                return
            elif time < item['end_time']:
                yield {
                    'subscription': Subscription.TOTAL,
                    'datetime': time,
                    'title': article['title'],
                    'category': article['category'],
                    'content': '',
                    'url': article['url'],
                    'source': 'fireant.vn',
                }
