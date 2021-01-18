from workflow.pipeline import Pipeline

from ..workflow import AnnouncementScraperJob
from .announcements_getting_stage import AnnouncementsGettingStage
from .scraper.bursamalaysia_scraper import BursaMalaysiaScraper


class Worker(AnnouncementScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=AnnouncementsGettingStage(
                scraper=BursaMalaysiaScraper(headless=self.args.headless),
                max_pages_to_load=100,
            )
        )


if __name__ == "__main__":
    Worker().main()
