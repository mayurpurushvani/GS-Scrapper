import os

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from app.model.link import Link as LinkModel
from app.web_driver import WebDriver


class Link:
    links = []

    @classmethod
    def scrape(cls):
        with WebDriver() as webdriver:
            default_url = os.getenv("STARTING_URL")
            page_num = int(os.getenv("STARTING_PAGE_NUM"))
            while True:
                try:
                    url = default_url.format(page_num=page_num)
                    webdriver.get(url)
                    print(f"Current Page: {page_num}")
                    cls.scrape_page_links(webdriver)
                    cls.store_links()
                    page_num += 1
                except TimeoutException as e:
                    print(e)
                    break
                except Exception as e:
                    print(e)
                    break
        cls.store_links()

    @classmethod
    def scrape_page_links(cls, webdriver):
        products = webdriver.find_elements(By.CSS_SELECTOR, '.s-result-item[data-component-type="s-search-result"]')
        for product in products:
            cls.links.append({
                "asin": product.get_attribute("data-asin"),
                "link": 'https://www.amazon.com/dp/' + product.get_attribute("data-asin")
            })

    @classmethod
    def store_links(cls):
        LinkModel.bulk_create_with_ignore(cls.links)
        cls.links = []
