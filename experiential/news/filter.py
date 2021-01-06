from experiential.filter import Filter as Ft


class Filter(Ft):
    @property
    def stock_info_table(self) -> str:
        """
        A table to store stocks' info:
          - stock_id
          - company short name
          - company full name
          - industry
          - sector
        :return: table name
        """
        return "malaysia_companies"

    @property
    def search_key_table(self) -> str:
        """
        A table to store customized search keys: holding/tracking stocks,
         special key words
          - search_key
          - subscription
        :return:
        """
        return "malaysia_search_keys"

    @property
    def category_table(self) -> str:
        """
        A table to store article categories (defined by the news media)
          - category
          - source
          - subscription
        :return:
        """
        return "malaysia_categories"
