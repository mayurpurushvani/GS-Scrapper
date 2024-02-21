import os
from concurrent.futures import ThreadPoolExecutor

from app.model.link import Link as LinkModel
from app.scrape.base_product import BaseProduct
from app.web_driver import WebDriver


class Product:

    @classmethod
    def get_links(cls):
        query = LinkModel.query()
        query = query.filter_by(is_scraped=False)
        limit = int(os.getenv('SCRAPE_PRODUCT_LIMIT', 0))
        if limit > 0:
            query = query.limit(limit)
        return query.all()

    @classmethod
    def scrape_product(cls, link):
        with WebDriver() as webdriver:
            base_product = BaseProduct(webdriver, link)
            base_product.scrape()
            link.is_scraped = True
            link.update()

    @classmethod
    def scrape(cls):
        links = cls.get_links()
        with ThreadPoolExecutor(max_workers=int(os.getenv('MAX_WORKERS'))) as executor:
            for result in executor.map(cls.scrape_product, links):
                try:
                    print(result)
                except Exception as exc:
                    print(f'Catch inside: {exc}')
