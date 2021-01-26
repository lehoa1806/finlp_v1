import logging
from typing import Dict, Iterator

from aws_apis.dynamodb.database import Database
from news.utils.common import VN_TIMEZONE, Subscription, get_time
from utils.url_tracker import UrlTracker
from workflow.stage import Stage

from .scraper.dtcp_scraper import DauTuCoPhieuScraper

TIME_FORMAT = '%d/%m/%Y'


class AnalysisGettingStage(Stage):
    def __init__(
        self,
        scraper: DauTuCoPhieuScraper,
    ) -> None:
        super().__init__('dautucophieu.net Analysis')
        self.scraper = scraper
        self.page_tracker = UrlTracker(Database.load_database())

    def process(self, item: Dict) -> Iterator[Dict]:
        self.scraper.load_phantichchungkhoan_page()
        analyses = self.scraper.get_analyses()
        for analysis in analyses:
            with self.page_tracker.track(analysis['url']) as url:
                if url is None:
                    logging.warning('Many known articles. Stopped ...')
                    return
                elif url == '':
                    logging.warning(
                        f'Known article: {analysis["url"]}. Ignored ...')
                    continue
            self.scraper.short_sleep()  # Avoid stressing DynamoDB
            time = get_time(analysis.get('date'), TIME_FORMAT, VN_TIMEZONE)
            if time < item['start_time']:
                logging.warning('Old articles. Stopped ...')
                return
            elif time < item['end_time']:
                yield {
                    'subscription': Subscription.ANNOUNCEMENT,
                    'datetime': time,
                    'company': analysis.get('company'),
                    'title': analysis.get('title'),
                    'source': 'dautucophieu.net',
                    'url': analysis.get('url'),
                    'description': analysis.get('description'),
                }
