from workflow.pipeline import Pipeline

from ..article_filtering_stage import ArticleFilteringStage
from ..news_task import NewsTask
from .articles_getting_stage import ArticlesGettingStage
from .scraper.malaymail_scraper import MalayMailScraper


class MalayMailScrapingTask(NewsTask):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=ArticlesGettingStage(
                scraper=MalayMailScraper(headless=self.headless),
            )
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=self.filter,
                source='malaymail.com',
            )
        )
