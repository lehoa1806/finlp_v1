import logging
from typing import Any, Dict, Iterator

from aws_apis.dynamodb.database import Database
from common.url_tracker import UrlTracker
from news.malaysia.malaymail.scraper.malaymail_scraper import MalayMailScraper
from news.utils.common import MY_TIMEZONE, get_time
from workflow.stage import Stage

TIME_FORMAT = '%A, %d %b %Y %I:%M %p'


class ArticlesGettingStage(Stage):
    def __init__(
        self,
        scraper: MalayMailScraper,
    ) -> None:
        super().__init__('MalayMail Getting')
        self.scraper = scraper
        self.page_tracker = UrlTracker(Database.load_database())

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        end_time = item['end_time']
        date_str = end_time.strftime('%Y/%m/%d')
        for article in self.scraper.get_money_articles(date_str):
            with self.page_tracker.track(article['url']) as url:
                if url is None:
                    logging.warning('Many known articles. Stopped ...')
                    return
                elif url == '':
                    logging.warning(
                        f'Known article: {article["url"]}. Ignored ...')
                    continue
            info = self.scraper.read_article(article['url'])
            time_str = info['time']
            datetime = get_time(time_str[:-4], TIME_FORMAT, MY_TIMEZONE)
            if datetime < item['start_time']:
                logging.warning('Old articles. Stopped ...')
                return
            elif datetime < item['end_time']:
                yield {
                    'datetime': datetime,
                    'title': info['title'],
                    'category': 'Money',
                    'content': info['content'],
                    'url': article['url'],
                }

        for article in self.scraper.get_malaysia_articles(date_str):
            with self.page_tracker.track(article['url']) as url:
                if url is None:
                    logging.warning('Many known articles. Stopped ...')
                    return
                elif url == '':
                    logging.warning(
                        f'Known article: {article["url"]}. Ignored ...')
                    continue
            info = self.scraper.read_article(article['url'])
            time_str = info['time']
            datetime = get_time(time_str[:-4], TIME_FORMAT, MY_TIMEZONE)
            if datetime < item['start_time']:
                logging.warning('Old articles. Stopped ...')
                return
            elif datetime < item['end_time']:
                yield {
                    'datetime': datetime,
                    'title': info['title'],
                    'category': 'Money',
                    'content': info['content'],
                    'url': article['url'],
                }
