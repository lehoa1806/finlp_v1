from news.article_filtering_stage import ArticleFilteringStage
from workflow.pipeline import Pipeline

from ..filter import Filter
from ..workflow import NewsScraperJob
from .scraper.tnck_scraper import TTCKScraper
from .tnck_getting_stage import TNCKGettingStage


class TNCKWorker(NewsScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=TNCKGettingStage(
                scraper=TTCKScraper(headless=self.args.headless),
            )
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=Filter(),
                source='tinnhanhchungkhoan.vn',
                pass_through=True,
            )
        )


if __name__ == "__main__":
    TNCKWorker().main()
