from workflow.pipeline import Pipeline

from ..workflow import NewsScraperTask
from .fireant_getting_stage import FireAntGettingStage
from .scraper.fireant_scraper import FireAntScraper


class FireAntTask(NewsScraperTask):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=FireAntGettingStage(
                scraper=FireAntScraper(headless=self.headless),
            )
        )
