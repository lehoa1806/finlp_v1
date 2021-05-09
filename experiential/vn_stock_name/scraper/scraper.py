from typing import Dict, Iterator

from machine.scraper import Scraper


class CafeFLiveBoardScraper(Scraper):
    def get_stocks(self) -> Iterator[Dict[str, str]]:
        self.wait_for_css_presence(
            css_selector='body > div > table > tbody > tr > td > label')
        for row in self.find_elements_by_css_selector(
            css_selector='body > div > table > tbody > tr'
        ):
            stock_elem = row.find_element_by_css_selector(
                css_selector='td > label'
            )
            # To get "title"
            self.mouse_over(stock_elem)
            stock_id = stock_elem.text.strip()
            stock_name = stock_elem.get_attribute('title').strip()
            yield {
                'id': stock_id,
                'name': stock_name,
            }
