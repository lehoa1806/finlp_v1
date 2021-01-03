from typing import Any, Dict, Iterator

from workflow.stage import Stage

from .scraper.theedgemarkets_scraper import TheEdgeMarketsScraper


class ArticleReadingStage(Stage):
    def __init__(
        self,
        scraper: TheEdgeMarketsScraper,
    ) -> None:
        super().__init__('The Edge Markets Reading')
        self.scraper = scraper

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        data = self.scraper.read_article(item['url'])
        data.update(item)
        yield data
