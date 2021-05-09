from typing import Dict, List

from machine.scraper import Scraper


class FreeMalaysiaTodayScraper(Scraper):
    def load_freemalaysiatoday(self, date: str):
        """
        '%Y/%m/%d'
        :param date: '2020/05/06/'
        :return:
        """
        url = f'https://www.freemalaysiatoday.com/category/business/{date}'
        self.load_url(url)
        self.deep_sleep()

    def get_highlight_articles(self) -> List[Dict[str, str]]:
        articles: List[Dict[str, str]] = []
        first_elem = self.wait_for_css_visibility(
            '.td_module_mx5 > div > a'
        )
        articles.append({'url': first_elem.get_attribute('href')})
        for elem in self.find_elements_by_css_selector(
            'div.td_module_mx6 > div > a'
        ):
            articles.append({'url': elem.get_attribute('href')})
        return articles

    def get_other_articles(self) -> List[Dict[str, str]]:
        articles: List[Dict[str, str]] = []
        for elem in self.find_elements_by_css_selector(
            'div.td-block-row > div > div'
        ):
            elem.find_element_by_css_selector('h3 > a')
            articles.append({
                'url': elem.find_element_by_css_selector(
                    'h3 > a').get_attribute('href').strip(),
                'time': elem.find_element_by_css_selector(
                    'div > span > time').text.strip()
            })
        return articles

    def read_article(
        self,
        url: str
    ) -> Dict[str, str]:
        self.load_url(url)
        title = self.wait_for_css_visibility(
            '.td-post-title > h1.entry-title'
        ).text.strip()
        time = self.find_element_by_css_selector(
            '.td-post-title > div > span.td-post-date > time'
        ).text.strip()
        content = self.find_element_by_css_selector(
            '.td-post-content').get_attribute('innerHTML')
        return {
            'title': title,
            'time': time,
            'content': content,
        }
