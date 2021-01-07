import logging
from typing import Dict, Iterator

from aws_apis.dynamodb.database import Database
from common.url_tracker import UrlTracker
from news.malaysia.bursamalaysia.scraper.bursamalaysia_scraper import \
    BursaMalaysiaScraper
from news.utils.common import MY_TIMEZONE, Subscription, get_time
from workflow.stage import Stage

TIME_FORMAT = '%d %b %Y'


class AnnouncementsGettingStage(Stage):
    def __init__(
        self,
        scraper: BursaMalaysiaScraper,
        max_pages_to_load: int = 100,
    ) -> None:
        super().__init__('BursaMalaysia Announcements')
        self.scraper = scraper
        self.max_pages_to_load = max_pages_to_load
        self.page_tracker = UrlTracker(Database.load_database())

    def process(self, item: Dict) -> Iterator[Dict]:
        for page in range(1, self.max_pages_to_load):
            self.scraper.load_company_announcement_page(page)
            announcements = self.scraper.get_announcements()
            for announcement in announcements:
                with self.page_tracker.track(announcement['url']) as url:
                    if url is None:
                        logging.warning('Many known articles. Stopped ...')
                        return
                    elif url == '':
                        logging.warning(
                            f'Known article: {announcement["url"]}. Ignored ...')
                        continue
                self.scraper.short_sleep()  # Avoid stressing DynamoDB
                announcement_time = get_time(announcement.get('date'),
                                             TIME_FORMAT, MY_TIMEZONE)
                if announcement_time < item['start_time']:
                    logging.warning('Old articles. Stopped ...')
                    return
                elif announcement_time < item['end_time']:
                    yield {
                        'subscription': Subscription.ANNOUNCEMENT,
                        'datetime': announcement_time,
                        'company': announcement.get('company'),
                        'title': announcement.get('title'),
                        'source': 'bursamalaysia.com',
                        'url': announcement.get('url'),
                        'description': announcement.get('description'),
                    }
