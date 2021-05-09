from typing import Any, Dict, Iterator

from news.utils.common import NEWS_QUERY
from utils.postgresql.database import Database
from workflow.stage import Stage


class ArticleQueryingStage(Stage):
    def __init__(
        self,
    ) -> None:
        super().__init__('News2Email Querying')
        self.database = Database.load_default_database()

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        query = NEWS_QUERY.format(table='news_to_email_all')
        keys = (
            'news_id',
            'Time',
            'Title',
            'Category',
            'Source',
            'Url',
            'Content',
        )
        for data in self.database.query(query=query, keys=keys):
            yield {
                'news_id': data.get('news_id'),
                'Time': data.get('Time'),
                'Title': data.get('Title'),
                'Category': data.get('Category'),
                'Source': data.get('Source'),
                'Url': data.get('Url'),
            }
