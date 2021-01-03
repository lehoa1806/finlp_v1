import logging
from datetime import datetime
from typing import Dict, Iterator

from news.malaysia.freemalaysiatoday.scraper.freemalaysiatoday_scraper import \
    FreeMalaysiaTodayScraper
from news.utils.common import MY_TIMEZONE, get_time
from postgresql.database import Database
from workflow.stage import Stage

TIME_FORMAT = '%b %d, %Y %I:%M %p'
SUB_TIME_FORMAT = '%B %d, %Y %I:%M %p'


class ArticlesGettingStage(Stage):
    def __init__(
        self,
        scraper: FreeMalaysiaTodayScraper,
        get_known: bool = False,
    ) -> None:
        super().__init__()
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
        response = list(self.database.query(query, ('exists',)))
        if len(response) > 0:
            logging.warning('This is a known article: {}!!!'.format(title))
        return len(response) > 0

    def process(self, item: Dict) -> Iterator[Dict]:
        start_time = item['start_time']
        end_time = item['end_time']
        date_str = end_time.strftime('%Y/%m/%d')
        self.scraper.load_freemalaysiatoday(date_str)
        highlight_articles = self.scraper.get_highlight_articles()
        other_articles = self.scraper.get_other_articles()

        for article in highlight_articles:
            info = self.scraper.read_article(article['url'])
            article_date = get_time(info['time'], TIME_FORMAT, MY_TIMEZONE,
                                    SUB_TIME_FORMAT)
            if (
                self.is_known_article(article_date, info['title']) or
                article_date < start_time
            ):
                break
            yield {
                'datetime': article_date,
                'title': info['title'],
                'time': info['time'],
                'content': info['content'],
                'url': article['url'],
            }
        for article in other_articles:
            article_date = get_time(article['time'], TIME_FORMAT, MY_TIMEZONE)
            if article_date < start_time:
                break
            info = self.scraper.read_article(article['url'])
            if self.is_known_article(article_date, info['title']):
                break
            yield {
                'datetime': article_date,
                'title': info['title'],
                'time': info['time'],
                'content': info['content'],
                'url': article['url'],
            }
