from typing import Dict, Iterator

from machine.scraper import Scraper
from scraper.elements.button import Button
from utils.configs.setting import Setting


class I3investorScraper(Scraper):
    def login(self) -> None:
        credentials = Setting().i3investor_credentials
        self.load_url(
            'https://klse.i3investor.com/jsp/admin/login.jsp')
        submit_button = Button(self.wait_for_css_visibility(
            'div.roundbox725b:nth-child(2) > div:nth-child(2) > '
            'input:nth-child(5)'
        ))

        user_input = self.wait_for_css_visibility(
            'div.roundbox725b:nth-child(2) > div:nth-child(2) > '
            'table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(1) > '
            'td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > '
            'tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)'
        )
        pass_input = self.wait_for_css_visibility(
            'div.roundbox725b:nth-child(2) > div:nth-child(2) > '
            'table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(1) > '
            'td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > '
            'tr:nth-child(3) > td:nth-child(2) > input:nth-child(1)'
        )
        self.short_sleep()
        user_input.send_keys(credentials[0])
        pass_input.send_keys(credentials[1])
        submit_button.click_and_wait()

    def get_price_targets(self) -> Iterator[Dict[str, str]]:
        self.login()
        url = 'https://klse.i3investor.com/jsp/pt.jsp'
        self.load_url(url)
        self.wait_for_css_visibility('.boxtitle')
        rows = self.browser.find_elements_by_css_selector(
            '.nc > tbody:nth-child(1) > tr'
        )
        for i in range(1, len(rows) - 1):
            columns = rows[i].find_elements_by_css_selector('td')
            yield {
                'Date': columns[0].text.strip(),
                'Stock Name':
                    columns[1].find_element_by_css_selector('a').text.strip(),
                'Url':
                    columns[1].find_element_by_css_selector(
                        'a').get_attribute('href'),
                'Last Price': columns[2].text.strip(),
                'Price Target': columns[3].text.strip(),
                'Upside/Downside': columns[4].find_element_by_css_selector(
                        'span').text.strip(),
                'Price Call': columns[5].text.strip(),
                'Source': columns[6].text.strip(),
            }
