from workflow.pipeline import Pipeline

from ..workflow import AnnouncementScraperTask
from .announcements_getting_stage import AnnouncementsGettingStage
from .scraper.bursamalaysia_scraper import BursaMalaysiaScraper


class BursaMalaysiaAnnouncement(AnnouncementScraperTask):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=AnnouncementsGettingStage(
                scraper=BursaMalaysiaScraper(headless=self.headless),
                max_pages_to_load=100,
            )
        )
