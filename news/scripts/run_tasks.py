import logging
from argparse import Namespace
from datetime import datetime, timedelta
from time import sleep
from typing import Dict, List

import pytz

# from news.malaysia.bursamalaysia.announcement_scraping_task import \
#    BursaMalaysiaAnnouncement
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
from news.utils.common import MY_TIMEZONE, VN_TIMEZONE, TimeShift
from news.vietnam.cafef_vn.cafef_scraping_task import CafefTask
from news.vietnam.dautucophieu.analysis_scraping_task import \
    DauTuCoPhieuAnnouncement
from news.vietnam.filter import Filter as VietnamFilter
from news.vietnam.fireant_vn.fireant_scraping_task import FireAntTask
from news.vietnam.tinnhanhchungkhoan.tnck_scraping_task import TNCKTask
from news.vietnam.vietstock.vietstock_scraping_task import VietStockTask
from utils.argument_parser import ArgumentParser
from utils.configs.setting import Setting
from utils.decorators.slack_notify import slack_notify
from news.vietnam.vndirect.warrant_scraping_task import WarrantScraperTask


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
        start_time = local_now.replace(hour=23) - timedelta(days=1)
        end_time = local_now.replace(hour=23, minute=59, second=59)

        return {
            'start_time': start_time,
            'end_time': end_time,
        }

    @classmethod
    def take_a_break(cls, timezones: List[str]) -> None:
        """
        00:00 -- sleep(3h) -- 08:00 -- sleep(5s) -- 19:00 --sleep(1h)-- 23:00
          |                                                               |
          ---------------------------- sleep(3h) -------------------------
        :param timezones: List of timezones
        :return: None
        """
        _rested_time = 0
        shifts = [TimeShift(timezone) for timezone in timezones]
        while True:
            logging.info('Sleep 300s ...')
            sleep(300)
            current_shifts = [shift.current for shift in shifts]
            if all(shift == TimeShift.REST for shift in current_shifts):
                _rested_time += 300
                if _rested_time >= 10800:
                    break
            elif all(shift >= TimeShift.NIGHT for shift in current_shifts):
                _rested_time += 300
                if _rested_time >= 3600:
                    break
            else:
                # if any(shift >= TimeShift.WORKING for shift in shifts):
                break

    def scrape_vn30_warrants(self):
        slack_notify(
            WarrantScraperTask.process_task,
            func_type='task',
            func_name='VnWarrantScraperTask.process_task',
        )(
            headless=self.args.headless,
        )
        sleep(5)

    def malaysia(self):
        malaysia_filter = MalaysiaFilter()
        times = self.get_time(MY_TIMEZONE)
        start_time = times.get('start_time')
        end_time = times.get('end_time')

        '''
        slack_notify(
            BursaMalaysiaAnnouncement.process_task,
            func_type='task',
            func_name='BursaMalaysiaAnnouncement.process_task',
        )(
            ft=malaysia_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)
        '''

        # self.scrape_vn30_warrants()

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

        # self.scrape_vn30_warrants()
        '''
        slack_notify(
            I3investorPriceTargetTask.process_task,
            func_type='task',
            func_name='I3investorPriceTargetTask.process_task',
        )(
            ft=malaysia_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)
        '''
        #self.scrape_vn30_warrants()

        slack_notify(
            MalayMailScrapingTask.process_task,
            func_type='task',
            func_name='MalayMailScrapingTask.process_task',
        )(
            ft=malaysia_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        self.scrape_vn30_warrants()

        slack_notify(
            TheEdgeMarketsScrapingTask.process_task,
            func_type='task',
            func_name='TheEdgeMarketsScrapingTask.process_task',
        )(
            ft=malaysia_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        self.scrape_vn30_warrants()

        slack_notify(
            TheStarScrapingTask.process_task,
            func_type='task',
            func_name='TheStarScrapingTask.process_task',
        )(
            ft=malaysia_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        self.scrape_vn30_warrants()

    def vietnam(self):
        vietnam_filter = VietnamFilter()
        times = self.get_time(VN_TIMEZONE)
        start_time = times.get('start_time')
        end_time = times.get('end_time')

        slack_notify(
            DauTuCoPhieuAnnouncement.process_task,
            func_type='task',
            func_name='DauTuCoPhieuAnnouncement.process_task',
        )(
            ft=vietnam_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        self.scrape_vn30_warrants()

        slack_notify(
            FireAntTask.process_task,
            func_type='task',
            func_name='FireAntTask.process_task',
        )(
            ft=vietnam_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        self.scrape_vn30_warrants()

        slack_notify(
            TNCKTask.process_task,
            func_type='task',
            func_name='TNCKTask.process_task',
        )(
            ft=vietnam_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        self.scrape_vn30_warrants()

        slack_notify(
            CafefTask.process_task,
            func_type='task',
            func_name='CafefTask.process_task',
        )(
            ft=vietnam_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        self.scrape_vn30_warrants()

        slack_notify(
            VietStockTask.process_task,
            func_type='task',
            func_name='VietStockTask.process_task',
        )(
            ft=vietnam_filter,
            start_time=start_time,
            end_time=end_time,
            headless=self.args.headless
        )
        sleep(5)

        self.scrape_vn30_warrants()


if __name__ == "__main__":
    worker = Worker()
    while True:
        if Setting().repo_updated:
            Setting().reset_repo_updated()
            logging.warning('REPO UPDATED is triggered. Exiting ... !!!')
            raise SystemExit(1)
        try:
            logging.info('Scrapping Malaysia news/announcements')
            worker.malaysia()
            logging.info('Scrapping Vietnam news/announcements')
            worker.vietnam()
            worker.take_a_break([MY_TIMEZONE, VN_TIMEZONE])
        except KeyboardInterrupt:
            logging.info('Stop scrappers')
            break
