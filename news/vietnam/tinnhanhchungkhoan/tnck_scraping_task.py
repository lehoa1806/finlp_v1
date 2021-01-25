from news.article_filtering_stage import ArticleFilteringStage
from workflow.pipeline import Pipeline

from ..workflow import NewsScraperTask
from .scraper.tnck_scraper import TTCKScraper
from .tnck_getting_stage import TNCKGettingStage


class TNCKTask(NewsScraperTask):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=TNCKGettingStage(
                scraper=TTCKScraper(headless=self.headless),
            )
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=self.filter,
                source='tinnhanhchungkhoan.vn',
                pass_through=True,
            )
        )
