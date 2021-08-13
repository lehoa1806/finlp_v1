import logging
from datetime import datetime
from typing import Dict, Iterator

import pytz
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)

from machine.scraper import Scraper
from news.utils.common import VN_TIMEZONE


class VnDirectScraper(Scraper):
    def load_warrant_home(self):
        url = 'https://trade.vndirect.com.vn/chung-khoan/chung-quyen'
        self.load_url(url)
        self.wait_for_css_presence('#banggia-chungquyen-body')

    @classmethod
    def str2int(cls, in_data: str) -> int:
        if in_data.count('.') == 0:
            last_comma_index = in_data.rfind(',')
            if last_comma_index > -1:
                in_data = (
                    in_data[:last_comma_index] +
                    '.' +
                    in_data[last_comma_index + 1:]
                )
        in_data = in_data.replace(',', '')
        return int(float(in_data)*1000)

    def get_warrant_info(self) -> Iterator[Dict[str, str]]:
        local_timezone = pytz.timezone(VN_TIMEZONE)
        timestamp = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(
            local_timezone)
        warrants = self.find_elements_by_css_selector(
            css_selector='#banggia-chungquyen-body > tr'
        )
        for warrant in warrants:
            try:
                name = warrant.find_element_by_css_selector(
                    css_selector='td.txtl > a > span'
                ).text
                provider = warrant.find_element_by_css_selector(
                    css_selector='td:nth-child(2)'
                ).text
                expired_date = datetime.strptime(
                    warrant.find_element_by_css_selector(
                        css_selector='td:nth-child(3)').text,
                    '%d/%m/%y',
                ).replace(tzinfo=pytz.utc).astimezone(
                    local_timezone)
                reference_price = self.str2int(
                    warrant.find_element_by_css_selector(
                        css_selector='td:nth-child(4)'
                    ).text
                )
                try:
                    volume = self.str2int(warrant.find_element_by_css_selector(
                        css_selector='td:nth-child(7) > span'
                    ).text)
                except (NoSuchElementException, TimeoutException, ValueError):
                    volume = 0
                try:
                    price = self.str2int(warrant.find_element_by_css_selector(
                        css_selector='td:nth-child(14) > span'
                    ).text)
                except (NoSuchElementException, TimeoutException, ValueError):
                    price = ''
                try:
                    share_price = self.str2int(
                        warrant.find_element_by_css_selector(
                            css_selector='td:nth-child(24) > span'
                        ).text
                    )
                except (NoSuchElementException, TimeoutException, ValueError):
                    share_price = ''
                try:
                    exercise_price = self.str2int(
                        warrant.find_element_by_css_selector(
                            css_selector='td:nth-child(25) > span'
                        ).text
                    )
                except (NoSuchElementException, TimeoutException, ValueError):
                    exercise_price = 0
                ratio_texts = warrant.find_element_by_css_selector(
                    css_selector='td:nth-child(26) > span'
                ).text.split(':')
                exercise_ratio = str(
                    float(ratio_texts[0])/float(ratio_texts[1])
                )[:6]
                try:
                    foreign_buy = self.str2int(
                        warrant.find_element_by_css_selector(
                            css_selector='td:nth-child(28) > span'
                        ).text
                    )
                except (NoSuchElementException, TimeoutException, ValueError):
                    foreign_buy = 0
                if price and share_price:
                    yield {
                        'datetime': timestamp,
                        'warrant': name,
                        'provider': provider,
                        'expiredDate': expired_date,
                        'exercisePrice': exercise_price,
                        'referencePrice': reference_price,
                        'volume': volume,
                        'price': price,
                        'sharePrice': share_price,
                        'exerciseRatio': exercise_ratio,
                        'foreignBuy': foreign_buy,
                    }
            except StaleElementReferenceException as error:
                logging.exception(error)
            except NoSuchElementException:
                raise NoSuchElementException('Failed to get Warrant Info')
