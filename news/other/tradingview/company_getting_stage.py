import logging
from typing import Any, Dict, Iterator

from workflow.stage import Stage

from .scraper.tradingview_scraper import TradingViewScraper


class CompanyGettingStage(Stage):
    def __init__(
        self,
        scraper: TradingViewScraper,
        url: str,
    ) -> None:
        super().__init__('TradingView Stock ID')
        self.scraper = scraper
        self.url = url

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        logging.info('Load Sector & Industry page')
        self.scraper.load_url(self.url)

        for company in self.scraper.get_companies():
            yield {
                'stock_id': company.get('stock_id'),
                'name': company.get('company_name'),
                'industry': company.get('industry_name', ''),
                'sector': company.get('sector_name', ''),
            }
