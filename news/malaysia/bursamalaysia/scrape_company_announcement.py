from news.malaysia.bursamalaysia.announcements_getting_stage import \
    AnnouncementsGettingStage
from news.malaysia.scraper_job import ScraperJob
from workflow.pipeline import Pipeline

from .scraper.bursamalaysia_scraper import BursaMalaysiaScraper


class Worker(ScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=AnnouncementsGettingStage(
                scraper=BursaMalaysiaScraper(headless=self.args.headless),
                max_pages_to_load=100,
                get_known=self.args.get_known,
            )
        )


if __name__ == "__main__":
    Worker(table='announcements').main()
