from news.malaysia.scraper_job import ScraperJob
from workflow.pipeline import Pipeline

from .articles_filtering_stage import ArticleFilteringStage
from .articles_getting_stage import ArticlesGettingStage
from .scraper.malaymail_scraper import MalayMailScraper


class Worker(ScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=ArticlesGettingStage(
                scraper=MalayMailScraper(headless=self.args.headless),
                get_known=self.args.get_known,
            )
        ).add_stage(
            stage=ArticleFilteringStage()
        )


if __name__ == "__main__":
    Worker(table='articles').main()
