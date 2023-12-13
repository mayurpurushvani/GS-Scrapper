import json
import sys

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from product import Product
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager


class MyProcess:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        # chrome_options.add_experimental_option('detach', True)

        self.driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

    def run(self):
        self.driver.get('https://www.amazon.com/s?k=laptops')
        if sys.argv[1] == 'scrape_products':
            self.scrape_products()
        if sys.argv[1] == 'scrape_links':
            self.scrape_all_links()

    def scrape_products(self):
        products = self.driver.find_elements(By.CSS_SELECTOR, '.s-result-item[data-component-type="s-search-result"]')
        for product in products:
            href = product.find_element(By.CSS_SELECTOR, '[data-component-type="s-product-image"] a').get_attribute(
                'href')
            self.scrape_product(href)

    def scrape_product(self, href):
        # TODO new tab
        # TODO open variant wise product
        # TODO Pagination
        self.driver.get(href)
        product = Product(self.driver)
        product_data = product.scrape()
        print(json.dumps(product_data, indent=4))

    def scrape_all_links(self):
        links = []
        while True:
            current_page_number = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'span.s-pagination-selected'))).text
            print("Current Page: " + current_page_number)
            try:
                for i in self.scrape_links():
                    links.append(i)
                print(links)
                next_page_link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'a.s-pagination-next')))
                next_page_link.click()
            except TimeoutException:
                print("Exiting. Last page: " + current_page_number)
                break

    def scrape_links(self):
        links = []
        products = self.driver.find_elements(By.CSS_SELECTOR, '.s-result-item[data-component-type="s-search-result"]')
        for product in products:
            href = 'https://www.amazon.com/dp/' + product.get_attribute('data-asin')
            links.append(href)
        return links

    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    my_process = MyProcess()
    my_process.run()
