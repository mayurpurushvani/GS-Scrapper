import json

from selenium import webdriver
from selenium.webdriver.common.by import By

from product import Product


class MyProcess:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        # chrome_options.add_experimental_option('detach', True)

        self.driver = webdriver.Chrome(options=chrome_options)

    def run(self):
        self.driver.get('https://www.amazon.com/s?k=laptops')

        products = self.driver.find_elements(By.CSS_SELECTOR, '.s-result-item[data-component-type="s-search-result"]')
        for product in products:
            href = product.find_element(By.CSS_SELECTOR, '[data-component-type="s-product-image"] a').get_attribute(
                'href')
            self.scrape_product(href)

    def scrape_product(self, href):
        # TODO new tab
        # TODO open variant wise product
        self.driver.get(href)
        product = Product(self.driver)
        product_data = product.scrape()
        print(json.dumps(product_data, indent=4))

    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    my_process = MyProcess()
    my_process.run()
