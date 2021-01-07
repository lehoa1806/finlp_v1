from workflow.pipeline import Pipeline

from ..article_filtering_stage import ArticleFilteringStage
from ..news_task import NewsTask
from .articles_getting_stage import ArticlesGettingStage
from .scraper.theedgemarkets_scraper import TheEdgeMarketsScraper


class TheEdgeMarketsScrapingTask(NewsTask):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=ArticlesGettingStage(
                scraper=TheEdgeMarketsScraper(headless=self.headless),
            )
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=self.filter,
                source='theedgemarkets.com',
            )
        )
