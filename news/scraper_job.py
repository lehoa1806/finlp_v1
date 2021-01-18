from argparse import Namespace

from common.argument_parser import ArgumentParser
from workflow.consumer import Consumer
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer


class ScraperJob(Job):
    @property
    def timezone(self) -> str:
        raise NotImplementedError

    def parse_args(self) -> Namespace:
        parser = ArgumentParser(
            description='Script to scrape articles/announcements',
        )
        parser.add_date_input(
            'start-time',
            timezone=self.timezone,
        )
        parser.add_date_input(
            'end-time',
            timezone=self.timezone,
        )
        parser.add_argument(
            'headless', action='store_true',
            help='Run in headless mode',
        )

        return parser.arguments

    @property
    def consumer(self) -> Consumer:
        raise NotImplementedError

    @property
    def pipeline(self) -> Pipeline:
        raise NotImplementedError

    @property
    def producer(self):
        return SingleItemProducer({
            'start_time': self.args.start_time,
            'end_time': self.args.end_time,
        })
