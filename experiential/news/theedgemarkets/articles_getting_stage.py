import logging
from datetime import datetime
from typing import Dict, Iterator, Optional

from aws_apis.dynamodb.database import Database
from common.url_tracker import UrlTracker
from news.malaysia.theedgemarkets.scraper.theedgemarkets_scraper import \
    TheEdgeMarketsScraper
from news.utils.common import MY_TIMEZONE, get_time
from workflow.stage import Stage

TIME_FORMAT = '%Y %d %b %I:%M%p'


class ArticlesGettingStage(Stage):
    def __init__(
        self,
        scraper: TheEdgeMarketsScraper,
        max_pages_to_load: Optional[int] = 10,
    ) -> None:
        super().__init__()
        self.scraper = scraper
        self.max_pages_to_load = max_pages_to_load
        self.page_tracker = UrlTracker(Database.load_database())

    def process(self, item: Dict) -> Iterator:
        for page in range(self.max_pages_to_load):
            self.scraper.load_malaysia_page(page)
            for article in self.scraper.get_articles_in_page():
                with self.page_tracker.track(article['url']) as url:
                    if url is None:
                        logging.warning('Many known articles. Stopped ...')
                        return
                    elif url == '':
                        logging.warning(
                            f'Known article: {article["url"]}. Ignored ...')
                        continue
                    times = [
                        ele.strip() for ele in article.get('time').split('|')
                    ]
                    time_str = ' '.join([str(datetime.now().year)] + times)
                    time = get_time(time_str, TIME_FORMAT, MY_TIMEZONE)
                    if time < item['start_time']:
                        logging.warning('Old articles. Stopped ...')
                        return
                    if time < item['end_time']:
                        data = self.scraper.read_article(url)
                        yield {
                            'datetime': time,
                            'title': data.get('title'),
                            'category': data.get('category'),
                            'content': data.get('content'),
                            'url': article.get('url'),
                        }
