from workflow.pipeline import Pipeline

from ..workflow import AnnouncementScraperJob
from .price_target_getting_stage import PriceTargetGettingStage
from .scraper.i3investor_scraper import I3investorScraper


class Worker(AnnouncementScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        scraper = I3investorScraper(headless=self.args.headless)
        return Pipeline(
            stage=PriceTargetGettingStage(
                scraper=scraper,
            )
        )


if __name__ == "__main__":
    Worker().main()
