from workflow.pipeline import Pipeline

from ..workflow import NewsScraperJob
from .fireant_getting_stage import FireAntGettingStage
from .scraper.fireant_scraper import FireAntScraper


class FireAntWorker(NewsScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=FireAntGettingStage(
                scraper=FireAntScraper(headless=self.args.headless),
            )
        )


if __name__ == "__main__":
    FireAntWorker().main()
