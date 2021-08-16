import re
from datetime import datetime, timedelta
from typing import Dict, Iterator

import pytz
from selenium.common.exceptions import NoSuchElementException

from machine.scraper import Scraper
from news.utils.common import VN_TIMEZONE
from scraper.elements.button import Button


class TTCKScraper(Scraper):
    def load_tnck_home(self):
        url = 'https://tinnhanhchungkhoan.vn/chung-khoan/'
        self.load_url(url)

    @classmethod
    def get_time(cls, time: str) -> str:
        local_timezone = pytz.timezone(VN_TIMEZONE)
        now = datetime.utcnow()
        local_now = now.replace(tzinfo=pytz.utc).astimezone(
            local_timezone)
        if re.compile(r'^\d* giờ trước$').match(time):
            return (
                local_now - timedelta(hours=int(time[:-10]))
            ).strftime('%d/%m/%Y %H:%M:%S')
        elif re.compile(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$').match(time):
            return f'{time}:00'
        else:
            return local_now.strftime('%d/%m/%Y %H:%M:%S')

    def get_highlight(self):
        try:
            article = self.find_element_by_css_selector(
                'body > div.wrapper.category-page > div > div.container > '
                'div > div > div.main-column > div.category-highlight > div > '
                'div.rank-1 > article > h2 > a'
            )
            url = article.get_attribute('href')
            title = article.text.strip()
            time = self.find_element_by_css_selector(
                'body > div.wrapper.category-page > div > div.container > '
                'div > div > div.main-column > div.category-highlight > '
                'div > div.rank-1 > article > div.story__meta > time'
            ).text.strip()
            timestamp = self.get_time(time)
            yield {
                'datetime': timestamp,
                'title': title,
                'url': url,
            }
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get highlighted article')

    def get_rank2_articles(self):
        try:
            articles = self.find_elements_by_css_selector(
                'body > div.wrapper.category-page > div > div.container > '
                'div > div > div.main-column > div.category-highlight > '
                'div > div.rank-2 > article'
            )
            for article in articles:
                title_elem = article.find_element_by_css_selector(
                    css_selector='h2 > a'
                )
                url = title_elem.get_attribute('href')
                title = title_elem.text.strip()
                time = article.find_element_by_css_selector(
                    css_selector='div > time'
                ).text.strip()
                timestamp = self.get_time(time)
                yield {
                    'datetime': timestamp,
                    'title': title,
                    'url': url,
                }
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get rank2 article')

    def get_articles(self) -> Iterator[Dict[str, str]]:
        for _ in range(5):
            try:
                Button(self.find_element_by_css_selector(
                    css_selector='#viewmore'
                )).click()
            except NoSuchElementException:
                pass
        try:
            for article in self.find_elements_by_css_selector(
                'body > div.wrapper.category-page > div > div.container > '
                'div > div > div.main-column > div.category-timeline > '
                'div.box-content > article'
            ):
                title_elem = article.find_element_by_css_selector(
                    css_selector='h2 > a'
                )
                url = title_elem.get_attribute('href')
                title = title_elem.text.strip()
                time = article.find_element_by_css_selector(
                    css_selector='div > time'
                ).text.strip()
                timestamp = self.get_time(time)
                yield {
                    'datetime': timestamp,
                    'title': title,
                    'url': url,
                }
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get Articles row')
