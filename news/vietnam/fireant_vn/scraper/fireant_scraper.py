import logging
import re
from datetime import datetime, timedelta
from typing import Dict, Iterator

import pytz
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)

from news.utils.common import VN_TIMEZONE
from scraper.elements.button import Button
from scraper.scraper import Scraper


class FireAntScraper(Scraper):
    def load_fireant_home(self):
        url = 'https://fireant.vn/home/'
        self.load_url(url)
        try:
            popup = self.wait_for_css_presence(
                'body > div.bp3-portal > div > div.bp3-dialog-container > '
                'div.bp3-dialog'
            )
            close = Button(popup.find_element_by_css_selector(
                'div.bp3-dialog-header > button'
            ))
            close.click_and_wait()
        except (NoSuchElementException,  TimeoutException):
            pass
        try:
            popup = self.wait_for_css_presence(
                'body > div > div > div.bp3-dialog-container > div.bp3-dialog'
            )
            close = Button(popup.find_element_by_css_selector(
                'div.bp3-dialog-header > button'
            ))
            close.click_and_wait()
        except (NoSuchElementException,  TimeoutException):
            pass

    def get_articles(self) -> Iterator[Dict[str, str]]:
        _time = datetime.utcnow()
        while True:
            try:
                self.scroll()
                articles = self.find_elements_by_css_selector(
                    css_selector='#root > div > div > div > div > div > div > '
                                 'div > div > div > div.sc-pIJJz.kEDzdV'
                )
                if len(articles) > 100:
                    break
                if (datetime.utcnow() - _time).seconds > 180:
                    break
            except NoSuchElementException:
                pass
        for article in articles:
            try:
                element_class = article.get_attribute('class')
                if 'bp3-card' in element_class:
                    continue

                category = 'N/A'
                try:
                    stocks = article.find_elements_by_css_selector(
                        'div.sc-pJurq.cTjcEC > span'
                    )
                    stock_ids = [stock.text for stock in stocks]
                    category = ", ".join(stock_ids)
                except NoSuchElementException:
                    pass
                link_elem = article.find_element_by_css_selector(
                    'div.sc-pRFjI.dWPMSi > a'
                )
                title = link_elem.text.strip()
                url = link_elem.get_attribute("href")
                try:
                    time = article.find_element_by_css_selector(
                        'div> div > span > time'
                    ).text.strip()
                except NoSuchElementException:
                    try:
                        time = article.find_element_by_css_selector(
                            'div.sc-oTbqq.fsuEer > div > span'
                        ).text.strip()
                    except NoSuchElementException:
                        time = ''

                local_timezone = pytz.timezone(VN_TIMEZONE)
                now = datetime.utcnow()
                local_now = now.replace(tzinfo=pytz.utc).astimezone(
                    local_timezone)
                _year = local_now.year
                _month = local_now.month
                _day = local_now.day
                if re.compile(r'^\d* phút').match(time):
                    times = time.split()
                    timestamp = (
                        local_now - timedelta(minutes=int(times[0]))
                    ).strftime('%-d/%-m/%Y %H:%M:%S')
                elif re.compile(r'^Khoảng \d* tiếng$').match(time):
                    times = time.split()
                    timestamp = (
                        local_now - timedelta(hours=int(times[1]))
                    ).strftime('%-d/%-m/%Y %H:%M:%S')
                elif re.compile(r'^Hôm qua lúc \d*:\d{2}$').match(time):
                    timestamp = f'{_day}/{_month}/{_year} {time[12:]}:00'
                elif re.compile(r'^(\d|/)* lúc \d*:\d{2}$').match(time):
                    times = time.split(' lúc ')
                    timestamp = f'{times[0]}/{_year} {times[1]}:00'
                else:
                    timestamp = local_now.strftime('%-d/%-m/%Y %H:%M:%S')

                yield {
                    'datetime': timestamp,
                    'title': title,
                    'category': category,
                    'url': url,
                }
            except StaleElementReferenceException as error:
                logging.exception(error)
            except NoSuchElementException:
                raise NoSuchElementException('Failed to get Articles row')
