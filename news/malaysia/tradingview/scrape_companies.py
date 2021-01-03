from argparse import Namespace

from common.argument_parser import ArgumentParser
from machine.postgres_batch_insert import PostgresBatchInsert
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer

from .company_getting_stage import CompanyGettingStage
from .scraper.tradingview_scraper import TradingViewScraper


class Worker(Job):
    def parse_args(self) -> Namespace:
        parser = ArgumentParser(
            description='Script to collect Stock ID from TradingView',
        )
        parser.add_argument(
            '--headless', action='store_true',
            help='Run in headless mode',
        )

        return parser.arguments

    @property
    def consumer(self) -> PostgresBatchInsert:
        return PostgresBatchInsert(
            table_name='companies',
            batch_size=10,
        )

    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=CompanyGettingStage(
                scraper=TradingViewScraper(headless=self.args.headless),
            )
        )

    @property
    def producer(self):
        return SingleItemProducer({})


if __name__ == "__main__":
    Worker().main()
