from workflow.pipeline import Pipeline

from ..workflow import AnnouncementScraperJob
from .analysis_getting_stage import AnalysisGettingStage
from .scraper.dtcp_scraper import DauTuCoPhieuScraper


class DTCPWorker(AnnouncementScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=AnalysisGettingStage(
                scraper=DauTuCoPhieuScraper(headless=self.args.headless),
            )
        )


if __name__ == "__main__":
    DTCPWorker().main()
