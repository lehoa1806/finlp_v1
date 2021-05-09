from typing import Any, Dict, List

from selenium.common.exceptions import NoSuchElementException

from machine.scraper import Scraper


class TradingViewScraper(Scraper):
    def get_industries(self) -> List[Dict[str, Any]]:
        industries: List[Dict[str, Any]] = []
        try:
            content_pane_class = 'tv-screener__content-pane'
            content_pane = self.find_element_by_class_name(content_pane_class)
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get Industry board')
        try:
            industry_table = content_pane.find_element_by_css_selector(
                'table > tbody')
            industry_rows = industry_table.find_elements_by_css_selector('tr')
            for industry_row in industry_rows:
                columns = industry_row.find_elements_by_css_selector('td > a')
                industry_name = columns[0].text.strip()
                industry_url = columns[0].get_attribute('href')
                sector_name = columns[1].text.strip()
                industries.append({
                    'industry_name': industry_name,
                    'industry_url': industry_url,
                    'sector_name': sector_name,
                })
        except NoSuchElementException:
            raise NoSuchElementException('Failed to get Industry table')
        return industries

    def get_companies(self) -> List[Dict[str, Any]]:
        companies: List[Dict[str, Any]] = []
        for industry in self.get_industries():
            self.load_url(industry.get('industry_url'))
            try:
                panel_class = 'tv-screener__content-pane'
                self.wait_for_class_visibility(panel_class)
                content_pane = self.find_element_by_class_name(panel_class)
                company_table = content_pane.find_element_by_css_selector(
                    'table > tbody')
                company_rows = company_table.find_elements_by_css_selector(
                    'tr')
                for company_row in company_rows:
                    stock_id = company_row.find_element_by_css_selector(
                        'td > div > div > a').text.strip()
                    company_name = company_row.find_element_by_css_selector(
                        'td > div > div > span.tv-screener__description'
                    ).text.strip()
                    companies.append({
                        'stock_id': stock_id,
                        'company_name': company_name,
                        'industry_name': industry.get('industry_name'),
                        'sector_name': industry.get('sector_name'),
                    })
            except NoSuchElementException:
                raise NoSuchElementException('Failed to get Industry table')
        return companies
