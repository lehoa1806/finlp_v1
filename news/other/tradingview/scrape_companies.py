from argparse import Namespace

from machine.postgres_batch_insert import PostgresBatchInsert
from utils.argument_parser import ArgumentParser
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer

from .company_getting_stage import CompanyGettingStage
from .scraper.tradingview_scraper import TradingViewScraper

COMPANY_TABLES = {
    'Malaysia': 'malaysia_companies',
    'Vietnam': 'vietnam_companies',
}
COMPANY_URLS = {
    'Malaysia': 'https://www.tradingview.com/markets/stocks-malaysia/'
                'sectorandindustry-industry/',
    'Vietnam': 'https://www.tradingview.com/markets/stocks-vietnam/'
               'sectorandindustry-industry/',
}


class Worker(Job):
    def __init__(self) -> None:
        super().__init__()
        self.table = COMPANY_TABLES.get(self.args.country)
        self.url = COMPANY_URLS.get(self.args.country)

    def parse_args(self) -> Namespace:
        parser = ArgumentParser(
            description='Script to collect Stock ID from TradingView',
        )
        parser.add_argument(
            '--country',
            choices=['Malaysia', 'Vietnam'],
            type=str,
            required=True,
            help='Country'
        )
        parser.add_argument(
            '--headless', action='store_true',
            help='Run in headless mode',
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
        return Pipeline(
            stage=CompanyGettingStage(
                scraper=TradingViewScraper(headless=self.args.headless),
                url=self.url,
            )
        )

    @property
    def producer(self):
        return SingleItemProducer({})


if __name__ == "__main__":
    Worker().main()
