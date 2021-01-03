from news.malaysia.scraper_job import ScraperJob
from workflow.pipeline import Pipeline

from .price_target_getting_stage import PriceTargetGettingStage
from .scraper.i3investor_scraper import I3investorScraper


class Worker(ScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        scraper = I3investorScraper(headless=self.args.headless)
        return Pipeline(
            stage=PriceTargetGettingStage(
                scraper=scraper,
                get_known=self.args.headless,
            )
        )


if __name__ == "__main__":
    Worker(table='announcements').main()
