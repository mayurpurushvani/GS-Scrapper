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
    def scrape_product(cls, worker_id, links):
        with WebDriver() as webdriver:
            for link in links:
                try:
                    base_product = BaseProduct(webdriver, link)
                    base_product.scrape()
                except Exception as e:
                    print(f"Worker {worker_id} encountered an exception:", e)
                link.is_scraped = True
                link.update()

    @classmethod
    def scrape(cls):
        workers = int(os.getenv('MAX_WORKERS'))
        links = cls.get_links()
        links_per_worker = [links[i::workers] for i in range(workers)]
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for worker_id, links_for_worker in enumerate(links_per_worker, 1):
                executor.submit(cls.scrape_product, worker_id, links_for_worker)
