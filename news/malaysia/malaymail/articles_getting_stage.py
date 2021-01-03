import logging
from datetime import datetime
from typing import Any, Dict, Iterator

from news.utils.common import MY_TIMEZONE, get_time
from postgresql.database import Database
from workflow.stage import Stage

from .scraper.malaymail_scraper import MalayMailScraper

TIME_FORMAT = '%A, %d %b %Y %I:%M %p'


class ArticlesGettingStage(Stage):
    def __init__(
        self,
        scraper: MalayMailScraper,
        get_known: bool = False,
    ) -> None:
        super().__init__('Malay Mail Getting')
        self.scraper = scraper
        self.get_known = get_known
        self.database = Database.load_default_database()

    def is_known_article(self, date: datetime, title: str) -> bool:
        if self.get_known:
            return False

        query = (
            'SELECT 1 FROM articles '
            'WHERE article_date = \'{}\' '
            'AND article_name = \'{}\''
        ).format(date, title.replace('\'', '\'\''),)
        keys = ('exists', )
        response = list(self.database.query(query, keys))
        if len(response) > 0:
            logging.warning('This is a known article: {}!!!'.format(title))
        return len(response) > 0

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        start_time = item['start_time']
        end_time = item['end_time']
        date_str = end_time.strftime('%Y/%m/%d')
        for article in self.scraper.get_money_articles(date_str):
            info = self.scraper.read_article(article['url'])
            time_str = info['time']
            article_date = get_time(time_str[:-4], TIME_FORMAT, MY_TIMEZONE)
            if (
                self.is_known_article(article_date, info['title']) or
                article_date < start_time
            ):
                break
            yield {
                'datetime': article_date,
                'title': info['title'],
                'time': time_str,
                'content': info['content'],
                'url': article['url'],
            }

        for article in self.scraper.get_malaysia_articles(date_str):
            info = self.scraper.read_article(article['url'])
            time_str = info['time']
            article_date = get_time(time_str[:-4], TIME_FORMAT, MY_TIMEZONE)
            if (
                self.is_known_article(article_date, info['title']) or
                article_date < start_time
            ):
                break
            yield {
                'datetime': article_date,
                'title': info['title'],
                'time': time_str,
                'content': info['content'],
                'url': article['url'],
            }
