from news.malaysia.announcement_job import ScraperJob
from news.malaysia.i3investor.scraper.i3investor_scraper import \
    I3investorScraper
from workflow.pipeline import Pipeline

from .price_target_getting_stage import PriceTargetGettingStage


class Worker(ScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        scraper = I3investorScraper(headless=self.args.headless)
        return Pipeline(
            stage=PriceTargetGettingStage(
                scraper=scraper,
            )
        )


if __name__ == "__main__":
    Worker(table='malaysia_announcements').main()
