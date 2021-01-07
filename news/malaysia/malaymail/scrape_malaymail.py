from news.malaysia.filter import Filter
from news.malaysia.malaymail.scraper.malaymail_scraper import MalayMailScraper
from news.malaysia.news_job import ScraperJob
from workflow.pipeline import Pipeline

from ..article_filtering_stage import ArticleFilteringStage
from .articles_getting_stage import ArticlesGettingStage


class Worker(ScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=ArticlesGettingStage(
                scraper=MalayMailScraper(headless=self.args.headless),
            )
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=Filter(),
                source='malaymail.com',
            )
        )


if __name__ == "__main__":
    Worker(table='malaysia_articles').main()
