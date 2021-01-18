from news.article_filtering_stage import ArticleFilteringStage
from news.malaysia.filter import Filter
from workflow.pipeline import Pipeline

from ..workflow import NewsScraperJob
from .articles_getting_stage import ArticlesGettingStage
from .scraper.freemalaysiatoday_scraper import FreeMalaysiaTodayScraper


class Worker(NewsScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=ArticlesGettingStage(
                scraper=FreeMalaysiaTodayScraper(headless=self.args.headless),
            )
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=Filter(),
                source='freemalaysiatoday.com',
            )
        )


if __name__ == "__main__":
    Worker().main()
