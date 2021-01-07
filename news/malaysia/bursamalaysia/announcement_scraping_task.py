from workflow.pipeline import Pipeline

from ..announcement_task import AnnouncementTask
from .announcements_getting_stage import AnnouncementsGettingStage
from .scraper.bursamalaysia_scraper import BursaMalaysiaScraper


class BursaMalaysiaAnnouncement(AnnouncementTask):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=AnnouncementsGettingStage(
                scraper=BursaMalaysiaScraper(headless=self.headless),
                max_pages_to_load=100,
            )
        )
