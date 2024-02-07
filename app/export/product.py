import csv
import os
from datetime import date

from app.model.product import Product as ProductModel
from app.model.attribute import Attribute as AttributeModel


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
            products = cls.get_products()
            finalArray = finalInsertArray = []
            attributeHeaders = 0

            # Set Data In Excel Array
            for p in products:
                if len(p.attributes) > attributeHeaders:
                    attributeHeaders = len(p.attributes)

                finalArray = (["external", p.sku, p.name, p.published, p.visibility_in_catalog,
                               p.short_description, p.description, p.in_stock, p.weight,
                               p.length, p.width, p.height, p.allow_customer_reviews,
                               p.sale_price, p.regular_price, p.categories, p.tags,
                               p.images, p.external_url, "Go To Store"])
                for attr in p.attributes:
                    finalArray += ([attr.attribute.title().replace('_', ' '), attr.value])
                finalInsertArray.append(finalArray)

            # Set Header In Excel
            headers = ["Type", "SKU", "Name", "Published", "Visibility in catalog", "Short description",
                       "Description", "In stock?", "Weight (lbs)", "Length (in)", "Width (in)",
                       "Height (in)", "Allow customer reviews?", "Sale price", "Regular price", "Categories",
                       "Tags", "Images", "External URL", "Button text"]
            if attributeHeaders != 0:
                for row in range(1, attributeHeaders + 1):
                    headers.append('Attribute {0} name'.format(row))
                    headers.append('Attribute {0} value(s)'.format(row))
            csvwriter.writerow(headers)

            # Set Data In Excel Sheet
            for data in finalInsertArray:
                csvwriter.writerow(data)

    @classmethod
    def get_products(cls):
        return ProductModel.query().join(AttributeModel, ProductModel.id == AttributeModel.product_id)
