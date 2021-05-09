from typing import Dict, Iterator, List

from selenium.common.exceptions import NoSuchElementException

from machine.scraper import Scraper


class TheStarScraper(Scraper):
    def load_business_page(self, page: int = 0) -> None:
        url = (
            'https://www.thestar.com.my/news/latest?pgno={page}&'
            'tag=Business#Latest'
        ).format(page=page)
        self.load_url(url.format(page))

    def get_articles(self, page: int = 0) -> Iterator[Dict[str, str]]:
        self.load_business_page(page=page)
        articles: List[Dict[str, str]] = []
        rows = self.wait_for_css_visibility(
            'body > div > div > main > div.container > div.row > div > div > '
            'div > div > section > div > div > ul.timeline'
        )
        for row in rows.find_elements_by_css_selector('li.row'):
            category_elem = row.find_element_by_css_selector('div > div > a')
            category = category_elem.text.strip()
            title_elem = row.find_element_by_css_selector('div > div > h2 > a')
            title = title_elem.text.strip()
            url = title_elem.get_attribute('href')
            time_elem = row.find_element_by_css_selector('div > time')
            estimated_time = time_elem.text.strip()
            articles.append({
                'category': category,
                'title': title,
                'url': url,
                'estimated_time': estimated_time,
            })
        yield from articles

    def read_article(
        self,
        url: str
    ) -> Dict[str, str]:
        self.load_url(url)
        html_page = self.browser.find_element_by_tag_name('html')
        date = self.wait_for_css_visibility(
            'body > div > div > main > div.container > div.row > div > div > '
            'div > ul > li > p.date'
        ).text.strip()
        try:
            time = html_page.find_element_by_tag_name(
                'body > div > div > main > div.container > div.row > div > '
                'div > div > ul > li > time.timestamp'
            ).text.strip()[:-4]
        except NoSuchElementException:
            time = ''
        content = self.wait_for_css_visibility(
            'body > div > div > main > div.container > div.row > div > div > '
            'div > article > div.story'
        ).get_attribute('innerHTML') or ''
        return {
            'date': date,
            'time': time,
            'content': content,
        }
