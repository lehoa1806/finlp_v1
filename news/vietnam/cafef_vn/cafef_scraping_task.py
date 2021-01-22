from workflow.pipeline import Pipeline

from ..workflow import NewsScraperTask
from .cafef_getting_stage import CafefGettingStage
from .scraper.cafef_scraper import CafefScraper


class CafefTask(NewsScraperTask):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=CafefGettingStage(
                scraper=CafefScraper(headless=self.headless),
            )
        )
