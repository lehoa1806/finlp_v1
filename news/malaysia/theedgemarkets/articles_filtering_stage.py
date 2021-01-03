import json
from datetime import datetime
from typing import Any, Dict, Iterator

import pytz

from common.rule import Rule
from news.utils.filter import Filter
from workflow.stage import Stage


class ArticleFilteringStage(Stage):
    def __init__(
        self,
    ) -> None:
        super().__init__('The Edge Markets Filtering')
        ft = Filter()
        captured_list = ft.build_common_filter()
        categories = ft.lower_all(ft.get_categories())
        self.rule = Rule({
            'contains_any': [{'content': captured_list},
                             {'category': categories}]
        })

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        content = item.get('content', '')
        category = item.get('category', '')
        if self.rule({
            'category': category.lower(),
            'content': content.lower().replace(
                'theedgemarkets', '').replace('the edge markets', ''),
        }):
            time_str = item.get('time', '')
            local = pytz.timezone(time_str[20:])
            article_date = local.localize(
                datetime.strptime(time_str[:19], '%Y-%m-%d %H:%M:%S')
            )
            yield {
                'date_added': datetime.utcnow(),
                'article_date': article_date,
                'article_name': item.get('title', ''),
                'article_source': 'theedgemarkets.com',
                'article_detail': json.dumps({
                    'time': time_str,
                    'category': category,
                    'title': item.get('title', ''),
                    'content': content,
                }),
                'article_url': item.get('url', ''),
            }
