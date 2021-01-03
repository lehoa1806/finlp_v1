import json
import logging
from datetime import datetime
from typing import Any, Dict, Iterator

from news.malaysia.bursamalaysia.scraper.bursamalaysia_scraper import \
    BursaMalaysiaScraper
from news.utils.common import MY_TIMEZONE, get_time
from postgresql.database import Database
from workflow.stage import Stage

TIME_FORMAT = '%d %b %Y'


class AnnouncementsGettingStage(Stage):
    def __init__(
        self,
        scraper: BursaMalaysiaScraper,
        max_pages_to_load: int = 100,
        get_known: bool = False,
    ) -> None:
        super().__init__('BursaMalaysia Announcements')
        self.scraper = scraper
        self.max_pages_to_load = max_pages_to_load
        self.get_known = get_known
        self.database = Database.load_default_database()

    def is_known_announcement(self, announcement: Dict[str, str]) -> bool:
        if self.get_known:
            return False
        announcement_date = get_time(announcement.get('date'),
                                     TIME_FORMAT, MY_TIMEZONE)
        query = (
            'SELECT announcement_detail FROM announcements '
            'WHERE announcement_date = \'{}\' '
            'AND announcement_source = \'{}\' '
            'AND announcement_company = \'{}\' '
            'AND announcement_title = \'{}\' '
        ).format(announcement_date,
                 'bursamalaysia.com',
                 announcement.get('company').replace('\'', '\'\''),
                 announcement.get('title').replace('\'', '\'\''))
        keys = ('announcement_detail', )
        response = list(self.database.query(query, keys))
        if len(response) > 0:
            logging.warning('This is a known announcement: {}!!!'.format(
                response[0].get('announcement_detail')))
        return len(response) > 0

    @classmethod
    def yield_announcement(
        cls,
        announcement: Dict[str, str],
    ) -> Iterator[Dict[str, Any]]:
        announcement_date = get_time(announcement.get('date'),
                                     TIME_FORMAT, MY_TIMEZONE)
        yield {
            'date_added': datetime.utcnow(),
            'announcement_date': announcement_date,
            'announcement_source': 'bursamalaysia.com',
            'announcement_company': announcement.get('company'),
            'announcement_title': announcement.get('title'),
            'announcement_url': announcement.get('url'),
            'announcement_detail': json.dumps({
                'time': announcement.get('date'),
                'title': announcement.get('title'),
                'description': announcement.get('description'),
            })
        }

    def process(self, item: Dict) -> Iterator[Dict]:
        start_time = item['start_time']
        end_time = item['end_time']
        for page in range(1, self.max_pages_to_load):
            self.scraper.load_company_announcement_page(page)
            announcements = self.scraper.get_announcements()
            announcement = next(announcements)
            announcement_date = get_time(announcement.get('date'),
                                         TIME_FORMAT, MY_TIMEZONE)
            if self.is_known_announcement(announcement):
                return
            if announcement_date < start_time:
                logging.warning('announcement_date < start_time')
                return
            yield from self.yield_announcement(announcement)
            for item in announcements:
                announcement_date = get_time(item.get('date'),
                                             TIME_FORMAT, MY_TIMEZONE)
                if announcement_date < start_time:
                    logging.warning('announcement_date < start_time')
                    return
                if announcement_date > end_time:
                    continue
                yield from self.yield_announcement(item)
