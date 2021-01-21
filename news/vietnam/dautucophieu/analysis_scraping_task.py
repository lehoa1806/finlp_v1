from workflow.pipeline import Pipeline

from ..workflow import AnnouncementScraperTask
from .analysis_getting_stage import AnalysisGettingStage
from .scraper.dtcp_scraper import DauTuCoPhieuScraper


class DauTuCoPhieuAnnouncement(AnnouncementScraperTask):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=AnalysisGettingStage(
                scraper=DauTuCoPhieuScraper(headless=self.headless),
            )
        )
