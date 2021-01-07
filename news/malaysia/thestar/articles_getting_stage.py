import logging
from typing import Any, Dict, Iterator

from aws_apis.dynamodb.database import Database
from common.url_tracker import UrlTracker
from news.malaysia.thestar.scraper.thestar_scraper import TheStarScraper
from news.utils.common import MY_TIMEZONE, get_time
from workflow.stage import Stage

TIME_FORMAT = '%A, %d %b %Y %I:%M %p'


class ArticlesGettingStage(Stage):
    def __init__(
        self,
        scraper: TheStarScraper,
        max_pages_to_load: int = 10,
    ) -> None:
        super().__init__('The Star Getting')
        self.scraper = scraper
        self.max_pages_to_load = max_pages_to_load
        self.page_tracker = UrlTracker(Database.load_database())

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        for page in range(1, self.max_pages_to_load):
            for article in self.scraper.get_articles(page):
                with self.page_tracker.track(article['url']) as url:
                    if url is None:
                        logging.warning('Many known articles. Stopped ...')
                        return
                    elif url == '':
                        logging.warning(
                            f'Known article: {article["url"]}. Ignored ...')
                        continue
                data = self.scraper.read_article(article['url'])
                date = data['date']
                time = data['time']
                estimated_time = article['estimated_time']
                if not estimated_time.endswith(' ago'):
                    logging.warning('This article is too old: {} !'.format(
                        estimated_time))
                    return
                estimated_time = estimated_time[:-4]
                if not time:
                    logging.warning(
                        'This article is older than 1 day: {} !'.format(
                            estimated_time))
                    return
                elif not time.startswith('1'):
                    time = '0{}'.format(time)

                time_str = '{} {}'.format(date, time)
                datetime = get_time(time_str, TIME_FORMAT, MY_TIMEZONE)
                if datetime < item['start_time']:
                    logging.warning('Old articles. Stopped ...')
                    return
                elif datetime < item['end_time']:
                    yield {
                        'datetime': datetime,
                        'title': article['title'],
                        'category': article['category'],
                        'content': data['content'],
                        'url': article['url'],
                    }
