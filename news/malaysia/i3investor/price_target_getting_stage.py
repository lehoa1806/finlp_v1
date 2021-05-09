import logging
from typing import Any, Dict, Iterator

from utils.dynamodb import Database
from news.malaysia.i3investor.scraper.i3investor_scraper import \
    I3investorScraper
from news.utils.common import MY_TIMEZONE, Subscription, get_time
from utils.url_tracker import UrlTracker
from workflow.stage import Stage

TIME_FORMAT = '%d/%m/%Y'


class PriceTargetGettingStage(Stage):
    def __init__(
        self,
        scraper: I3investorScraper,
    ) -> None:
        super().__init__('I3investor Price Target')
        self.scraper = scraper
        self.page_tracker = UrlTracker(Database.load_database())

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        for announcement in self.scraper.get_price_targets():
            announcement_url = announcement['Url']
            with self.page_tracker.track(announcement_url) as url:
                if url is None:
                    logging.warning('Many known articles. Stopped ...')
                    return
                elif url == '':
                    logging.warning(
                        f'Known article: {announcement_url}. Ignored ...')
                    continue
            self.scraper.short_sleep()  # Avoid stressing DynamoDB

            time_str = announcement['Date']
            time = get_time(time_str, TIME_FORMAT, MY_TIMEZONE)
            stock_name = announcement['Stock Name']
            last_price = announcement['Last Price']
            price_target = announcement['Price Target']
            price_change = announcement['Upside/Downside']
            price_action = announcement['Price Call']
            source = announcement['Source']
            title = 'Price target of {} was changed: to {}'.format(
                stock_name, price_target
            )

            if time < item['start_time']:
                logging.warning('Old articles. Stopped ...')
                return
            elif time < item['end_time']:
                description = (
                    f'Last Price: {last_price}, Price Target {price_target},'
                    f' Upside/Downside: {price_change},'
                    f' Price Call: {price_action}, Source: {source}'
                )
                yield {
                    'subscription': Subscription.HOT,
                    'datetime': time,
                    'company': stock_name,
                    'title': title,
                    'source': source,
                    'url': announcement_url,
                    'description': description,
                }
