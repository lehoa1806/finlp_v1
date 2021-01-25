from news.article_filtering_stage import ArticleFilteringStage
from workflow.pipeline import Pipeline

from ..workflow import NewsScraperTask
from .fireant_getting_stage import FireAntGettingStage
from .scraper.fireant_scraper import FireAntScraper


class FireAntTask(NewsScraperTask):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=FireAntGettingStage(
                scraper=FireAntScraper(headless=self.headless, timeout=15),
            )
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=self.filter,
                source='fireant.vn',
                pass_through=True,
            )
        )
