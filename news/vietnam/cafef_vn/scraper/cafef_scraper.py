from datetime import datetime
from typing import Dict, Iterator

import pytz
from selenium.common.exceptions import NoSuchElementException

from machine.scraper import Scraper
from news.utils.common import VN_TIMEZONE


class CafefScraper(Scraper):
    def load_cafef_home(self):
        url = 'https://cafef.vn/thi-truong-chung-khoan.chn'
        self.load_url(url)

    @classmethod
    def get_time(cls) -> str:
        local_timezone = pytz.timezone(VN_TIMEZONE)
        now = datetime.utcnow()
        local_now = now.replace(tzinfo=pytz.utc).astimezone(
            local_timezone)
        return local_now.strftime('%Y-%m-%d %H:%M:%S')

    def get_highlight(self):
        try:
            article = self.find_element_by_css_selector(
                '#form1 > div.cate-page > div.adm-mainsection > div > '
                'div.left_cate > div > div.left > div > div > h2 > a'
            )
            url = article.get_attribute('href')
            title = article.text.strip()
            timestamp = self.get_time()
            yield {
                'datetime': timestamp,
                'title': title,
                'category': 'Highlight',
                'url': url,
            }
            for article in self.find_elements_by_css_selector(
                '#form1 > div.cate-page > div.adm-mainsection > '
                'div > div.left_cate > div.noibat_cate > div.left > '
                'div > ul > li > h3 > a'
            ):
                url = article.get_attribute('href')
                title = article.text.strip()
                timestamp = self.get_time()
                yield {
                    'datetime': timestamp,
                    'title': title,
                    'category': 'Highlight',
                    'url': url,
                }
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get highlighted article')

    def get_articles(self) -> Iterator[Dict[str, str]]:
        _time = datetime.utcnow()
        while True:
            try:
                self.scroll()
                articles = self.find_elements_by_css_selector(
                    css_selector='#LoadListNewsCat > li'
                )
                if len(articles) > 32:
                    break
                if (datetime.utcnow() - _time).seconds > 180:
                    break
            except NoSuchElementException:
                pass
        try:
            for article in articles:
                try:
                    category = article.find_element_by_css_selector(
                        css_selector='div > p.top5_news_mack.magiaodich'
                    ).text.strip()
                except NoSuchElementException:
                    category = 'N/A'
                title_elem = article.find_element_by_css_selector(
                    css_selector='h3 > a'
                )
                url = title_elem.get_attribute('href')
                title = title_elem.text.strip()
                timestamp = self.get_time()
                yield {
                    'datetime': timestamp,
                    'title': title,
                    'category': category,
                    'url': url,
                }
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get Articles row')
