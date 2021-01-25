from news.article_filtering_stage import ArticleFilteringStage
from workflow.pipeline import Pipeline

from ..filter import Filter
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
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=Filter(),
                source='vietstock.vn',
                pass_through=True,
            )
        )


if __name__ == "__main__":
    VietStockWorker().main()
