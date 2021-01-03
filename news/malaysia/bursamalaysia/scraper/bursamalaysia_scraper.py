from typing import Dict, Iterator

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from scraper.scraper import Scraper


class BursaMalaysiaScraper(Scraper):
    def load_company_announcement_page(
        self,
        page: int = 0,
    ):
        url = (f'https://www.bursamalaysia.com/market_information/'
               f'announcements/company_announcement?per_page=50&page={page}')
        self.load_url(url)

    def get_company_announcement_board(self) -> WebElement:
        return self.wait_for_css_visibility(
            'body > div > section > div > div > div > div > div > div '
            'table > tbody')

    def get_announcements(self) -> Iterator[Dict[str, str]]:
        try:
            announcement_table = self.get_company_announcement_board()
            rows = announcement_table.find_elements_by_css_selector('tr')
            for row in rows:
                columns = row.find_elements_by_css_selector('td')
                date = columns[1].text.strip()
                try:
                    company = columns[2].find_element_by_css_selector(
                        'a').text.strip()
                except NoSuchElementException:
                    company = 'N/A'
                title = columns[3].find_element_by_css_selector(
                    'a').text.strip()
                url = columns[3].find_element_by_css_selector(
                    'a').get_attribute('href')
                try:
                    edited = columns[3].find_element_by_css_selector(
                        'span').text.strip()
                    title = '{} {}'.format(title, edited)
                except NoSuchElementException:
                    pass
                try:
                    description = columns[3].find_element_by_css_selector(
                        'p').text.strip()
                except NoSuchElementException:
                    description = 'N/A'
                yield {
                    'date': date,
                    'company': company,
                    'title': title,
                    'url': url,
                    'description': description,
                }
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get Articles row')
