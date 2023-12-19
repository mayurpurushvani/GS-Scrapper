import sys

from dotenv import load_dotenv

load_dotenv()

from app.scrape.link import Link
from app.scrape.product import Product


class App:
    def run(self):
        if sys.argv[1] == 'scrape_link':
            link = Link()
            link.scrape()
        elif sys.argv[1] == 'scrape_product':
            link = Product()
            link.scrape()


if __name__ == '__main__':
    app = App()
    app.run()
