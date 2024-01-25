import csv
import os
from datetime import date

from app.model.product import Product as ProductModel


class Product:
    @classmethod
    def export(cls):
        curr_date = date.today().strftime("%d%m%Y")
        file_path = './export/'
        file_name = "product_export_{0}.csv".format(curr_date)
        try:
            os.mkdir(file_path)
        except OSError as e:
            pass
        with open(file_path + file_name, "w", newline="", encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(["Type", "SKU", "Name", "Published", "Visibility in catalog", "Short description",
                                "Description", "In stock?", "Weight (unit)", "Length (unit)", "Width (unit)",
                                "Height (unit)", "Allow customer reviews?", "Sale price", "Regular price", "Categories",
                                "Tags", "Images", "External URL", "Button text"])
            products = cls.get_products()
            for p in products:
                csvwriter.writerow(['external', p.sku, p.name, p.published, p.visibility_in_catalog,
                                    p.short_description, p.description, p.in_stock, p.weight, p.length, p.width,
                                    p.height, p.allow_customer_reviews, p.sale_price, p.regular_price, p.categories,
                                    p.tags, p.images, p.external_url, "Go To Store"])

    @classmethod
    def get_products(cls):
        return ProductModel.query().all()
