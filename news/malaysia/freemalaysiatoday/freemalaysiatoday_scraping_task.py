from news.article_filtering_stage import ArticleFilteringStage
from workflow.pipeline import Pipeline

from ..workflow import NewsScraperTask
from .articles_getting_stage import ArticlesGettingStage
from .scraper.freemalaysiatoday_scraper import FreeMalaysiaTodayScraper


class FreeMalaysiaTodayScrapingTask(NewsScraperTask):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=ArticlesGettingStage(
                scraper=FreeMalaysiaTodayScraper(headless=self.headless),
            )
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=self.filter,
                source='freemalaysiatoday.com',
            )
        )
