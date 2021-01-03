import json
from datetime import datetime
from typing import Any, Dict, Iterator

from common.rule import Rule
from news.utils.filter import Filter
from workflow.stage import Stage


class ArticleFilteringStage(Stage):
    def __init__(
        self,
    ) -> None:
        super().__init__('The Star Filtering')
        ft = Filter()
        captured_list = ft.build_common_filter()
        self.rule = Rule({
            'contains_any': [{'content': captured_list},
                             {'title': captured_list}],
        })

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        content = item.get('content', '')
        title = item.get('title', '')
        if self.rule({
            'title': title.lower(),
            'content': content.lower().replace('thestar', ''),
        }):
            yield {
                'date_added': datetime.utcnow(),
                'article_date': item.get('datetime'),
                'article_name': item.get('title', ''),
                'article_source': 'thestar.com.my',
                'article_detail': json.dumps({
                    'time': item.get('time', ''),
                    'title': item.get('title', ''),
                    'category': item.get('category', ''),
                    'content': content,
                }),
                'article_url': item.get('url', ''),
            }
