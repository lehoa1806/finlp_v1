from typing import Dict, Set

from news.utils.common import Subscription
from postgresql.database import Database
from utils.decorators.functools import cached_property


class Filter:
    def __init__(self) -> None:
        self.database = Database.load_default_database()

    @property
    def stock_info_table(self) -> str:
        """
        A table to store stocks' info:
          - stock_id
          - company short name
          - company full name
        :return: table name
        """
        raise NotImplementedError

    @property
    def search_key_table(self) -> str:
        """
        A table to store customized search keys: holding/tracking stocks,
         special key words
          - search_key
          - subscription
        :return:
        """
        raise NotImplementedError

    @property
    def category_table(self) -> str:
        """
        A table to store article categories (defined by the news media)
          - category
          - subscription
        :return:
        """
        raise NotImplementedError

    @cached_property
    def stocks(self) -> Dict:
        """
        A dict of stock_id and company sort name
        :return: Dict
        """
        query = f'SELECT stock_id, short_name FROM {self.stock_info_table};'
        return {
            item['id'].lower(): (item.get('name') or item['id']).lower()
            for item in self.database.query(
                query=query, keys=('id', 'name'))
        }

    @cached_property
    def categories(self) -> Dict:
        query = f'SELECT category, subscription FROM {self.category_table};'
        return {
            item['category'].lower(): item['subscription']
            for item in self.database.query(
                query=query, keys=('category', 'subscription'))
        }

    @cached_property
    def search_keys(self) -> Dict:
        query = f'SELECT search_key, subscription ' \
                f'FROM {self.search_key_table};'
        return {
            item['search_key'].lower(): item['subscription']
            for item in self.database.query(
                query=query, keys=('search_key', 'subscription'))
        }

    @cached_property
    def stock_ids(self) -> Set:
        return set(self.stocks.keys())

    @cached_property
    def stock_names(self) -> Set:
        return set(self.stocks.values())

    @cached_property
    def categories_all(self) -> Set:
        return set(self.categories.keys())

    @cached_property
    def categories_hot(self) -> Set:
        return set(k for k, v in self.categories.items()
                   if v == Subscription.HOT.value)

    @cached_property
    def search_keys_all(self) -> Set:
        return set(self.search_keys.keys())

    @cached_property
    def search_keys_hot(self):
        return set(k for k, v in self.search_keys.items()
                   if v == Subscription.HOT.value)

    @cached_property
    def holding_ids(self):
        return set(k for k, v in self.search_keys.items()
                   if v == Subscription.HOLDING.value)

    @cached_property
    def holding_names(self):
        return set(
            self.stocks[k] for k in self.holding_ids if self.stocks.get(k)
        )

    @cached_property
    def excludes(self):
        return set(f' {k.lower()} ' for k, v in self.search_keys.items()
                   if v == Subscription.EXCLUDE.value)

    @cached_property
    def common_keys(self):
        _stock_names = set(f' {k} ' for k in self.stock_names)
        _stock_ids = set(f' {k} ' for k in self.stock_ids)
        _keys_total = set(f' {k} ' for k in self.search_keys_all)
        return _stock_names.union(_stock_ids).union(_keys_total).difference(
            self.excludes)

    @cached_property
    def holding_keys(self):
        _holding_names = set(f' {k} ' for k in self.holding_names)
        _holding_ids = set(f' {k} ' for k in self.holding_ids)
        return _holding_names.union(_holding_ids).difference(self.excludes)

    @cached_property
    def hot_keys(self):
        _keys_hot = set(' {} '.format(key) for key in self.search_keys_hot)
        return _keys_hot.difference(self.excludes).union(self.holding_keys)

    @cached_property
    def common_categories(self):
        return self.categories_all

    @cached_property
    def hot_categories(self):
        return self.categories_hot
