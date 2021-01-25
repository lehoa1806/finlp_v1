from news.article_filtering_stage import ArticleFilteringStage
from workflow.pipeline import Pipeline

from ..filter import Filter
from ..workflow import NewsScraperJob
from .fireant_getting_stage import FireAntGettingStage
from .scraper.fireant_scraper import FireAntScraper


class FireAntWorker(NewsScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=FireAntGettingStage(
                scraper=FireAntScraper(headless=self.args.headless),
            )
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=Filter(),
                source='fireant.vn',
                pass_through=True,
            )
        )


if __name__ == "__main__":
    FireAntWorker().main()
