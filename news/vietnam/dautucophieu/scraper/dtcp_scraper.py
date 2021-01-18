from typing import Dict, Iterator

from selenium.common.exceptions import NoSuchElementException

from scraper.scraper import Scraper


class DauTuCoPhieuScraper(Scraper):
    def load_phantichchungkhoan_page(self):
        url = 'https://dautucophieu.net/phan-tich-chung-khoan/'
        self.load_url(url)

    def get_analyses(self) -> Iterator[Dict[str, str]]:
        try:
            for row in self.find_elements_by_css_selector(
                    css_selector='#content > div.row > article > div.row'):
                url_title_el = row.find_element_by_css_selector('div > h4 > a')
                url = url_title_el.get_attribute('href')
                title = url_title_el.text.strip()
                description_el = row.find_element_by_css_selector('div > p')
                description = description_el.text.strip()
                company_el = row.find_element_by_css_selector('div > a')
                company = company_el.text.strip()
                date_el = row.find_elements_by_css_selector(
                    'div > div > time')[0]
                date = date_el.text.strip()
                yield {
                    'date': date,
                    'company': company,
                    'title': title,
                    'url': url,
                    'description': description,
                }
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get Articles row')
