import sys

from dotenv import load_dotenv

load_dotenv()

from app.scrape.link import Link
from app.scrape.product import Product
from app.export.product import Product as ExportProduct


class App:
    def run(self):
        if sys.argv[1] == 'scrape_link':
            Link.scrape()
        elif sys.argv[1] == 'scrape_product':
            Product.scrape()
        elif sys.argv[1] == 'export_product':
            ExportProduct.export()


if __name__ == '__main__':
    app = App()
    app.run()
