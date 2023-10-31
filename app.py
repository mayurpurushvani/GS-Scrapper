import json
import sys

from selenium import webdriver

from product import Product


class MyProcess:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        # chrome_options.add_experimental_option('detach', True)
        chrome_options.add_argument('--start-maximized')

        self.driver = webdriver.Chrome(options=chrome_options)

    def run(self):
        self.scrapeProduct('https://www.amazon.com/dp/B0CC2GD4D9')
        # self.driver.get('https://www.amazon.com/s?k=laptops')
        #
        # elements = self.driver.find_elements(By.CSS_SELECTOR, '.s-result-item[data-component-type="s-search-result"]')
        # for element in elements:
        #     aTag = element.find_element(By.CSS_SELECTOR, '[data-component-type="s-product-image"] a')
        #     href = aTag.get_attribute('href')
        #     self.scrapeProduct(href)

    def scrapeProduct(self, href):
        # self.driver.switch_to.new_window('tab')
        self.driver.get(href)

        product = Product(self.driver)
        data = product.get_rating()
        print(json.dumps(data, indent=4))
        """
            # TO DO open variant wise product 
            # https://www.amazon.com/dp/B0CGTVW7ZX?th=1
            
            [Products related to this item ASIN]
        """
        sys.exit()

    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    my_process = MyProcess()
    my_process.run()
