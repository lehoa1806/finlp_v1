from news.malaysia.scraper_job import ScraperJob
from workflow.pipeline import Pipeline

from .articles_filtering_stage import ArticleFilteringStage
from .articles_getting_stage import ArticlesGettingStage
from .articles_reading_stage import ArticleReadingStage
from .scraper.theedgemarkets_scraper import TheEdgeMarketsScraper


class Worker(ScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        scraper = TheEdgeMarketsScraper(headless=self.args.headless)
        return Pipeline(
            stage=ArticlesGettingStage(
                scraper=scraper,
                max_pages_to_load=10,
                get_known=self.args.get_known,
            )
        ).add_stage(
            stage=ArticleReadingStage(
                scraper=scraper,
            )
        ).add_stage(
            stage=ArticleFilteringStage()
        )


if __name__ == "__main__":
    Worker(table='articles').main()
