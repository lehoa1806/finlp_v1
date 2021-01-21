import logging
from argparse import Namespace
from datetime import datetime
from time import sleep

import pytz

from common.argument_parser import ArgumentParser
from common.decorators import slack_notify
from news.utils.common import MY_TIMEZONE

from ..bursamalaysia.announcement_scraping_task import \
    BursaMalaysiaAnnouncement
from ..filter import Filter
# from ..freemalaysiatoday.freemalaysiatoday_scraping_task import \
#    FreeMalaysiaTodayScrapingTask
from ..i3investor.i3investor_price_target_task import I3investorPriceTargetTask
from ..malaymail.malaymail_scraping_task import MalayMailScrapingTask
from ..theedgemarkets.theedgemarkets_scraping_task import \
    TheEdgeMarketsScrapingTask
from ..thestar.thestar_scraping_task import TheStarScrapingTask


class Script:
    def __init__(self) -> None:
        local_timezone = pytz.timezone(MY_TIMEZONE)
        now = datetime.utcnow()
        local_now = now.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        local_year = local_now.year
        local_month = local_now.month
        local_day = local_now.day
        hot_time_start = local_timezone.localize(
            datetime(local_year, local_month, local_day, 8))
        hot_time_end = local_timezone.localize(
            datetime(local_year, local_month, local_day, 19))
        if hot_time_start < local_now < hot_time_end:
            self.cooldown = 300
        else:
            self.cooldown = 3600
        self.start_time = local_timezone.localize(
            datetime(local_year, local_month, local_day - 1, 23))
        self.end_time = local_timezone.localize(
            datetime(local_year, local_month, local_day, 23, 59, 59))
        self.args = self.parse_args()
        self.filter = Filter()

    @classmethod
    def parse_args(cls) -> Namespace:
        parser = ArgumentParser(
            description='Script to scrape articles from Malaysia NewsPapers',
        )
        parser.add_argument(
            'headless', action='store_true',
            help='Run in headless mode',
        )

        return parser.arguments

    def main(self):
        slack_notify(
            BursaMalaysiaAnnouncement.process_task,
            func_type='task',
            name='BursaMalaysiaAnnouncement.process_task',
        )(
            ft=self.filter,
            start_time=self.start_time,
            end_time=self.end_time,
            headless=self.args.headless
        )
        sleep(5)

        '''
        slack_notify(
            FreeMalaysiaTodayScrapingTask.process_task,
            func_type='task',
            name='FreeMalaysiaTodayScrapingTask.process_task',
        )(
            ft=self.filter,
            table='malaysia_articles',
            start_time=self.start_time,
            end_time=self.end_time,
            headless=self.args.headless
        )
        sleep(5)
        '''

        slack_notify(
            I3investorPriceTargetTask.process_task,
            func_type='task',
            name='I3investorPriceTargetTask.process_task',
        )(
            ft=self.filter,
            start_time=self.start_time,
            end_time=self.end_time,
            headless=self.args.headless
        )
        sleep(5)

        slack_notify(
            MalayMailScrapingTask.process_task,
            func_type='task',
            name='MalayMailScrapingTask.process_task',
        )(
            ft=self.filter,
            start_time=self.start_time,
            end_time=self.end_time,
            headless=self.args.headless
        )
        sleep(5)

        slack_notify(
            TheEdgeMarketsScrapingTask.process_task,
            func_type='task',
            name='TheEdgeMarketsScrapingTask.process_task',
        )(
            ft=self.filter,
            start_time=self.start_time,
            end_time=self.end_time,
            headless=self.args.headless
        )
        sleep(5)

        slack_notify(
            TheStarScrapingTask.process_task,
            func_type='task',
            name='TheStarScrapingTask.process_task',
        )(
            ft=self.filter,
            start_time=self.start_time,
            end_time=self.end_time,
            headless=self.args.headless
        )
        sleep(self.cooldown)


if __name__ == "__main__":
    while True:
        try:
            Script().main()
        except KeyboardInterrupt:
            logging.info('Stop Malaysia scrappers')
            break
