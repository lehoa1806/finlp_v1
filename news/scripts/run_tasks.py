import logging
from argparse import Namespace
from datetime import datetime
from time import sleep
from typing import Dict

import pytz

from common.argument_parser import ArgumentParser
from common.decorators import slack_notify
from news.malaysia.bursamalaysia.announcement_scraping_task import \
    BursaMalaysiaAnnouncement
from news.malaysia.filter import Filter as MalaysiaFilter
# from ..freemalaysiatoday.freemalaysiatoday_scraping_task import \
#    FreeMalaysiaTodayScrapingTask
from news.malaysia.i3investor.i3investor_price_target_task import \
    I3investorPriceTargetTask
from news.malaysia.malaymail.malaymail_scraping_task import \
    MalayMailScrapingTask
from news.malaysia.theedgemarkets.theedgemarkets_scraping_task import \
    TheEdgeMarketsScrapingTask
from news.malaysia.thestar.thestar_scraping_task import TheStarScrapingTask
from news.utils.common import MY_TIMEZONE, VN_TIMEZONE
from news.vietnam.dautucophieu.analysis_scraping_task import \
    DauTuCoPhieuAnnouncement
from news.vietnam.filter import Filter as VietnamFilter
from news.vietnam.fireant_vn.fireant_scraping_task import FireAntTask


class Worker:
    def __init__(self) -> None:
        self.args = self.parse_args()

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

    @classmethod
    def get_time(cls, timezone: str) -> Dict:
        local_timezone = pytz.timezone(timezone)
        now = datetime.utcnow()
        local_now = now.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        local_year = local_now.year
        local_month = local_now.month
        local_day = local_now.day
        start_time = local_timezone.localize(
            datetime(local_year, local_month, local_day - 1, 23))
        end_time = local_timezone.localize(
            datetime(local_year, local_month, local_day, 23, 59, 59))
        return {
            'start_time': start_time,
            'end_time': end_time,
        }

    @classmethod
    def get_cooldown(cls, timezone: str) -> int:
        local_timezone = pytz.timezone(timezone)
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
            return 300
        else:
            return 3600

    def malaysia(self):
        malaysia_filter = MalaysiaFilter()
        times = self.get_time(MY_TIMEZONE)
        start_time = times.get('start_time')
        end_time = times.get('end_time')

        slack_notify(
            BursaMalaysiaAnnouncement.process_task,
            func_type='task',
            name='BursaMalaysiaAnnouncement.process_task',
        )(
            ft=malaysia_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        '''
        slack_notify(
            FreeMalaysiaTodayScrapingTask.process_task,
            func_type='task',
            name='FreeMalaysiaTodayScrapingTask.process_task',
        )(
            ft=self.malaysia_filter,
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
            ft=malaysia_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        slack_notify(
            MalayMailScrapingTask.process_task,
            func_type='task',
            name='MalayMailScrapingTask.process_task',
        )(
            ft=malaysia_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        slack_notify(
            TheEdgeMarketsScrapingTask.process_task,
            func_type='task',
            name='TheEdgeMarketsScrapingTask.process_task',
        )(
            ft=malaysia_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        slack_notify(
            TheStarScrapingTask.process_task,
            func_type='task',
            name='TheStarScrapingTask.process_task',
        )(
            ft=malaysia_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

    def vietnam(self):
        vietnam_filter = VietnamFilter()
        times = self.get_time(VN_TIMEZONE)
        start_time = times.get('start_time')
        end_time = times.get('end_time')

        slack_notify(
            DauTuCoPhieuAnnouncement.process_task,
            func_type='task',
            name='DauTuCoPhieuAnnouncement.process_task',
        )(
            ft=vietnam_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        slack_notify(
            FireAntTask.process_task,
            func_type='task',
            name='FireAntTask.process_task',
        )(
            ft=vietnam_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)


if __name__ == "__main__":
    worker = Worker()
    while True:
        try:
            logging.info('Scrapping Malaysia news/announcements')
            worker.malaysia()
            logging.info('Scrapping Vietnam news/announcements')
            worker.vietnam()
            cooldown = min(worker.get_cooldown(MY_TIMEZONE),
                           worker.get_cooldown(VN_TIMEZONE))
            sleep(cooldown)
        except KeyboardInterrupt:
            logging.info('Stop scrappers')
            break
