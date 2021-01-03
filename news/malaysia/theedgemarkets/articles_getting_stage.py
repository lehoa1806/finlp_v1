import logging
from datetime import datetime
from typing import Any, Dict, Iterator, Optional

from news.utils.common import MY_TIMEZONE, get_time
from postgresql.database import Database
from workflow.stage import Stage

from .scraper.theedgemarkets_scraper import TheEdgeMarketsScraper

TIME_FORMAT = '%Y %d %b %I:%M%p'


class ArticlesGettingStage(Stage):
    def __init__(
        self,
        scraper: TheEdgeMarketsScraper,
        max_pages_to_load: Optional[int] = 10,
        get_known: bool = False,
    ) -> None:
        super().__init__('The Edge Markets Getting')
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
        for page in range(self.max_pages_to_load):
            self.scraper.load_malaysia_page(page)
            for article in self.scraper.get_articles_in_page():
                times = [ele.strip() for ele in article.get('time').split('|')]
                time_str = ' '.join([str(datetime.now().year)] + times)
                time = get_time(time_str, TIME_FORMAT, MY_TIMEZONE)
                if (
                    self.is_known_article(time, article['title']) or
                    time < item['start_time']
                ):
                    return
                if time < item['end_time']:
                    yield {
                        'time': time.strftime(
                            '%Y-%m-%d %H:%M:%S {}'.format(MY_TIMEZONE)),
                        'url': article.get('url'),
                    }
