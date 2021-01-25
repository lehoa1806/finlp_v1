from news.article_filtering_stage import ArticleFilteringStage
from workflow.pipeline import Pipeline

from ..filter import Filter
from ..workflow import NewsScraperJob
from .cafef_getting_stage import CafefGettingStage
from .scraper.cafef_scraper import CafefScraper


class CafefWorker(NewsScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=CafefGettingStage(
                scraper=CafefScraper(headless=self.args.headless),
            )
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=Filter(),
                source='cafef.vn',
                pass_through=True,
            )
        )


if __name__ == "__main__":
    CafefWorker().main()
