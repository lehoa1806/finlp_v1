from news.malaysia.filter import Filter
from news.malaysia.freemalaysiatoday.articles_getting_stage import \
    ArticlesGettingStage
from news.malaysia.freemalaysiatoday.scraper.freemalaysiatoday_scraper import \
    FreeMalaysiaTodayScraper
from news.malaysia.news_job import ScraperJob
from workflow.pipeline import Pipeline

from ..article_filtering_stage import ArticleFilteringStage


class Worker(ScraperJob):
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
    Worker(table='malaysia_articles').main()
