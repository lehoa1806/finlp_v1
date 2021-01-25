from workflow.pipeline import Pipeline

from ..workflow import NewsScraperJob
from .scraper.vietstock_scraper import VietStockScraper
from .vietstock_getting_stage import VietStockGettingStage


class VietStockWorker(NewsScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=VietStockGettingStage(
                scraper=VietStockScraper(headless=self.args.headless),
            )
        )


if __name__ == "__main__":
    VietStockWorker().main()
