from news.malaysia.announcement_job import ScraperJob
from news.malaysia.bursamalaysia.announcements_getting_stage import \
    AnnouncementsGettingStage
from news.malaysia.bursamalaysia.scraper.bursamalaysia_scraper import \
    BursaMalaysiaScraper
from workflow.pipeline import Pipeline


class Worker(ScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=AnnouncementsGettingStage(
                scraper=BursaMalaysiaScraper(headless=self.args.headless),
                max_pages_to_load=100,
            )
        )


if __name__ == "__main__":
    Worker(table='malaysia_announcements').main()
