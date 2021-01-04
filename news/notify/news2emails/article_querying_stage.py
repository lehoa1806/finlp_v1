from typing import Any, Dict, Iterator

from common.rule import Rule
from news.utils.common import NEWS_QUERY
from news.utils.filter import Filter
from workflow.stage import Stage


class ArticleQueryingStage(Stage):
    def __init__(
        self,
    ) -> None:
        super().__init__('News2Email Querying')
        ft = Filter()
        captured_list = ft.build_common_filter()
        categories = ft.lower_all(ft.get_categories())
        self.rule = Rule({
            'contains_any': [{'content': captured_list},
                             {'category': categories}]
        })

        self.database = ft.database

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
            category = data.get('Category', '').lower()
            content = data.get('Content', '').lower()
            source = data.get('Source', '').lower()
            if 'theedgemarkets' in source:
                content = content.replace(
                    'theedgemarkets', '').replace('the edge markets', '')
            if self.rule({
                'category': category,
                'content': content,
            }):
                yield {
                    'news_id': data.get('news_id'),
                    'Time': data.get('Time'),
                    'Title': data.get('Title'),
                    'Category': data.get('Category'),
                    'Source': data.get('Source'),
                    'Url': data.get('Url'),
                }
