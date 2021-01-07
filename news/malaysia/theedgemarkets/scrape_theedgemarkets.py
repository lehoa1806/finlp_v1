from news.malaysia.filter import Filter
from news.malaysia.news_job import ScraperJob
from news.malaysia.theedgemarkets.articles_getting_stage import \
    ArticlesGettingStage
from news.malaysia.theedgemarkets.scraper.theedgemarkets_scraper import \
    TheEdgeMarketsScraper
from workflow.pipeline import Pipeline

from ..article_filtering_stage import ArticleFilteringStage


class Worker(ScraperJob):
    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=ArticlesGettingStage(
                scraper=TheEdgeMarketsScraper(headless=self.args.headless),
            )
        ).add_stage(
            stage=ArticleFilteringStage(
                ft=Filter(),
                source='theedgemarkets.com',
            )
        )


if __name__ == "__main__":
    Worker(table='malaysia_articles').main()
