from typing import Dict, Iterator

from common.rule import Rule
from experiential.filter import Subscription
from experiential.news.filter import Filter
from workflow.stage import Stage


class ArticleFilteringStage(Stage):
    def __init__(
        self,
        ft: Filter,
        source: str,
    ) -> None:
        super().__init__()
        self.holding_rule = Rule({
            'contains_any': [{'content': ft.holding_keys},
                             {'title': ft.holding_keys}]
        })
        self.hot_rule = Rule({
            'contains_any': [{'content': ft.hot_keys},
                             {'category': ft.hot_categories},
                             {'title': ft.hot_keys}]
        })
        self.common_rule = Rule({
            'contains_any': [{'content': ft.common_keys},
                             {'category': ft.common_categories},
                             {'title': ft.common_keys}]
        })
        self.source = source

    def process(self, item: Dict) -> Iterator:
        content = item['content']
        category = item['category']
        article_date = item['datetime']
        title = item['title']
        content_to_filter = content.lower().replace(self.source, '')
        category_to_filter = category.lower()
        title_to_filter = title.lower()
        if self.holding_rule({
            'category': category_to_filter,
            'content': content_to_filter,
        }):
            yield {
                'subscription': Subscription.HOLDING,
                'datetime': article_date,
                'category': category,
                'title': item['title'],
                'source': self.source,
                'content': content,
                'url': item['url'],
            }
        elif self.hot_rule({
            'category': category_to_filter,
            'content': content_to_filter,
            'title': title_to_filter,
        }):
            yield {
                'subscription': Subscription.HOT,
                'datetime': article_date,
                'category': category,
                'title': item['title'],
                'source': self.source,
                'content': content,
                'url': item['url'],
            }
        elif self.common_rule({
            'category': category_to_filter,
            'content': content_to_filter,
            'title': title_to_filter,
        }):
            yield {
                'subscription': Subscription.TOTAL,
                'datetime': article_date,
                'category': category,
                'title': item['title'],
                'source': self.source,
                'content': content,
                'url': item['url'],
            }
