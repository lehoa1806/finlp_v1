from workflow.pipeline import Pipeline

from ..workflow import NewsScraperTask
from .scraper.vietstock_scraper import VietStockScraper
from .vietstock_getting_stage import VietStockGettingStage


class VietStockTask(NewsScraperTask):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=VietStockGettingStage(
                scraper=VietStockScraper(headless=self.headless),
            )
        )
