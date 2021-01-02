from typing import Iterable, List, Set

from postgresql.database import Database


class Filter:
    def __init__(self) -> None:
        self.database = Database.load_default_database()

    def get_categories(self) -> List[str]:
        query = 'SELECT category, data_source FROM categories;'
        return [
            category.get('category', '')
            for category in self.database.query(query, ('category', 'source'))
        ]

    def get_companies(self) -> List[str]:
        query = 'SELECT company_name FROM companies;'
        return [
            com.get('company', '')
            for com in self.database.query(query, ('company',))
        ]

    def get_company_short_names(self) -> List[str]:
        query = 'SELECT company_short_name FROM companies;'
        return [
            com.get('company_short_name', '')
            for com in self.database.query(query, ('company_short_name',))
        ]

    def get_stocks(self) -> List[str]:
        query = 'SELECT stock_id FROM companies;'
        return [
            com.get('stock', '')
            for com in self.database.query(query, ('stock',))
        ]

    def get_search_keys(self) -> List[str]:
        query = 'SELECT search_key FROM search_keys;'
        return [
            item.get('search_key', '')
            for item in self.database.query(query, ('search_key',))
        ]

    @classmethod
    def lower_all(cls, input_list: Iterable[str]) -> List[str]:
        return [elem.lower() for elem in input_list]

    def build_common_filter(self) -> Set[str]:
        # A list of common keys which cause false positive matches
        _excludes = set('at')
        search_keys = [
            ' {} '.format(key) for key in self.get_search_keys()]
        companies = [
            ' {} '.format(com) for com in self.get_companies()
        ]
        company_short_names = [
            ' {} '.format(com) for com in self.get_company_short_names()
        ]
        stocks = [
            ' {} '.format(stock) for stock in self.get_stocks()
        ]
        _keys = set(
            self.lower_all(
                search_keys + companies + company_short_names + stocks)
        ) - _excludes
        return _keys
