from typing import Dict, Iterator

from aws_apis.dynamodb.database import Database as DynamoDB
from news.malaysia.freemalaysiatoday.scraper.freemalaysiatoday_scraper import \
    FreeMalaysiaTodayScraper
from news.utils.common import MY_TIMEZONE, get_time
from utils.url_tracker import UrlTracker
from workflow.stage import Stage

TIME_FORMAT = '%b %d, %Y %I:%M %p'
SUB_TIME_FORMAT = '%B %d, %Y %I:%M %p'


class ArticlesGettingStage(Stage):
    def __init__(
        self,
        scraper: FreeMalaysiaTodayScraper,
    ) -> None:
        super().__init__()
        self.scraper = scraper
        self.page_tracker = UrlTracker(DynamoDB.load_database())

    def process(self, item: Dict) -> Iterator[Dict]:
        start_time = item['start_time']
        end_time = item['end_time']
        date_str = end_time.strftime('%Y/%m/%d')
        self.scraper.load_freemalaysiatoday(date_str)
        highlight_articles = self.scraper.get_highlight_articles()
        other_articles = self.scraper.get_other_articles()

        for article in highlight_articles:
            with self.page_tracker.track(article['url']) as url:
                if url is None:
                    break
                elif url == '':
                    continue
            info = self.scraper.read_article(article['url'])
            time = get_time(info['time'], TIME_FORMAT, MY_TIMEZONE,
                            SUB_TIME_FORMAT)
            if time < start_time:
                break
            elif time < item['end_time']:
                yield {
                    'datetime': time,
                    'title': info['title'],
                    'category': 'Business',
                    'content': info['content'],
                    'url': article['url'],
                }
        for article in other_articles:
            with self.page_tracker.track(article['url']) as url:
                if url is None:
                    break
                elif url == '':
                    continue
            time = get_time(article['time'], TIME_FORMAT, MY_TIMEZONE)
            if time < start_time:
                break
            info = self.scraper.read_article(article['url'])
            if time < item['end_time']:
                yield {
                    'datetime': time,
                    'title': info['title'],
                    'category': 'Business',
                    'content': info['content'],
                    'url': article['url'],
                }
