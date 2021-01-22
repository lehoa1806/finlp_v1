from workflow.pipeline import Pipeline

from ..workflow import NewsScraperJob
from .scraper.tnck_scraper import TTCKScraper
from .tnck_getting_stage import TNCKGettingStage


class TNCKWorker(NewsScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=TNCKGettingStage(
                scraper=TTCKScraper(headless=self.args.headless),
            )
        )


if __name__ == "__main__":
    TNCKWorker().main()
