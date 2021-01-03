from news.malaysia.freemalaysiatoday.articles_filtering_stage import \
    ArticleFilteringStage
from news.malaysia.freemalaysiatoday.articles_getting_stage import \
    ArticlesGettingStage
from news.malaysia.scraper_job import ScraperJob
from workflow.pipeline import Pipeline

from .scraper.freemalaysiatoday_scraper import FreeMalaysiaTodayScraper


class Worker(ScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=ArticlesGettingStage(
                scraper=FreeMalaysiaTodayScraper(headless=self.args.headless),
                get_known=self.args.get_known,
            )
        ).add_stage(
            stage=ArticleFilteringStage()
        )


if __name__ == "__main__":
    Worker(table='articles').main()
