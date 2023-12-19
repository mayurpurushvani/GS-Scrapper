import os

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app.model.Link import Link as LinkModel
from app.web_driver import WebDriver


class Link:
    def __init__(self):
        self.links = []

    def scrape(self):
        with WebDriver() as webdriver:
            webdriver.get(os.getenv("STARTING_URL"))
            while True:
                try:
                    current_page_number = WebDriverWait(webdriver, int(os.getenv('DRIVER_TIMEOUT'))).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.s-pagination-selected'))).text
                    print(f"Current Page: {current_page_number}")
                    self.scrape_page_links(webdriver)
                    next_page_link = WebDriverWait(webdriver, int(os.getenv('DRIVER_TIMEOUT'))).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.s-pagination-next')))
                    next_page_link.click()
                except TimeoutException:
                    print("Exiting. Last page: " + current_page_number)
                    break
        self.store_links()

    def scrape_page_links(self, webdriver):
        products = webdriver.find_elements(By.CSS_SELECTOR, '.s-result-item[data-component-type="s-search-result"]')
        for product in products:
            self.links.append({
                "asin": product.get_attribute("data-asin"),
                "link": 'https://www.amazon.com/dp/' + product.get_attribute("data-asin")
            })

    def store_links(self):
        LinkModel.bulk_create(self.links)
