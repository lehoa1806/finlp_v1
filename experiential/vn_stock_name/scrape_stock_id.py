from argparse import Namespace

from common.argument_parser import ArgumentParser
from machine.postgres_batch_insert import PostgresBatchInsert
from workflow.consumer import Consumer
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer

from .scraper.scraper import CafeFLiveBoardScraper
from .stock_id_getting_stage import StockIdGettingStage


class Worker(Job):
    @classmethod
    def parse_args(cls) -> Namespace:
        parser = ArgumentParser(
            description='Script to scrape stocks from CafeF liveboard',
        )
        parser.add_argument(
            'headless', action='store_true',
            help='Run in headless mode',
        )

        return parser.arguments

    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=StockIdGettingStage(
                scraper=CafeFLiveBoardScraper(headless=self.args.headless),
            )
        )

    @property
    def consumer(self) -> Consumer:
        return PostgresBatchInsert(
            table_name='vietnam_companies_2',
            batch_size=10,
        )

    @property
    def producer(self):
        return SingleItemProducer({})


if __name__ == "__main__":
    Worker().main()
