import logging
import re
from datetime import datetime, timedelta
from typing import Dict, Iterator

import pytz
from selenium.common.exceptions import NoSuchElementException

from machine.scraper import Scraper
from news.utils.common import VN_TIMEZONE


class VietStockScraper(Scraper):
    def load_vietstock_home(self):
        url = 'https://vietstock.vn/chung-khoan.htm/'
        self.load_url(url)

    @classmethod
    def get_time(cls, time: str) -> str:
        local_timezone = pytz.timezone(VN_TIMEZONE)
        now = datetime.utcnow()
        local_now = now.replace(tzinfo=pytz.utc).astimezone(
            local_timezone)
        if re.compile(r'^\d* phút trước').match(time):
            times = time.split()
            timestamp = (
                local_now - timedelta(minutes=int(times[0]))
            ).strftime('%d/%m/%Y %H:%M:%S')
        elif re.compile(r'^\d* giờ trước').match(time):
            times = time.split()
            timestamp = (
                local_now - timedelta(hours=int(times[0]))
            ).strftime('%d/%m/%Y %H:%M:%S')
        elif re.compile(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$').match(time):
            timestamp = f'{time}:00'
        else:
            timestamp = local_now.strftime('%d/%m/%Y %H:%M:%S')
        return timestamp

    def get_articles(self) -> Iterator[Dict[str, str]]:
        _num_of_articles = 0
        while True:
            try:
                articles = self.find_elements_by_css_selector(
                    css_selector='#channel-container > section > div'
                )
            except NoSuchElementException:
                raise NoSuchElementException('Failed to get Articles')

            for article in articles:
                try:
                    category_elem = article.find_element_by_css_selector(
                        css_selector='div > div > a > span'
                    )
                    category = category_elem.text.strip()
                except NoSuchElementException:
                    category = ''

                title_elem = article.find_element_by_css_selector(
                    css_selector='div > div > h2 > a'
                )
                time = article.find_element_by_css_selector(
                    css_selector='div > div > div > span'
                ).text.strip()
                try:
                    stock_id = article.find_element_by_css_selector(
                        css_selector='div > div > p > span'
                    ).text.strip()
                    category += f': {stock_id}'
                except NoSuchElementException:
                    pass

                yield {
                    'datetime': self.get_time(time),
                    'title': title_elem.text.strip(),
                    'category': category,
                    'url': title_elem.get_attribute('href'),
                }
                _num_of_articles += 1
                if _num_of_articles > 100:
                    logging.warning(
                        'Too many articles were collected !!! Leaving ...')
                    break
            try:
                self.force_click(
                    self.find_element_by_css_selector(
                        '#content-paging > li.pagination-page.next > a'
                    )
                )
            except NoSuchElementException:
                logging.warning(
                    'Unable to locate the next page !!! Leaving ...')
                break
