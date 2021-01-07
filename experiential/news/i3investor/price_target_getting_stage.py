import json
import logging
from datetime import datetime
from typing import Any, Dict, Iterator

from news.utils.common import MY_TIMEZONE, get_time
from postgresql.database import Database
from workflow.stage import Stage

from .scraper.i3investor_scraper import I3investorScraper

TIME_FORMAT = '%d/%m/%Y'


class PriceTargetGettingStage(Stage):
    def __init__(
        self,
        scraper: I3investorScraper,
        get_known: bool = False,
    ) -> None:
        super().__init__('I3investor Price Target')
        self.scraper = scraper
        self.get_known = get_known
        self.database = Database.load_default_database()

    def is_known_announcement(
        self,
        time: datetime,
        source: str,
        company: str,
        title: str,
        url: str,
    ) -> bool:
        if self.get_known:
            return False
        query = (
            'SELECT announcement_detail FROM announcements '
            'WHERE announcement_date = \'{}\' '
            'AND announcement_source = \'{}\' '
            'AND announcement_company = \'{}\' '
            'AND announcement_title = \'{}\' '
            'AND announcement_url = \'{}\''
        ).format(time, source, company.replace('\'', '\'\''),
                 title.replace('\'', '\'\''), url)
        keys = ('announcement_detail', )
        response = list(self.database.query(query, keys))
        if len(response) > 0:
            logging.warning('This is a known announcement: {}!!!'.format(
                response[0].get('announcement_detail')))
        return len(response) > 0

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        for announcement in self.scraper.get_price_targets():
            time_str = announcement['Date']
            time = get_time(time_str, TIME_FORMAT, MY_TIMEZONE)
            stock_name = announcement['Stock Name']
            last_price = announcement['Last Price']
            price_target = announcement['Price Target']
            price_change = announcement['Upside/Downside']
            price_action = announcement['Price Call']
            source = announcement['Source']
            url = announcement['Url']
            title = 'Price target of {} was changed: to {}'.format(
                stock_name, price_target
            )

            if self.is_known_announcement(
                    time, source, stock_name, title, url):
                continue
            elif time < item['start_time']:
                return
            if time < item['end_time']:
                yield {
                    'date_added': datetime.utcnow(),
                    'announcement_date': time,
                    'announcement_source': source,
                    'announcement_company': stock_name,
                    'announcement_title': title,
                    'announcement_url': url,
                    'announcement_detail': json.dumps({
                        'time': time_str,
                        'title': title,
                        'description':
                            'Last Price: {}, Price Target {}, Upside/Downside:'
                            ' {}, Price Call: {}, Source: {}'.format(
                                last_price, price_target, price_change,
                                price_action, source),
                    })
                }
