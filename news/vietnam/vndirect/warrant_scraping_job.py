from argparse import Namespace

from machine.postgres_batch_insert import PostgresBatchInsert
from utils.argument_parser import ArgumentParser
from workflow.consumer import Consumer
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer

from .scraper.vndirect_scraper import VnDirectScraper
from .warrant_getting_stage import WarrantGettingStage


class WarrantScraperJob(Job):
    @property
    def timezone(self) -> str:
        raise NotImplementedError

    def parse_args(self) -> Namespace:
        parser = ArgumentParser(
            description='Script to scrape VN30 warrants',
        )
        parser.add_argument(
            'headless', action='store_true',
            help='Run in headless mode',
        )

        return parser.arguments

    @property
    def consumer(self) -> Consumer:
        return PostgresBatchInsert(
            table_name='vietnam_warrants',
            batch_size=100,
        )

    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=WarrantGettingStage(
                scraper=VnDirectScraper(headless=self.args.headless, timeout=15),
            )
        )

    @property
    def producer(self):
        return SingleItemProducer({})


if __name__ == "__main__":
    WarrantScraperJob().main()
