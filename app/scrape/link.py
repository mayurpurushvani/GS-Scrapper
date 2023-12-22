import os

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app.model.Link import Link as LinkModel
from app.web_driver import WebDriver


class Link:
    links = []

    @classmethod
    def scrape(cls):
        with WebDriver() as webdriver:
            webdriver.get(os.getenv("STARTING_URL"))
            while True:
                try:
                    current_page_number = WebDriverWait(webdriver, int(os.getenv('DRIVER_TIMEOUT'))).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.s-pagination-selected'))).text
                    print(f"Current Page: {current_page_number}")
                    cls.scrape_page_links(webdriver)
                    next_page_link = WebDriverWait(webdriver, int(os.getenv('DRIVER_TIMEOUT'))).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.s-pagination-next')))
                    next_page_link.click()
                except TimeoutException:
                    print("Exiting. Last page: " + current_page_number)
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
        LinkModel.bulk_create(cls.links)
