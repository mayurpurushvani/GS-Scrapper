import os
from concurrent.futures import ThreadPoolExecutor

from app.model.Link import Link as LinkModel
from app.scrape import BaseProduct
from app.web_driver import WebDriver


class Product:

    @classmethod
    def get_links(cls):
        return LinkModel.query().filter_by(is_scraped=False).all()

    @classmethod
    def scrape_product(cls, link):
        with WebDriver() as webdriver:
            base_product = BaseProduct(webdriver, link.link)
            base_product.scrape()
        link.is_scraped = 1
        link.update()

    @classmethod
    def scrape(cls):
        links = cls.get_links()
        with ThreadPoolExecutor(max_workers=int(os.getenv('MAX_WORKERS'))) as executor:
            executor.map(cls.scrape_product, links)
