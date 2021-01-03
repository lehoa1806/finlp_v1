from typing import Dict, List

from selenium.common.exceptions import NoSuchElementException

from scraper.scraper import Scraper


class MalayMailScraper(Scraper):
    def load_malaymail_money(
        self,
        date: str,
    ):
        """
        '%Y/%m/%d'
        :param date: '2020/05/06/'
        :return:
        """
        url = 'https://www.malaymail.com/news/money/{}'.format(date)
        self.load_url(url)

    def load_malaymail_malaysia(
        self,
        date: str,
    ):
        """
        '%Y/%m/%d'
        :param date: '2020/05/06/'
        :return:
        """
        url = 'https://www.malaymail.com/news/malaysia/{}'.format(date)
        self.load_url(url)

    def get_malaysia_articles(self, date: str) -> List[Dict[str, str]]:
        # Read malaysia tag
        self.load_malaymail_malaysia(date)
        return self.get_articles()

    def get_money_articles(self, date: str) -> List[Dict[str, str]]:
        # Read money tag
        self.load_malaymail_money(date)
        return self.get_articles()

    def get_articles(self) -> List[Dict[str, str]]:
        articles: List[Dict[str, str]] = []
        while True:
            page = self.browser.find_element_by_tag_name('html')
            # Safety handle for "No articles found."
            try:
                alert = page.find_element_by_css_selector(
                    'body > div.content > section.article > div.container > '
                    'div.row > div > div > p'
                )
                if 'no articles found' in alert.text.strip().lower():
                    break
            except NoSuchElementException:
                pass
            table = self.wait_for_css_visibility(
                'body > div.content > section.article > div.container > '
                'div.row > div > table.table > tbody'
            )
            table_rows = table.find_elements_by_css_selector('tr > td > a')
            articles.extend([{
                'title': row.text.strip(),
                'url': row.get_attribute('href')
            } for row in table_rows])
            try:
                buttons = page.find_elements_by_css_selector(
                    'body > div.content > section.article > div.container > '
                    'div > div > div > div > div > ul > li'
                )
                if len(buttons) != 2:
                    break
                next_button = buttons[1].find_element_by_css_selector('a')
                next_url = next_button.get_attribute('href')
                if not next_url:
                    break
                self.load_url(next_url)
            except NoSuchElementException:
                break
        return articles

    def read_article(
        self,
        url: str
    ) -> Dict[str, str]:
        self.load_url(url)
        page = self.browser.find_element_by_tag_name('html')
        title_elem = self.wait_for_css_visibility(
            'body > div.content > section.article > div.container > '
            'div.row > div > h1'
        )
        title = title_elem.text.strip()
        time_elem = page.find_element_by_css_selector(
            'body > div.content > section.article > div.container > '
            'div.row > div > div > p'
        )
        time = time_elem.text.strip()
        content_elem = page.find_element_by_css_selector(
            'body > div.content > section.article > div.container > '
            'div.row > div > article'
        )
        content = content_elem.get_attribute('innerHTML')
        return {
            'title': title,
            'time': time,
            'content': content,
        }
