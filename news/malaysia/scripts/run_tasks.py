import logging
from argparse import Namespace

from common.argument_parser import ArgumentParser
from common.decorators import do_and_sleep, slack_notify
from news.utils.common import MY_TIMEZONE

from ..bursamalaysia.announcement_scraping_task import \
    BursaMalaysiaAnnouncement
from ..filter import Filter
from ..freemalaysiatoday.freemalaysiatoday_scraping_task import \
    FreeMalaysiaTodayScrapingTask
from ..i3investor.i3investor_price_target_task import I3investorPriceTargetTask
from ..malaymail.malaymail_scraping_task import MalayMailScrapingTask
from ..theedgemarkets.theedgemarkets_scraping_task import \
    TheEdgeMarketsScrapingTask
from ..thestar.thestar_scraping_task import TheStarScrapingTask


@do_and_sleep(level=60)
def sleep():
    pass


class Script:
    def __init__(self) -> None:
        self.args = self.parse_args()
        self.filter = Filter()

    @classmethod
    def parse_args(cls) -> Namespace:
        parser = ArgumentParser(
            description='Script to scrape articles from Malaysia NewsPapers',
        )
        parser.add_date_input(
            'start-time',
            timezone=MY_TIMEZONE,
        )
        parser.add_date_input(
            'end-time',
            timezone=MY_TIMEZONE,
        )
        parser.add_argument(
            'headless', action='store_true',
            help='Run in headless mode',
        )

        return parser.arguments

    def main(self):
        slack_notify(
            BursaMalaysiaAnnouncement.process_task(
                ft=self.filter,
                table='malaysia_announcements',
                start_time=self.args.start_time,
                end_time=self.args.end_time,
                headless=self.args.headless
            )
        )
        sleep()

        slack_notify(
            FreeMalaysiaTodayScrapingTask.process_task(
                ft=self.filter,
                table='malaysia_articles',
                start_time=self.args.start_time,
                end_time=self.args.end_time,
                headless=self.args.headless
            )
        )
        sleep()

        slack_notify(
            I3investorPriceTargetTask.process_task(
                ft=self.filter,
                table='malaysia_articles',
                start_time=self.args.start_time,
                end_time=self.args.end_time,
                headless=self.args.headless
            )
        )
        sleep()

        slack_notify(
            MalayMailScrapingTask.process_task(
                ft=self.filter,
                table='malaysia_articles',
                start_time=self.args.start_time,
                end_time=self.args.end_time,
                headless=self.args.headless
            )
        )
        sleep()

        slack_notify(
            TheEdgeMarketsScrapingTask.process_task(
                ft=self.filter,
                table='malaysia_articles',
                start_time=self.args.start_time,
                end_time=self.args.end_time,
                headless=self.args.headless
            )
        )
        sleep()

        slack_notify(
            TheStarScrapingTask.process_task(
                ft=self.filter,
                table='malaysia_articles',
                start_time=self.args.start_time,
                end_time=self.args.end_time,
                headless=self.args.headless
            )
        )
        sleep()


if __name__ == "__main__":
    while True:
        try:
            Script().main()
        except KeyboardInterrupt:
            logging.info('Stop Malaysia scrappers')
