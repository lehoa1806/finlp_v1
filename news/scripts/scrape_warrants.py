import logging
from argparse import Namespace
from datetime import datetime
from time import sleep

import pytz

from news.utils.common import VN_TIMEZONE
from news.vietnam.vndirect.warrant_scraping_task import WarrantScraperTask
from utils.argument_parser import ArgumentParser
from utils.configs.setting import Setting
from utils.decorators.slack_notify import slack_notify


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
        parser.add_argument(
            "cool-down",
            type=int,
            default=60,
            help='Cool-down period',
        )
        parser.add_argument(
            "break-period",
            type=int,
            default=3600,
            help='Break period',
        )
        return parser.arguments

    @classmethod
    def take_a_break(cls) -> None:
        """
        09:00 -- sleep(5s) -- 15:00
          |                     |
          -------- sleep -------
        :return: None
        """
        while True:
            utcnow = datetime.utcnow()
            local_timezone = pytz.timezone(VN_TIMEZONE)
            now = utcnow.replace(tzinfo=pytz.utc).astimezone(local_timezone)
            if now.weekday() in [5, 6]:
                logging.info('Weekend -- stop working and enjoy the sleep!!!')
                sleep(21600)
                continue
            start_morning = now.replace(hour=8, minute=55, second=0)
            end_morning = now.replace(hour=11, minute=30, second=0)
            start_evening = now.replace(hour=12, minute=55, second=0)
            end_evening = now.replace(hour=15, minute=0, second=0)
            if now < start_morning or now > end_evening:
                logging.info('Non-working time -- back to sleep')
                sleep(300)
            elif end_morning < now < start_evening:
                logging.info('Lunch time -- let\'s eat')
                sleep(300)
            else:
                break

    def scrape(self):
        slack_notify(
            WarrantScraperTask.process_task,
            func_type='task',
            func_name='VnWarrantScraperTask.process_task',
        )(
            cool_down=self.args.cool_down,
            break_period=self.args.break_period,
            headless=self.args.headless,
        )


if __name__ == "__main__":
    worker = Worker()
    while True:
        if Setting().repo_updated:
            Setting().reset_repo_updated()
            logging.warning('REPO UPDATED is triggered. Exiting ... !!!')
            raise SystemExit(1)
        try:
            worker.take_a_break()
            worker.scrape()
        except KeyboardInterrupt:
            logging.info('Stop scrapping VN warrants')
            break
