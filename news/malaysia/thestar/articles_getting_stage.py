import logging
from datetime import datetime
from typing import Any, Dict, Iterator

from news.utils.common import MY_TIMEZONE, get_time
from postgresql.database import Database
from workflow.stage import Stage

from .scraper.thestar_scraper import TheStarScraper

TIME_FORMAT = '%A, %d %b %Y %I:%M %p'


class ArticlesGettingStage(Stage):
    def __init__(
        self,
        scraper: TheStarScraper,
        max_pages_to_load: int = 10,
        get_known: bool = False,
    ) -> None:
        super().__init__('The Star Getting')
        self.scraper = scraper
        self.max_pages_to_load = max_pages_to_load
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
        for page in range(1, self.max_pages_to_load):
            for article in self.scraper.get_articles(page):
                time_str = article.get('time', '')
                article_date = get_time(time_str, TIME_FORMAT, MY_TIMEZONE)
                if (
                    self.is_known_article(article_date, article['title']) or
                    article_date < item['start_time']
                ):
                    return
                if article_date < item['end_time']:
                    yield {
                        'datetime': article_date,
                        'time': article['time'],
                        'title': article['title'],
                        'category': article['category'],
                        'content': article['content'],
                        'url': article['url'],
                    }
