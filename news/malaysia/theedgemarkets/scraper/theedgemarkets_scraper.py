from typing import Dict, List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from machine.scraper import Scraper


class TheEdgeMarketsScraper(Scraper):
    def load_malaysia_page(
        self,
        page: int = 0,
    ):
        url = 'https://www.theedgemarkets.com/categories/malaysia?page={}'
        self.load_url(url.format(page))

    def get_articles_board(self) -> WebElement:
        try:
            main_content_class = 'main-content-inner'
            main_content_el = self.wait_for_class_visibility(
                main_content_class)
            content_class = 'views-view-grid'
            content_el = main_content_el.find_element_by_class_name(
                content_class)
            return content_el
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get Articles board')

    def get_articles_rows(self) -> List[WebElement]:
        try:
            articles_board = self.get_articles_board()
            class_name = 'views-row'
            return articles_board.find_elements_by_class_name(class_name)
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get Articles row')

    @classmethod
    def get_articles_in_row(
        cls,
        row: WebElement,
    ) -> List[WebElement]:
        try:
            class_name = 'grid'
            columns = row.find_elements_by_class_name(class_name)
            return [
                column.find_element_by_css_selector('div') for column in
                columns
            ]
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get Articles in row')

    @classmethod
    def get_article_content(
        cls,
        article: WebElement
    ) -> Dict[str, str]:
        try:
            date_time = article.find_element_by_css_selector(
                'div.views-field-created > span.field-content'
            ).text
            url = article.find_element_by_css_selector(
                'div > div.views-field-title > span.field-content > a'
            ).get_attribute('href')
            title = article.find_element_by_css_selector(
                'div > div.views-field-title > span.field-content > a'
            ).text.strip()
            return {
                'title': title,
                'time': date_time,
                'url': url,
            }
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get Articles content')

    def get_articles_in_page(self) -> List[Dict[str, str]]:
        articles: List[Dict[str, str]] = []
        rows = self.get_articles_rows()
        for row in rows:
            articles_in_row = self.get_articles_in_row(row)
            for article in articles_in_row:
                articles.append(self.get_article_content(article))
        return articles

    def read_article(
        self,
        url: str
    ) -> Dict[str, str]:
        self.load_url(url)
        try:
            main_content_class = 'main-content-inner'
            main_content_el = self.wait_for_class_visibility(
                main_content_class)
            block_content_el = main_content_el.find_element_by_css_selector(
                'div.content-main > div > div > div > div.block-content > '
                'div > article'
            )
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get Articles board')

        try:
            title = block_content_el.find_element_by_css_selector(
                'div.post-title > h1'
            ).text.strip()
            content = block_content_el.find_element_by_css_selector(
                'div > div.post-content > div.article_content > div > '
                'div.field-items'
            ).get_attribute('innerHTML')
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get Articles in row')

        try:
            category = block_content_el.find_element_by_css_selector(
                'div.post-options > span > div > div > div > a'
            ).text.strip()
        except NoSuchElementException:
            category = ''

        return {
            'title': title,
            'category': category,
            'content': content,
        }
