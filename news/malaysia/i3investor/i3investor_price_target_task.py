from workflow.pipeline import Pipeline

from ..announcement_task import AnnouncementTask
from .price_target_getting_stage import PriceTargetGettingStage
from .scraper.i3investor_scraper import I3investorScraper


class I3investorPriceTargetTask(AnnouncementTask):
    @property
    def pipeline(self) -> Pipeline:
        scraper = I3investorScraper(headless=self.headless)
        return Pipeline(
            stage=PriceTargetGettingStage(
                scraper=scraper,
            )
        )
