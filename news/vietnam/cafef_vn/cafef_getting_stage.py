import logging
from typing import Dict, Iterator

from utils.dynamodb import Database
from news.utils.common import VN_TIMEZONE, get_time
from utils.url_tracker import UrlTracker
from workflow.stage import Stage

from .scraper.cafef_scraper import CafefScraper

TIME_FORMAT = '%-d/%-m/%Y %H:%M:%S'


class CafefGettingStage(Stage):
    def __init__(
        self,
        scraper: CafefScraper,
    ) -> None:
        super().__init__('CafefGettingStage news')
        self.scraper = scraper
        self.page_tracker = UrlTracker(Database.load_database())

    def process(self, item: Dict) -> Iterator[Dict]:
        self.scraper.load_cafef_home()
        for articles in [
            self.scraper.get_highlight(),
            self.scraper.get_articles(),
        ]:
            for article in articles:
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
