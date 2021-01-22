from workflow.pipeline import Pipeline

from ..workflow import NewsScraperJob
from .cafef_getting_stage import CafefGettingStage
from .scraper.cafef_scraper import CafefScraper


class CafefWorker(NewsScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=CafefGettingStage(
                scraper=CafefScraper(headless=self.args.headless),
            )
        )


if __name__ == "__main__":
    CafefWorker().main()
