from experiential.news.filter import Filter
from experiential.news.news_job import ScraperJob
from workflow.pipeline import Pipeline

from ..article_filtering_stage import ArticleFilteringStage
from .articles_getting_stage import ArticlesGettingStage
from .scraper.thestar_scraper import TheStarScraper


class Worker(ScraperJob):
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
    Worker(table='malaysia_articles').main()
