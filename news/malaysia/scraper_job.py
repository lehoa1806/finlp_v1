from argparse import Namespace

from common.argument_parser import ArgumentParser
from machine.postgres_batch_insert import PostgresBatchInsert
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer

from ..utils.common import MY_TIMEZONE


class ScraperJob(Job):
    def __init__(self, table: str) -> None:
        super().__init__()
        self.table = table

    def parse_args(self) -> Namespace:
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
        parser.add_argument(
            'get-known', action='store_true',
            help='Get known articles/announcements',
        )

        return parser.arguments

    @property
    def consumer(self) -> PostgresBatchInsert:
        return PostgresBatchInsert(
            table_name=self.table,
            batch_size=10,
        )

    @property
    def pipeline(self) -> Pipeline:
        raise NotImplementedError

    @property
    def producer(self):
        return SingleItemProducer({
            'start_time': self.args.start_time,
            'end_time': self.args.end_time,
        })
