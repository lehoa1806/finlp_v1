from typing import Any, Dict, Iterator

from workflow.stage import Stage

from .scraper.tradingview_scraper import TradingViewScraper


class CompanyGettingStage(Stage):
    def __init__(
        self,
        scraper: TradingViewScraper,
    ) -> None:
        super().__init__('TradingView Stock ID')
        self.scraper = scraper

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        for company in self.scraper.get_companies():
            yield {
                'stock_id': company.get('stock_id'),
                'company_name': company.get('company_name'),
                'industry': company.get('industry_name', ''),
                'sector': company.get('sector_name', ''),
            }
