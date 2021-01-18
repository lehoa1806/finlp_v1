from news.article_filtering_stage import ArticleFilteringStage
from news.malaysia.filter import Filter
from workflow.pipeline import Pipeline

from ..workflow import NewsScraperJob
from .articles_getting_stage import ArticlesGettingStage
from .scraper.thestar_scraper import TheStarScraper


class Worker(NewsScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=ArticlesGettingStage(
                scraper=TheStarScraper(headless=self.args.headless),
                max_pages_to_load=10,
            )
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=Filter(),
                source='thestar.com.my',
            )
        )


if __name__ == "__main__":
    Worker().main()
